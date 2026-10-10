"""Convert upstream gita/gita verse.json -> unified schema (data/unified/gita.json).

Upstream: data/full/gita_verses.json, list of
  {chapter_id, chapter_number, externalId, id, text (Devanagari),
   title, verse_number, verse_order, transliteration, word_meanings}
Upstream has NO full literary English translation; `word_meanings` is a
word-gloss, used here as `translation` and labeled honestly via translator/.
Run: python3 scripts/convert_gita.py
"""
import io
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = ROOT / "data" / "full" / "gita_verses.json"
DST = ROOT / "data" / "unified" / "gita.json"

TRANSLATOR = "gita/gita contributors — word-meanings gloss (not a full literary translation)"
EDITION = "gita/gita data/verse.json"
LICENSE = "Unlicense (PD)"


def convert(rec):
    ch = int(rec["chapter_number"])
    v = int(rec["verse_number"])
    return {
        "id": f"BG_{ch}_{v}",
        "tradition": "gita",
        "book": None,
        "kanda": None,
        "chapter": ch,
        "sarga": None,
        "item_number": v,
        "canonical_reference": f"BG {ch}:{v}",
        "source_text": str(rec["text"]).strip(),
        "transliteration": str(rec.get("transliteration", "")).strip(),
        "translation": str(rec.get("word_meanings", "")).strip(),
        "translator": TRANSLATOR,
        "edition": EDITION,
        "license": LICENSE,
        "source_url": None,
        "keywords": ["bhagavad-gita", f"chapter-{ch}"],
    }


def main():
    raw = json.loads(SRC.read_text(encoding="utf-8"))
    out = [convert(r) for r in raw]
    DST.parent.mkdir(parents=True, exist_ok=True)
    with io.open(DST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {DST} records={len(out)}")


if __name__ == "__main__":
    main()
