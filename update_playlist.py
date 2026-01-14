import requests
import json

# Your CloudPlay URL
URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        response = requests.get(URL)
        data = response.json()
        
        # Start building the M3U content
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get("name", "Unknown")
            logo = item.get("logo", "")
            group = item.get("group", "Entertainment")
            m3u8 = item.get("m3u8_url", "")
            ua = item.get("user_agent", "")
            
            # Extract headers safely
            headers = item.get("headers", {})
            cookie = headers.get("Cookie", "")
            origin = headers.get("Origin", "")
            referer = headers.get("Referer", "")

            # Build the entry string
            m3u_content += f'#EXTINF:-1 tvg-id="{item.get("id", "")}" tvg-logo="{logo}" group-title="{group}",{name}\n'
            if ua: m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            if referer: m3u_content += f'#EXTVLCOPT:http-referrer={referer}\n'
            if origin: m3u_content += f'#EXTVLCOPT:http-origin={origin}\n'
            if cookie: m3u_content += f'#EXTHTTP:{{"Cookie":"{cookie}"}}\n'
            m3u_content += f'{m3u8}\n'

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print("Playlist updated successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
