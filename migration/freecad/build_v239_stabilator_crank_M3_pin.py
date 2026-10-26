import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v237_STABILATOR_D_CRANK_DRIVE.FCStd'; out=R/'migration/freecad/F14_v239_STABILATOR_CRANK_M3_PIN.FCStd'; audp=R/'migration/freecad/freecad_v239_stabilator_crank_M3_pin_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v239_STABILATOR_CRANK_M3_PIN'); remove={'V237_D_CRANK_R','V237_D_CRANK_L'}
for o in d.Objects:
 if o.Name in remove: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=736.0078983334656; rows=[]
def d_bore(sgn):
 cyl=Part.makeCylinder(3.05,4,App.Vector(px,sgn*76,0),App.Vector(0,sgn,0)); lo=px-4.05; hi=px+2.45; ya=min(sgn*76,sgn*80)-1; yb=max(sgn*76,sgn*80)+1; clip=Part.makeBox(hi-lo,yb-ya,8.1,App.Vector(lo,ya,-4.05)); return cyl.common(clip)
for lab,sgn in [('R',1),('L',-1)]:
 outer=Part.makeCylinder(18.9,4,App.Vector(px,sgn*76,0),App.Vector(0,sgn,0)); crank=outer.cut(d_bore(sgn)); pin=Part.makeCylinder(1.6,4.4,App.Vector(px+15.0,sgn*75.8,0),App.Vector(0,sgn,0)); crank=crank.cut(pin).removeSplitter(); o=doc.addObject('PartDesign::Feature','V239_D_CRANK_M3_'+lab); o.Shape=crank; o.Label='v239 D-bore crank '+lab+' / M3 pushrod hole r15mm'
 shaft=doc.getObject('V237_D_SHAFT_'+lab).Shape; fit=doc.getObject('V235_D_ROOT_FITTING_'+lab).Shape; servo=doc.getObject('V233_TORQ_SERVICE_'+lab).Shape
 rows.append({'side':lab,'valid':crank.isValid(),'solid_count':len(crank.Solids),'volume_cm3':crank.Volume/1000,'shaft_intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(crank.common(shaft)),'to_root_fitting_mm':crank.distToShape(fit)[0],'to_servo_service_mm':crank.distToShape(servo)[0]})
doc.recompute();doc.saveAs(str(out))
aud={'status':'V239_STABILATOR_CRANK_M3_PIN','geometry':{'outer_radius_mm':18.9,'thickness_mm':4,'D_bore_radius_mm':3.05,'D_bore_flat_x_mm':2.45,'pushrod_hole_center_radius_mm':15.0,'pushrod_hole_d_mm':3.2,'radial_edge_ligament_mm':2.3,'matched_servo_arm_radius_mm':6.34920634920635},'rows':rows,'gates':{'cranks_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'shaft_clearance_no_intersection':all(r['shaft_intersection_mm3']<1e-6 for r in rows),'root_fitting_gap_ge_2mm':all(r['to_root_fitting_mm']>=2 for r in rows),'servo_service_clearance_ge_3mm':all(r['to_servo_service_mm']>=3 for r in rows),'M3_pin_actual_hardware_selected':False,'ball_link_or_clevis_selected':False,'crank_material_frozen':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))