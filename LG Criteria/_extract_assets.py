from pypdf import PdfReader, PdfWriter
from pathlib import Path
from PIL import Image
import io

src = Path(r"D:\LG Criteria\LG Criteria Update 03-09-2026.pdf")
out = Path(r"D:\LG Criteria\_assets")
pages_th = Path(r"D:\LG Criteria\pages-th")
out.mkdir(exist_ok=True)
pages_th.mkdir(exist_ok=True)

reader = PdfReader(str(src))

# Split original into one PDF per page
for i, page in enumerate(reader.pages, 1):
    w = PdfWriter()
    w.add_page(page)
    dest = pages_th / f"page-{i:02d}.pdf"
    with dest.open("wb") as f:
        w.write(f)
    print("split", dest.name)

# Extract images from page 1
page = reader.pages[0]
xobj = page["/Resources"]["/XObject"].get_object()
for name in xobj:
    obj = xobj[name]
    if obj["/Subtype"] != "/Image":
        continue
    data = obj.get_data()
    w, h = int(obj["/Width"]), int(obj["/Height"])
    cs = str(obj.get("/ColorSpace"))
    filt = str(obj.get("/Filter"))
    safe = str(name).replace("/", "")
    print(name, w, h, cs, filt, len(data))
    path_png = out / f"{safe}.png"
    try:
        if "DCTDecode" in filt:
            img = Image.open(io.BytesIO(data))
            img.save(out / f"{safe}.jpg")
            print("saved jpg", safe)
            continue
        channels = 3 if "RGB" in cs else 1
        mode = "RGB" if channels == 3 else "L"
        expected = w * h * channels
        if len(data) == expected:
            img = Image.frombytes(mode, (w, h), data)
            img.save(path_png)
            print("saved png", safe, img.size, img.mode)
        else:
            print("size mismatch", expected, len(data))
            try:
                img = Image.open(io.BytesIO(data))
                img.save(path_png)
                print("pil saved", safe)
            except Exception as e:
                print("pil fail", e)
    except Exception as e:
        print("fail", name, e)

print("assets", list(out.iterdir()))
print("pages-th", list(pages_th.iterdir()))
