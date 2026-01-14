import requests
import json

# Your CloudPlay URL
URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "playlist.m3u"

def generate_m3u():
    try:
        # Some workers require a mobile User-Agent to show all sports channels
        headers_request = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
        }
        
        response = requests.get(URL, headers=headers_request)
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        count = 0
        
        for item in data:
            # Get data with fallbacks
            name = item.get("name", "Unknown Channel")
            group = item.get("group", "General")
            
            # Extract the stream and headers
            m3u8 = item.get("m3u8_url", "")
            if not m3u8: continue # Skip if no URL
            
            ua = item.get("user_agent", "Mozilla/5.0")
            headers = item.get("headers", {})
            cookie = headers.get("Cookie", "")
            
            # Format the M3U entry
            m3u_content += f'#EXTINF:-1 tvg-logo="{item.get("logo", "")}" group-title="{group}",{name}\n'
            m3u_content += f'#EXTVLCOPT:http-user-agent={ua}\n'
            if cookie:
                m3u_content += f'#EXTVLCOPT:http-cookie={cookie}\n'
            m3u_content += f'{m3u8}\n'
            count += 1

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"Success! Processed {count} channels.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_m3u()
