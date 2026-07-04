#!/usr/bin/env python3
"""Extract figures from Bedny first/last-author papers for website reference."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "paper-figures"
TMP = OUT / "_tmp"
MIN_W, MIN_H = 500, 350

# eLife figures PDFs (CC-BY) — Bedny last author unless noted
ELIFE_FIGURES = [
    {
        "slug": "tian-2026-connectivity",
        "url": "https://cdn.elifesciences.org/articles/93067/elife-93067-figures-v1.pdf",
        "paper": "Tian et al. (2026) eLife — Visual experience shapes occipital connectivity",
        "role": "last author",
    },
    {
        "slug": "hauptman-2025-animacy",
        "url": "https://cdn.elifesciences.org/articles/101944/elife-101944-figures-v1.pdf",
        "paper": "Hauptman & Bedny (2025) eLife — Animacy semantic network / illness causality",
        "role": "last author",
    },
    {
        "slug": "liu-2020-code",
        "url": "https://cdn.elifesciences.org/articles/59340/elife-59340-figures-v1.pdf",
        "paper": "Liu et al. (2020) eLife — Code comprehension & logical inference",
        "role": "last author",
    },
]

# Local PDFs — render figure-heavy pages at 200 dpi
LOCAL_PDFS = [
    {
        "slug": "bedny-2011-language-occipital",
        "path": "pubs/Bedny_2011_Proc_Natl_Acad_Sci_USA.pdf",
        "pages": "2-4",
        "paper": "Bedny et al. (2011) PNAS — Language in occipital cortex of blind adults",
        "role": "first author",
    },
    {
        "slug": "bedny-2009-pluripotent",
        "path": "pubs/Bedny_2009_Proc_Natl_Acad_Sci_USA.pdf",
        "pages": "2-4",
        "paper": "Bedny et al. (2009) PNAS — Cognitively pluripotent cortex",
        "role": "first author",
    },
    {
        "slug": "bedny-2011-numerical",
        "path": "pubs/kanjlia_numerical_cog_2018.pdf",
        "pages": "2-5",
        "paper": "Kanjlia et al. — Numerical thinking without visual experience",
        "role": "last author",
    },
    {
        "slug": "kanjlia-2021-ans",
        "path": "pubs/ANS_Kanjlia.pdf",
        "pages": "2-5",
        "paper": "Kanjlia, Feigenson & Bedny (2021) Cortex — Approximate number system",
        "role": "last author",
    },
    {
        "slug": "kim-2021-color",
        "path": "pubs/Kim_etal_2021.pdf",
        "pages": "2-5",
        "paper": "Kim et al. (2021) PNAS — Shared understanding of color",
        "role": "last author",
    },
    {
        "slug": "kim-2019-animals",
        "path": "pubs/animals_manuscript_pnas.pdf",
        "pages": "2-5",
        "paper": "Kim, Elli & Bedny (2019) PNAS — Knowledge of animal appearance",
        "role": "last author",
    },
    {
        "slug": "bedny-2019-sparkle",
        "path": "pubs/Sparkle_2019.pdf",
        "pages": "2-5",
        "paper": "Bedny et al. (2019) Cognition — Knowledge of vision/light verbs",
        "role": "first author",
    },
    {
        "slug": "pant-2020-sensitive-period",
        "path": "pubs/sensitive_period_2019.pdf",
        "pages": "2-5",
        "paper": "Pant, Kanjlia & Bedny (2020) — Sensitive period for language in blind",
        "role": "last author",
    },
    {
        "slug": "loiotile-2020-narratives",
        "path": "pubs/Loiotile_etal_JoN.pdf",
        "pages": "2-4",
        "paper": "Loiotile, Cusack & Bedny (2020) JoN — Narratives synchronize visual cortex",
        "role": "last author",
    },
    {
        "slug": "musz-2023-audio-movies",
        "path": "pubs/Musz_etal_23.pdf",
        "pages": "2-5",
        "paper": "Musz et al. (2023) Cerebral Cortex — Audio-movies in blind visual cortex",
        "role": "last author",
    },
    {
        "slug": "tian-2023-braille",
        "path": "pubs/Tian_etal_2023.pdf",
        "pages": "2-5",
        "paper": "Tian et al. (2023) Cerebral Cortex — Braille reading network",
        "role": "last author",
    },
    {
        "slug": "liu-2020-code-local",
        "path": "pubs/Liu_etal_Code2020.pdf",
        "pages": "2-5",
        "paper": "Liu et al. (2020) eLife — Code comprehension (local PDF)",
        "role": "last author",
    },
    {
        "slug": "bedny-2015-jon",
        "path": "pubs/Bedny_2015_JoN.pdf",
        "pages": "2-4",
        "paper": "Bedny et al. (2015) JoN — Syntactic movement in blind visual cortex",
        "role": "first author",
    },
    {
        "slug": "bedny-2011-cereb-cortex",
        "path": "pubs/Bedny_2011_Cereb_Cortex.pdf",
        "pages": "2-5",
        "paper": "Bedny et al. (2011) Cerebral Cortex — Theory of mind in blind children",
        "role": "first author",
    },
    {
        "slug": "arcos-2022-memory",
        "path": "pubs/Arcos_etal_2022.pdf",
        "pages": "2-4",
        "paper": "Arcos et al. (2022) Exp Brain Res — Verbal memory in congenital blindness",
        "role": "last author",
    },
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "NPDL-figure-gather/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
        shutil.copyfileobj(resp, f)


def pdf_to_pngs(pdf: Path, prefix: Path, pages: str | None = None) -> list[Path]:
    cmd = ["pdftoppm", "-png", "-r", "200"]
    if pages:
        start, end = pages.split("-")
        cmd.extend(["-f", start, "-l", end])
    cmd.extend([str(pdf), str(prefix)])
    subprocess.run(cmd, check=True, capture_output=True)
    return sorted(prefix.parent.glob(f"{prefix.name}-*.png"))


def trim_whitespace(src: Path, dest: Path) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w < MIN_W or h < MIN_H:
        im.save(dest)
        return w, h
    bg = im.getpixel((0, 0))
    bbox = None
    pixels = im.load()
    for y in range(h):
        for x in range(w):
            if pixels[x, y] != bg:
                box = (x, y, x + 1, y + 1)
                bbox = box if bbox is None else (
                    min(bbox[0], x), min(bbox[1], y), max(bbox[2], x + 1), max(bbox[3], y + 1)
                )
    if bbox:
        im = im.crop(bbox)
    im.save(dest, optimize=True)
    return im.size


def main() -> None:
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []

    for item in ELIFE_FIGURES:
        slug = item["slug"]
        pdf_path = TMP / f"{slug}.pdf"
        print(f"Downloading eLife figures: {slug}")
        try:
            download(item["url"], pdf_path)
        except Exception as exc:
            print(f"  skip download: {exc}")
            continue
        prefix = TMP / slug
        try:
            pngs = pdf_to_pngs(pdf_path, prefix)
        except subprocess.CalledProcessError as exc:
            print(f"  skip render: {exc.stderr.decode()[:200]}")
            continue
        for i, png in enumerate(pngs, 1):
            out_name = f"{slug}-fig{i:02d}.png"
            out_path = OUT / out_name
            w, h = trim_whitespace(png, out_path)
            if w < MIN_W and h < MIN_H:
                out_path.unlink(missing_ok=True)
                continue
            manifest.append({
                "file": f"images/paper-figures/{out_name}",
                "paper": item["paper"],
                "bedny_role": item["role"],
                "source": item["url"],
                "figure_index": i,
                "width": w,
                "height": h,
            })
            print(f"  saved {out_name} ({w}x{h})")

    for item in LOCAL_PDFS:
        pdf = ROOT / item["path"]
        if not pdf.exists():
            print(f"Missing PDF: {pdf}")
            continue
        slug = item["slug"]
        print(f"Rendering local PDF: {slug}")
        prefix = TMP / slug
        try:
            pngs = pdf_to_pngs(pdf, prefix, item.get("pages"))
        except subprocess.CalledProcessError as exc:
            print(f"  skip: {exc.stderr.decode()[:200]}")
            continue
        for i, png in enumerate(pngs, 1):
            out_name = f"{slug}-p{i:02d}.png"
            out_path = OUT / out_name
            w, h = trim_whitespace(png, out_path)
            if max(w, h) < 400:
                out_path.unlink(missing_ok=True)
                continue
            manifest.append({
                "file": f"images/paper-figures/{out_name}",
                "paper": item["paper"],
                "bedny_role": item["role"],
                "source": str(item["path"]),
                "page": item.get("pages"),
                "figure_index": i,
                "width": w,
                "height": h,
            })
            print(f"  saved {out_name} ({w}x{h})")

    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"\nDone: {len(manifest)} figures -> {OUT}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
