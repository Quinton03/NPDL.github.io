# NPDL Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Bedny Lab / NPDL website with a single, highly accessible (WCAG 2.1 AA), hand-editable static site that preserves all existing content, retiring the parallel `-alltext.html` pages.

**Architecture:** Plain HTML5 + one shared `css/site.css` design system. No build step — pages are hand-written semantic HTML and host as-is on GitHub Pages. Shared header/footer are duplicated per page inside marked comment blocks (so they work with JS off). The only JavaScript is one optional progressive enhancement (publications topic filter); every page is fully usable without it.

**Tech Stack:** HTML5, CSS (custom properties, grid/flex), a tiny vanilla JS file (optional). Verification via a local `python3 -m http.server` + Playwright + axe-core, plus manual keyboard / no-JS / zoom checks.

---

## Spec

Source spec: `docs/superpowers/specs/2026-06-17-npdl-website-redesign-design.md`. Read it before starting.

## Conventions (read once, apply everywhere)

- **Preserve all content.** Migrate text, citations, people, news, photos, and links **verbatim** from the existing files. Only fix broken markup; never drop or reword content (except obvious typo `Cusac`→`Cusack` is fine to leave as-is — do not invent edits).
- **Branch:** work on the existing `remodel` branch. Commit after every task.
- **No `visibility:hidden`, no `onload` body reveal, no skel.js/jQuery.** Content is plain HTML.
- **Email obfuscation:** the old site wrote `name at jhu dot edu`. In the redesign, use real `mailto:` links (e.g. `<a href="mailto:plasticity_lab@jhu.edu">plasticity_lab@jhu.edu</a>`). This is fine and more accessible.
- **Alt text:** every content image gets descriptive `alt` conveying its point. Decorative/background images get `alt=""`. Draft alt text is provided for key figures below; for the rest, write a clear one-sentence description and flag it in the final task for the lab to verify.
- **Shared blocks:** the header and footer HTML are defined once in Task 2. Paste them verbatim into every page between the marked comment fences, changing only which nav link has `aria-current="page"`.

## File Structure

**Create:**
- `css/site.css` — the entire design system (tokens, base, components, responsive, a11y).
- `js/enhance.js` — optional progressive-enhancement JS (publications topic filter only).
- New/rewritten pages (same filenames as today): `index.html`, `research.html`, `publications.html`, `people.html`, `participate.html`, `join_lab.html`, `news.html`, `photos.html`, `2014_photos.html`…`2019_photos.html`, `contact.html`, `resources-and-data.html`.
- Redirect stubs at every old `*-alltext.html` path.

**Modify:** none in place — pages are rewritten.

**Delete (Task 16):** dead template assets — `js/main.js`, `js/js_Load.js`, `js/skel*.js`, `js/init.js`, `js/jquery.min.js`, `js/slideshow.js`, `css/main.css`, `css/main.min.css`, `css/skel.css`, `css/style*.css`, `css/font-awesome.min.css`, `css/W3.css`, and the `fonts/` dir if unreferenced.

**Keep untouched:** `images/`, `pubs/`, `forms/`, `CNAME`, `license.txt`.

---

## Verification Recipe (referenced by every page task as "run the Verification Recipe")

Run these against a page after building it. Assume the local server from Task 1 is running at `http://localhost:8000`.

1. **Render + screenshot.** With Playwright: `browser_navigate` to `http://localhost:8000/<page>.html`, then `browser_take_screenshot` (fullPage). Confirm layout matches the approved mockups and no content is missing.
2. **Automated a11y (axe-core).** With Playwright `browser_evaluate`, inject and run axe:
   ```js
   () => new Promise(res => { const s=document.createElement('script');
     s.src='https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js';
     s.onload=()=>axe.run(document,{},(e,r)=>res(r.violations.map(v=>({id:v.id,nodes:v.nodes.length,help:v.help}))));
     document.head.appendChild(s); })
   ```
   **Expected:** `[]` (zero violations). Fix any reported issue before committing.
3. **Keyboard pass.** Reload, press `Tab` repeatedly (Playwright `browser_press_key Tab`). Confirm: skip-link appears first and works, focus is visible on every interactive element, tab order is logical, no keyboard trap.
4. **No-JS check.** `browser_evaluate` to confirm content is present in DOM without relying on JS — or load with JS disabled — and confirm the page is fully readable/navigable. (Content must never depend on JS.)
5. **Heading order.** `browser_evaluate`: `[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+': '+h.textContent.trim().slice(0,40))` — confirm exactly one `h1` and no skipped levels.

Manual (do once at the end in Task 17, not per page): VoiceOver pass, 400% zoom, 320px width reflow.

---

## Task 1: Local preview server + accessibility tooling baseline

**Files:** none (environment setup).

- [ ] **Step 1: Start a local static server**

Run (background): `cd "<repo root>" && python3 -m http.server 8000`
Expected: serves the repo at `http://localhost:8000`. Leave running for all later tasks.

- [ ] **Step 2: Confirm Playwright + axe injection works**

Navigate Playwright to `http://localhost:8000/index.html` (the OLD page is fine for now) and run the axe injection snippet from the Verification Recipe.
Expected: it returns a JSON array (likely many violations on the OLD site — that's expected; it proves the tooling works).

- [ ] **Step 3: Commit** (nothing to commit yet — skip; this task is environment only.)

---

## Task 2: Design system — `css/site.css` + canonical header/footer

**Files:**
- Create: `css/site.css`
- Reference blocks (used by all pages): canonical `<header>` and `<footer>` defined in Step 2.

- [ ] **Step 1: Create `css/site.css` with the full design system**

```css
/* ============================================================
   NPDL site stylesheet — single source of truth.
   Edit design tokens here; component styles cascade from them.
   ============================================================ */
:root{
  /* palette */
  --ink:#11201e; --body:#243431; --muted:#5d6b69;
  --teal:#0a4542; --teal-deep:#06302d; --teal-bright:#0e6a63; --teal-pale:#86cabf;
  --paper:#f7faf9; --card:#ffffff; --cool:#eaf1ef; --line:#d4dddb; --hair:#c2cecb;
  /* type */
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --maxw:1140px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sans);color:var(--body);background:var(--paper);
     line-height:1.62;font-size:17px;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block;height:auto}
a{color:var(--teal)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 30px}

/* visible keyboard focus everywhere */
:focus-visible{outline:3px solid var(--teal-bright);outline-offset:2px;border-radius:3px}

/* skip link */
.skip{position:absolute;left:12px;top:-60px;background:var(--ink);color:#fff;padding:10px 16px;
      border-radius:8px;z-index:50;transition:top .15s}
.skip:focus{top:12px}

/* editorial kicker (uppercase label + short rule) */
.kicker{text-transform:uppercase;letter-spacing:.2em;font-size:12px;font-weight:700;
        display:inline-flex;align-items:center;gap:14px;color:var(--teal)}
.kicker::before{content:"";width:30px;height:2px;background:currentColor;display:inline-block}

/* ---------- header / masthead ---------- */
header.site{position:sticky;top:0;background:rgba(247,250,249,.93);backdrop-filter:blur(8px);
            border-bottom:1px solid var(--hair);z-index:40}
.bar{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:78px;
     flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
.brand{text-decoration:none;display:flex;flex-direction:column;line-height:1.05}
.brand b{color:var(--ink);font-size:21px;font-weight:800;letter-spacing:-.01em}
.brand span{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.13em;margin-top:4px}
nav.main ul{display:flex;gap:4px;list-style:none;margin:0;padding:0;align-items:center;flex-wrap:wrap}
nav.main a{text-decoration:none;color:var(--ink);font-size:15px;font-weight:600;padding:9px 12px;border-radius:8px}
nav.main a:hover{background:var(--cool)}
nav.main a[aria-current="page"]{color:var(--teal);text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:2px}
nav.main a.cta{background:var(--teal);color:#fff;padding:9px 16px}
nav.main a.cta:hover{background:var(--teal-bright)}

/* ---------- buttons ---------- */
.btns{display:flex;gap:14px;flex-wrap:wrap}
.btn{text-decoration:none;font-weight:700;font-size:15.5px;padding:13px 22px;border-radius:10px;display:inline-block}
.btn-primary{background:#fff;color:var(--teal-deep)}
.btn-primary:hover{background:#dffaf6}
.btn-ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.5)}
.btn-ghost:hover{box-shadow:inset 0 0 0 1.5px #fff}
.btn-solid{background:var(--teal);color:#fff}
.btn-solid:hover{background:var(--teal-bright)}

/* ---------- hero / page header (teal band) ---------- */
.hero,.page-head{background:linear-gradient(168deg,var(--teal),var(--teal-deep));color:#e8f5f2}
.hero .top{display:flex;justify-content:space-between;align-items:center;padding:22px 0 0;color:var(--teal-pale)}
.hero .grid{display:grid;grid-template-columns:1.12fr .88fr;gap:52px;align-items:center;padding:30px 0 70px}
.hero h1{font-size:50px;font-weight:800;line-height:1.07;letter-spacing:-.02em;color:#fff;margin:18px 0 22px}
.hero p.lead{font-size:19px;color:#cfe9e4;margin:0 0 30px;max-width:33em;line-height:1.55}
.hero figure{margin:0}
.hero figure img{width:100%;border-radius:12px;background:#fff;padding:14px;box-shadow:0 20px 44px rgba(0,0,0,.3)}
.hero figcaption{font-style:italic;font-size:14px;color:#9fd8d0;margin-top:11px}
.hero figcaption b{font-style:normal;text-transform:uppercase;letter-spacing:.12em;font-size:11px;color:#7cc3b8;margin-right:8px}
.page-head .wrap{padding:46px 30px 50px}
.page-head h1{font-size:46px;font-weight:800;letter-spacing:-.02em;color:#fff;margin:14px 0 14px}
.page-head p{max-width:42em;color:#cfe9e4;font-size:18px;margin:0 0 6px}
.page-head .kicker{color:var(--teal-pale)}

/* ---------- thesis statement band ---------- */
.thesis{border-bottom:1px solid var(--line);background:var(--card)}
.thesis .wrap{padding:56px 30px;text-align:center}
.thesis p{font-size:28px;line-height:1.35;color:var(--ink);margin:0 auto;max-width:23em;font-weight:600;letter-spacing:-.01em}
.thesis p em{color:var(--teal);font-style:normal}

/* ---------- generic content section ---------- */
section.block{padding:74px 0}
.block.alt{background:var(--cool);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sec-head{display:flex;align-items:center;gap:18px;margin-bottom:42px}
.sec-head h2{font-size:12px;text-transform:uppercase;letter-spacing:.2em;color:var(--teal);margin:0;font-weight:700;white-space:nowrap}
.sec-head .rule{flex:1;height:1px;background:var(--hair)}
.sec-head .more a{font-size:14.5px;font-weight:600;text-decoration:none;white-space:nowrap}

/* prose blocks (Research, Participate, etc.) */
.prose{max-width:42em}
.prose h2{font-size:30px;font-weight:800;letter-spacing:-.02em;color:var(--ink);margin:40px 0 14px}
.prose h3{font-size:22px;font-weight:800;color:var(--ink);margin:30px 0 10px}
.prose p{margin:0 0 18px}
.prose a{font-weight:600}

/* ---------- research areas (numbered, figure + text) ---------- */
.area{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;padding:18px 0 46px;border-bottom:1px solid var(--line)}
.area:last-child{border-bottom:0}
.area.flip .fig{order:2}
.fig{margin:0}
.fig img{width:100%;border:1px solid var(--line);border-radius:10px;background:#fff;padding:16px}
.fig figcaption{font-style:italic;font-size:14px;color:var(--muted);margin-top:11px}
.area .num{font-size:14px;color:var(--teal);font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.area h2,.area h3{font-size:30px;font-weight:800;line-height:1.15;letter-spacing:-.02em;color:var(--ink);margin:8px 0 14px}
.area p{margin:0 0 18px;color:var(--body)}
.read{font-weight:700;text-decoration:none;border-bottom:2px solid var(--teal);padding-bottom:2px}
.read::after{content:" \2192"}

/* ---------- featured publication card ---------- */
.pubcard{background:#fff;border:1px solid var(--line);border-radius:12px;padding:30px 32px;max-width:860px}
.pubcard .tag{font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--teal)}
.pubcard h3{font-size:24px;font-weight:800;line-height:1.25;letter-spacing:-.01em;color:var(--ink);margin:12px 0 8px}
.pubcard .cite{font-style:italic;color:var(--muted);font-size:16px;margin:0 0 18px}

/* ---------- publications list (year rail + items) ---------- */
.layout{display:grid;grid-template-columns:190px 1fr;gap:54px;padding:50px 0 80px}
nav.years{position:sticky;top:100px;align-self:start}
nav.years h2{font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:var(--muted);margin:0 0 12px}
nav.years ul{list-style:none;margin:0;padding:0}
nav.years a{display:block;text-decoration:none;color:var(--body);font-weight:600;font-size:15px;padding:6px 0;border-left:2px solid var(--line);padding-left:14px}
nav.years a:hover{color:var(--teal);border-left-color:var(--teal)}
.scholar{display:inline-flex;align-items:center;gap:10px;background:#fff;color:var(--teal-deep);text-decoration:none;font-weight:700;padding:11px 18px;border-radius:10px;font-size:15px;margin-top:18px}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:26px}
.toolbar .lbl{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;font-weight:700;margin-right:4px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;font-size:14px;font-weight:600;color:var(--body);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--teal);color:#fff;border-color:var(--teal)}
.year{margin-bottom:14px}
.year-head{display:flex;align-items:baseline;gap:16px;margin:34px 0 10px}
.year-head h2{font-size:26px;font-weight:800;color:var(--ink);margin:0;letter-spacing:-.01em}
.year-head .rule{flex:1;height:1px;background:var(--hair)}
.year-head .count{font-size:13px;color:var(--muted)}
ul.pub-list{list-style:none;margin:0;padding:0}
li.pub{padding:18px 0;border-bottom:1px solid var(--line)}
li.pub .authors{margin:0 0 4px;font-size:14.5px;color:var(--muted)}
li.pub .authors b{color:var(--ink)}
li.pub .title{margin:0 0 6px;font-size:18.5px;line-height:1.35;font-weight:700}
li.pub .title a{color:var(--ink);text-decoration:none;border-bottom:2px solid rgba(10,69,66,.25)}
li.pub .title a:hover{color:var(--teal);border-bottom-color:var(--teal)}
li.pub .venue{margin:0;font-style:italic;color:var(--muted);font-size:15px}
li.pub .tags{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap}
li.pub .tag{font-size:11.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--teal);background:var(--cool);border-radius:6px;padding:3px 8px}

/* ---------- people cards ---------- */
.people-group{margin-bottom:46px}
.people-group > h2{font-size:22px;font-weight:800;color:var(--ink);margin:0 0 20px;padding-bottom:8px;border-bottom:2px solid var(--ink)}
.people-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:28px}
.person{display:flex;gap:16px}
.person img{width:96px;height:96px;border-radius:10px;object-fit:cover;flex:none;background:var(--cool)}
.person h3{margin:0 0 4px;font-size:18px;font-weight:800;color:var(--ink)}
.person .role{font-size:13px;color:var(--teal);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin:0 0 6px}
.person p{margin:0 0 6px;font-size:15px}
.person a{font-weight:600}

/* ---------- news list ---------- */
ul.news{list-style:none;margin:0;padding:0;max-width:48em}
ul.news li{padding:20px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:120px 1fr;gap:20px}
ul.news .date{color:var(--teal);font-weight:700;font-size:14px}
ul.news h2{margin:0 0 6px;font-size:18px;font-weight:700;color:var(--ink)}
ul.news p{margin:0}

/* ---------- photos gallery / timeline ---------- */
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}
.gallery figure{margin:0}
.gallery img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;border:1px solid var(--line)}
.gallery figcaption{font-size:14px;color:var(--muted);margin-top:8px}
.year-index{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:30px}
.year-index a{text-decoration:none;font-weight:700;border:1px solid var(--line);border-radius:999px;padding:8px 18px;color:var(--ink)}
.year-index a:hover{background:var(--cool)}

/* ---------- participate / join band (photo + scrim) ---------- */
.join{position:relative;color:#fff;overflow:hidden}
.join img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.join .scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,48,45,.94),rgba(6,48,45,.62))}
.join .wrap{position:relative;padding:80px 30px}
.join h2{font-size:34px;font-weight:800;color:#fff;margin:14px 0 12px;letter-spacing:-.02em;max-width:16em}
.join p{color:#cfe9e4;max-width:33em;margin:0 0 26px;font-size:17.5px}
.join .kicker{color:var(--teal-pale)}

/* ---------- contact ---------- */
.contact-maps{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:24px 0}
.contact-maps img{border-radius:10px;border:1px solid var(--line)}
.contact-list{list-style:none;margin:0;padding:0;max-width:46em}
.contact-list li{padding:10px 0;border-bottom:1px solid var(--line)}

/* ---------- footer ---------- */
footer.site{background:var(--ink);color:#bccac7}
footer.site .wrap{padding:56px 30px;display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:40px}
footer.site .fbrand b{color:#fff;font-size:20px;font-weight:800;display:block;margin-bottom:10px}
footer.site .fbrand p{margin:0;max-width:30em;color:#9fb0ad}
footer.site h2{color:#fff;font-size:12px;letter-spacing:.14em;text-transform:uppercase;margin:0 0 14px}
footer.site a{color:#9fd8d0;text-decoration:none}
footer.site a:hover{text-decoration:underline}
footer.site ul{list-style:none;margin:0;padding:0;line-height:2}
footer .legal{border-top:1px solid #243634;color:#7e8e8b;font-size:13px;padding:18px 0;text-align:center}

/* ---------- responsive ---------- */
@media (max-width:820px){
  .hero .grid,.area,.area.flip .fig,.layout,.contact-maps,footer.site .wrap{grid-template-columns:1fr;gap:28px}
  .area.flip .fig{order:0}
  .hero h1{font-size:34px} .page-head h1{font-size:32px} .thesis p{font-size:23px}
  nav.years{position:static} nav.years ul{display:flex;flex-wrap:wrap;gap:6px}
  nav.years a{border:1px solid var(--line);border-radius:999px;padding:6px 12px}
  ul.news li{grid-template-columns:1fr;gap:4px}
}

/* ---------- reduced motion ---------- */
@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important;scroll-behavior:auto!important}
}
```

- [ ] **Step 2: Record the canonical header & footer blocks**

These exact blocks get pasted into every page. (Set `aria-current="page"` on the matching link per page.)

Canonical **header** (goes right after `<body>`):
```html
<a class="skip" href="#main">Skip to main content</a>
<!-- SHARED HEADER — keep identical across all pages; only change aria-current -->
<header class="site">
  <div class="wrap bar">
    <a class="brand" href="index.html">
      <b>Neuroplasticity &amp; Development Lab</b>
      <span>Bedny Lab · Johns Hopkins</span>
    </a>
    <nav class="main" aria-label="Primary">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="research.html">Research</a></li>
        <li><a href="publications.html">Publications</a></li>
        <li><a href="people.html">People</a></li>
        <li><a href="news.html">News</a></li>
        <li><a href="photos.html">Photos</a></li>
        <li><a href="participate.html" class="cta">Participate</a></li>
      </ul>
    </nav>
  </div>
</header>
<!-- /SHARED HEADER -->
```

Canonical **footer** (goes right before `</body>`):
```html
<!-- SHARED FOOTER — keep identical across all pages -->
<footer class="site">
  <div class="wrap">
    <div class="fbrand">
      <b>Neuroplasticity &amp; Development Lab</b>
      <p>Department of Psychological &amp; Brain Sciences, Johns Hopkins University.</p>
    </div>
    <nav aria-labelledby="foot-explore">
      <h2 id="foot-explore">Explore</h2>
      <ul>
        <li><a href="research.html">Research</a></li>
        <li><a href="publications.html">Publications</a></li>
        <li><a href="people.html">People</a></li>
        <li><a href="join_lab.html">Join the Lab</a></li>
        <li><a href="resources-and-data.html">Resources &amp; Data</a></li>
      </ul>
    </nav>
    <nav aria-labelledby="foot-contact">
      <h2 id="foot-contact">Contact</h2>
      <ul>
        <li>3400 N. Charles St, Ames Hall 108, Baltimore MD 21218</li>
        <li><a href="tel:+14108709895">(410) 870-9895</a></li>
        <li><a href="mailto:plasticity_lab@jhu.edu">plasticity_lab@jhu.edu</a></li>
        <li><a href="https://scholar.google.com/citations?user=BO08yNQAAAAJ&amp;hl=en">Google Scholar</a></li>
      </ul>
    </nav>
  </div>
  <div class="legal">© 2026 Neuroplasticity &amp; Development Laboratory</div>
</footer>
<!-- /SHARED FOOTER -->
```

The standard `<head>` for every page:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PAGE TITLE — Neuroplasticity &amp; Development Lab</title>
<meta name="description" content="ONE-SENTENCE PAGE DESCRIPTION">
<link rel="stylesheet" href="css/site.css">
</head>
```

- [ ] **Step 3: Commit**

```bash
git add css/site.css docs/superpowers/plans/2026-06-17-npdl-website-redesign.md
git commit -m "Add NPDL design system stylesheet and implementation plan"
```

---

## Task 3: Home page (`index.html`)

**Files:** Create/rewrite `index.html`. Content source: existing `index.html` + `index-alltext.html`.

- [ ] **Step 1: Build `index.html`**

Use the standard `<head>` (title "Home"), paste canonical header (set `aria-current="page"` on the Home link) and footer. Body is the approved homepage. Full reference markup:

```html
<body>
<!-- (skip link + SHARED HEADER here, Home link gets aria-current="page") -->
<main id="main">
  <section class="hero">
    <div class="wrap">
      <div class="top"><span class="kicker">Cognitive Neuroscience &amp; Psychology</span></div>
      <div class="grid">
        <div>
          <span class="kicker" style="color:var(--teal-pale)">Neuroplasticity &amp; Development Laboratory</span>
          <h1>How do nature and nurture shape the human mind and brain?</h1>
          <p class="lead">We investigate the origins and structure of human cognition by comparing the
            minds and brains of people with different developmental experiences — congenitally blind,
            late-blind, and sighted individuals.</p>
          <div class="btns">
            <a class="btn btn-primary" href="research.html">Explore our research</a>
            <a class="btn btn-ghost" href="participate.html">Participate in a study</a>
          </div>
        </div>
        <figure>
          <img src="images/brains.jpg" alt="Inflated MRI brain surfaces with colored activation maps; warm colors mark regions more active for some tasks, cool colors for others, shown across several individuals.">
          <figcaption><b>Fig. 1</b>Task-driven cortical activity across individuals in our neuroimaging studies.</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="thesis"><div class="wrap">
    <p>We study the human mind by studying minds that have been <em>shaped differently</em> — and the brains that grow with them.</p>
  </div></section>

  <section class="block"><div class="wrap">
    <div class="sec-head"><h2>Research</h2><span class="rule"></span>
      <span class="more"><a href="research.html">All research areas →</a></span></div>

    <div class="area">
      <figure class="fig">
        <img src="images/Visual_Cortex.jpg" alt="Brain maps for sighted, late-blind, and congenitally blind people beside bar charts; in congenitally blind people, occipital 'visual' cortex responds during math and language tasks.">
        <figcaption>Math- and language-responsive “visual” cortex in congenitally blind adults.</figcaption>
      </figure>
      <div>
        <span class="num">01 — Plasticity</span>
        <h3>Cortical plasticity in blindness</h3>
        <p>In sighted people, much of the occipital lobe is dedicated to vision. What happens when it
          never receives its typical input? In blindness, “visual” areas take on higher-cognitive
          functions — language, mathematical reasoning, and executive control — revealing how
          experience shapes cortical specialization.</p>
        <a class="read" href="research.html">Read more</a>
      </div>
    </div>

    <div class="area flip">
      <figure class="fig">
        <img src="images/MDS.png" alt="Two word maps comparing how blind and sighted adults organize visual verbs such as 'peek', 'glance', and 'stare'; the overall arrangement is strikingly similar across groups.">
        <figcaption>How blind and sighted adults organize knowledge of vision-related words.</figcaption>
      </figure>
      <div>
        <span class="num">02 — Concepts</span>
        <h3>Conceptual development</h3>
        <p>How does experience contribute to the concepts we form? We compare what blind and sighted
          people know about things only directly accessible through vision — light, color, and acts of
          seeing — to isolate the roles of sensory experience and of language in human knowledge.</p>
        <a class="read" href="research.html">Read more</a>
      </div>
    </div>
  </div></section>

  <section class="block alt"><div class="wrap">
    <div class="sec-head"><h2>Recent work</h2><span class="rule"></span>
      <span class="more"><a href="publications.html">All publications →</a></span></div>
    <div class="pubcard">
      <span class="tag">Featured</span>
      <h3>Sensitive period for cognitive repurposing of human visual cortex</h3>
      <p class="cite">Kanjlia, S., Pant, R., &amp; Bedny, M. (2018). Cerebral Cortex.</p>
      <a class="read" href="pubs/sensitive_period_2018.pdf">Read the paper</a>
    </div>
  </div></section>

  <section class="join">
    <img class="bg" src="images/Lindsay_brain_photo.jpg" alt="">
    <div class="scrim"></div>
    <div class="wrap">
      <span class="kicker">Get involved</span>
      <h2>Take part in our research, or join the lab</h2>
      <p>We work with blind and sighted volunteers, and we welcome curious students and researchers.
        There’s a place for you in this work.</p>
      <div class="btns">
        <a class="btn btn-primary" href="participate.html">Participate in a study</a>
        <a class="btn btn-ghost" href="join_lab.html">Join the lab</a>
      </div>
    </div>
  </section>
</main>
<!-- (SHARED FOOTER here) -->
</body>
```

- [ ] **Step 2: Run the Verification Recipe** against `http://localhost:8000/index.html`. Expected: 0 axe violations; renders like the approved mockup; works with JS off.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Rebuild Home page on accessible design system"
```

---

## Task 4: Research page (`research.html`)

**Files:** Create `research.html`. Content source: existing `research.html` + `research-alltext.html` + the two research blurbs already on the home page.

- [ ] **Step 1: Build the page.** Standard head (title "Research"); header (Research link `aria-current`); footer. Use a `.page-head` teal band (kicker "Research", `<h1>Research</h1>`, one-line intro). Then a `<section class="block"><div class="wrap">` containing the full research areas using the `.area` / `.area.flip` pattern from Task 3 — but with the **complete** text migrated from `research.html` (not the shortened home version), each with its figure (`images/Visual_Cortex.jpg`, `images/MDS.png`, and any others present in `research.html`) and descriptive alt text. Include the "Figure from:" publication references that appear in the source, as `<p>` citations linking the existing `pubs/*.pdf`.

- [ ] **Step 2: Run the Verification Recipe** against `research.html`. Expected: 0 violations; all source content present.

- [ ] **Step 3: Commit**
```bash
git add research.html && git commit -m "Add accessible Research page"
```

---

## Task 5: Publications page (`publications.html`)

**Files:** Create `publications.html`. Content source: existing `publications.html` (the full year-grouped list, "UNDER REVIEW" through the oldest year) + Google Scholar link.

- [ ] **Step 1: Build the page** using the approved publications layout. Standard head (title "Publications"); header (Publications `aria-current`); footer.

Structure:
```html
<div class="page-head"><div class="wrap">
  <span class="kicker">Publications</span>
  <h1>Our research, in print</h1>
  <p>Peer-reviewed articles, reviews, and chapters from the lab. Each title links to the paper.
     Names in <b style="color:#fff">bold</b> indicate the lab’s principal investigator.</p>
  <a class="scholar" href="https://scholar.google.com/citations?user=BO08yNQAAAAJ&amp;hl=en">↗ Latest on Google Scholar</a>
</div></div>

<main id="main" class="wrap"><div class="layout">
  <nav class="years" aria-label="Jump to year">
    <h2>Jump to</h2>
    <ul><!-- one <li><a href="#yYYYY">YYYY</a></li> per year section, plus Under review --></ul>
  </nav>
  <div>
    <!-- OPTIONAL filter toolbar: include ONLY if Task 15 (JS) is done; otherwise omit this .toolbar block entirely -->
    <section class="year" id="yYYYY" aria-labelledby="hYYYY">
      <div class="year-head"><h2 id="hYYYY">YYYY</h2><span class="rule"></span><span class="count">N papers</span></div>
      <ul class="pub-list">
        <li class="pub">
          <p class="authors">Author, A., <b>Bedny, M.</b></p>
          <p class="title"><a href="LINK">Exact title from source.</a></p>
          <p class="venue">Journal · YYYY</p>
        </li>
      </ul>
    </section>
  </div>
</div></main>
```

Migration rules for each `<li>` in source `publications.html`:
- Split each entry into **authors** (everything before the linked title; wrap `Bedny, M.`/`Bedny M.` in `<b>`), **title** (the linked text → `.title` with the same `href`), **venue** (journal/book text after the link → `.venue`, append `· YYYY` using the section year).
- Recreate **every** year section and **every** entry, including "UNDER REVIEW". Do not drop any.
- Entries with no link (e.g. some book chapters): render `.title` as plain text (no `<a>`).
- Do **not** add topic `.tags` yet (tags are only needed if the optional filter in Task 15 is built).

- [ ] **Step 2: Verify counts.** `browser_evaluate`: `document.querySelectorAll('li.pub').length` — compare to the number of `<li>` in the old `publications.html`. Expected: equal (no lost entries).

- [ ] **Step 3: Run the Verification Recipe** against `publications.html`. Expected: 0 violations; year rail anchors jump correctly.

- [ ] **Step 4: Commit**
```bash
git add publications.html && git commit -m "Add accessible Publications page with year rail"
```

---

## Task 6: People page (`people.html`)

**Files:** Create `people.html`. Content source: existing `people.html` (all groups: Principal Investigator, Post-Doctoral Research Fellows, PhD Students & Candidates, plus any Lab Managers / RAs / Undergrads / Alumni present).

- [ ] **Step 1: Build the page.** Standard head (title "People"); header (People `aria-current`); footer. `.page-head` band (`<h1>People</h1>`). Then one `<section class="people-group">` per role group:
```html
<section class="people-group" aria-labelledby="g-pi">
  <h2 id="g-pi">Principal Investigator</h2>
  <div class="people-grid">
    <article class="person">
      <img src="images/people/marina_picture.jpg" alt="Portrait of Marina Bedny.">
      <div>
        <h3>Marina Bedny</h3>
        <p class="role">Principal Investigator</p>
        <p>RESEARCH INTEREST TEXT migrated verbatim (if present).</p>
        <p><a href="https://pbs.jhu.edu/directory/marina-bedny/">Directory</a> ·
           <a href="pubs/BednyCV_2019_latest.pdf">CV</a> ·
           <a href="mailto:marina.bedny@jhu.edu">marina.bedny@jhu.edu</a></p>
      </div>
    </article>
    <!-- repeat .person for each member in this group -->
  </div>
</section>
```
Migrate **every** person from the source, preserving photo (`images/people/*`), name, role, research-interest text, external link, and email (convert `x at jhu dot edu` → real `mailto:`). Give each portrait alt text "Portrait of NAME." Keep alumni/past-members groups if present.

- [ ] **Step 2: Verify count.** `browser_evaluate`: `document.querySelectorAll('.person').length` vs number of people in old `people.html`. Expected: equal.

- [ ] **Step 3: Run the Verification Recipe** against `people.html`. Expected: 0 violations.

- [ ] **Step 4: Commit**
```bash
git add people.html && git commit -m "Add accessible People page"
```

---

## Task 7: Participate page (`participate.html`)

**Files:** Create `participate.html`. Content source: existing `participate.html`.

- [ ] **Step 1: Build the page.** Standard head (title "Participate"); header (Participate `aria-current`); footer. `.page-head` band (`<h1>Participate in Research</h1>`). A `.prose` section with the two paragraphs migrated verbatim. Convert contact details to real links: `mailto:plasticity_lab@jhu.edu`, `tel:+14108709895`, video phone `tel:+14102145087`. Add a closing line linking to `join_lab.html`. Optionally include the `images/Lindsay_brain_photo.jpg` as a `<figure>` with the existing caption ("Graduate student Judy Kim applies TMS to Dr. Marina Bedny.") as descriptive alt + figcaption.

- [ ] **Step 2: Run the Verification Recipe** against `participate.html`. Expected: 0 violations.

- [ ] **Step 3: Commit**
```bash
git add participate.html && git commit -m "Add accessible Participate page"
```

---

## Task 8: Join the Lab page (`join_lab.html`)

**Files:** Create `join_lab.html`. Content source: existing `join_lab.html` + `join_lab-alltext.html`.

- [ ] **Step 1: Build the page.** Standard head (title "Join the Lab"); header (no nav item is `aria-current` — Join is a footer link; leave none set or set Participate); footer. `.page-head` band (`<h1>Join the Lab</h1>`). `.prose` section with all content migrated verbatim (openings for prospective students, postdocs, RAs, and how to apply). Preserve all links/emails as real `mailto:`/`href`.

- [ ] **Step 2: Run the Verification Recipe** against `join_lab.html`. Expected: 0 violations.

- [ ] **Step 3: Commit**
```bash
git add join_lab.html && git commit -m "Add accessible Join the Lab page"
```

---

## Task 9: News page (`news.html`)

**Files:** Create `news.html`. Content source: existing `news.html` (the largest content page) + `news-alltext.html`.

- [ ] **Step 1: Build the page.** Standard head (title "News"); header (News `aria-current`); footer. `.page-head` band (`<h1>News</h1>`). A single `<ul class="news">` with every news item migrated verbatim, newest first:
```html
<li>
  <span class="date">MONTH YEAR</span>
  <div>
    <h2>Headline / item</h2>
    <p>Body text, with any links preserved.</p>
  </div>
</li>
```
If a source item has no date, omit the `.date` span’s text (keep the cell empty) rather than inventing one. Preserve any images in news items as `<img>` with descriptive alt.

- [ ] **Step 2: Run the Verification Recipe** against `news.html`. Expected: 0 violations; all items present.

- [ ] **Step 3: Commit**
```bash
git add news.html && git commit -m "Add accessible News page"
```

---

## Task 10: Photos pages (`photos.html` + year archives)

**Files:** Create `photos.html` and `2014_photos.html`…`2019_photos.html` (and a current-year page if the source implies one). Content source: existing `photos.html` (timeline of year links) and each `YYYY_photos.html`.

- [ ] **Step 1: Build `photos.html`.** Standard head (title "Photos"); header (Photos `aria-current`); footer. `.page-head` band (`<h1>Photos</h1>`). A `.year-index` of links to each year archive page:
```html
<main id="main" class="wrap block">
  <nav class="year-index" aria-label="Photo years">
    <a href="2019_photos.html">2019</a>
    <a href="2018_photos.html">2018</a>
    <!-- … through 2014 -->
  </nav>
</main>
```

- [ ] **Step 2: Build each `YYYY_photos.html`.** Same head/header/footer. `.page-head` band (`<h1>Photos — YYYY</h1>`). A `<section class="block"><div class="wrap"><div class="gallery">` containing every image from the source year page as:
```html
<figure><img src="images/timeline/YYYY/FILE.jpg" alt="DESCRIBE the photo (people, event).">
  <figcaption>Short caption if known.</figcaption></figure>
```
Migrate **all** images from each source year page. Provide a plain descriptive alt for each (these are casual lab photos — e.g. "Lab members hiking, 2018."). Add a "← All photo years" link back to `photos.html`.

- [ ] **Step 3: Run the Verification Recipe** against `photos.html` and one year page (e.g. `2018_photos.html`). Expected: 0 violations; images load.

- [ ] **Step 4: Commit**
```bash
git add photos.html 20*_photos.html && git commit -m "Add accessible Photos pages"
```

---

## Task 11: Contact page (`contact.html`)

**Files:** Create `contact.html`. Content source: existing `contact.html`.

- [ ] **Step 1: Build the page.** Standard head (title "Contact"); header (no primary item current; Contact lives in footer); footer. `.page-head` band (`<h1>Contact Us</h1>`). Then:
```html
<main id="main" class="wrap block">
  <div class="contact-maps">
    <img src="images/map_ames.jpg" alt="Map showing the lab’s location at Ames Hall, 3400 N. Charles St, Baltimore.">
    <img src="images/map_kki.jpg" alt="Map showing the scanner location at 707 N. Broadway, Baltimore.">
  </div>
  <ul class="contact-list">
    <li><strong>NPDL address:</strong> 3400 North Charles St, Ames Hall 108, Baltimore MD 21218</li>
    <li><strong>Scanner address:</strong> 707 North Broadway, Baltimore MD 21205</li>
    <li><strong>Phone:</strong> <a href="tel:+14108709895">(410) 870-9895</a></li>
    <li><strong>Video phone:</strong> <a href="tel:+14102145087">(410) 214-5087</a></li>
    <li>To participate, email <a href="mailto:plasticity_lab@jhu.edu">plasticity_lab@jhu.edu</a>.
        For lab business, email Elizabeth Droubi at <a href="mailto:edroubi1@jh.edu">edroubi1@jh.edu</a>.
        To reach the PI, email Dr. Marina Bedny at <a href="mailto:marina.bedny@jhu.edu">marina.bedny@jhu.edu</a>.</li>
  </ul>
</main>
```

- [ ] **Step 2: Run the Verification Recipe** against `contact.html`. Expected: 0 violations.

- [ ] **Step 3: Commit**
```bash
git add contact.html && git commit -m "Add accessible Contact page"
```

---

## Task 12: Resources & Data page (`resources-and-data.html`)

**Files:** Create `resources-and-data.html` (note: hyphenated filename, replacing the space-containing `resources and data.html`). Content source: existing `resources and data.html`.

- [ ] **Step 1: Build the page.** Standard head (title "Resources & Data"); header (no current item; it’s a footer link); footer. `.page-head` band (`<h1>Resources &amp; Data</h1>`). A `.prose` section with an `<h2>Data</h2>` and a real `<ul>` of links migrated verbatim (fix the source’s broken/unclosed `<a>` tags), e.g. `<li><a href="https://www.openicpsr.org/openicpsr/project/198832/version/V1/view">Blindness Resting State</a></li>`. Include every resource/data/script link present in the source.

- [ ] **Step 2: Add a redirect stub at the old space-named path.** Create `resources and data.html` containing only the redirect stub (see Task 13 template) pointing to `resources-and-data.html`, so old links keep working.

- [ ] **Step 3: Run the Verification Recipe** against `resources-and-data.html`. Expected: 0 violations.

- [ ] **Step 4: Commit**
```bash
git add resources-and-data.html "resources and data.html" && git commit -m "Add accessible Resources & Data page"
```

---

## Task 13: Redirect stubs for retired `-alltext.html` pages

**Files:** Overwrite each existing `*-alltext.html` with a redirect stub. The set: `index-alltext.html`, `publications-alltext.html`, `people-alltext.html`, `participate-alltext.html`, `news-alltext.html`, `contact-alltext.html`, `research-alltext.html`, `join_lab-alltext.html`, and any others present (run `ls *-alltext.html` to enumerate).

- [ ] **Step 1: Write the stub** into each file, pointing at its new equivalent (e.g. `index-alltext.html` → `index.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=TARGET.html">
<link rel="canonical" href="TARGET.html">
<title>Page moved</title>
</head>
<body>
<p>This page has moved. If you are not redirected automatically,
   <a href="TARGET.html">continue to the page</a>.</p>
</body>
</html>
```

- [ ] **Step 2: Verify** one stub: navigate to `http://localhost:8000/index-alltext.html`; expected: it lands on `index.html` (or shows the working text link).

- [ ] **Step 3: Commit**
```bash
git add *-alltext.html && git commit -m "Replace -alltext pages with redirect stubs to the unified accessible site"
```

---

## Task 14: Cross-page consistency check (nav/footer in sync)

**Files:** none (audit; fix any page that drifted).

- [ ] **Step 1: Diff the shared blocks across pages.** For each page, `browser_evaluate` to extract `document.querySelector('header.site').outerHTML` and `document.querySelector('footer.site').outerHTML`. Confirm header markup is identical across pages except the single `aria-current="page"` link, and footer is identical everywhere. Fix any mismatch.

- [ ] **Step 2: Confirm every nav link resolves.** For each link in the header/footer, confirm the target file exists (no 404s). Expected: all resolve.

- [ ] **Step 3: Commit** any fixes
```bash
git add -A && git commit -m "Sync shared header/footer across all pages"
```

---

## Task 15 (OPTIONAL): Publications topic filter (progressive enhancement)

Only do this if the lab wants topic filtering. The page must remain fully functional with this file absent.

**Files:** Create `js/enhance.js`; modify `publications.html` (add `data-topic` to `<li class="pub">`, add the `.toolbar` chip row, add `<script defer src="js/enhance.js"></script>` before `</body>`).

- [ ] **Step 1: Tag entries.** Add `data-topic="blindness-plasticity concepts-language development reviews"` (space-separated, any that apply) to each `li.pub`. Add the `.toolbar` from Task 5’s structure with `<button class="chip" data-filter="all" aria-pressed="true">All</button>` etc.

- [ ] **Step 2: Write `js/enhance.js`**
```js
// Progressive enhancement: filter publications by topic. Page works fully without this file.
document.querySelectorAll('.toolbar .chip').forEach(btn => {
  btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    document.querySelectorAll('.toolbar .chip').forEach(b => b.setAttribute('aria-pressed', b === btn));
    document.querySelectorAll('li.pub').forEach(li => {
      li.hidden = !(f === 'all' || (li.dataset.topic || '').split(' ').includes(f));
    });
    // hide year sections that end up empty
    document.querySelectorAll('section.year').forEach(sec => {
      sec.hidden = ![...sec.querySelectorAll('li.pub')].some(li => !li.hidden);
    });
  });
});
```

- [ ] **Step 3: Verify.** With JS on: clicking a chip filters and updates `aria-pressed`; empty years hide. With JS off (rename the file temporarily / block it): all entries still show. Run the Verification Recipe; expected 0 axe violations (buttons are real `<button>`s with `aria-pressed`).

- [ ] **Step 4: Commit**
```bash
git add js/enhance.js publications.html && git commit -m "Add optional publications topic filter (progressive enhancement)"
```

---

## Task 16: Remove dead template assets

**Files:** Delete unused template CSS/JS/fonts (see File Structure list).

- [ ] **Step 1: Confirm nothing references them.** `grep -rIl --include=*.html -e "main.js" -e "skel" -e "jquery" -e "js_Load" -e "main.min.css" -e "font-awesome" .` — expected: no matches among the new pages (only, possibly, the old stubs which no longer load them). Also `grep -rIl "css/site.css" *.html` should list all real pages.

- [ ] **Step 2: Delete** the dead files:
```bash
git rm js/main.js js/js_Load.js js/skel.min.js js/skel-layers.min.js js/init.js js/jquery.min.js js/slideshow.js \
  css/main.css css/main.min.css css/skel.css css/style.css css/style-*.css css/font-awesome.min.css css/W3.css
```
(Adjust to actual filenames from `ls js css`. Keep `js/enhance.js` if Task 15 was done. Remove `fonts/` only if `grep -r "fonts/" *.html css/site.css` is empty.)

- [ ] **Step 3: Re-verify** the Home and Publications pages still render correctly (no missing CSS). Run the Verification Recipe on both. Expected: unchanged, 0 violations.

- [ ] **Step 4: Commit**
```bash
git add -A && git commit -m "Remove unused TEMPLATED theme assets"
```

---

## Task 17: Final accessibility audit (whole site)

**Files:** none (audit; fix findings, then commit).

- [ ] **Step 1: axe pass on every page.** Run the axe snippet on each page (`index, research, publications, people, participate, join_lab, news, photos, one year page, contact, resources-and-data`). Expected: `[]` for all. Fix any finding.

- [ ] **Step 2: Heading-order pass on every page.** Run the heading snippet from the Verification Recipe. Expected: exactly one `h1` per page, no skipped levels.

- [ ] **Step 3: Keyboard + reflow.** On Home and Publications: tab through entirely (skip link → nav → content → footer), confirm visible focus throughout. Resize Playwright viewport to 320px wide and to 400% zoom equivalent; confirm no horizontal scrolling of content and nothing is clipped.

- [ ] **Step 4: Alt-text review list.** `grep -rno 'alt="[^"]*"' *.html` and produce a list of every image + its alt text. Flag any placeholder alt (the "WRITE DESCRIPTIVE ALT" markers from Task 3) and replace with a real description. Note in the PR/commit which alt texts the lab should sanity-check for scientific accuracy.

- [ ] **Step 5: Manual screen-reader spot check.** Using VoiceOver (macOS: ⌘F5), navigate Home and Publications by landmarks (rotor) and headings; confirm the reading order is sensible and figures are announced with their descriptions.

- [ ] **Step 6: Commit** any fixes
```bash
git add -A && git commit -m "Final accessibility audit fixes"
```

---

## Self-Review (completed by plan author)

**Spec coverage:** Goal → all tasks. "Why replace" (no-JS, alltext drift, non-semantic) → Tasks 3–13 + 16. Decisions table: independent brand → header/footer text; no-build plain HTML → whole approach; keep pages → Tasks 3–12; peer audience → Publications/Research emphasis; teal editorial-sans → Task 2 CSS; baseline-only a11y (no widgets) → no toggle tasks, Verification Recipe; redirect stubs → Tasks 12–13; one-pass rollout → all pages built together. A11y approach → Task 2 (skip link, focus, landmarks, reduced-motion), per-page Verification Recipe, Task 17. IA → Task 2 header/footer + page tasks. Visual system → Task 2. Page-by-page → Tasks 3–12. Tech architecture → Tasks 1, 2, 16. Migration/no content lost → verbatim-migration rule + count checks in Tasks 5, 6, 9. Out of scope honored (no CMS/dark-mode/search). 

**Placeholder scan:** Intentional, flagged placeholders only where content must come from source files (per-page "migrate verbatim from X") or lab-verified alt text ("WRITE DESCRIPTIVE ALT", resolved in Task 17). Full reusable code (CSS, header, footer, Home, filter JS) is provided literally. No "add error handling"-style vagueness.

**Type/name consistency:** CSS class names used in page tasks (`.hero`, `.area`, `.area.flip`, `.thesis`, `.pubcard`, `.layout`, `nav.years`, `li.pub`, `.person`, `.people-group`, `ul.news`, `.gallery`, `.year-index`, `.join`, `.contact-maps`, `.contact-list`, `.kicker`, `.read`, `.btn*`, `.chip`) all match definitions in Task 2 `site.css`. Filenames consistent (`resources-and-data.html` new + `resources and data.html` stub; `*-alltext.html` stubs). `js/enhance.js` referenced only in Task 15.
