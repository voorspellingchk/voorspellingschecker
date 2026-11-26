# Voorspellingschecker / Prediction Checker

Twee sites, één broncode. Nieuwe features of vormgeving NOOIT los in één taal maken.

1. Pas `tools/site/editor_nl.html` aan (dat is de editorpagina van de Voorspellingschecker).
2. Nieuwe Nederlandse tekst krijgt een Engelse vertaling in `tools/site/en_code.json` (of `en_text.json`).
3. Draai `python3 tools/site/build.py`. Die stopt als er Nederlands in de Engelse versie achterblijft.
4. Publiceer en push alle vier de uitvoerbestanden uit `tools/site/out/`:
   - `nl_editor.html` -> artifact 874758de-e1ed-4185-9536-a26cdfbf83c4 (index.html)
   - `en_editor.html` -> artifact f6eaae4e-6999-4370-95c7-0438eca11e86 (index.html)
   - `nl_public.html` -> `index.html` van deze repo (voorspellingschecker.nl)
   - `en_public.html` -> `index.html` van voorspellingchk/predictionchecker (predictionchk.com)

Data (`data.json`), databases en geplande taken blijven per site gescheiden.
Een artifact kan alleen worden bijgewerkt vanuit een sessie die het mag wijzigen (bijv. een chat geopend vanaf de artifactpagina).
