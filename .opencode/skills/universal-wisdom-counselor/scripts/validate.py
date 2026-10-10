import json
import re
import sys
from pathlib import Path

GITA_MAX = {1:47,2:72,3:43,4:42,5:29,6:47,7:30,8:28,9:34,10:42,11:55,12:20,13:35,14:27,15:20,16:24,17:28,18:78}
DHP_VAGGA_RANGES = {1:(1,20),2:(21,32),3:(33,43),4:(44,59),5:(60,75),6:(76,89),7:(90,99),8:(100,115),9:(116,128),10:(129,145),11:(146,156),12:(157,166),13:(167,178),14:(179,196),15:(197,208),16:(209,220),17:(221,234),18:(235,255),19:(256,272),20:(273,289),21:(290,305),22:(306,319),23:(320,333),24:(334,359),25:(360,382),26:(383,423)}
QURAN_MAX = {1:7,2:286,3:200,4:176,5:120,6:165,7:206,8:75,9:129,10:109,11:123,12:111,13:43,14:52,15:99,16:128,17:111,18:110,19:98,20:135,21:112,22:78,23:118,24:64,25:77,26:227,27:93,28:88,29:69,30:60,31:34,32:30,33:73,34:54,35:45,36:83,37:182,38:88,39:75,40:85,41:54,42:53,43:89,44:59,45:37,46:35,47:38,48:29,49:18,50:45,51:60,52:49,53:62,54:55,55:78,56:96,57:29,58:22,59:24,60:13,61:14,62:11,63:11,64:18,65:12,66:12,67:30,68:52,69:52,70:44,71:28,72:28,73:20,74:56,75:40,76:31,77:50,78:40,79:46,80:42,81:29,82:19,83:36,84:25,85:22,86:17,87:19,88:26,89:30,90:20,91:15,92:21,93:11,94:8,95:8,96:19,97:5,98:8,99:8,100:11,101:11,102:8,103:3,104:9,105:5,106:4,107:7,108:3,109:6,110:3,111:5,112:4,113:5,114:6}
BIBLE_CH_MAX = {"Genesis":50,"Exodus":40,"Leviticus":27,"Numbers":36,"Deuteronomy":34,"Joshua":24,"Judges":21,"Ruth":4,"1 Samuel":31,"2 Samuel":24,"1 Kings":22,"2 Kings":25,"1 Chronicles":29,"2 Chronicles":36,"Ezra":10,"Nehemiah":13,"Esther":10,"Job":42,"Psalms":150,"Proverbs":31,"Ecclesiastes":12,"Song of Solomon":8,"Isaiah":66,"Jeremiah":52,"Lamentations":5,"Ezekiel":48,"Daniel":12,"Hosea":14,"Joel":3,"Amos":9,"Obadiah":1,"Jonah":4,"Micah":7,"Nahum":3,"Habakkuk":3,"Zephaniah":3,"Haggai":2,"Zechariah":14,"Malachi":4,"Matthew":28,"Mark":16,"Luke":24,"John":21,"Acts":28,"Romans":16,"1 Corinthians":16,"2 Corinthians":13,"Galatians":6,"Ephesians":6,"Philippians":4,"Colossians":4,"1 Thessalonians":5,"2 Thessalonians":3,"1 Timothy":6,"2 Timothy":4,"Titus":3,"Philemon":1,"Hebrews":13,"James":5,"1 Peter":5,"2 Peter":3,"1 John":5,"2 John":1,"3 John":1,"Jude":1,"Revelation":22}
BIBLE_MAX = {"Proverbs":{3:35},"Ecclesiastes":{1:18},"Psalms":{23:6}}
RAM_KANDAS = {"Bala":1,"Ayodhya":2,"Aranya":3,"Kishkindha":4,"Sundara":5,"Yuddha":6,"Uttara":7}
RAM_SARGA_MAX = {"Bala":77,"Ayodhya":119,"Aranya":75,"Kishkindha":67,"Sundara":68,"Yuddha":128,"Uttara":111}

ID_RE = re.compile(r"^(BG_\d+_\d+|RAM_[A-Z]+_\d+_\d+|DHP_\d{3}|BIBLE_[A-Z]+_\d+_\d+|QUR_\d+_\d+)$")
CIT_RE = {
 "gita": re.compile(r"^BG \d+:\d+$"),
 "ramayana": re.compile(r"^Ramayana \d+\.\d+\.\d+$"),
 "dhammapada": re.compile(r"^Dhp \d+$"),
 "bible": re.compile(r"^[A-Za-z ]+ \d+:\d+ \[(WEB|KJV)\]$"),
 "quran": re.compile(r"^Surah \d+:\d+$"),
}

def validate(e):
    assert ID_RE.match(e["id"]), f"bad id {e['id']}"
    assert isinstance(e["keywords"], list) and all(isinstance(k,str) and k for k in e["keywords"]), "keywords must be string[]"
    assert e["source_url"] is None or isinstance(e["source_url"], str)
    t = e["tradition"]
    assert CIT_RE[t].match(e["canonical_reference"]), f"bad citation for {t}: {e['canonical_reference']}"
    c, n = e["chapter"], e["item_number"]
    if t=="gita":
        assert e["book"] is None and e["kanda"] is None and e["sarga"] is None and isinstance(e["transliteration"],str)
        assert 1<=c<=18 and 1<=n<=GITA_MAX[c]
        assert e["id"]==f"BG_{c}_{n}"
    elif t=="ramayana":
        assert isinstance(e["kanda"],str) and isinstance(c,int) and isinstance(e["sarga"],int)
        assert RAM_KANDAS[e["kanda"]]==c
        assert 1<=e["sarga"]<=RAM_SARGA_MAX[e["kanda"]], f"sarga out of range for {e['kanda']}"
    elif t=="dhammapada":
        assert 1<=c<=26 and e["transliteration"]
        lo,hi = DHP_VAGGA_RANGES[c]
        assert lo<=n<=hi
        assert "brahmi" not in e["source_text"].lower()
    elif t=="bible":
        assert isinstance(e["book"],str) and e["transliteration"] is None
        assert e["book"] in BIBLE_CH_MAX, f"unknown book {e['book']}"
        assert 1<=c<=BIBLE_CH_MAX[e["book"]]
    elif t=="quran":
        assert 1<=c<=114 and 1<=n<=QURAN_MAX[c]; assert e["id"]==f"QUR_{c}_{n}"
    return True

if __name__ == "__main__":
    p = Path(__file__).parent.parent / "data" / "samples.json"
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
    items = json.loads(p.read_text(encoding="utf-8"))
    for e in items:
        validate(e)
        print(f"OK {e['id']}")
    print(f"Validated {len(items)} records.")
