# Versions — what supports what

| Package | Contents | Size | Texts covered | Offline? | Citation guarantee | Best for |
|---|---|---|---|---|---|---|
| Samples | `data/samples.json` (5 records) | ~5 KB | 1 anchor/tradition (BG 2:47, Ram 2.18.15, Dhp 1, Prov 3:5 WEB, Surah 2:255) | Yes | Validator 5/5; all other verses fall back to episode summary | Demo, eval smoke test, zero-download trial |
| Unified | `data/unified/*.json` | 32.5 MB (Gita 0.8, Dhp 0.4, Bible 5.2, Quran 5.4, Ramayana 20.7) | Gita 701 (gloss-only), Dhp 423 Sujato CC0, Bible 7376 (Prov/Eccl/Psalms/Matt/Mark/Luke/John WEB), Quran 6236 (AR+Pickthall), Ramayana 22707 shlokas Sanskrit-only | Yes | Full boundary validation (20/20 eval); Gita/Ramayana EN limits disclosed | Offline counsel + local RAG (recommended runtime) |
| Full raw | `data/full/` | 13.6 MB | Upstream dumps: Gita verse/chapters, 7 Ramayana kandas, 7 WEB books, Quran AR + Pickthall txt, 26 Dhp API caches + LICENSES.json | Yes | Provenance/audit only, not read at counsel time | Rebuild, license audit, reconvert |
| Full release | `uniwisdom-data-full-v1.zip` | 5.7 MB | Unified + full + references + scripts | Yes, unzip once | Same as Unified + rebuildable | GitHub Release one-download offline |

Notes: Gita translation = word-gloss (no literary EN upstream); Ramayana translation = placeholder (use Griffith PD separately); Saheeh/Yusuf Ali never bundled (copyrighted); SuttaCentral asks no LLM-training use.
