import json, os, time, requests, random
from concurrent.futures import ThreadPoolExecutor
os.makedirs("nq",exist_ok=True)
s1=json.load(open("s1.json"))
syms=[r["sym"] for r in s1 if "." not in r["sym"]]
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept":"application/json"}
def w(s):
    fn=f"nq/{s}.json"
    if os.path.exists(fn): return
    for a in range(3):
        try:
            r=requests.get(f"https://api.nasdaq.com/api/analyst/{s}/earnings-forecast",headers=H,timeout=30)
            json.dump(r.json(),open(fn,"w")); return
        except Exception as e:
            time.sleep(2+random.random()*3)
with ThreadPoolExecutor(4) as ex: list(ex.map(w,syms))
print("done",len(os.listdir("nq")))
