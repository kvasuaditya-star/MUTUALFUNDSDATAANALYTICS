import os
import requests
import pandas as pd

# List of scheme codes to fetch
schemes = {
    'HDFC Top 100 Direct': 125497,
    'SBI Bluechip': 119551,
    'ICICI Bluechip': 120503,
    'Nippon Large Cap': 118632,
    'Axis Bluechip': 119092,
    'Kotak Bluechip': 120841
}

output_dir = 'data/raw'
os.makedirs(output_dir, exist_ok=True)

def fetch_nav(scheme_name, scheme_code):
    print(f"Fetching NAV data for {scheme_name} ({scheme_code})...")
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            # The API returns date and nav
            file_path = os.path.join(output_dir, f"{scheme_code}_NAV.csv")
            df.to_csv(file_path, index=False)
            print(f"Saved {len(df)} records to {file_path}")
        else:
            print(f"No 'data' key found in JSON response for {scheme_code}")
    else:
        print(f"Failed to fetch data for {scheme_code}. Status code: {response.status_code}")

if __name__ == "__main__":
    for name, code in schemes.items():
        fetch_nav(name, code)
    
    print("ETL Data ingestion completed.")
