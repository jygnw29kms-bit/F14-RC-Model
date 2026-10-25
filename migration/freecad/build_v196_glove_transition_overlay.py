import FreeCAD as App, os, json, hashlib
B=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad"
OUT=os.path.join(B,'F14_v196_GLOVE_TRANSITION_OVERLAY.FCStd')
AUD=os.path.join(B,'freecad_v196_glove_transition_overlay_audit.json')
v=App.openDocument(os.path.join(B,'F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
g=App.openDocument(os.path.join(B,'F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'))
r=App.openDocument(os.path.join(B,'F14_v196_GLOVE_TRANSITION_PLAN_RAILS.FCStd'))
d=App.newDocument('F14_v196_GLOVE_TRANSITION_OVERLAY')
sets=[('V195',['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L']),('GLOVE',['PLAN_UPPER_GLOVE_COMPONENT','PLAN_LOWER_GLOVE_COMPONENT']),('TRANS',['TRANSITION_RAIL_R','TRANSITION_RAIL_L','DIRECT_CHORD_R','DIRECT_CHORD_L','WING_ROOT_TARGET_R','WING_ROOT_TARGET_L'])]
srcs={'V195':v,'GLOVE':g,'TRANS':r}
counts={}
for tag,names in sets:
 grp=d.addObject('App::DocumentObjectGroup',tag); counts[tag]=0
 for n in names:
  o=srcs[tag].getObject(n)
  if not o or not hasattr(o,'Shape'): continue
  c=d.addObject('PartDesign::Feature',tag+'_'+n); c.Label=f'[{tag}] {o.Label}'; c.Shape=o.Shape.copy(); grp.addObject(c); counts[tag]+=1
meta=d.addObject('App::FeaturePython','META'); meta.Label='V196 PLAN-OVERLAY / Z NICHT REGISTRIERT / KEINE OML-FREIGABE'
d.recompute(); d.saveAs(OUT)
a={'status':'V196_GLOVE_TRANSITION_OVERLAY_REVIEW','counts':counts,'gates':{'plan_only':True,'Z_registered':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(open(OUT,'rb').read()).hexdigest()}
open(AUD,'w',encoding='utf-8').write(json.dumps(a,indent=2)); print(json.dumps(a,indent=2))
