# Rebuilding the PDF

The illustrations are generated vector drawings, not raster assets, so the book
prints cleanly at any size.

- `art.py` — the drawing primitives: bots, people, clouds, limbs, eyes, palette.
- `scenes.py` — one function per illustration. Canvas is 900×720, matching the
  10in × 8in page exactly so nothing gets cropped when it bleeds.
- `build.py` — page sequence, verse, CSS, and the HTML assembly.

```sh
pip install pymupdf                       # only needed for the preview renders
python3 build.py                          # -> book.html (font embedded as base64)
chromium --headless --no-pdf-header-footer \
         --print-to-pdf=book.pdf book.html
```

Two layout modes for illustrated pages: a side `panel` (verse in a bordered
card, left or right — keep the art in the opposite half) and a `band` (full
width caption along the bottom, used for the dark cinematic spreads — keep
everything above y≈556 on the canvas).

Type is Fredoka, embedded from `fonts/`.
