# Marcha — AI tools assessments for medspas

The public site is a short marketing page for Marcha’s **$1,999 business assessment**. The story is hero (what Marcha sells) → one recognition beat → economics → the offer (judgment, including how sensitive data is handled) → about → one data FAQ → fit call. Implementation is scoped and priced separately, after the assessment. The fee is not in the hero.

Plain HTML, CSS, and vanilla JS. No build step.

```sh
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000).

The assessment instruments under `tools/` load JSON with `fetch`, so they need that static server too. `index.html` itself can also be opened as a file.

## Marketing site

| File | Role |
|------|------|
| `index.html` | Scenes, copy, booking form |
| `styles.css` | Canvas, ink, orange disc system, sticky scenes |
| `main.js` | Loader, scroll-linked mockup, rail, cursor, nav, mailto |
| `brand.js` | Name, email, tagline (`data-brand` hooks) |
| `CHANGELOG.md` | Scene-system techniques and where they live |
| `previews/` | Scene screenshots |

Screenshot helpers: `?preview=loader|hero|problem|hours|shift|mock|why|offer|faq|book`. For the plan frame, `?preview=mock&at=0.55` parks on a settled sheet (`at` is 0–1).

Booking opens a `mailto:` to the address in `brand.js`. The form checks name, email, and practice type first, then disables the button while the mail app opens. Voice on the page is we / our team. Beachhead copy leads with medspas.

## Publishing

GitHub Pages for this repo is already on, from the **`main` branch**, path `/`:

[https://runmarcha.com/](https://runmarcha.com/)

`canonical`, `og:url`, `og:image`, `sitemap.xml`, and `robots.txt` use that URL. Merge to `main` when the page should go live. A custom domain later means updating those five spots to the new origin. The worksheets under `tools/` stay `noindex` and are disallowed in `robots.txt`.

## The toolkit

The worksheets that deliver the assessment live in `tools/`. They stay client-side: a practice’s week is sensitive even when it carries no patient names, so there is no database and no account.

```
worksheet ──intake.json──> prescription builder ──report.json──> printed PDF
                                   ↑
                            vendor register
```

**`tools/intake/`** — twenty-one questions across six areas, ordered so the practice describes its week before anyone says software. Autosaves on the device and exports the file the builder reads.

**`tools/report/`** — loads a worksheet, puts a named tool against each bottleneck, and computes hours returned × hourly value × 52, minus what the software costs. If the total falls under five hours a week, the interface and the report say the assessment is free.

**`tools/vendors/`** — the register. Every entry starts at `unverified`. A BAA position only leaves that state with a `source_url` and a `verified_on` date.

```sh
node scripts/validate-data.mjs   # register vs schema
node scripts/test-validate.mjs   # negative tests for those rules
node scripts/check-pages.mjs     # pages parse, local links resolve
```

Prices need a `checked_on` date. Anything verified over a year ago warns. The register ships with unverified BAA positions on purpose — verification is a human step with a source.

## Licence

[MIT](LICENSE). The code is reusable. The copy and the Marcha name are not.
