import json
import requests

# Configuration
JSON_URL = "https://raw.githubusercontent.com/kajju027/Jiohotstar-Events-Json/refs/heads/main/jiotv.json"
OUTPUT_FILE = "jiotv.m3u"
USER_AGENT = "plaYtv/7.1.3 (Linux;Android 13) ygx/824.1 ExoPlayerLib/824.0"

def generate_m3u():
    try:
        # Fetching the JSON data
        print(f"Fetching JSON from {JSON_URL}...")
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            # Write M3U Header
            f.write("#EXTM3U\n\n")

            for item in data:
                # Extracting values from JSON
                name = item.get("name", "Unknown")
                tvg_id = item.get("id", "")
                group = item.get("category", "General")
                logo = item.get("logo", "")
                
                # License keys (ClearKey)
                key_id = item.get("key_id", "")
                key = item.get("key", "")
                
                # URL and Cookies
                stream_url = item.get("url", "")
                cookie = item.get("cookie", "")

                # Writing the M3U entry based on your sample
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n')
                
                if key_id and key:
                    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key}\n')
                
                f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
                
                if cookie:
                    f.write(f'#EXTHTTP:{{ "cookie":"{cookie}" }}\n')
                
                f.write(f'{stream_url}\n\n')

        print(f"Success! File saved as {OUTPUT_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_m3u()

