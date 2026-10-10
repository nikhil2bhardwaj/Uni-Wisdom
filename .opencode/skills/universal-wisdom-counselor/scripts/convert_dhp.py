"""Build unified Dhammapada JSON (423 verses) from SuttaCentral Bilara raw cache.

Reads: data/full/dhp_raw_*.json (SuttaCentral /api/bilarasuttas/dhp{lo}-{hi}/sujato)
Writes: data/unified/dhammapada.json in references/schema.json format.

Pali root: Mahasangiti (PD). English: Bhikkhu Sujato 2021 (CC0-1.0).
No Brahmi: Bilara root_text is Pali in Roman script only.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "full"
OUT = ROOT / "data" / "unified" / "dhammapada.json"

DHP_VAGGA_RANGES = {1: (1, 20), 2: (21, 32), 3: (33, 43), 4: (44, 59), 5: (60, 75),
                    6: (76, 89), 7: (90, 99), 8: (100, 115), 9: (116, 128), 10: (129, 145),
                    11: (146, 156), 12: (157, 166), 13: (167, 178), 14: (179, 196),
                    15: (197, 208), 16: (209, 220), 17: (221, 234), 18: (235, 255),
                    19: (256, 272), 20: (273, 289), 21: (290, 305), 22: (306, 319),
                    23: (320, 333), 24: (334, 359), 25: (360, 382), 26: (383, 423)}

VAGGA_PALI = {1: "Yamakavagga", 2: "Appamadavagga", 3: "Cittavagga", 4: "Pupphavagga",
              5: "Balavagga", 6: "Panditavagga", 7: "Arahantavagga", 8: "Sahassavagga",
              9: "Papavagga", 10: "Dandavagga", 11: "Jaravagga", 12: "Attavagga",
              13: "Lokavagga", 14: "Buddhavagga", 15: "Sukhavagga", 16: "Piyavagga",
              17: "Kodhavagga", 18: "Malavagga", 19: "Dhammatthavagga", 20: "Maggavagga",
              21: "Pakinnakavagga", 22: "Nirayavagga", 23: "Nagavagga", 24: "Tanhavagga",
              25: "Bhikkhuvagga", 26: "Brahmanavagga"}

VAGGA_EN = {1: "pairs", 2: "heedfulness", 3: "mind", 4: "flowers", 5: "fools",
            6: "wise", 7: "arahant", 8: "thousands", 9: "evil", 10: "punishment",
            11: "old age", 12: "self", 13: "world", 14: "buddha", 15: "happiness",
            16: "affection", 17: "anger", 18: "stains", 19: "dhamma", 20: "path",
            21: "miscellaneous", 22: "hell", 23: "elephant", 24: "craving",
            25: "mendicant", 26: "brahmin"}

VERSE_TO_VAGGA = {}
for vagga, (lo, hi) in DHP_VAGGA_RANGES.items():
    for n in range(lo, hi + 1):
        VERSE_TO_VAGGA[n] = vagga


def join_segments(seg_dict, order, verse_num):
    prefix = "dhp%d:" % verse_num
    keys = [k for k in order if k.startswith(prefix) and ":0." not in k]
    if not keys:  # fallback if keys_order missing
        keys = sorted([k for k in seg_dict if k.startswith(prefix) and ":0." not in k])
    parts = []
    for k in keys:
        t = (seg_dict.get(k) or "").strip()
        if t:
            parts.append(t)
    text = " ".join(parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    raw_files = sorted(RAW_DIR.glob("dhp_raw_*.json"))
    if not raw_files:
        raise SystemExit("no raw files in %s" % RAW_DIR)
    root_all = {}
    trans_all = {}
    order_all = []
    for f in raw_files:
        j = json.loads(f.read_text(encoding="utf-8"))
        root_all.update(j["root_text"])
        trans_all.update(j["translation_text"])
        order_all.extend(j.get("keys_order", []))
    records = []
    for n in range(1, 424):
        vagga = VERSE_TO_VAGGA[n]
        pali = join_segments(root_all, order_all, n)
        eng = join_segments(trans_all, order_all, n)
        assert pali, "missing Pali for Dhp %d" % n
        assert eng, "missing EN for Dhp %d" % n
        assert "brahmi" not in pali.lower(), "brahmi leak Dhp %d" % n
        for ch in pali + eng:
            assert not ("\u1000" <= ch <= "\u109F"), "Brahmi/Myanmar char in Dhp %d" % n
        records.append({
            "id": "DHP_%03d" % n,
            "tradition": "dhammapada",
            "book": None,
            "kanda": None,
            "chapter": vagga,
            "sarga": None,
            "item_number": n,
            "canonical_reference": "Dhp %d" % n,
            "source_text": pali,
            "transliteration": pali,
            "translation": eng,
            "translator": "Bhikkhu Sujato",
            "edition": "SuttaCentral Bilara ms/sujato-2021",
            "license": "CC0-1.0",
            "source_url": "https://suttacentral.net/dhp%d/en/sujato" % n,
            "keywords": ["dhammapada", VAGGA_EN[vagga], VAGGA_PALI[vagga].lower()],
        })
    assert len(records) == 423, "expected 423, got %d" % len(records)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s records=%d" % (OUT, len(records)))


if __name__ == "__main__":
    main()
