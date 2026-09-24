import json, os
L=json.load(open('v2/liquid.json'))
keep=[];drop=0;miss=0
for s in L:
    fn=f'd1/{s}.json'
    if not os.path.exists(fn): miss+=1; keep.append(s); continue
    i=json.load(open(fn)).get('info') or {}
    if i.get('quoteType') not in (None,'EQUITY') or (i.get('industry') or '').startswith('REIT'): drop+=1; continue
    eb=i.get('ebitda'); fe=i.get('forwardEps'); ni=i.get('netIncomeToCommon')
    if (eb and eb>0) or (fe and fe>0) or (ni and ni>0) or i.get('sector')=='Financial Services': keep.append(s)
    else: drop+=1
todo=[s for s in keep if not os.path.exists(f'd2/{s}.json')]
json.dump(todo,open('v2/d2todo.json','w')); print('keep',len(keep),'drop',drop,'missing d1',miss,'todo',len(todo))
