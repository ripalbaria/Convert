import json
import requests

# Configuration
JSON_URL = "https://raw.githubusercontent.com/kajju027/Jiohotstar-Events-Json/refs/heads/main/jiotv.json"
OUTPUT_FILE = "jiotv.m3u"
USER_AGENT = "plaYtv/7.1.3 (Linux;Android 13) ygx/824.1 ExoPlayerLib/824.0"

def generate_m3u():
    try:
        print(f"Fetching JSON from {JSON_URL}...")
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()

        # Check if the data is a dictionary with a 'channels' key
        if isinstance(data, dict) and "channels" in data:
            channels = data["channels"]
        elif isinstance(data, list):
            channels = data
        else:
            print("Unexpected JSON structure.")
            return

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")

            for item in channels:
                # Key names based on your specific jiotv.json file
                name = item.get("name", "Unknown")
                tvg_id = item.get("id", "")
                group = item.get("category", "General")
                logo = item.get("logo", "")
                
                # License keys (ClearKey)
                key_id = item.get("key_id", "")
                key = item.get("key", "")
                
                # Stream URL and Cookie
                stream_url = item.get("url", "")
                cookie = item.get("cookie", "")

                if not stream_url:
                    continue

                # M3U Entry Formatting
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n')
                
                if key_id and key:
                    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key}\n')
                
                f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
                
                if cookie:
                    f.write(f'#EXTHTTP:{{"cookie":"{cookie}"}}\n')
                
                f.write(f'{stream_url}\n\n')

        print(f"Successfully generated {OUTPUT_FILE} with {len(channels)} channels.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_m3u()
