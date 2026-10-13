"""Arma docs/index.html: un solo archivo que funciona sin internet (jsPDF incluido).

GitHub Pages publica la carpeta docs/.

pines.html es la fuente y también la página que se publica en claude.ai
(sin doctype/head/body: el publicador los agrega).
"""
import re
from pathlib import Path

here = Path(__file__).parent
src = (here / "pines.html").read_text(encoding="utf-8")
lib = (here / "vendor" / "jspdf.umd.min.js").read_text(encoding="utf-8")
assert "</script" not in lib.lower()

tag = re.compile(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jspdf/[^"]+"[^>]*></script>')
assert len(tag.findall(src)) == 1, "no encontré la etiqueta de jsPDF"
body = tag.sub(lambda _: "<script>/* jsPDF 2.5.1 (MIT) */\n" + lib + "\n</script>", src)

out = (
    '<!doctype html>\n<html lang="es">\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + body + "\n</html>\n"
)
(here / "docs").mkdir(exist_ok=True)
(here / "docs" / "index.html").write_text(out, encoding="utf-8")
print(f"docs/index.html: {len(out.encode()) // 1024} KB")
