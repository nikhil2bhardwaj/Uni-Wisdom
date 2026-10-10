"""Convert vendored Qur'an AR + Pickthall -> data/unified/quran.json (UniWisdom schema).

Raw:
  data/full/quran_ar.json      (quran-json@3.1.2: [{id, name, transliteration, type, total_verses, verses:[{id, text}]}])
  data/full/quran_pickthall.txt (Tanzil en.pickthall, pipe format: sura|aya|text + '#' comment header)
Only Pickthall EN is bundled (PD, d.1936). NEVER bundle Saheeh/Yusuf Ali.
Run: python3 scripts/convert_quran.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
FULL = ROOT / "data" / "full"
OUT = ROOT / "data" / "unified"
OUT.mkdir(parents=True, exist_ok=True)

QURAN_MAX = {1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75,
             9: 129, 10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99,
             16: 128, 17: 111, 18: 110, 19: 98, 20: 135, 21: 112, 22: 78,
             23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88, 29: 69,
             30: 60, 31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83,
             37: 182, 38: 88, 39: 75, 40: 85, 41: 54, 42: 53, 43: 89,
             44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18, 50: 45,
             51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29,
             58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11, 64: 18,
             65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44, 71: 28,
             72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40,
             79: 46, 80: 42, 81: 29, 82: 19, 83: 36, 84: 25, 85: 22,
             86: 17, 87: 19, 88: 26, 89: 30, 90: 20, 91: 15, 92: 21,
             93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8, 100: 11,
             101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7,
             108: 3, 109: 6, 110: 3, 111: 5, 112: 4, 113: 5, 114: 6}

AR_SRC = "https://cdn.jsdelivr.net/npm/quran-json@3.1.2/dist/quran.json"
EN_SRC = "https://tanzil.net/trans/en.pickthall"


def load_pickthall():
    trans = {}
    for line in (FULL / "quran_pickthall.txt").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.count("|") < 2:
            continue
        s, a, text = line.split("|", 2)
        trans[(int(s), int(a))] = text.strip()
    return trans


def main():
    surahs = json.loads((FULL / "quran_ar.json").read_text(encoding="utf-8"))
    assert len(surahs) == 114, f"expected 114 surahs, got {len(surahs)}"
    trans = load_pickthall()
    entries = []
    for surah in surahs:
        s = int(surah["id"])
        verses = surah["verses"]
        assert len(verses) == QURAN_MAX[s], (
            f"s{s}: {len(verses)} ayahs != boundary {QURAN_MAX[s]}")
        for v in verses:
            a = int(v["id"])
            key = (s, a)
            assert key in trans, f"missing Pickthall for {s}:{a}"
            entries.append({
                "id": f"QUR_{s}_{a}",
                "tradition": "quran",
                "book": None,
                "kanda": None,
                "chapter": s,
                "sarga": None,
                "item_number": a,
                "canonical_reference": f"Surah {s}:{a}",
                "source_text": v["text"].strip(),
                "transliteration": surah.get("transliteration") or None,
                "translation": trans[key],
                "translator": "M. Pickthall (1930, public domain)",
                "edition": "Pickthall-1930",
                "license": ("Public Domain (Pickthall translation); "
                            "Arabic text via Tanzil verbatim-use with attribution"),
                "source_url": EN_SRC,
                "keywords": ["quran", f"surah-{s}"],
            })
    assert len(entries) == 6236, f"expected 6236 ayahs, got {len(entries)}"
    assert AR_SRC and EN_SRC
    (OUT / "quran.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT / 'quran.json'} ({len(entries)} records, 114 surahs)")


if __name__ == "__main__":
    main()
