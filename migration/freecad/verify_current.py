import FreeCAD as App, json, os, sys
base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
meta_path = os.path.join(base, 'migration', 'freecad', 'CURRENT.json')
with open(meta_path, encoding='utf-8-sig') as f:
    meta = json.load(f)
master = os.path.join(base, meta['current_master'].replace('/', os.sep))
if not os.path.exists(master):
    raise SystemExit('CURRENT master missing: ' + master)
doc = App.openDocument(master)
records=[]
fail=[]
for o in doc.Objects:
    if not hasattr(o, 'Shape'):
        continue
    s=o.Shape
    if s.isNull():
        continue
    rec={'name':o.Name,'label':o.Label,'valid':bool(s.isValid()),'solids':len(s.Solids),'faces':len(s.Faces),'volume_mm3':float(s.Volume)}
    records.append(rec)
    if not rec['valid']:
        fail.append(o.Name)
for rel in meta.get('required_audits',[]):
    p=os.path.join(base,rel.replace('/',os.sep))
    if not os.path.exists(p):
        fail.append('missing_audit:'+rel)
result={'status':'F14_FREECAD_CURRENT_VERIFY','master':meta['current_master'],'revision':meta['current_revision'],'shape_objects':len(records),'invalid_or_missing':fail,'pass':not fail,'print_release':False,'flight_release':False}
out=os.path.join(base,'migration','freecad','current_verify.json')
with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
App.closeDocument(doc.Name)
raise SystemExit(0 if result['pass'] else 2)
