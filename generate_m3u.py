import requests
import re
import time
from urllib.parse import urlparse, parse_qs

SRC_URL = "https://raw.githubusercontent.com/kajju027/Jiohotstar-Events-Json/refs/heads/main/jiotv.json"
OUT_FILE = "jtv.m3u"

UA = "plaYtv/7.1.3 (Linux;Android 13)"
EPG_URL = "https://avkb.short.gy/jioepg.xml.gz"

data = requests.get(SRC_URL, timeout=30).json()

lines = []
lines.append(f'#EXTM3U x-tvg-url="{EPG_URL}"')
lines.append(f"#Generated on {int(time.time())}")
lines.append("")

for ch in data:
    name = ch.get("name") or ch.get("title")
    tvg_id = ch.get("id", "")
    logo = ch.get("logo", "")
    group = ch.get("category", "Entertainment")
    stream = ch.get("url") or ch.get("stream_url")
    license_url = ch.get("license_url", "")

    if not name or not stream or not license_url:
        continue

    # cookie
    parsed = urlparse(license_url)
    cookie = parse_qs(parsed.query).get("cookie", [""])[0]

    # keyid:key
    m = re.search(r"([0-9a-fA-F]{16,32}:[0-9a-fA-F]{16,32})", license_url)
    if not m:
        continue
    clearkey = m.group(1)

    lines.append(
        f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}'
    )
    lines.append("#KODIPROP:inputstream.adaptive.license_type=clearkey")
    lines.append(f"#KODIPROP:inputstream.adaptive.license_key={clearkey}")
    lines.append(f"#EXTVLCOPT:http-user-agent={UA}")

    if cookie:
        lines.append(f'#EXTHTTP:{{"cookie":"{cookie}"}}')

    lines.append(stream)
    lines.append("")

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("jtv.m3u generated")
