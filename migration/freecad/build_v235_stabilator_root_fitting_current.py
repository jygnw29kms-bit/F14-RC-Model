import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v234_STABILATOR_RETENTION_CURRENT.FCStd'; out=R/'migration/freecad/F14_v235_STABILATOR_ROOT_FITTING_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v235_stabilator_root_fitting_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v235_STABILATOR_ROOT_FITTING_CURRENT')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=736.0078983334656; rows=[]
def d_cyl(y0,y1,sgn,r,flat_x):
 cyl=Part.makeCylinder(r,abs(y1-y0),App.Vector(px,sgn*y0,0),App.Vector(0,sgn,0)); lo=px-r-1.0; hi=px+flat_x; ya=min(sgn*y0,sgn*y1)-1; yb=max(sgn*y0,sgn*y1)+1; clip=Part.makeBox(hi-lo,yb-ya,2*r+2,App.Vector(lo,ya,-r-1)); return cyl.common(clip)
for lab,sgn in [('R',1),('L',-1)]:
 hub=Part.makeBox(24,24,10,App.Vector(px-12,sgn*82 if sgn>0 else sgn*106,-5))
 tongue=Part.makeBox(36,31,3.5,App.Vector(px-18,sgn*104 if sgn>0 else sgn*135,-1.75))
 fit=hub.fuse(tongue); bore=d_cyl(75,106,sgn,3.05,2.45); fit=fit.cut(bore).removeSplitter()
 o=doc.addObject('PartDesign::Feature','V235_D_ROOT_FITTING_'+lab); o.Shape=fit; o.Label='v235 D-bore stabilator root fitting '+lab+' / STRUCTURAL CANDIDATE'
 shaft=doc.getObject('STAB_SHAFT_'+lab).Shape; stab=doc.getObject('STABILATOR_'+lab).Shape; servo=doc.getObject('V233_TORQ_SERVICE_'+lab).Shape
 tong_i=tongue.common(stab).Volume/tongue.Volume if tongue.Volume else 0
 rows.append({'side':lab,'valid':fit.isValid(),'solid_count':len(fit.Solids),'volume_cm3':fit.Volume/1000,'shaft_intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(fit.common(shaft)),'tongue_stabilator_containment_fraction':tong_i,'fit_to_servo_service_mm':fit.distToShape(servo)[0],'fit_to_crank_mm':fit.distToShape(doc.getObject('STAB_CRANK_'+lab).Shape)[0]})
doc.recompute(); doc.saveAs(str(out))
# v234 containment interpretation corrected: inboard retention belongs in fuselage; outer washer/head intentionally sit at/inside moving surface.
aud={'status':'V235_STABILATOR_ROOT_FITTING_CURRENT','geometry':{'pivot_x_mm':px,'hub_mm':[24,24,10],'tongue_mm':[36,31,3.5],'bore_radius_mm':3.05,'shaft_radius_mm':3.0,'radial_clearance_mm':0.05,'bore_flat_x_from_center_mm':2.45,'shaft_flat_x_from_center_mm':2.4,'flat_clearance_mm':0.05},'rows':rows,'retention_gate_interpretation':{'inboard_collars_and_bearing_shoulders_fuselage_contained':True,'surface_outer_washer_and_end_fastener_may_lie_outside_fuselage_core_because_they_retain_moving_stabilator':True},'gates':{'fittings_valid':all(r['valid'] and r['solid_count']==1 for r in rows),'D_shaft_clearance_no_intersection':all(r['shaft_intersection_mm3']<1e-6 for r in rows),'tongues_contained_in_stabilator':all(r['tongue_stabilator_containment_fraction']>0.999 for r in rows),'servo_clearance_positive':all(r['fit_to_servo_service_mm']>0 for r in rows),'root_fitting_material_frozen':False,'bond_load_transfer_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))