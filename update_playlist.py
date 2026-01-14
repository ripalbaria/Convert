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
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Entertainment")
            
            # Star Sports uses mpd_url
            stream_url = item.get("m3u8_url") or item.get("mpd_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")

            # Player compatibility ke liye headers ko URL ke piche "|" ke saath lagana
            # Isse player ko pata chalta hai ki stream aur license dono ke liye ye headers use karne hain
            header_suffix = f'|User-Agent={ua}&Referer={headers.get("Referer", "")}&Cookie={cookie.replace(";", "%3B")}'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Widevine DRM setup for Star Sports 1
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                # License URL ke piche bhi headers lagana zaroori hai
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{header_suffix}\n'
            
            # Final stream URL with headers
            m3u_content += f'{stream_url}{header_suffix}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Playlist updated with advanced Header-Append logic!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
