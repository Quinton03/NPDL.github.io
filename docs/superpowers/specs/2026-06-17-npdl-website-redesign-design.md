# NPDL Website Redesign — Design Spec

**Date:** 2026-06-17
**Project:** Full redesign of the Neuroplasticity & Development Laboratory (Bedny Lab) website (`NPDL.github.io`)
**Status:** Draft for review

---

## 1. Goal

Fully redesign the Bedny Lab / NPDL website while **preserving all existing content**. The
redesign replaces a dated free template ("Ion" by TEMPLATED) and its fragile accessibility setup
with a single, modern, **highly accessible** site.

**The defining requirement: accessibility.** This lab studies blindness and brain plasticity;
blind colleagues, participants, and peers are a core part of its audience. The site must be
excellent with a screen reader and keyboard, not merely passable.

## 2. Why the current site needs replacing

Observed in the existing code:

- **Content hidden until JavaScript runs.** Every page uses `<body style="visibility:hidden" onload="js_Load()">`.
  If JS is slow, blocked, or fails, the page shows *nothing*. This is the single worst issue —
  catastrophic for accessibility, performance, and resilience.
- **A separate, drifting accessibility track.** Accessibility is handled by a parallel set of
  `-alltext.html` pages. They have already fallen out of sync (e.g. the all-text home page is
  missing the Photos link and has broken/unclosed markup). This is the classic "separate but
  unequal" anti-pattern.
- **Non-semantic markup.** Headings used for links ("CLICK HERE FOR ALL TEXT"), `<h3>`/`<h4>`
  nested directly inside `<ul>`/`<ol>`, `<br>` used for layout spacing, content images with empty
  `alt=""`, layout via floats and inline styles.

## 3. Decisions (confirmed with stakeholder)

| Area | Decision |
|---|---|
| **Branding** | Fully independent lab identity. No requirement to match Johns Hopkins brand styling (affiliation is acknowledged in text/footer). |
| **Build/tech** | Plain, hand-editable HTML + CSS. **No build step.** Hosts as-is on GitHub Pages. |
| **Site structure** | Keep the same pages. Redesign + make accessible; refine navigation grouping only. |
| **Primary audience** | Academic peers (scholarly, publication-forward) — with accessibility as the non-negotiable baseline. |
| **Visual direction** | Deep-teal cool palette; **editorial layout** (kickers, hairline rules, numbered sections, thesis band, masthead) in a **clean system sans** typeface; **image-forward** using the lab's existing figures. |
| **Accessibility scope** | Strong WCAG 2.1 AA baseline only — no dark-mode/text-size/contrast widgets; rely on semantics, contrast, and the visitor's own OS/browser tools. |
| **Old `-alltext.html` URLs** | Replaced by redirect stubs that forward to the new equivalent page. |
| **Rollout** | Whole site redesigned in one pass. |

## 4. Accessibility approach (the core of this project)

Target: **WCAG 2.1 AA** as a floor; AAA where it's free.

**Structure & semantics**
- Valid HTML5 with one `<h1>` per page and a correct, non-skipping heading hierarchy.
- Landmark elements on every page: `<header>`, `<nav aria-label>`, `<main id="main">`, `<footer>`.
- Real lists for lists; `<figure>`/`<figcaption>` for figures; `<table>` only for tabular data.
- A visible **"Skip to main content"** link as the first focusable element.

**No-JavaScript resilience**
- All content and navigation are plain HTML and fully usable with JavaScript disabled.
- **The `visibility:hidden`/`onload` pattern is removed entirely.** Nothing is hidden waiting on JS.
- Any JS is *progressive enhancement only* (e.g. the optional publications topic-filter); the
  underlying content works without it.

**Keyboard & focus**
- Everything operable by keyboard in a logical tab order.
- Clear, high-visibility `:focus-visible` styles on all interactive elements.

**Images & media**
- Every content image (brain figures, MDS plots, etc.) gets **descriptive `alt` text** conveying
  the scientific point, not a filename. Decorative images use `alt=""`.
- Figures use `<figure>` + `<figcaption>`.

**Color & contrast**
- All text/background combinations meet AA (≥4.5:1 normal, ≥3:1 large). Palette chosen to clear
  this comfortably; every combination is verified during implementation.
- Information is never conveyed by color alone (links are underlined or otherwise marked; topic
  tags carry text labels).

**Motion & responsiveness**
- `prefers-reduced-motion` respected (animations/transitions reduced or removed).
- Layout is responsive and reflows without loss of content/function down to 320px and up to 400%
  zoom. Text uses relative units (`rem`/`em`) so OS/browser text scaling works.

**Forms (Participate / Contact)**
- Every field has an associated `<label>`; errors are announced and programmatically associated.

**Verification (done during implementation)**
- Automated pass (axe / WAVE), manual keyboard pass, and a screen-reader pass (VoiceOver) on
  every page type. HTML validated.

## 5. Information architecture

All existing pages are kept. Navigation is grouped for clarity:

- **Primary nav (header):** Home · Research · Publications · People · News · Photos · **Participate** (call-to-action button)
- **Footer (secondary):** Contact · Join the Lab · Resources & Data · affiliation/contact details · Google Scholar
- **Photos** retains its per-year archive (2014–2019 + current) as sub-sections/links within the Photos page.
- **Join the Lab** is reachable from Participate, People, and the footer.

Full page inventory (all preserved): Home, Research, Publications, People, Participate, Join the
Lab, News, Photos (+ year archives), Contact, Resources & Data.

## 6. Visual design system

**Palette (CSS custom properties)**
- Paper `#f7faf9` (page), Card `#ffffff`, Cool `#eaf1ef` (section bands)
- Ink `#11201e` (headings), Body `#243431`, Muted `#5d6b69`
- Teal `#0a4542` (primary), Teal-deep `#06302d` (gradient end), Teal-bright `#0e6a63` (hover)
- Hairline/border `#d4dddb` / `#c2cecb`

**Typography**
- System sans stack only (no external/Google fonts) → fast, private, dependency-free:
  `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Editorial *feel* comes from layout and hierarchy, not a special typeface: bold tight headlines,
  uppercase letter-spaced "kicker" labels with a short rule, italic captions, numbered sections.

**Reusable components**
- Masthead/header (sticky) with wordmark + primary nav + Participate CTA.
- Hero band (teal gradient): kicker, headline, lead, buttons, figure with caption.
- Section header: small-caps label + hairline rule + optional "see all" link.
- "Thesis" statement band (one editorial pull-statement).
- Research entry: numbered (01/02), figure + heading + text + read-more.
- Featured publication card.
- Publication list: year sections + sticky "jump to year" anchor rail + citation items
  (authors with PI bolded, linked title, italic venue, topic tags) + optional JS topic filter.
- People card: photo + name + role + research-interest text + links.
- Participate/Join band: photographic background with dark scrim + CTAs.
- Footer: wordmark, affiliation, contact, explore links.

A single shared `css/site.css` holds all tokens and component styles. Page-specific tweaks live in
small, clearly-labeled blocks.

## 7. Page-by-page treatment

- **Home** — Hero (mission question + lead + CTAs + Fig. 1), thesis band, Research preview (01/02
  with figures), Featured/recent publication, Participate/Join band. *(Mockup approved.)*
- **Research** — Full version of the research areas: cortical plasticity in blindness, conceptual
  development, and any additional threads, each with figures + descriptions + key papers.
- **Publications** — Year-grouped list with sticky year rail, Google Scholar callout, PI-bolded
  citations, linked titles, italic venues, optional topic filter. *(Mockup approved.)*
- **People** — Grouped by role (PI, Postdocs, PhD students, etc.), each person as a card with
  photo (descriptive alt), name, role, interests, and links. Includes alumni.
- **Participate** — Plain-language description of studies, who can take part (blind & sighted
  volunteers), and an accessible sign-up/contact path.
- **Join the Lab** — Openings and how to apply, for prospective students/postdocs.
- **News** — Reverse-chronological updates (the current site's largest content page), as a clean
  dated list/timeline.
- **Photos** — Accessible image gallery with captions and alt text; per-year archive retained.
- **Contact** — Address, phone, email (as real `mailto:` links), map/directions, lab location.
- **Resources & Data** — Links to datasets, tools, and `fMRI scripts`/`forms` resources.

## 8. Technical architecture

- **Static HTML + CSS**, no build step, served directly by GitHub Pages (existing `CNAME`
  preserved). Optional vanilla JS only as progressive enhancement.
- **Shared header/footer without a build step:** because there is no templating, the semantic
  header nav and footer are repeated in each page's HTML (this keeps them working without JS, which
  is the accessible choice). Each shared block is wrapped in clearly marked
  `<!-- SHARED HEADER — keep in sync across pages -->` comments so lab members know what to copy
  when editing. (~10 pages; acceptable duplication.)
- **File organization:** one `css/site.css`; images stay under `images/`; PDFs under `pubs/`. Dead
  template assets (skel.js, jQuery, font-awesome, old `main.css`, `js_Load.js`, etc.) are removed.
- **Fonts:** none loaded over the network (system stack). The unused `fonts/` template files are
  removed unless referenced.
- **Editability:** pages are well-commented and use plain, readable HTML so non-developers can
  update content (add a publication, a person, a news item) by copy-editing an existing entry.

## 9. Migration & content preservation

- **No content is lost.** Text, citations, people, news, photos, and resource links are carried
  over verbatim (cleaned up only where markup was broken).
- The parallel `-alltext.html` pages are **retired**; each old path is replaced with a minimal
  redirect stub (`<meta http-equiv="refresh">` + canonical link + a plain text link) pointing to
  the new equivalent page, so existing bookmarks/links don't break.
- Existing `index-alltext.html`, etc. → redirect to `index.html`, etc.

## 10. Out of scope (possible future work)

- CMS / build pipeline / templating (explicitly declined — staying no-build).
- Search, dark-mode toggle, text-size/contrast widgets (declined — baseline only).
- New content creation (we redesign existing content; new copy is the lab's to add later).
- Automated publication import from Google Scholar.

## 11. Open questions

None blocking. Minor items to confirm during implementation:
- Final per-figure alt-text wording (drafted by us, lab to verify scientific accuracy).
- Exact primary-nav label order if the lab has a preference.
