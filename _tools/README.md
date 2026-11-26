# en.html builder
English copy of the quotation request form. After ANY edit to index.html run:

    python3 _tools/build.py

It copies index.html to en.html, flips it to English (dir=ltr), and adds the translation layer (i18n.js + dict.json).
Any new Arabic text in index.html must get its English line added to dict.json (key = Arabic text exactly as shown).
