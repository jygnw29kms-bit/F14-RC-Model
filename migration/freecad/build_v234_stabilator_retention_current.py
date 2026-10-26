import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v233_TCM1022_STABILATOR_CURRENT.FCStd'; out=R/'migration/freecad/F14_v234_STABILATOR_RETENTION_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v234_stabilator_retention_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v234_STABILATOR_RETENTION_CURRENT')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=736.0078983334656; fuse=doc.getObject('FUSELAGE_CURRENT').Shape; rows=[]
def cyl_y(y0,sgn,od,id_,length):
 outer=Part.makeCylinder(od/2,length,App.Vector(px,y0,0),App.Vector(0,sgn,0)); inner=Part.makeCylinder(id_/2,length,App.Vector(px,y0,0),App.Vector(0,sgn,0)); return outer.cut(inner)
for lab,sgn in [('R',1),('L',-1)]:
 # v177 retention stack, mirrored. y ranges are absolute magnitudes.
 parts=[]
 specs=[('BEARING_INBOARD_COLLAR',47,3,10,6.1),('BEARING_OUTER_SHOULDER',75,1,9,6.1),('SURFACE_INNER_COLLAR',80,2,10,6.1),('SURFACE_OUTER_WASHER',106,2,10,3.2)]
 for nm,ay,l,od,id_ in specs:
  y0=sgn*ay; sh=cyl_y(y0,sgn,od,id_,l); o=doc.addObject('PartDesign::Feature','V234_'+nm+'_'+lab); o.Shape=sh; o.Label='v234 '+nm+' '+lab+' / candidate retention'; parts.append(o)
 # positive end-fastener head envelope, 6mm OD x3mm
 head=Part.makeCylinder(3.0,3.0,App.Vector(px,sgn*108,0),App.Vector(0,sgn,0)); ho=doc.addObject('PartDesign::Feature','V234_END_FASTENER_HEAD_'+lab); ho.Shape=head; ho.Label='v234 end fastener head '+lab+' / envelope'; parts.append(ho)
 rec={'side':lab,'objects':[]}
 for o in parts:
  sh=o.Shape; inside=sh.common(fuse).Volume/sh.Volume if sh.Volume else 0; ds={}
  for n in ['STAB_SHAFT_'+lab,'STAB_BEARING_'+lab+'_1','STAB_BEARING_'+lab+'_2','STAB_HOUSING_'+lab+'_1','STAB_HOUSING_'+lab+'_2','STAB_CRANK_'+lab,'V233_TORQ_SERVICE_'+lab,'STABILATOR_'+lab]:
   q=doc.getObject(n)
   if q: ds[n]=sh.distToShape(q.Shape)[0]
  rec['objects'].append({'name':o.Name,'inside_fraction':inside,'distances_mm':ds})
 rows.append(rec)
doc.recompute();doc.saveAs(str(out))
# contacts with shaft/bearings are intentional; report containment and unintended servo/crank interference only
allparts=[x for r in rows for x in r['objects']]
aud={'status':'V234_STABILATOR_RETENTION_CURRENT','source_v233':str(src),'architecture':'two 6x13x5 radial bearings per side + inboard collar/outboard shoulder + surface inner collar + outer washer/end fastener; no transverse shaft hole','rows':rows,'gates':{'retention_parts_contained':all(x['inside_fraction']>=0.999 for x in allparts),'retention_to_servo_service_no_interference':all(x['distances_mm'].get('V233_TORQ_SERVICE_'+r['side'],999)>0 for r in rows for x in r['objects']),'shaft_actual_hardware_frozen':False,'bearing_actual_hardware_frozen':False,'end_fastener_thread_strength_verified':False,'printed_housing_load_path_verified':False,'bench_proof':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))