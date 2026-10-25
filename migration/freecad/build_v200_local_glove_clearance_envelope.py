import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
src=R/'migration/freecad/F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'
outp=R/'migration/freecad/F14_v200_LOCAL_GLOVE_CLEARANCE_ENVELOPE.FCStd'
auditp=R/'migration/freecad/freecad_v200_local_glove_clearance_envelope_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v200_LOCAL_GLOVE_CLEARANCE_ENVELOPE')
# copy context: fuselage/wings/pivots only
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Label='[CTX] '+o.Label; q.Shape=o.Shape.copy()
# construct local clearance envelope around root, not OML: prism-like fences from x 488..520 at y +/-148.826 with wing lower z sampled conservatively from prior scans
# Candidate envelope is BELOW wing lower surface by 1 mm, visual only. Use interpolated known samples around pivot zone.
y=148.8263775443693
samples=[(490,-3.85),(492,-4.03),(496,-4.25),(500,-4.45),(504.346,-4.742),(508,-4.85),(512,-4.95),(516,-5.05),(520,-5.10)]
clear=1.0
for sgn,lab in [(1,'R'),(-1,'L')]:
 pts=[App.Vector(x,sgn*y,z-clear) for x,z in samples]
 rail=Part.makePolygon(pts)
 o=doc.addObject('PartDesign::Feature','CLEARANCE_RAIL_'+lab); o.Label=f'v200 fixed-glove lower clearance rail {lab} / 1mm below wing-root / REFERENCE ONLY'; o.Shape=rail
 # secondary rail inward by 18 mm to show envelope corridor
 pts2=[App.Vector(x,sgn*(y-18.0),z-clear-1.5) for x,z in samples]
 r2=Part.makePolygon(pts2)
 o2=doc.addObject('PartDesign::Feature','INNER_RAIL_'+lab); o2.Label=f'v200 inner glove support rail {lab} / candidate / REFERENCE ONLY'; o2.Shape=r2
 # ruled surface between rails as candidate local envelope, not OML
 try:
  surf=Part.makeRuledSurface(rail,r2)
  so=doc.addObject('PartDesign::Feature','GLOVE_ENVELOPE_'+lab); so.Label=f'v200 local fixed glove clearance envelope {lab} / NOT OML'; so.Shape=surf
 except Exception as e:
  print('surface_fail',lab,e)
# meta
m=doc.addObject('App::FeaturePython','V200_GATE');m.addProperty('App::PropertyString','Status');m.Status='LOCAL GLOVE CLEARANCE ENVELOPE – REFERENCE ONLY – ABSOLUTE Z UNVERIFIED'
doc.recompute(); doc.saveAs(str(outp))
rows=[]
for o in doc.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): rows.append({'name':o.Name,'valid':o.Shape.isValid(),'edges':len(o.Shape.Edges),'faces':len(o.Shape.Faces)})
aud={'status':'V200_LOCAL_GLOVE_CLEARANCE_ENVELOPE_REFERENCE_ONLY','clearance_target_mm':clear,'x_range_mm':[490,520],'root_abs_y_mm':y,'object_count':len(rows),'all_shapes_valid':all(r['valid'] for r in rows),'rows':rows,'gates':{'source_wing_preserved':True,'pivot_XY_preserved':True,'absolute_Z_verified':False,'production_OML':False,'master_changed':False,'production_release':False}}
aud['output_sha256']=hashlib.sha256(outp.read_bytes()).hexdigest();auditp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))
