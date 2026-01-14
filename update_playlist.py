import requests
import json

URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        response = requests.get(URL)
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            # Extracting basic info from JSON
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Entertainment")
            tvg_id = item.get("id", "")
            
            # Hotstar streams can be mpd or m3u8
            stream_url = item.get("mpd_url") or item.get("m3u8_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "plaYtv/7.1.3 (Linux;Android 13)")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")
            
            # --- Arrangement as per your screenshot ---
            
            # 1. EXTINF Line
            m3u_content += f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n'
            
            # 2. KODIPROP Tags (License Type)
            # Agar license_url hai toh Widevine, nahi toh default Clearkey (as per example)
            lic_type = "widevine" if license_url else "clearkey"
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_type={lic_type}\n'
            m3u_content += f'#KODIPROP:inputstream.adaptive.license_type={lic_type}\n' # Repeated as in example
            
            # 3. KODIPROP License Key
            if license_url:
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}\n'
            
            # 4. EXTVLCOPT User-Agent
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            
            # 5. EXTHTTP Cookie JSON
            if cookie:
                m3u_content += f'#EXTHTTP:{{"cookie":"{cookie}"}}\n'
            
            # 6. Stream URL with Double Pipe arrangement
            # URL || cookie=COOKIE_VALUE
            m3u_content += f'{stream_url}||cookie={cookie}\n\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Success! Data arranged in exact M3U format.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
