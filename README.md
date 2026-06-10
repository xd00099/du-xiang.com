# du xiang · personal site

The personal site of Du Xiang, currently styled as **2003–2007 web standards
minimalism**: a white 760px page on warm gray, Georgia prose, Verdana metadata,
dotted borders, float-based layout, 80×15 antipixel badges, a blogroll, a
colophon, and a hand-coded RSS 2.0 feed. Built with [Astro](https://astro.build).

(The previous incarnation was a faithful 1999 GeoCities cyber-home — starfield,
MIDI jukebox, guestbook — and before that a 2026 dark-mode portfolio. The git
history remembers everything.)

## Pages

| Route | What's there |
| :--- | :--- |
| `/` | Front page: intro, recent essays, brief timeline, sidebar |
| `/blog` | The essay archive, grouped by year |
| `/blog/<slug>` | Long-form essays (technical + personal, one bilingual) |
| `/links` | The blogroll + 80×15 "link to me" button |
| `/colophon` | The obligatory page about the fonts |
| `/rss.xml` | Full-text RSS 2.0 feed |

## Generated assets

- `scripts/make_2005_badges.py` — antipixel badges, XML chiclet, feed icon → `public/standards/`
- `scripts/make_retro_gifs.py` — the 1999 GIF set (starfield, construction banner, counter digits) → `public/retro/` (kept for posterity; the colophon links to it)

## Commands

| Command | Action |
| :--- | :--- |
| `npm install` | Installs dependencies |
| `npm run dev` | Starts local dev server at `localhost:4321` |
| `npm run build` | Build the production site to `./dist/` |
| `npm run preview` | Preview the build locally |

Deploys to GitHub Pages automatically on push to `master`.

## Gotchas (learned the hard way)

The Astro compiler's HTML parser has sharp edges around old-school markup:

- A `<textarea>` with literal text content inside a `<table>` makes the compiler
  drop the table's closing tag (everything after gets swallowed into the table).
  Fix: use expression content — `<textarea>{snippet}</textarea>`.
- An expression that yields `<div>`s as the direct content of a *static* `<td>`
  does the same. Fix: have expressions yield whole `<tr>` rows instead.
- Don't nest `<center>` inside `<center>`. Use `<div align="center">` inside tables.
- `new Date('YYYY-MM-DD')` parses as UTC midnight and renders the previous day
  in US timezones. Parse date-only strings at noon.
