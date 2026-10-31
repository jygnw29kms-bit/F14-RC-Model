import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v244_CURRENT_ENDMODEL_STATE.FCStd'
out=R/'migration/freecad/F14_v247_ADJUSTABLE_TAIL_SERVO_CRADLE.FCStd'
audp=R/'migration/freecad/freecad_v247_adjustable_tail_servo_cradle_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v247_ADJUSTABLE_TAIL_SERVO_CRADLE')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
rows=[]
for lab,sgn in [('R',1),('L',-1)]:
    # 36 x 36 x 2 mm open frame under servo, side guides outside 23x27.5x12 body.
    y0=sgn*42 if sgn>0 else sgn*78
    base=Part.makeBox(36,36,2,App.Vector(682,min(sgn*42,sgn*78),-9))
    cut=Part.makeBox(26,26,3,App.Vector(687,min(sgn*47,sgn*73),-9.5))
    frame=base.cut(cut)
    # Side guides: 2 mm thick, 16 mm tall; servo can slide longitudinally ±4 mm.
    ya=min(sgn*43.5,sgn*45.5); yb=min(sgn*74.5,sgn*76.5)
    g1=Part.makeBox(36,2,16,App.Vector(682,ya,-8))
    g2=Part.makeBox(36,2,16,App.Vector(682,yb,-8))
    sh=frame.fuse(g1).fuse(g2).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V247_TAIL_SERVO_CRADLE_'+lab); o.Shape=sh; o.Label='v247 adjustable PPA-CF tail servo cradle '+lab
    servo=doc.getObject('V233_TORQ_TCM1022_'+lab).Shape; service=doc.getObject('V233_TORQ_SERVICE_'+lab).Shape
    crank=doc.getObject('V241_LIGHT_D_CRANK_'+lab).Shape; fit=doc.getObject('V235_D_ROOT_FITTING_'+lab).Shape
    inter=sh.common(servo); iv=0.0 if inter.isNull() else inter.Volume
    inside=sh.common(fus).Volume/sh.Volume if sh.Volume else 0
    rows.append(dict(side=lab,valid=sh.isValid(),solids=len(sh.Solids),volume_cm3=sh.Volume/1000,mass_PPA_CF_g=sh.Volume/1000*1.25,servo_intersection_mm3=iv,containment_fraction=inside,to_crank_mm=sh.distToShape(crank)[0],to_root_fitting_mm=sh.distToShape(fit)[0],to_service_envelope_mm=sh.distToShape(service)[0]))
doc.recompute(); doc.saveAs(str(out))
pairmass=sum(r['mass_PPA_CF_g'] for r in rows)
aud={'status':'V247_ADJUSTABLE_TAIL_SERVO_CRADLE','geometry':{'x_range_mm':[682,718],'x_adjustment_from_nominal_mm':4.0,'frame_thickness_mm':2.0,'guide_height_mm':16.0,'servo_body_nominal_mm':[23,27.5,12]},'rows':rows,'mass':{'pair_PPA_CF_g':pairmass},'gates':{'valid':all(r['valid'] for r in rows),'no_servo_body_intersection':all(r['servo_intersection_mm3']<1e-6 for r in rows),'fuselage_containment_ge_0p995':all(r['containment_fraction']>=0.995 for r in rows),'crank_clearance_ge_3mm':all(r['to_crank_mm']>=3 for r in rows),'root_fitting_clearance_ge_3mm':all(r['to_root_fitting_mm']>=3 for r in rows),'exact_servo_ear_pattern_required':False,'exact_spline_x_offset_required_for_mount':False,'clamp_strap_detail_open':True,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
