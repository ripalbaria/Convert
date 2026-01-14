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
            
            # DASH (MPD) support for Star Sports
            stream_url = item.get("m3u8_url") or item.get("mpd_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")

            # Sabse important step: Headers ko URL format mein convert karna
            # DRM license servers ko authentication ke liye yehi headers chahiye
            header_params = f'|User-Agent={ua}&Referer=https://www.hotstar.com/&Cookie={cookie.replace(";", "%3B")}'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Widevine DRM Setup
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                # License URL ke saath headers append karna taaki authentication pass ho
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{header_params}\n'
            
            # Final stream URL with headers
            m3u_content += f'{stream_url}{header_params}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Final DRM-Fix playlist generated!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
