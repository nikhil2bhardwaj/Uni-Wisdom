"""Convert vendored WEB per-book JSON -> data/unified/bible.json (UniWisdom schema).

Raw: data/full/bible_<slug>.json (TehShrike/world-english-bible per-book files:
list of segments; verses split across 'paragraph text' / 'line text' segments
sharing (chapterNumber, verseNumber); 'header'/'stanza'/'break' carry no verse text).
Run: python3 scripts/convert_bible.py  (reads ../data/full, writes ../data/unified/bible.json)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
FULL = ROOT / "data" / "full"
OUT = ROOT / "data" / "unified"
OUT.mkdir(parents=True, exist_ok=True)

# slug -> (display book name, ID code). Codes follow data/samples.json (PROV etc.).
BOOKS = {
    "proverbs": ("Proverbs", "PROV"),
    "ecclesiastes": ("Ecclesiastes", "ECCL"),
    "psalms": ("Psalms", "PS"),
    "matthew": ("Matthew", "MATT"),
    "mark": ("Mark", "MARK"),
    "luke": ("Luke", "LUKE"),
    "john": ("John", "JOHN"),
}

# Expected chapter counts (references/boundaries.md).
CHAPTER_MAX = {"Proverbs": 31, "Ecclesiastes": 12, "Psalms": 150,
               "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21}

SRC = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/{}.json"
WS = re.compile(r"\s+")


def load_verses(slug):
    raw = json.loads((FULL / f"bible_{slug}.json").read_text(encoding="utf-8"))
    parts = {}  # (chapter, verse) -> [segments in order]
    for seg in raw:
        if seg.get("type") not in ("paragraph text", "line text"):
            continue
        ch, v = seg.get("chapterNumber"), seg.get("verseNumber")
        if not isinstance(ch, int) or not isinstance(v, int):
            continue
        parts.setdefault((ch, v), []).append(seg.get("value", ""))
    verses = {}
    for (ch, v), segs in parts.items():
        text = WS.sub(" ", " ".join(s.strip() for s in segs)).strip()
        if text:
            verses[(ch, v)] = text
    return verses


def main():
    entries = []
    for slug, (book, code) in BOOKS.items():
        verses = load_verses(slug)
        chapters = sorted({c for c, _ in verses})
        expect = CHAPTER_MAX[book]
        assert chapters == list(range(1, expect + 1)), (
            f"{book}: chapters {chapters[:3]}..{chapters[-3:]} != 1..{expect}")
        for (ch, v) in sorted(verses):
            text = verses[(ch, v)]
            entries.append({
                "id": f"BIBLE_{code}_{ch}_{v}",
                "tradition": "bible",
                "book": book,
                "kanda": None,
                "chapter": ch,
                "sarga": None,
                "item_number": v,
                "canonical_reference": f"{book} {ch}:{v} [WEB]",
                "source_text": text,
                "transliteration": None,
                "translation": text,
                "translator": "World English Bible",
                "edition": "WEB",
                "license": "Public Domain",
                "source_url": SRC.format(slug),
                "keywords": ["bible", book.lower(), "web"],
            })
        n_verses = len(verses)
        n_ch = len(chapters)
        print(f"{book}: {n_ch} chapters, {n_verses} verses")
    (OUT / "bible.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT / 'bible.json'} ({len(entries)} records)")


if __name__ == "__main__":
    main()
