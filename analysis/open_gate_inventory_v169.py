import json,pathlib,re
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
items=[]
for p in (root/'analysis').glob('*.json'):
    m=re.search(r'_v(\d+)\.json$',p.name)
    if not m or int(m.group(1))<100: continue
    try: d=json.loads(p.read_text(encoding='utf-8-sig'))
    except Exception: continue
    release=d.get('release',{}) if isinstance(d,dict) else {}
    gates=d.get('gates',{}) if isinstance(d,dict) else {}
    false=[]
    for src_name,obj in [('release',release),('gates',gates)]:
        if isinstance(obj,dict):
            for k,v in obj.items():
                if v is False: false.append(f'{src_name}.{k}')
    status=d.get('status') if isinstance(d,dict) else None
    items.append({'revision':int(m.group(1)),'file':str(p.relative_to(root)).replace('\\','/'),'status':status,'false_gates':false})
items.sort(key=lambda x:(x['revision'],x['file']))
# classify latest actionable themes from names/gates
for x in items:
    name=x['file'].lower();
    if any(k in name for k in ['proof','hardware','acceptance','material']): x['dependency_hint']='physical/hardware likely'
    elif any(k in name for k in ['cad','geometry','packaging','corridor','tray','linkage','pivot']): x['dependency_hint']='CAD/analysis actionable'
    else: x['dependency_hint']='analysis/review'
(root/'analysis/open_gate_inventory_v169.json').write_text(json.dumps({'status':'V169_OPEN_GATE_INVENTORY','items':items},indent=2),encoding='utf-8')
for x in items[-35:]: print(f"v{x['revision']:03d} {x['file']} | {x['status']} | false={','.join(x['false_gates'])} | {x['dependency_hint']}")