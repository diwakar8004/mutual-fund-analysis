import os
import requests
import pandas as pd

print("--- FULL DATA EXTRACTION START ---")

# All 6 required mutual fund schemes from your assignment guidelines
SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

RAW_FOLDER = "data/raw"
os.makedirs(RAW_FOLDER, exist_ok=True)

for code, name in SCHEMES.items():
    url = f"https://api.mfapi.in/mf/{code}"
    print(f"\nFetching: {name} (Code: {code})...")
    
    try:
        # Requesting data with an increased timeout of 20 seconds in case the API is slow
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            json_data = response.json()
            price_history = json_data.get("data", [])
            
            df = pd.DataFrame(price_history)
            df["scheme_code"] = code
            df["scheme_name"] = name
            
            output_file = f"{RAW_FOLDER}/{code}_{name.lower()}.csv"
            df.to_csv(output_file, index=False)
            print(f"✅ Saved successfully! Row count: {len(df)}")
        else:
            print(f"❌ API issues for {name}. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Connection skipped for {name}: {e}")

print("\n--- FULL DATA EXTRACTION END ---")