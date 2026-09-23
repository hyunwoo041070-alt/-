# Build the US universe (market cap >= $2B) from the Nasdaq screener API
import json, requests
H={"User-Agent":"Mozilla/5.0","Accept":"application/json"}
d=requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true",headers=H,timeout=60).json()
json.dump(d,open("nasdaq.json","w"))
u=[]
for r in d["data"]["rows"]:
    s=r["symbol"].strip()
    if any(c in s for c in "^/ "): continue
    try: mc=float(r["marketCap"] or 0)
    except: mc=0
    try: px=float(r["lastsale"].replace("$","").replace(",",""))
    except: px=0
    try: vol=float(r["volume"] or 0)
    except: vol=0
    if mc>=2e9: u.append((s,mc,px*vol,r["name"],r["sector"],r["industry"],r["country"]))
json.dump(u,open("universe_us.json","w"))
print(len(u))
