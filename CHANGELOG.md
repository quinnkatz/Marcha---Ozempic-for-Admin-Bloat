# Changelog — Marcha interaction system

The public page is a scene-based marketing site. The $1,999 assessment price is withheld until after recognition, Why Marcha, economics, and trust. Implementation is separately scoped. Sticky scrub is shorter: hours and the before/after hold at 140vh, and the diagnostic device at 190vh.

## Techniques implemented

1. **Full-viewport brand loader.** Teal-ink field (`#223034`), white M, orange ring (`#FF5A1F`). The ring draws on, then the loader wipes upward to reveal the white page. Repeats on each fresh load. Skipped when `prefers-reduced-motion: reduce`.
2. **White canvas, condensed display, punchy orange, teal ink.** Canvas `#FFFFFF`, ink `#223034`, accent `#FF5A1F`, body `#333333`. Barlow Condensed uppercase for display and nav; Barlow for copy. Orange discs use a lighter highlight of the same orange. Cards carry a hairline and a stronger shadow so they still lift off white. Practice tiles use only white, ink, orange, and a light blue wash.
3. **Scene-based sticky scroll.** `YOUR TEAM GETS HOURS BACK`, the before/after mask, and the prescription mockup are pinned scenes with tall tracks. Progress comes from scroll position, not a stack of equal document sections. The squeeze, why-Marcha, and offer rows are overlapping plates on orange discs — rotated, clipped, and lifted — rather than equal card grids.
4. **Clipped layers and moving plates.** Hero disc is cropped by the scene. Oversized outline words (`SQUEEZE`, `HOURS`) translate behind `overflow: hidden` masks. Stacked cards overlap only on empty corners — every visible line is complete at rest. Cards stack at several shadow elevations.
5. **Hover affordances that draw.** Text CTAs grow an underline with `scaleX(0 → 1)` (500ms, origin left) and nudge the arrow 6px (300ms). Nav color transitions in 500ms. Cards lift and pick up an orange glow. The eye-badge ticks rotate. Tile art scales inside its mask.
6. **One scroll-linked device.** In How it works, a fixed browser frame keeps its bezel while the inner plan (discover → map → prescribe → deliver) translates with scene progress. Each plan fills the white screen and holds there; only the handoff between steps crosses the clip, so titles stay inside the frame instead of sitting under the chrome. A thumb on the inner track and a SCROLL cue move with it. The eye control advances one step.
7. **Slim progress rail and scroll cues.** Fixed left rail with a traveling orange segment, circular up/down controls, hero copy track with an orange segment, and the device SCROLL pill.
8. **Contextual cursor, used sparingly.** An orange SCROLL cursor scales from 0 to 1 only over the hero mock and the prescription screen (~300ms). It hides on links, buttons, and fields. It is not mounted for coarse pointers or reduced motion.
9. **Nav reveal.** Process opens a clipped submenu (`overflow: hidden`, children rise into the mask) without changing header height.
10. **Depth on white.** Cards, discs, and shadows carry the dimension. The page canvas stays plain white, with no grey noise veil. Motion is scroll-linked and hover-drawn; nothing ambient-bounces.
11. **Rituals of depth.** The loader holds about a second and a half, then wipes into a staggered hero. Orange discs are oversized and clipped by the scene. The hours title leaves a ghost trail while the line in the card rises into place. The before/after mask has an inset lip, and the disc behind the plates drifts at a different rate than the plates. Hover draws underlines (500ms), nudges arrows (300ms), lifts plates into an orange shadow, and staggers the rows inside a mock window. The left rail carries a scene name with the orange segment. `prefers-reduced-motion` still unpins the tracks and drops the trail.
12. **Hand-feel.** Hover micros settle on `cubic-bezier(0.16, 1, 0.3, 1)` in 300ms, with row stagger at most 120ms. Underlines and color stay at 500ms. Sticky scrub is shorter: hours 210vh, shift 165vh (readable hold, short slide, readable hold), device 250vh with an 80% dwell so a plan is readable and the handoff is a beat. Disc parallax is smaller and locked to scroll position. A smoothstep eases the travel at the start and end of a scene, and the disc stops the moment the scroll stops.
13. **Launch path.** Share card and canonical URL point at the GitHub Pages root. The booking form checks name, email, and practice type, then opens mail, and it disables the button while that handoff runs. The mobile book bar appears after the hero and steps aside at the form and while the menu is open. On a phone the process steps and the plan sheets stack in full instead of sitting inside a clipped frame. `prefers-reduced-motion` still unpins the tracks.

## Story order

Hero (promise + what Marcha sells) → recognition → why Marcha → economics → booked-vs-paid → philosophy → diagnostic → a shorter leave-with → trust → **then** the $1,999 assessment → a later Tuesday → monologue → who / leadership → FAQ → book. The fee is not in the hero or in Why Marcha.

## Preview

`python3 -m http.server 8000` then open `http://localhost:8000/`.

Screenshot helpers (loader stays up only for `loader`):

`?preview=loader|hero|problem|hours|shift|mock|who|why|offer|faq|book`
