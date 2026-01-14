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
            
            # Star Sports uses mpd_url, Colors uses m3u8_url
            stream_url = item.get("m3u8_url") or item.get("mpd_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")

            # Headers for DRM authentication
            header_params = f'|User-Agent={ua}&Referer=https://www.hotstar.com/&Cookie={cookie.replace(";", "%3B")}'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Setup for Widevine DRM
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{header_params}\n'
            
            # Standard VLC headers for HLS channels
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
            
            # Stream URL with appended headers for Player compatibility
            m3u_content += f'{stream_url}{header_params}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Success! Playlist updated with corrected DRM & Header logic.")

    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    generate_m3u()
