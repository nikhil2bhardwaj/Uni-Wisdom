# UniWisdom — Universal Wisdom Counselor (OpenCode Skill, offline-first)

Grounded counsel from Gita, Ramayana, Dhammapada, Bible (WEB), Qur'an (Pickthall) with verified citations and 4-part response. See `docs/VERSIONS.md` for packages.

## Install (online, one time)

```sh
git clone https://github.com/nikhil2bhardwaj/Uni-Wisdom.git
cd Uni-Wisdom
# Project-local: .opencode/ is auto-discovered. Nothing else to do.
```

Global (all projects): copy `.opencode/skills/universal-wisdom-counselor/` to `~/.config/opencode/skills/` (Linux/macOS) or `%USERPROFILE%\.config\opencode\skills\` (Windows), and `.opencode/commands/wisdom-*.md` to `~/.config/opencode/commands/`.

No clone of the data needed if you use the zip — see Offline.

## Use

- `@universal-wisdom-counselor <dilemma>` — auto-routes to best-fit tradition
- `@universal-wisdom-counselor gita: <dilemma>` — lock a tradition
- `/wisdom-gita|ramayana|dhammapada|bible|quran <dilemma>` — explicit shortcuts

## Use offline (air-gapped, after one download)

The skill never fetches the web at counsel time. Texts are already in the repo (`data/unified/`). Three ways to go air-gapped:

1. **Clone once online, then unplug.** `git clone` above is the only network step. Everything after runs from `data/unified/`.
2. **Zip only (no git).** Download `uniwisdom-data-full-v1.zip` (5.7MB) from [Releases](https://github.com/nikhil2bhardwaj/Uni-Wisdom/releases), unzip into a project so it contains `.opencode/` + `data/` + `references/` + `scripts/`. OpenCode discovers it the same way.
3. **Local LLM (fully private).** Point RAG at the unified JSONs:
   - LM Studio / Ollama / Open WebUI: create a Knowledge collection from `.opencode/skills/universal-wisdom-counselor/data/unified/*.json`, attach to a preset whose system prompt is `SKILL.md`.
   - AnythingLLM: workspace → upload `data/unified/*.json` → set mode to **Query (RAG)**.
   - Chunking: one JSON object per verse already; embed `translation` + `keywords` only (skips Devanagari/Arabic tokens, better retrieval).

Offline behavior: if a verse is missing locally, the skill summarizes the episode conceptually and never invents verse numbers or source text (`references/sources.md` has the provenance; `scripts/validate.py` enforces boundaries).

Rebuild from raw upstream later (needs internet once): `python scripts/fetch.py` then `convert_*.py`.

## Layout
`.opencode/skills/universal-wisdom-counselor/` (SKILL.md, references/, data/, scripts/, evals/) + `.opencode/commands/wisdom-*.md`. `docs/VERSIONS.md` compares Samples vs Unified vs Full.

## Honesty notes
Gita translation = word-gloss; Ramayana = Sanskrit-only (use Griffith EN separately); Saheeh/Yusuf Ali never bundled; SuttaCentral: no LLM-training use. Validator 20/20 (`evals/report.md`).
