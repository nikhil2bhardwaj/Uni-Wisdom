# Canonical Boundaries (verified 2026-10-10)

## Gita — 18 ch / 700 verses (already complete)

`1:47 2:72 3:43 4:42 5:29 6:47 7:30 8:28 9:34 10:42 11:55 12:20 13:35 14:27 15:20 16:24 17:28 18:78`

## Dhammapada — 26 vaggas / 423 verses (already complete)

`1:1-20 2:21-32 3:33-43 4:44-59 5:60-75 6:76-89 7:90-99 8:100-115 9:116-128 10:129-145 11:146-156 12:157-166 13:167-178 14:179-196 15:197-208 16:209-220 17:221-234 18:235-255 19:256-272 20:273-289 21:290-305 22:306-319 23:320-333 24:334-359 25:360-382 26:383-423`

## Qur'an — 114 surahs / 6236 ayahs (Kufi/Madani, via api.alquran.cloud/v1/meta, sum=6236)

1:7 2:286 3:200 4:176 5:120 6:165 7:206 8:75 9:129 10:109 11:123 12:111 13:43 14:52 15:99 16:128 17:111 18:110 19:98 20:135 21:112 22:78 23:118 24:64 25:77 26:227 27:93 28:88 29:69 30:60 31:34 32:30 33:73 34:54 35:45 36:83 37:182 38:88 39:75 40:85 41:54 42:53 43:89 44:59 45:37 46:35 47:38 48:29 49:18 50:45 51:60 52:49 53:62 54:55 55:78 56:96 57:29 58:22 59:24 60:13 61:14 62:11 63:11 64:18 65:12 66:12 67:30 68:52 69:52 70:44 71:28 72:28 73:20 74:56 75:40 76:31 77:50 78:40 79:46 80:42 81:29 82:19 83:36 84:25 85:22 86:17 87:19 88:26 89:30 90:20 91:15 92:21 93:11 94:8 95:8 96:19 97:5 98:8 99:8 100:11 101:11 102:8 103:3 104:9 105:5 106:4 107:7 108:3 109:6 110:3 111:5 112:4 113:5 114:6

Notes: S9=129 no basmala; S1 basmala=v1. Basran/Shami/Makki differ by few ayahs. Rule: `1<=s<=114 and 1<=a<=MAX[s]`, else fabricated.

## Bible — 66 books, chapter counts (WEB=KJV chapters, via holyword/biblebelievers, spot-checked via bible-api.com)

Genesis:50 Exodus:40 Leviticus:27 Numbers:36 Deuteronomy:34 Joshua:24 Judges:21 Ruth:4 1Samuel:31 2Samuel:24 1Kings:22 2Kings:25 1Chron:29 2Chron:36 Ezra:10 Nehemiah:13 Esther:10 Job:42 Psalms:150 Proverbs:31 Ecclesiastes:12 Song:8 Isaiah:66 Jeremiah:52 Lamentations:5 Ezekiel:48 Daniel:12 Hosea:14 Joel:3 Amos:9 Obadiah:1 Jonah:4 Micah:7 Nahum:3 Habakkuk:3 Zephaniah:3 Haggai:2 Zechariah:14 Malachi:4 Matthew:28 Mark:16 Luke:24 John:21 Acts:28 Romans:16 1Cor:16 2Cor:13 Galatians:6 Ephesians:6 Philippians:4 Colossians:4 1Thess:5 2Thess:3 1Tim:6 2Tim:4 Titus:3 Philemon:1 Hebrews:13 James:5 1Peter:5 2Peter:3 1John:5 2John:1 3John:1 Jude:1 Revelation:22

Key ceilings (WEB): Ps119=176, Prov8=36, Eccl7=29, Luke1=80, Matt26=75, Mark14=72, John6=71. Single-ch books accept `Jude 25` or `Jude 1:25`. Rule: `book in list AND 1<=ch<=MAX_CH AND 1<=v<=verse_count(book,ch)` via bundled WEB JSON or bible-api.com, never memory. ±1 verse translation variance = flag not hard-fail.

## Ramayana — 7 Kandas, 645 sargas CE (Baroda; observed Southern text via valmikiramayan.net)

1 Bala:77 | 2 Ayodhya:119 | 3 Aranya:75 | 4 Kishkindha:67 | 5 Sundara:68 | 6 Yuddha:128 | 7 Uttara:111

Variance: Northern/Southern/Gita Press differ by few sargas, esp. Yuddha/Uttara; Bala+Uttara later additions. Guidance: cite `Ramayana <Kanda> <sarga>` (e.g. Ayodhya 119 verifiable); never cite shloka numbers (vary wildly). Uncertain sarga -> `Kanda + episode` + flag for human check.
