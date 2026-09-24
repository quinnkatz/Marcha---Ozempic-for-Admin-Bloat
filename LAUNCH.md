# Launch

## Live URL after merge

GitHub Pages publishes the **`main`** branch from the repository root:

https://quinnkatz.github.io/Marcha---Ozempic-for-Admin-Bloat/

The work on this branch is not live until it is merged. Do not expect the share card or the new pages to resolve on that URL before the merge.

## Preview locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. The assessment tools under `tools/` need that same server because they load JSON with `fetch`.

## Morning checklist

- [ ] Merge the open pull request into `main` when the page should go live.
- [ ] Custom domain later: update `canonical`, `og:url`, `og:image`, `twitter:image` in `index.html`, the URL in `sitemap.xml`, and the Sitemap line in `robots.txt`.
- [ ] Calendly is not connected. The book form opens the visitor’s mail app to hello@runmarcha.com. Stripe and email DNS are not set up either.
- [ ] Send one test request from a phone and confirm the draft looks right.
