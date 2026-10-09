"""Build the deploy-ready site in public/ for https://abdullahautomations.com/.

index.html is authored as a page body (it also publishes as a Claude artifact);
this wraps it in a full HTML document with <html lang> and a real <head>,
then copies the assets, demo sites, robots.txt and sitemap.xml next to it.
"""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "public"

src = (ROOT / "index.html").read_text(encoding="utf-8")
split = src.index("</style>") + len("</style>")
head, body = src[:split], src[split:]

page = (
    '<!doctype html>\n<html lang="en">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    f"{head}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
(OUT / "index.html").write_text(page, encoding="utf-8")
for name in ["favicon.svg", "apple-touch-icon.png", "og-image.jpg", "robots.txt", "sitemap.xml"]:
    shutil.copy2(ROOT / name, OUT / name)
shutil.copytree(ROOT / "demos", OUT / "demos")
(OUT / "video").mkdir()
for f in (ROOT / "video").iterdir():
    if f.suffix in {".mp4", ".webm", ".jpg"}:
        shutil.copy2(f, OUT / "video" / f.name)
print("Built", OUT)
