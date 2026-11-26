# Eén broncode voor beide sites

De Nederlandse en Engelse site (Voorspellingschecker en Prediction Checker) worden uit ÉÉN bestand gebouwd:
`editor_nl.html` (de editorpagina van de Voorspellingschecker). Nieuwe features en vormgeving altijd hier aanpassen,
nooit los in de Engelse versie.

    python3 tools/site/build.py

Dit maakt in `tools/site/out/`:

| bestand | waarheen |
|---|---|
| nl_editor.html | artifact 874758de-e1ed-4185-9536-a26cdfbf83c4 (Voorspellingschecker, editor) |
| en_editor.html | artifact f6eaae4e-6999-4370-95c7-0438eca11e86 (Prediction Checker, editor) |
| nl_public.html | index.html in deze repo (voorspellingschecker.nl) |
| en_public.html | index.html in github.com/voorspellingchk/predictionchecker (predictionchk.com) |

Vertalingen: nieuwe Nederlandse tekst krijgt een Engelse vertaling in `en_code.json` (exacte stukjes code/tekst)
of `en_text.json` (korte zinnen binnen tekst). `build.py` stopt met een lijst als er nog Nederlandse woorden
in de Engelse versie staan. Data (data.json) en databases blijven per site gescheiden.
