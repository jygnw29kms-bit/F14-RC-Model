import json, pathlib, glob
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
# Collect known vertical datum evidence from active analyses/audits.
records=[]
def add(src,label,val,unit='mm',note=''):
    records.append({'source':src,'label':label,'value':val,'unit':unit,'note':note})
# fuselage OML envelope near aft stations
f=json.loads((root/'analysis/upc_fuselage_30stations_scaled.json').read_text())
for s in f['stations']:
    if s['index'] in (18,19,20,21,22,23,24,25,26):
        add('analysis/upc_fuselage_30stations_scaled.json',f"fuselage_station_{s['index']}_z_top",s['z_top_mm'])
        add('analysis/upc_fuselage_30stations_scaled.json',f"fuselage_station_{s['index']}_z_bottom",s['z_bottom_mm'])
# pivot and wingbox source data
candidates=[
 root/'cad/exports/pivot_cassette_v30/F14_v30_pivot_cassette_audit.json',
 root/'cad/exports/wingbox_fork_v31/F14_v31_wingbox_fork_audit.json',
 root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/center_wingbox_v103/F14_v103_extended_hardpoint_audit.json',
 root/'analysis/F14_pivot_cassette_screen_v30.json',
]
for p in candidates:
    if not p.exists(): continue
    try:d=json.loads(p.read_text())
    except: continue
    txt=json.dumps(d)
    # recursive collect keys with z/wl/pivot
    def walk(o,path=''):
        if isinstance(o,dict):
            for k,v in o.items():
                q=f"{path}.{k}" if path else k
                if isinstance(v,(dict,list)): walk(v,q)
                elif isinstance(v,(int,float)) and any(t in k.lower() for t in ['z','wl','waterline']):
                    add(str(p.relative_to(root)),q,v,note='recursive datum evidence')
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    walk(d)
out={'status':'V126_AIRFRAME_VERTICAL_DATUM_EVIDENCE_INVENTORY','records':records,'gates':{'common_fuselage_wingbox_Z_transform_verified':False,'source_traceable_waterline_verified':False,'propulsion_absolute_Z_ready':False,'fusion_required_yet':False}}
(root/'analysis/airframe_vertical_datum_inventory_v126.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('records',len(records))
for x in records:
    if 'pivot' in x['label'].lower() or 'waterline' in x['label'].lower() or 'bbox' in x['label'].lower(): print(x)