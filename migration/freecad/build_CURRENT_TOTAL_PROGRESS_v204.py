import FreeCAD as App, json, hashlib
from pathlib import Path
B=Path(r'C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad')
base=B/'F14_v203_INTEGRATED_FULL_MODEL_CANDIDATE.FCStd'
struct=B/'F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd'
out=B/'F14_CURRENT_TOTAL_PROGRESS_v204.FCStd'
d=App.openDocument(str(base)); s=App.openDocument(str(struct))
# import v204 structural objects and keep v203 full-model context
names=['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','V204_PIVOT_SHAFT_R','V204_PIVOT_SHAFT_L','V204_BEARING_LOWER_R','V204_BEARING_UPPER_R','V204_BEARING_LOWER_L','V204_BEARING_UPPER_L']
imp=[]
for n in names:
    o=s.getObject(n)
    if o and hasattr(o,'Shape') and not o.Shape.isNull():
        no=d.addObject('PartDesign::Feature','TOTAL_'+n); no.Label='[STRUCT] '+o.Label; no.Shape=o.Shape.copy(); imp.append(no.Name)
meta=d.addObject('App::FeaturePython','TOTAL_PROGRESS_META'); meta.Label='AKTUELLER GESAMTSTAND v204 / REVIEW'
for p,v in [('Status','Gesamtstand v204: v203 full model + v204 structural wingbox'),('Note','Review only; servo relocation v205 pending; glove absolute Z/OML not released')]:
    meta.addProperty('App::PropertyString',p,'Review'); setattr(meta,p,v)
d.recompute(); d.saveAs(str(out))
a={'status':'CURRENT_TOTAL_PROGRESS_V204','base':str(base),'structural':str(struct),'imported':imp,'shape_count':sum(1 for o in d.Objects if hasattr(o,'Shape') and o.Shape and not o.Shape.isNull()),'gates':{'servo_relocation_v205_pending':True,'absolute_glove_Z_open':True,'production_release':False},'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(B/'freecad_CURRENT_TOTAL_PROGRESS_v204_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
print(json.dumps(a,indent=2))
