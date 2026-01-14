import requests

URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        response = requests.get(URL)
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Others")
            tvg_id = item.get("id", "")
            stream_url = item.get("mpd_url") or item.get("m3u8_url")
            
            if not stream_url:
                continue

            # Extracting headers and keys from JSON
            headers = item.get("headers", {})
            ua = item.get("user_agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
            cookie = headers.get("Cookie", "")
            referer = headers.get("Referer", "https://www.hotstar.com/")
            origin = headers.get("Origin", "https://www.hotstar.com")
            
            # Clearkey logic: Extracting keyid and key from the license_url
            # Format: ...keyid=FE77...&key=624E...
            lic_url = item.get("license_url", "")
            key_id = ""
            key_val = ""
            if "keyid=" in lic_url and "&key=" in lic_url:
                key_id = lic_url.split("keyid=")[1].split("&")[0]
                key_val = lic_url.split("&key=")[1]

            # --- Arrangement as per your working example ---
            # Structure: URL?|Cookie=...&User-agent=...&Referer=...&Origin=...&drmScheme=clearkey&drmLicense=ID:KEY
            final_url = (
                f"{stream_url}?|Cookie={cookie}&User-agent={ua}&"
                f"Referer={referer}&Origin={origin}&drmScheme=clearkey&"
                f"drmLicense={key_id}:{key_val}"
            )

            m3u_content += f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n'
            m3u_content += f'{final_url}\n\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Success! Working playlist generated in single-URL format.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
