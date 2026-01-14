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
            
            # DASH stream check (Star Sports ke liye)
            stream_url = item.get("mpd_url") or item.get("m3u8_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")
            
            # Formatting headers for the player
            # Inhe ek sath jodne se player authentication pass kar deta hai
            headers_pipe = f'|User-Agent={ua}&Cookie={cookie.replace(";", "%3B")}&Referer=https://www.hotstar.com/&Origin=https://www.hotstar.com'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Widevine License configuration
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                # License URL ke piche headers hona mandatory hai
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{headers_pipe}\n'
            
            # Stream URL with all necessary headers
            m3u_content += f'{stream_url}{headers_pipe}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Success! Playlist updated with final DRM logic.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
