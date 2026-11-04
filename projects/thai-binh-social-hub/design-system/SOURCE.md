# Thai Binh design system — offline snapshot

- **Live source of truth:** Claude Design System artifact "Thai Binh Corporation", https://claude.ai/artifact/DWNMgAxFRgSUc4PWrAo1C1
- **Brand Assets library (logos as plain files):** https://claude.ai/artifact/T9Hf7U5NJwD5hd5HNHA1h5
- **Snapshot taken:** 2026-11-04, from artifact version `1793752467-aa7d` (last change by "Quijote", note: "Re-extracted corporate logo …").

| File | What |
|---|---|
| `tokens.json` | Exact copy of `project/tokens.json`: colors (light = content, dark = section), Montserrat type styles at slide scale (1440×810), spacing, radius, shadow |
| `bundle.css` | Exact copy of `project/components/bundle.css`: `tb-*` slide component patterns |
| `BRAND_README.md` | The brand book text: voice, color, type, layout and iconography rules (generated "Consuming" section removed) |

**Not included:**
- **Logo PNGs:** get them from the Brand Assets library (`logos/*.png`) or unzip the BOD deck (`ppt/media/`). Never recolour, stretch or redraw them.
- **3D icons and real photography:** these aren't in the design system yet (owner action).

**Rules for this project:**
- The snapshot is read-only reference data. If the live artifact changes, re-snapshot it; don't hand-edit these files.
- The app's mobile type scale, motion tokens and gamified components are a **new App & Gamification layer** (PLAN.md › UX/UI plan). Publish it to the live design system only with owner approval.
