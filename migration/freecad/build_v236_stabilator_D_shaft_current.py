import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v235_STABILATOR_ROOT_FITTING_CURRENT.FCStd'; out=R/'migration/freecad/F14_v236_STABILATOR_D_SHAFT_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v236_stabilator_D_shaft_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v236_STABILATOR_D_SHAFT_CURRENT'); remove={'STAB_SHAFT_R','STAB_SHAFT_L'}
for o in d.Objects:
 if o.Name in remove: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=736.0078983334656; rows=[]
def d_segment(sgn):
 # round inboard region |Y|45..82; D-flat only |Y|82..106
 round_in=Part.makeCylinder(3.0,37.0,App.Vector(px,sgn*45,0),App.Vector(0,sgn,0))
 outer=Part.makeCylinder(3.0,24.0,App.Vector(px,sgn*82,0),App.Vector(0,sgn,0))
 lo=px-4.0; hi=px+2.4; ya=min(sgn*82,sgn*106)-1; yb=max(sgn*82,sgn*106)+1; clip=Part.makeBox(hi-lo,yb-ya,8.0,App.Vector(lo,ya,-4.0)); dpart=outer.common(clip)
 return round_in.fuse(dpart).removeSplitter()
for lab,sgn in [('R',1),('L',-1)]:
 shaft=d_segment(sgn); o=doc.addObject('PartDesign::Feature','V236_D_SHAFT_'+lab); o.Shape=shaft; o.Label='v236 6mm D-shaft '+lab+' / round bearings + local D engagement'
 fit=doc.getObject('V235_D_ROOT_FITTING_'+lab).Shape; crank=doc.getObject('STAB_CRANK_'+lab).Shape
 bearing1=doc.getObject('STAB_BEARING_'+lab+'_1').Shape; bearing2=doc.getObject('STAB_BEARING_'+lab+'_2').Shape
 rows.append({'side':lab,'valid':shaft.isValid(),'solid_count':len(shaft.Solids),'volume_cm3':shaft.Volume/1000.0,'fitting_intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(shaft.common(fit)),'bearing1_intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(shaft.common(bearing1)),'bearing2_intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(shaft.common(bearing2)),'shaft_to_crank_mm':shaft.distToShape(crank)[0],'shaft_to_servo_service_mm':shaft.distToShape(doc.getObject('V233_TORQ_SERVICE_'+lab).Shape)[0]})
doc.recompute();doc.saveAs(str(out))
aud={'status':'V236_STABILATOR_D_SHAFT_CURRENT','geometry':{'diameter_mm':6.0,'round_region_abs_y_mm':[45,82],'D_region_abs_y_mm':[82,106],'shaft_flat_x_from_center_mm':2.4,'fitting_bore_radius_mm':3.05,'fitting_bore_flat_x_from_center_mm':2.45,'nominal_radial_clearance_mm':0.05,'nominal_flat_clearance_mm':0.05},'rows':rows,'gates':{'shaft_single_valid_solid_each_side':all(r['valid'] and r['solid_count']==1 for r in rows),'D_fitting_clearance_no_intersection':all(r['fitting_intersection_mm3']<1e-6 for r in rows),'bearing_regions_no_solid_interference':all(r['bearing1_intersection_mm3']<1e-6 and r['bearing2_intersection_mm3']<1e-6 for r in rows),'crank_region_round_and_contacting':all(r['shaft_to_crank_mm']==0 for r in rows),'actual_shaft_material_frozen':False,'machining_flat_tolerance_verified':False,'bench_proof':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))