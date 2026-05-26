import json
import urllib.request
import urllib.parse
import time

def fetch_and_send_combined_rates():
    fiat_url = "https://v6.exchangerate-api.com/v6/b2039c00936e994b7e58c2e3/latest/USD"
    # CoinGecko's public API for real-time crypto prices relative to USD
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=solana,bitcoin,ethereum&x_cg_demo_api_key=CG-ZcGDRkjx9vvRq2Pfccffvaqr"
    
    # Target currencies (NGN is now explicitly included as a standard fiat option)
    target_fiat = ["NGN", "GHS", "KES", "ZAR", "GBP", "EUR", "CAD"]
    
    try:
        # 1. Fetch live global fiat rates ($1 USD Base)
        with urllib.request.urlopen(fiat_url) as fiat_response:
            if fiat_response.status == 200:
                fiat_data = json.loads(fiat_response.read().decode())
                all_fiat = fiat_data.get("conversion_rates", {})
                timestamp = fiat_data.get("time_last_update_utc", "Unknown")
                
                # Filter out our target currencies relative to 1 USD
                extracted_rates = {}
                for currency in target_fiat:
                    if currency in all_fiat:
                        extracted_rates[currency] = round(all_fiat[currency], 2)
                
                # 2. Fetch live crypto values based on current USD rate
                req = urllib.request.Request(crypto_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as crypto_response:
                    if crypto_response.status == 200:
                        crypto_data = json.loads(crypto_response.read().decode())
                        
                        # Store current raw USD token rates directly
                        extracted_rates["BTC"] = float(crypto_data["bitcoin"]["usd"])
                        extracted_rates["ETH"] = float(crypto_data["ethereum"]["usd"])
                        extracted_rates["SOL"] = float(crypto_data["solana"]["usd"])
                
                print(f"📊 Extracted Rates Matrix ($1 USD base): {extracted_rates}")
                
                # 3. Transmit the payload to the PHP backend
                payload = {
                    "rates_json": json.dumps(extracted_rates),
                    "updated_at": timestamp
                }
                
                backend_url = "../backend/fx-fiat.php" 
                encoded_data = urllib.parse.urlencode(payload).encode('utf-8')
                post_req = urllib.request.Request(backend_url, data=encoded_data, method="POST")
                
                with urllib.request.urlopen(post_req) as backend_response:
                    print("🚀 Sync Response:", backend_response.read().decode())
            else:
                print("❌ Error: API timeout.")
                
    except Exception as e:
        print(f"⚠️ Loop Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Persistent 1 USD-Base Scraper Active...")
    print("Press CTRL + C to stop anytime.\n")
    
    while True:
        fetch_and_send_combined_rates()
        time.sleep(5)
