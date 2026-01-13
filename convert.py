import json
import requests

JSON_URL = "https://raw.githubusercontent.com/kajju027/Jiohotstar-Events-Json/refs/heads/main/jiotv.json"
OUTPUT_FILE = "jiotv.m3u"
USER_AGENT = "plaYtv/7.1.3 (Linux;Android 13) ygx/824.1 ExoPlayerLib/824.0"

def generate_m3u():
    try:
        print(f"Fetching JSON from {JSON_URL}...")
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()

        # Handle different JSON structures (List vs Dictionary)
        if isinstance(data, dict):
            channels = data.get("channels", data.get("result", data.get("data", [])))
        else:
            channels = data

        print(f"Found {len(channels)} items to process.")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            count = 0

            for item in channels:
                # 1. Get Name (Checking all possible keys)
                name = item.get("name") or item.get("tvg_name") or item.get("title") or "Unknown"
                
                # 2. Get ID
                tvg_id = item.get("id") or item.get("tvg_id") or ""
                
                # 3. Get Logo
                logo = item.get("logo") or item.get("tvg_logo") or item.get("image") or ""
                
                # 4. Get Group
                group = item.get("category") or item.get("group_title") or "General"
                
                # 5. Get Stream URL (Crucial Fix)
                stream_url = item.get("url") or item.get("link") or item.get("stream_url") or ""
                
                # 6. Get Cookies & Keys
                cookie = item.get("cookie") or ""
                key_id = item.get("key_id") or ""
                key = item.get("key") or ""

                if not stream_url:
                    continue  # Skip only if there is absolutely no URL

                # Build the M3U Entry
                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{group}" tvg-logo="{logo}",{name}\n')
                
                if key_id and key:
                    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key}\n')
                
                f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
                
                if cookie:
                    f.write(f'#EXTHTTP:{{"cookie":"{cookie}"}}\n')
                
                f.write(f'{stream_url}\n\n')
                count += 1

        print(f"Success! Final M3U contains {count} channels.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_m3u()
