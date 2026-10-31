import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v247_ADJUSTABLE_TAIL_SERVO_CRADLE.FCStd'; out=R/'migration/freecad/F14_v248_TAIL_SERVO_MOUNT_INTEGRATED.FCStd'; audp=R/'migration/freecad/freecad_v248_tail_servo_mount_integrated_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v248_TAIL_SERVO_MOUNT_INTEGRATED')
rows=[]
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
        rows.append((o.Name,o.Shape.isValid()))
doc.recompute(); doc.saveAs(str(out))
cradles=[doc.getObject('V247_TAIL_SERVO_CRADLE_R'),doc.getObject('V247_TAIL_SERVO_CRADLE_L')]
mass=sum(o.Shape.Volume/1000*1.25 for o in cradles)
old_reserve=27.9194097652027; reserve=old_reserve-mass
aud={'status':'V248_TAIL_SERVO_MOUNT_INTEGRATED','shape_count':len(rows),'all_shapes_valid':all(v for _,v in rows),'tail_servo_cradle_pair_PPA_CF_g':mass,'mass_budget':{'reserve_before_cradles_g':old_reserve,'reserve_after_cradles_g':reserve,'projected_AUW_g':1174.574700301657,'margin_to_1200_g':25.425299698342997},'required_objects':{n:(doc.getObject(n) is not None) for n in ['V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V241_LIGHT_D_CRANK_R','V241_LIGHT_D_CRANK_L','V237_D_SHAFT_R','V237_D_SHAFT_L']},'gates':{'cradle_integrated':True,'reserve_remaining_positive':reserve>0,'exact_TCM1022_CB2_spline_offset_measured':False,'clamp_strap_fastener_pattern_frozen':False,'bench_fit_required':True,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
