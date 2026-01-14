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
            
            # DASH (MPD) aur HLS (M3U8) dono ko check karein
            stream_url = item.get("m3u8_url") or item.get("mpd_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")
            
            # Headers formatting (Pipe format for OTT Navigator/Televizo)
            header_suffix = f'|User-Agent={ua}&Cookie={cookie.replace(";", "%3B")}&Referer=https://www.hotstar.com/&Origin=https://www.hotstar.com'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Widevine DRM Setup
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{header_suffix}\n'
            
            # Standard VLC Opts (Backup)
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
            
            # Final URL with header injection
            m3u_content += f'{stream_url}{header_suffix}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Success! Playlist updated with all channels.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
