"""Convert DharmicData ValmikiRamayana kandas -> unified schema (data/unified/ramayana.json).

Upstream files (data/full/): ramayana_bala.json (1_balakanda content) +
  2_ayodhyakanda.json … 7_uttarakanda.json, each a list of
  {kaanda, sarg, shloka, text (Sanskrit Devanagari)}.
Upstream has NO English translation / transliteration; placeholders state
that honestly (skill must summarize episodes, never invent).

Upstream data corrections applied (logged at runtime, evidence-backed):
1. Exact-duplicate rows (same kaanda/sarg/shloka/text, e.g. Kishkindha
   sarga 10 doubled upstream) — keep first.
2. Sarga gap-fill: a verse whose trailing embedded marker ‖K-S-V‖ names this
   file's kanda K with a sarga S that is otherwise absent from the file is
   refiled to S. (Fires only for Aranya sarga 24: 36 verses filed under
   sarga 34 carry ‖3-24-N‖ markers and sarga 24 is otherwise empty.)
Untouched upstream variance (reported, not "fixed"): Bala 57/58 embedded
markers swapped vs fields; shloka-number offsets (e.g. Aranya 7); sargas
absent upstream entirely (Bala 70-72, Kishkindha 11/65, Yuddha 4/67/114).
Run: python3 scripts/convert_ramayana.py
"""
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "full"
DST = ROOT / "data" / "unified" / "ramayana.json"

# filename -> (Kanda display name, chapter index 1-7, ID abbrev)
KANDAS = {
    "ramayana_bala.json": ("Bala", 1, "BAL"),
    "2_ayodhyakanda.json": ("Ayodhya", 2, "AYO"),
    "3_aranyakanda.json": ("Aranya", 3, "ARA"),
    "4_kishkindhakanda.json": ("Kishkindha", 4, "KIS"),
    "5_sundarakanda.json": ("Sundara", 5, "SUN"),
    "6_yudhhakanda.json": ("Yuddha", 6, "YUD"),
    "7_uttarakanda.json": ("Uttara", 7, "UTT"),
}

MARKER_RE = re.compile(r"\u0965{1,2}(\d+)-(\d+)-(\d+)\u0965{1,2}\s*$")

TRANSLATOR = "N/A (source-text only; verify vs critical ed.)"
LICENSE = "shlokas PD; DharmicData compilation ODbL-1.0"
NO_TRANSLITERATION = "(transliteration not vendored; see source_text)"
NO_TRANSLATION = "(English translation not vendored; Sanskrit source only — summarize episode, never invent)"


def convert(rec, sarg, kanda, chapter, abbrev, edition):
    n = int(rec["shloka"])
    return {
        "id": f"RAM_{abbrev}_{sarg}_{n}",
        "tradition": "ramayana",
        "book": None,
        "kanda": kanda,
        "chapter": chapter,
        "sarga": sarg,
        "item_number": n,
        "canonical_reference": f"Ramayana {chapter}.{sarg}.{n}",
        "source_text": str(rec["text"]).strip(),
        "transliteration": NO_TRANSLITERATION,
        "translation": NO_TRANSLATION,
        "translator": TRANSLATOR,
        "edition": edition,
        "license": LICENSE,
        "source_url": None,
        "keywords": ["ramayana", kanda.lower(), f"sarga-{sarg}"],
    }


def main():
    out = []
    for fname, (kanda, chapter, abbrev) in KANDAS.items():
        raw = json.loads((DATA / fname).read_text(encoding="utf-8"))
        # 1. exact-dupe removal
        seen, deduped = set(), []
        ndup = 0
        for r in raw:
            key = (r.get("kaanda"), r.get("sarg"), r.get("shloka"), r.get("text"))
            if key in seen:
                ndup += 1
                continue
            seen.add(key)
            deduped.append(r)
        # 2. sarga gap-fill via embedded trailing marker
        field_sargas = {int(r["sarg"]) for r in deduped}
        nmoved = 0
        for r in deduped:
            m = MARKER_RE.search(str(r["text"]).strip())
            if m and int(m.group(1)) == chapter:
                es = int(m.group(2))
                if es != int(r["sarg"]) and es not in field_sargas:
                    r = dict(r, sarg=es)
                    nmoved += 1
            out.append(convert(r, int(r["sarg"]), kanda, chapter, abbrev,
                               f"DharmicData ValmikiRamayana/{fname}"))
        print(f"{fname}: raw={len(raw)} exact_dupes_dropped={ndup} marker_moves={nmoved}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    with io.open(DST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {DST} records={len(out)}")


if __name__ == "__main__":
    main()
