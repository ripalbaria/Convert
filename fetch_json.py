import requests
import json

# CloudPlay API URL
URL = "https://cloudplay-app.cloudplay-help.workers.dev/hotstar?password=all"
OUTPUT_FILE = "data.json"

def save_raw_json():
    try:
        # Requesting the API
        response = requests.get(URL)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Saving the exact JSON response to a file
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            
            print(f"Success! Saved raw data to {OUTPUT_FILE}")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    save_raw_json()
