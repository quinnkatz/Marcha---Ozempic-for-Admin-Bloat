# Frigeri &amp; Co. — The Practice Hours Audit

The site and the working tools behind a nurse-led operations practice: a fixed-scope
audit that finds the admin hours a small healthcare practice loses every week, and
prescribes the specific software that gives them back.

Plain HTML, CSS and vanilla JS. No framework, no build step, no dependencies —
`git clone` and open it. Everything runs in the browser and keeps its state on the
device, which is a deliberate choice rather than a shortcut (see
[Why there is no backend](#why-there-is-no-backend)).

```
.
├── index.html              the public site
├── 404.html
├── tools/                  the instruments the audit is actually delivered with
│   ├── intake/             step 02 · the audit call worksheet
│   ├── report/             step 03 · the prescription builder
│   └── vendors/            the vendor register browser
├── data/
│   ├── vendors.json        the register
│   ├── vendors.schema.json its schema, including the verification rules
│   └── intake-questions.json
├── scripts/                zero-dependency checks, run in CI
└── assets/                 shared design tokens and helpers
```

## The tools

The audit is a product, so it has instruments rather than a folder of half-named
documents. The three hand work to each other as plain JSON files:

```
worksheet ──intake.json──> prescription builder ──report.json──> printed PDF
                                   ↑
                            vendor register
```

**`tools/intake/` — the audit worksheet.** Twenty-one questions across six areas of a
practice, ordered so the practice describes its week before anyone says the word
software. Records bottlenecks in the owner's own words with an hours-per-week
estimate, autosaves to the device, and exports the file the builder eats.

**`tools/report/` — the prescription builder.** Loads a worksheet, puts a named tool
against each bottleneck, and computes the arithmetic: hours returned × hourly value ×
52, minus what the software costs. Renders the four printable pages. If the total
falls under five hours a week it says so in the interface and on the report itself,
because that is the point at which the audit is free.

**`tools/vendors/` — the register.** Every tool worth considering, and the honest state
of what has been checked about each one.

## The rule this repo is built around

A practice cannot adopt a tool until it knows whether that tool may touch patient
information. Getting that answer wrong is not a bad recommendation, it is a compliance
problem — so the register is built so that guessing is impossible rather than merely
discouraged.

Every entry starts at `unverified`. A BAA position only leaves that state with a
`source_url` and a `verified_on` date, and `scripts/validate-data.mjs` fails the build
otherwise:

```jsonc
"baa": {
  "status": "offered_on_tier",   // requires all three fields below
  "tier": "Enterprise",
  "source_url": "https://…",     // where the vendor says so, in writing
  "verified_on": "2026-01-15",
  "notes": ""
}
```

Prices follow the same discipline: a number requires a `checked_on` date, because
prices move. Anything verified over a year ago raises a warning rather than passing
quietly.

**The register currently ships with 20 vendors and 0 verified BAA positions.** That is
not an oversight — it is the honest state of the data, and it is what the tool is
supposed to show until someone does the reading. Verification is a human step with a
source, and the schema will not let it be faked.

## Checks

```sh
node scripts/validate-data.mjs   # the register against its schema and the rules above
node scripts/test-validate.mjs   # 12 negative tests — proves each rule actually bites
node scripts/check-pages.mjs     # every page parses, every local link resolves
```

`check-pages.mjs` exists because a repo with no build step has no compiler to catch a
moved file or a typo inside a `<script>` block. It parses every inline script, resolves
every local `href` and `src` against the filesystem, and checks each page carries the
meta tags it needs to work on a phone. All three run on every push
([`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## Why there is no backend

A practice's week, written down, is sensitive even when it carries no patient names.
Every tool here is client-side: there is no database to breach, no accounts to manage,
and no extra vendor for anyone to add to a risk assessment — including this one. The
contact form on the public site composes a `mailto:` draft rather than posting
anywhere.

The cost is that clearing browser data clears unsaved work, so both tools autosave to
the device and export a file, and say so in the interface.

## Running it

```sh
python3 -m http.server 8000     # then open http://localhost:8000
```

A static server is needed rather than opening the files directly, because the tools
`fetch` their data from `data/`. The public site at `index.html` works either way.

Deploy anywhere static — GitHub Pages, Netlify, Cloudflare Pages, Vercel. `404.html` is
picked up automatically by all of them.

## Before the site goes live

One config object at the bottom of `index.html`:

```js
var SITE = {
  BOOKING_URL: "",     // Cal.com / Calendly / SavvyCal link
  CONTACT_EMAIL: ""    // where replies should land
};
```

While `BOOKING_URL` is empty the booking buttons scroll to the on-page form instead of
sitting dead. While both are empty a setup note shows in the booking section so the
state is obvious in the browser.

## Licence

[MIT](LICENSE). The code is reusable; the copy, the register's contents and the
Frigeri &amp; Co. name are not.
