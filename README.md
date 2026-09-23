# Frigeri & Co. — The Practice Hours Audit

A single-page marketing site for a nurse-led operations practice. Plain HTML, CSS and
vanilla JS — no build step, no dependencies, no framework. Open `index.html` in a
browser and it works.

## Before it goes live

Everything that needs filling in lives in one place: the `SITE` object at the top of
the `<script>` block near the bottom of `index.html`.

```js
var SITE = {
  BOOKING_URL: "",              // Cal.com / Calendly / SavvyCal link
  CONTACT_EMAIL: "",            // where replies should land
  SUBJECT: "The Practice Hours Audit — a question"
};
```

How the page behaves before you fill those in:

| Setting | Empty | Filled |
| --- | --- | --- |
| `BOOKING_URL` | "Book a call" buttons scroll to the on-page form | Buttons open the calendar in a new tab |
| `CONTACT_EMAIL` | Email links stay hidden; the form says it isn't set up | Form composes a pre-filled email in the visitor's own mail app |

If both are empty, a dashed amber setup note appears in the booking section so the
state is obvious in the browser. It disappears as soon as either is set.

## What's on the page

Hero → the problem → an hours/rate calculator → how it works → what's in the report →
pricing → fit → who we are → FAQ → booking and contact form → footer.

## Notes

- **No backend.** The contact form builds a `mailto:` draft in the visitor's own email
  client; nothing is stored or posted anywhere. If a real form endpoint is wanted later
  (Formspree, Basin, a serverless function), it replaces the `submit` handler only.
- **No patient data.** The form copy says so explicitly, and it should stay that way.
- **Theme.** Follows the system setting, with a manual override remembered in
  `localStorage` (wrapped in try/catch so private browsing can't break the page).
- **Accessibility.** Skip link, landmarks, labelled sections, visible focus rings,
  `prefers-reduced-motion` respected, and a page that works with JS disabled apart from
  the calculator and the form.
- **SEO/social.** Description, Open Graph and Twitter tags, JSON-LD `ProfessionalService`
  schema, and a `404.html`. Add an `og:image` and an absolute `og:url` once the domain
  is settled.

## Deploying

Any static host works — drop the folder on Netlify, Cloudflare Pages, Vercel, or turn on
GitHub Pages for this repo. `404.html` is picked up automatically by all of them.

Local preview:

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```
