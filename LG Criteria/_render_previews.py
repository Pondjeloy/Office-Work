import pypdfium2 as pdfium
from pathlib import Path

ROOT = Path(r"D:\LG Criteria")
jobs = [
    (ROOT / "LG Criteria Update 01-10-2026.pdf", ROOT / "_preview-th"),
    (ROOT / "LG Criteria Update 01-10-2026 EN.pdf", ROOT / "_preview-en"),
]
for src, out in jobs:
    out.mkdir(exist_ok=True)
    doc = pdfium.PdfDocument(str(src))
    for i, pg in enumerate(doc, 1):
        img = pg.render(scale=1.7).to_pil()
        dest = out / f"page-{i:02d}.png"
        img.save(dest, "PNG")
        print(src.name, dest.name, img.size)
