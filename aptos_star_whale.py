import requests, time

def star_whale():
    print("Aptos — Star Whale Detected (> 50M APT moved in one block)")
    seen = set()
    while True:
        r = requests.get("https://aptos-mainnet-api.allthatnode.com/v1/transactions?limit=30")
        for tx in r.json():
            h = tx.get("hash")
            if not h or h in seen: continue
            seen.add(h)

            if tx.get("type") != "user_transaction": continue
            if not tx.get("success"): continue

            amount = 0
            for change in tx.get("changes", []):
                if change.get("type") == "write_resource":
                    data = change.get("data", {})
                    if "coin" in str(data) and "value" in data:
                        try:
                            amount += int(data["value"])
                        except:
                            continue

            if amount >= 50_000_000_000_000:  # > 50M APT (8 decimals)
                usd = amount / 100_000_000 * 7.5  # rough price
                print(f"STAR WHALE BREACHED\n"
                      f"{amount/100_000_000:,.0f} APT (~${usd/1_000_000:.1f}M) moved\n"
                      f"Sender: {tx['sender'][:12]}...\n"
                      f"Tx: https://aptoscan.com/tx/{h}\n"
                      f"→ Aptos just flexed its 160k TPS muscle\n"
                      f"→ This is institutional or exchange-level move\n"
                      f"{'-'*80}")
        time.sleep(1.1)  # Aptos is extremely fast

if __name__ == "__main__":
    star_whale()
