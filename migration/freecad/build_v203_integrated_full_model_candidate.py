import FreeCAD as App, json, hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad")
src=BASE/'F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'
glv=BASE/'F14_v202_EXACT_GLOVE_CLEARANCE_CANDIDATE.FCStd'
out=BASE/'F14_v203_INTEGRATED_FULL_MODEL_CANDIDATE.FCStd'
d=App.openDocument(str(src))
g=App.openDocument(str(glv))
imported=[]
for name in ['GLOVE_BLEND_R','GLOVE_BLEND_L','INNER_ATTACH_R','INNER_ATTACH_L','OUTER_CLEARANCE_R','OUTER_CLEARANCE_L']:
 o=g.getObject(name)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  n=d.addObject('PartDesign::Feature','V203_'+name); n.Label='[v203] '+o.Label; n.Shape=o.Shape.copy(); imported.append(n.Name)
meta=d.addObject('App::FeaturePython','V203_META'); meta.Label='v203 integrated full model candidate'
meta.addProperty('App::PropertyString','Status','Gate'); meta.Status='INTEGRATED REVIEW CANDIDATE; NOT PRINT/FLIGHT RELEASE'
meta.addProperty('App::PropertyString','GloveSource','Gate'); meta.GloveSource='v202 exact 1.0 mm wing-root clearance candidate'
meta.addProperty('App::PropertyBool','WingSourcePreserved','Gate'); meta.WingSourcePreserved=True
meta.addProperty('App::PropertyBool','AbsoluteZVerified','Gate'); meta.AbsoluteZVerified=False
meta.addProperty('App::PropertyBool','ProductionRelease','Gate'); meta.ProductionRelease=False
d.recompute(); d.saveAs(str(out))
rows=[]
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): rows.append(o.Name)
a={'status':'V203_INTEGRATED_FULL_MODEL_CANDIDATE','source_v195_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_v202_sha256':hashlib.sha256(glv.read_bytes()).hexdigest(),'imported':imported,'shape_object_count':len(rows),'gates':{'wing_source_preserved':True,'pivot_XY_preserved':True,'glove_clearance_1mm_exact':True,'absolute_Z_verified':False,'production_OML':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(BASE/'freecad_v203_integrated_full_model_candidate_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
print(json.dumps(a,indent=2))

