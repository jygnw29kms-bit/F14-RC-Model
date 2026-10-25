import FreeCAD as App, os, json, hashlib
B=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad"
OUT=os.path.join(B,'F14_CURRENT_MODEL_REVIEW_v196.FCStd')
AUD=os.path.join(B,'freecad_F14_CURRENT_MODEL_REVIEW_v196_audit.json')
sources=[
 ('V195',os.path.join(B,'F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')),
 ('CURRENT_SURFACE',os.path.join(B,'F14_ABCDEF_CR172559_SURFACE_REVIEW_CAGE.FCStd')),
 ('TRANS',os.path.join(B,'F14_v196_GLOVE_TRANSITION_PLAN_RAILS.FCStd')),
 ('RADOME',os.path.join(B,'F14_ORIGINAL_RADOME_SEAM_GUIDES.FCStd')),
 ('NOSE',os.path.join(B,'F14_ORIGINAL_NOSE_PROJECTION_GUIDES.FCStd')),
]
d=App.newDocument('F14_CURRENT_MODEL_REVIEW_v196')
counts={}; hashes={}
for tag,path in sources:
 s=App.openDocument(path); grp=d.addObject('App::DocumentObjectGroup',tag); counts[tag]=0; hashes[tag]=hashlib.sha256(open(path,'rb').read()).hexdigest()
 for o in s.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull(): continue
  # avoid container-compound duplicates from imported review docs
  if o.Name in ['OUTER_AIRFRAME','TECH_CURRENT','REFERENCE','V195','CURRENT_SURFACE','TRANS']: continue
  c=d.addObject('PartDesign::Feature',f'{tag}_{o.Name}'); c.Label=f'[{tag}] {o.Label}'; c.Shape=o.Shape.copy(); grp.addObject(c); counts[tag]+=1
 App.closeDocument(s.Name)
meta=d.addObject('App::FeaturePython','REVIEW_META'); meta.Label='ENTWICKLUNGSSTAND v196 / X KANDIDAT / Y PIVOT SOURCE-BACKED / Z FAIL-CLOSED'
d.recompute(); d.saveAs(OUT)
a={'status':'F14_CURRENT_MODEL_REVIEW_V196','sources':hashes,'counts':counts,'gates':{'v195_X_candidate_used':True,'pivot_Y_source_backed':True,'common_Z_registered':False,'glove_transition_plan_only':True,'production_OML':False,'master_release':False,'production_release':False},'output_sha256':hashlib.sha256(open(OUT,'rb').read()).hexdigest()}
open(AUD,'w',encoding='utf-8').write(json.dumps(a,indent=2)); print(json.dumps(a,indent=2))
