import json, os, time, sys, random
from concurrent.futures import ThreadPoolExecutor, as_completed
from qs import qs
os.makedirs("raw", exist_ok=True)
us=[x[0] for x in json.load(open("universe_us.json"))]
intl=open("intl.txt").read().split()
# Yahoo uses '-' for class shares (BRK-B)
syms=[s.replace('.','-') for s in us]+intl
todo=[s for s in syms if not os.path.exists(f"raw/{s}.json")]
print(len(syms), "todo", len(todo), flush=True)
def work(s):
    for a in range(4):
        try:
            r=qs(s)
            json.dump(r, open(f"raw/{s}.json","w"))
            return s, "ok"
        except Exception as e:
            msg=str(e)
            if "Not Found" in msg or "No fundamentals" in msg or "404" in msg:
                return s, "nf"
            time.sleep(2**a + random.random())
    return s, "fail:"+msg[:80]
ok=0; bad=[]
with ThreadPoolExecutor(8) as ex:
    futs=[ex.submit(work,s) for s in todo]
    for i,f in enumerate(as_completed(futs)):
        s,st=f.result()
        if st=="ok": ok+=1
        else: bad.append((s,st))
        if i%200==0: print(i, ok, len(bad), flush=True)
print("done", ok, len(bad))
json.dump(bad, open("bad.json","w"))
