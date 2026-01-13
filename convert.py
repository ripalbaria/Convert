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
        full_data = response.json()

        # The JSON uses 'channels' as the main list
        channels = full_data.get("channels", [])

        if not channels:
            print("No channels found.")
            return

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")

            for item in channels:
                # UPDATED KEYS based on your specific JSON source
                name = item.get("tvg_name", "Unknown")
                tvg_id = item.get("tvg_id", "")
                group = item.get("group_title", "General")
                logo = item.get("tvg_logo", "")
                
                # License keys
                key_id = item.get("key_id", "")
                key = item.get("key", "")
                
                # URL and Cookies
                # Note: If 'url' is missing, it checks for 'stream_url'
                stream_url = item.get("url") or item.get("stream_url", "")
                cookie = item.get("cookie", "")

                # Skip entries with no URL
                if not stream_url:
                    continue

                # Writing the M3U entry
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n')
                
                if key_id and key:
                    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key}\n')
                
                f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
                
                if cookie:
                    f.write(f'#EXTHTTP:{{"cookie":"{cookie}"}}\n')
                
                f.write(f'{stream_url}\n\n')

        print(f"Success! Created {OUTPUT_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_m3u()
