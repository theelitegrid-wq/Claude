"""Build the deploy-ready site in public/ for https://abdullahautomations.com/.

index.html is authored as a page body (it also publishes as a Claude artifact);
this wraps it in a full HTML document with <html lang> and a real <head>,
then copies the assets and demo sites, renders the service, industry and guide
pages from content.py, and writes robots.txt and a sitemap listing every page.
"""
import pathlib
import shutil

from company_pages import render_company
from pages import LASTMOD, render_all

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
for name in ["favicon.svg", "apple-touch-icon.png", "og-image.jpg", "robots.txt", "llms.txt", *[f.name for f in ROOT.glob("*.txt") if len(f.stem) == 32]]:
    shutil.copy2(ROOT / name, OUT / name)
shutil.copytree(ROOT / "demos", OUT / "demos")
(OUT / "video").mkdir()
for f in (ROOT / "video").iterdir():
    if f.suffix in {".mp4", ".webm", ".jpg"}:
        shutil.copy2(f, OUT / "video" / f.name)
shutil.copytree(ROOT / "assets", OUT / "assets")

urls = ["https://abdullahautomations.com/"] + render_all(OUT) + render_company(OUT)
entries = "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>\n" for u in urls)
sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
(OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print("Built", OUT, "with", len(urls), "indexable pages")
