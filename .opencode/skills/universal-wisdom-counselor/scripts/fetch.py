"""One-time vendoring for fully-offline use. Run once with internet, then skill works air-gapped."""
import hashlib, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "full"
DATA.mkdir(parents=True, exist_ok=True)

# Small, PD-safe core. Full Ramayana/Quran/Bible pulled as separate files (see SOURCES).
SOURCES = {
 "gita_chapters": "https://raw.githubusercontent.com/gita/gita/main/data/chapters.json",
 "gita_verses": "https://raw.githubusercontent.com/gita/gita/main/data/verse.json",
 "bible_genesis_sample": "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/genesis.json",
 "ramayana_bala": "https://raw.githubusercontent.com/bhavykhatri/DharmicData/main/ValmikiRamayana/1_balakanda.json",
}
LICENSES = {
 "gita": "Unlicense (PD)",
 "bible_web": "Public Domain (trademark: don't rename modified text 'WEB')",
 "ramayana_sanskrit": "shlokas PD; DharmicData compilation ODbL-1.0",
 "quran_ar": "Tanzil verbatim+attribution; Pickthall EN PD — fetch via scripts, not bundled here until you accept Tanzil terms",
 "dhammapada": "Pali PD; Sujato EN CC0 — fetch per-vagga from SuttaCentral API, cache locally",
}

def fetch(name, url):
    dst = DATA / f"{name}.json"
    print(f"GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "uniwisdom-offline/1.0"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    dst.write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()[:16]
    print(f"saved {dst} {len(raw)//1024}KB sha:{sha}")
    return dst

if __name__ == "__main__":
    for k, u in SOURCES.items():
        try:
            fetch(k, u)
        except Exception as ex:
            print(f"FAIL {k}: {ex}")
    (DATA / "LICENSES.json").write_text(json.dumps(LICENSES, indent=2), encoding="utf-8")
    (DATA / "HOW-OFFLINE.txt").write_text(
        "Offline rule: skill reads data/full/*.json + data/samples.json + references/*.md only.\n"
        "No runtime webfetch required. If a verse missing locally, summarize episode — never invent.\n"
        "Full corpora: re-run scripts/fetch.py with internet once, or unzip uniwisdom-data-full.zip into data/full/.\n",
        encoding="utf-8")
    print("done. See data/full/LICENSES.json")
