import requests
import json

URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        # Requesting the API with a Mobile User-Agent to ensure full data
        res = requests.get(URL)
        data = res.json()
        
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Entertainment")
            
            # DASH content detection
            stream_url = item.get("mpd_url") or item.get("m3u8_url")
            if not stream_url:
                continue

            headers = item.get("headers", {})
            ua = item.get("user_agent", "Hotstar;in.startv.hotstar/25.01.27.5.3788")
            cookie = headers.get("Cookie", "")
            license_url = item.get("license_url", "")
            
            # Format headers for player compatibility
            # Encoding cookie and adding referer
            safe_cookie = cookie.replace(";", "%3B")
            auth_headers = f'|User-Agent={ua}&Cookie={safe_cookie}&Referer=https://www.hotstar.com/&Origin=https://www.hotstar.com'

            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            
            if license_url:
                # Widevine DRM tags for players like OTT Navigator
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_type=widevine\n'
                m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={license_url}{auth_headers}\n'
            
            # Adding VLC specific options as backup
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
            
            # Appending headers to the stream URL itself
            m3u_content += f'{stream_url}{auth_headers}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Playlist Fixed! Use an app like OTT Navigator or TiviMate for DASH/DRM.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
