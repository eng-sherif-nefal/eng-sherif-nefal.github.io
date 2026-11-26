# en.html builder
English copy of the quotation request form. After ANY edit to index.html run:

    python3 _tools/build.py

It copies index.html to en.html, flips it to English (dir=ltr), and adds the translation layer (i18n.js + dict.json).
Any new Arabic text in index.html must get its English line added to dict.json (key = Arabic text exactly as shown).

# Brand sync (order 267)
Brand choices for concealed / wall / cassette / floor / central split / package / desert / exhaust fans are mirrored from the
newest "Nefal_Price_List_V*.xlsx" in Google Drive (folder "Price References"): every brand sheet with prices appears, sheets removed
from the file disappear, and the operation (inverter / on-off) and cooling/heating options come from the sheet sections.

    python3 -I _tools/brands_sync.py /path/Nefal_Price_List_Vxx.xlsx      # updates index.html + en.html, prints added/removed

_tools/brands_state.json keeps the Drive file id + modifiedTime last synced. Display names and order: _tools/brands_config.json.
After a sync, also apply the same .brx blocks to the Claude artifact copy (YX53yACGSSgsi7cHygDPwD).
