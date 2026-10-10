# Verified Dataset Sources (200 OK via webfetch, 2026-10-10)

Replaces dead endpoints in `UniversalSkill-GitaRamayanaBibleQuran.md:23-29`:
`vedicscriptures/bhagavad-gita-api verse.json` 404, `risan/quran-json quran.json` 404, `scrollmapper/bible_databases t_web.json` 404.

## 1. Bhagavad Gita — 18 ch, 700 verses — Bundle

- `https://raw.githubusercontent.com/gita/gita/main/data/verse.json` (~659 KB, Sanskrit + IAST + meanings)
- `https://raw.githubusercontent.com/gita/gita/main/data/chapters.json` (~44 KB, summaries)
- License: `https://raw.githubusercontent.com/gita/gita/main/LICENSE` = Unlicense (PD dedication)
- Bundle verse.json + chapters.json. Link, don't bundle `translation.json` (2.3 MB, check credit) and `commentary.json` (28 MB).

## 2. Dhammapada — 26 vaggas, 423 verses — Link via API

- `https://suttacentral.net/api/suttas/dhp1/sujato?lang=en` (suttaplex dhp1-20)
- `https://suttacentral.net/api/bilarasuttas/dhp1-20/sujato?lang=en` (Pali root + Sujato EN)
- License: Pali Mahasangiti = PD; Sujato EN (2021) = CC0. Buddharakkhita/Feldmeier/Anandajoti = copyrighted, do NOT bundle.
- Cache per-vagga at runtime. Note: SuttaCentral requests no LLM training use — respect + attribute.

## 3. Qur'an — 114 surahs, 6236 ayahs — Bundle AR + Pickthall only

- AR: `https://cdn.jsdelivr.net/npm/quran-json@3.1.2/dist/quran.json` (~1.7 MB)
- EN Pickthall: `https://tanzil.net/trans/en.pickthall` (pipe `sura|aya|text`), terms `https://tanzil.net/download` (verbatim + credit + linkback, no modification)
- License: Arabic Tanzil = free-verbatim + attribution (CC-BY-like), NOT PD. Pickthall (d.1936) = PD life+70.
- WARNING: Saheeh International / Yusuf Ali are copyrighted. Do NOT bundle `quran_en.json` (Saheeh) as PD. `risan/quran-json` redistributes restricted editions — avoid.

## 4. Holy Bible WEB — 66 books — Bundle subset or link

- Per-verse: `https://bible-api.com/John+3:16` (`translation_id:web`, PD — verified)
- Per-book JSON: `https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/genesis.json`
- Terms: `https://ebible.org/details.php?id=engwebp` — PD; trademark: if modified don't call it "World English Bible"
- Bundle needed books (Proverbs, Ecclesiastes, Psalms, Gospels) or link bible-api.com / eBible USFM.

## 5. Valmiki Ramayana — 7 Kandas, ~24k shlokas — Bundle Sanskrit + PD EN

- Sanskrit per-kanda: `https://raw.githubusercontent.com/bhavykhatri/DharmicData/main/ValmikiRamayana/1_balakanda.json` (pattern 1-7, 0.7-1.8 MB each, ~8 MB total). Listing: `https://api.github.com/repos/bhavykhatri/DharmicData/contents/ValmikiRamayana`
- EN PD: `https://sacred-texts.com/hin/rama/index.htm` (Griffith, "Public domain", 506 ch)
- License: Griffith (1895) / Dutt (1891-94) = PD. DharmicData compilation = ODbL-1.0 (shlokas PD, compilation share-alike). Sample files are Sanskrit-only.
- Bundle 7 Sanskrit files or subset; bundle/scrape Griffith EN separately with attribution.

## Rule

Bundle: Gita verse+chapters, WEB subset, Ramayana Sanskrit, Qur'an AR+Pickthall. Link: SuttaCentral, Tanzil, eBible, sacred-texts. Never bundle Saheeh/Yusuf Ali/ESV as PD.
