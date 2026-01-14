import requests

URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        response = requests.get(URL)
        data = response.json()
        
        # M3U Header
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Sports")
            tvg_id = item.get("id", "")
            stream_url = item.get("mpd_url") or item.get("m3u8_url")
            
            if not stream_url:
                continue

            # Headers extract karna
            headers = item.get("headers", {})
            ua = item.get("user_agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
            cookie = headers.get("Cookie", "")
            referer = headers.get("Referer", "https://www.hotstar.com/")
            origin = headers.get("Origin", "https://www.hotstar.com")
            
            # ClearKey DRM Extraction
            lic_url = item.get("license_url", "")
            key_id = ""
            key_val = ""
            if "keyid=" in lic_url and "&key=" in lic_url:
                key_id = lic_url.split("keyid=")[1].split("&")[0]
                key_val = lic_url.split("&key=")[1]

            # --- Sahi M3U Arrangement for the Player ---
            m3u_content += f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n'
            
            # ClearKey DRM Tags
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key_val}\n'
            
            # Network Stream Headers (VLCOPT & HTTP)
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            m3u_content += f'#EXTVLCOPT:http-referrer={referer}\n'
            m3u_content += f'#EXTVLCOPT:http-origin={origin}\n'
            m3u_content += f'#EXTHTTP:{{"Cookie":"{cookie}"}}\n'
            
            # Final Stream URL
            m3u_content += f'{stream_url}\n\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Playlist generated successfully with ClearKey and Header tags!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
