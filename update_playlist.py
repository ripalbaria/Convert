import requests
import json

URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        response = requests.get(URL)
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        count = 0
        
        for item in data:
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Entertainment")
            
            # Analysis: Check for both HLS and DASH URLs
            # Star Sports uses mpd_url, Colors uses m3u8_url
            stream_url = item.get("m3u8_url") or item.get("mpd_url")
            
            if not stream_url:
                continue

            # Headers extraction
            ua = item.get("user_agent", "")
            headers = item.get("headers", {})
            cookie = headers.get("Cookie", "")
            origin = headers.get("Origin", "")
            referer = headers.get("Referer", "")

            # M3U Entry creation
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            # Standard VLC/IPTV Player headers
            if ua: m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            if referer: m3u_content += f'#EXTVLCOPT:http-referrer={referer}\n'
            if origin: m3u_content += f'#EXTVLCOPT:http-origin={origin}\n'
            if cookie: m3u_content += f'#EXTHTTP:{{"Cookie":"{cookie}"}}\n'
            
            # DRM Logic for Star Sports (DASH content)
            license_url = item.get("license_url")
            if license_url:
                # Adding KODI properties for Widevine support
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}\n'
            
            m3u_content += f'{stream_url}\n'
            count += 1

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"Success! Processed {count} channels (Sports included).")

    except Exception as e:
        print(f"Error analysis: {e}")

if __name__ == "__main__":
    generate_m3u()
