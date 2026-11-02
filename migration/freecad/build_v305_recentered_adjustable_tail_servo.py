import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v303_DYNAMIC_STABILATOR_LINKAGE_SWEEP.FCStd'
out=R/'migration/freecad/F14_v305_RECENTERED_ADJUSTABLE_TAIL_SERVO.FCStd'
audp=R/'migration/freecad/freecad_v305_recentered_adjustable_tail_servo_audit.json'
v303=json.loads((R/'migration/freecad/freecad_v303_dynamic_stabilator_linkage_sweep_audit.json').read_text(encoding='utf-8'))
v304=json.loads((R/'migration/freecad/freecad_v304_servo_adjustment_envelope_audit.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v305_RECENTERED_ADJUSTABLE_TAIL_SERVO')
old={'V299_TORQ_TCM1022_R','V299_TORQ_TCM1022_L','V299_TORQ_SERVICE_R','V299_TORQ_SERVICE_L','V299_TAIL_SERVO_CRADLE_R','V299_TAIL_SERVO_CRADLE_L'}
for ob in d.Objects:
    if ob.Name in old: continue
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
rows=[]; dynamic=[]
def rod(a,b,r):
    v=b.sub(a); return Part.makeCylinder(r,v.Length,a,v.normalize())
for side,sgn in [('R',1),('L',-1)]:
    cx=710.0; cy=sgn*20.0; cz=5.0
    body_old=Part.makeBox(23,27.5,12,App.Vector(cx-11.5,cy-13.75,cz-6))
    svc_old=Part.makeBox(27,31.5,16,App.Vector(cx-13.5,cy-15.75,cz-8))
    # Rebuild the compact v299 twin-rail cradle parametrically at the new Z datum.
    y_inner=cy-16.25; y_outer=cy+16.25; rail_z=cz-8.0
    rail1=Part.makeBox(27,2,3,App.Vector(cx-13.5,y_inner,rail_z))
    rail2=Part.makeBox(27,2,3,App.Vector(cx-13.5,y_outer-2,rail_z))
    bridge1=Part.makeBox(1.5,y_outer-y_inner,3,App.Vector(cx-13.5,y_inner,rail_z))
    bridge2=Part.makeBox(1.5,y_outer-y_inner,3,App.Vector(cx+12.0,y_inner,rail_z))
    cradle_old=rail1.fuse(rail2).fuse(bridge1).fuse(bridge2).removeSplitter()
    bo=doc.addObject('PartDesign::Feature','V305_TORQ_TCM1022_'+side); bo.Shape=body_old; bo.Label='v305 recentered TORQ TCM-1022 candidate '+side
    so=doc.addObject('PartDesign::Feature','V305_TORQ_SERVICE_'+side); so.Shape=svc_old; so.Label='v305 recentered servo service '+side
    co=doc.addObject('PartDesign::Feature','V305_TAIL_SERVO_CRADLE_'+side); co.Shape=cradle_old; co.Label='v305 recentered compact servo cradle '+side
    # Continuous swept volume for all service-box translations: +/-2 X/Y and +/-1 Z around new center z=5.
    y0=(20.0*sgn)-17.75 if sgn>0 else (-20.0)-17.75
    # For left side the same global width is centered at -20.
    if sgn<0: y0=-20.0-17.75
    sweep=Part.makeBox(31.0,35.5,18.0,App.Vector(710-15.5,y0,5-9.0))
    eo=doc.addObject('PartDesign::Feature','V305_ADJUSTMENT_SWEEP_'+side); eo.Shape=sweep; eo.Label='v305 full servo adjustment sweep +/-2 XY +/-1 Z '+side
    edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape; fit=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    rows.append({'side':side,'body_center_mm':[710,sgn*20,5],'body_OML_fraction':body_old.common(oml).Volume/body_old.Volume,'service_OML_fraction':svc_old.common(oml).Volume/svc_old.Volume,'cradle_OML_fraction':cradle_old.common(oml).Volume/cradle_old.Volume,'service_EDF_clearance_mm':svc_old.distToShape(edf)[0],'cradle_EDF_clearance_mm':cradle_old.distToShape(edf)[0],'service_root_clearance_mm':svc_old.distToShape(fit)[0],'adjustment_sweep_OML_fraction':sweep.common(oml).Volume/sweep.Volume,'adjustment_sweep_EDF_clearance_mm':sweep.distToShape(edf)[0]})
    # Recheck all 25 dynamic linkage samples against the cradle after +1 mm recentering.
    for sample in v303['samples']:
        q=next(x for x in sample['sides'] if x['side']==side); hp=App.Vector(*q['horn_tip_mm']); cp=App.Vector(*q['crank_pin_mm'])
        sh=rod(hp,cp,2.0)
        dynamic.append({'side':side,'servo_deg':sample['servo_deg'],'stabilator_deg':sample['stabilator_deg'],'service_to_recentered_cradle_mm':sh.distToShape(cradle_old)[0],'service_cradle_intersection_mm3':sh.common(cradle_old).Volume})
doc.recompute();doc.saveAs(str(out))
aud={'status':'V305_RECENTERED_ADJUSTABLE_TAIL_SERVO','source_model':src.name,'adjustment_source':'migration/freecad/freecad_v304_servo_adjustment_envelope_audit.json','geometry':{'new_body_center_R_mm':[710,20,5],'new_body_center_L_mm':[710,-20,5],'shift_from_v299_mm':[0,0,1],'continuous_adjustment_translation_mm':{'x':[-2,2],'y':[-2,2],'z':[-1,1]}},'rows':rows,'dynamic_cradle_recheck':dynamic,'gates':{'v304_discrete_3x3x3_cube_pass':v304['gates']['full_3x3x3_adjustment_cube_pass'],'recentered_body_service_cradle_OML_ge_0p999':all(r['body_OML_fraction']>=0.999 and r['service_OML_fraction']>=0.999 and r['cradle_OML_fraction']>=0.999 for r in rows),'recentered_service_EDF_clearance_ge_1p5mm':all(r['service_EDF_clearance_mm']>=1.5 for r in rows),'continuous_adjustment_sweep_OML_ge_0p999':all(r['adjustment_sweep_OML_fraction']>=0.999 for r in rows),'continuous_adjustment_sweep_EDF_clearance_ge_1p5mm':all(r['adjustment_sweep_EDF_clearance_mm']>=1.5 for r in rows),'dynamic_service_zero_recentered_cradle_intersection':all(q['service_cradle_intersection_mm3']<1e-6 for q in dynamic),'dynamic_service_recentered_cradle_clearance_ge_5mm':all(q['service_to_recentered_cradle_mm']>=5.0 for q in dynamic),'actual_servo_spline_offset_measured':False,'physical_adjustment_slot_hardware_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps({'status':aud['status'],'rows':rows,'min_dynamic_cradle_clearance_mm':min(q['service_to_recentered_cradle_mm'] for q in dynamic),'gates':aud['gates']},indent=2))
