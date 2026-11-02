import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v298_EDF_PACKAGING_ENVELOPE.FCStd'
out=R/'migration/freecad/F14_v299_TAIL_SERVO_RELOCATION_CANDIDATE.FCStd'
audp=R/'migration/freecad/freecad_v299_tail_servo_relocation_candidate_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v299_TAIL_SERVO_RELOCATION_CANDIDATE')
remove={'V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V233_TORQ_SERVICE_R','V233_TORQ_SERVICE_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L'}
for ob in d.Objects:
    if ob.Name in remove: continue
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
cx=710.0; ay=20.0; cz=4.0
rows=[]; total_cradle_mass=0.0
for side,sgn in [('R',1),('L',-1)]:
    cy=sgn*ay
    body=Part.makeBox(23,27.5,12,App.Vector(cx-11.5,cy-13.75,cz-6))
    service=Part.makeBox(27,31.5,16,App.Vector(cx-13.5,cy-15.75,cz-8))
    bo=doc.addObject('PartDesign::Feature','V299_TORQ_TCM1022_'+side); bo.Shape=body; bo.Label='v299 relocated TORQ TCM-1022 '+side
    so=doc.addObject('PartDesign::Feature','V299_TORQ_SERVICE_'+side); so.Shape=service; so.Label='v299 relocated TCM-1022 service '+side
    # Body-hugging twin-rail mount. Full rectangular frames waste OML volume in this narrow aft bay.
    # Rails sit just outside the 27.5 mm servo width; short end bridges keep the mount one rigid solid.
    y_inner=cy-16.25
    y_outer=cy+16.25
    rail_z=cz-8.0
    rail1=Part.makeBox(27,2,3,App.Vector(cx-13.5,y_inner,rail_z))
    rail2=Part.makeBox(27,2,3,App.Vector(cx-13.5,y_outer-2,rail_z))
    # Bridges live fully before/behind the 23 mm servo body in X, so they can span the rails without touching it.
    bridge1=Part.makeBox(1.5,y_outer-y_inner,3,App.Vector(cx-13.5,y_inner,rail_z))
    bridge2=Part.makeBox(1.5,y_outer-y_inner,3,App.Vector(cx+12.0,y_inner,rail_z))
    cradle=rail1.fuse(rail2).fuse(bridge1).fuse(bridge2).removeSplitter()
    co=doc.addObject('PartDesign::Feature','V299_TAIL_SERVO_CRADLE_'+side); co.Shape=cradle; co.Label='v299 inboard adjustable PPA-CF tail servo cradle '+side
    total_cradle_mass += cradle.Volume/1000*1.25
    edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape
    crank=doc.getObject('V241_LIGHT_D_CRANK_'+side).Shape
    root=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    rec={'side':side,'servo_center_mm':[cx,cy,cz],'body_oml_fraction':body.common(oml).Volume/body.Volume,'service_oml_fraction':service.common(oml).Volume/service.Volume,'cradle_oml_fraction':cradle.common(oml).Volume/cradle.Volume,'body_edf_clearance_mm':body.distToShape(edf)[0],'service_edf_clearance_mm':service.distToShape(edf)[0],'cradle_edf_clearance_mm':cradle.distToShape(edf)[0],'cradle_servo_intersection_mm3':cradle.common(body).Volume,'service_to_crank_mm':service.distToShape(crank)[0],'service_to_root_fitting_mm':service.distToShape(root)[0],'cradle_valid':cradle.isValid(),'cradle_solids':len(cradle.Solids),'cradle_mass_PPA_CF_g':cradle.Volume/1000*1.25}
    rows.append(rec)
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V299_TAIL_SERVO_RELOCATION_CANDIDATE','source_model':src.name,'decision_basis':'v298 exposed full 73.5 mm EDF collision with legacy v233 servo and v247 cradle; targeted scan selected inboard relocation','geometry':{'servo_center_R_mm':[cx,ay,cz],'servo_center_L_mm':[cx,-ay,cz],'servo_body_mm':[23,27.5,12],'service_mm':[27,31.5,16]},'rows':rows,'mass':{'pair_cradle_PPA_CF_g':total_cradle_mass},'gates':{'bilateral_service_OML_ge_0p999':all(r['service_oml_fraction']>=0.999 for r in rows),'bilateral_cradle_OML_ge_0p995':all(r['cradle_oml_fraction']>=0.995 for r in rows),'service_EDF_clearance_ge_3mm':all(r['service_edf_clearance_mm']>=3.0 for r in rows),'cradle_EDF_clearance_ge_2mm':all(r['cradle_edf_clearance_mm']>=2.0 for r in rows),'cradle_no_servo_body_intersection':all(r['cradle_servo_intersection_mm3']<1e-6 for r in rows),'cradle_valid_single_solids':all(r['cradle_valid'] and r['cradle_solids']==1 for r in rows),'new_linkage_required':True,'exact_servo_spline_offset_measured':False,'pushrod_bellcrank_routing_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
