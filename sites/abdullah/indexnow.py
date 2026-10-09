"""Tell Bing, Yandex and other IndexNow search engines about every page in the sitemap.

Run after each deploy:  python3 indexnow.py
The key file 3ab06e77feb3abd6df0ce0f95fe7d73f.txt must be live at https://abdullahautomations.com/3ab06e77feb3abd6df0ce0f95fe7d73f.txt
"""
import json
import pathlib
import re
import urllib.request

KEY = "3ab06e77feb3abd6df0ce0f95fe7d73f"
HOST = "abdullahautomations.com"
urls = re.findall(r"<loc>(.*?)</loc>", (pathlib.Path(__file__).parent / "sitemap.xml").read_text())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow response:", r.status, f"({len(urls)} URLs submitted)")
