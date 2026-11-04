# BOD pitch deck — rebuild

`build.js` generates `../Thai-Binh-Social-Hub-BOD-Pitch-VI.pptx`: 13 slides in Vietnamese with speaker notes, on the Thai Binh design-system tokens.

To rebuild locally:

```bash
cd projects/thai-binh-social-hub/deck
npm init -y >/dev/null
npm install pptxgenjs@3.12.0 react-icons@5.3.0 react@18.3.1 react-dom@18.3.1 sharp@0.33.5
# Logos: put the six PNGs from the TBCorp Brand Assets library (logos/*.png) in ./logos
#   https://claude.ai/artifact/T9Hf7U5NJwD5hd5HNHA1h5  — or unzip the current deck: ppt/media/
node build.js
```

- `node_modules/` and `logos/` are not committed.
- Optional: set `PPTX_SKILL=<path to the pptx skill>` to also write the theme colours into the file.
- Install **Montserrat** (Google Fonts, OFL licence) on any computer that presents or edits the deck. Without it, PowerPoint substitutes another font.

Open data gaps in the deck:
- **Slide 2:** follower count and average engagement, shown as `[ ? ]`; take them from Meta Business Suite.
- **Slide 11:** cost figures, marked "Cần báo giá" (quote needed) or "Marcom đề xuất" (Marcom to propose).
