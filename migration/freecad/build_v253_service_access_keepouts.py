import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v252_SEGMENT_ALIGNMENT_KEYS.FCStd'; out=R/'migration/freecad/F14_v253_SERVICE_ACCESS_KEEPOUTS.FCStd'; audp=R/'migration/freecad/freecad_v253_service_access_keepouts_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v253_SERVICE_ACCESS_KEEPOUTS')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
spec=[('BATTERY',250,428,-36,36,10,100,['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK']),('SWEEP',430,535,-50,50,8,100,['V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20']),('TAIL_R',675,725,38,86,-12,70,['V233_TORQ_TCM1022_R','V247_TAIL_SERVO_CRADLE_R']),('TAIL_L',675,725,-86,-38,-12,70,['V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_L'])]
rows=[]
for lab,x0,x1,y0,y1,z0,z1,targets in spec:
 sh=Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0)); o=doc.addObject('PartDesign::Feature','V253_ACCESS_'+lab); o.Shape=sh; o.Label=f'v253 service access keepout {lab} / NOT SHELL CUT'
 ov={}
 for n in targets:
  t=doc.getObject(n); ov[n]=0.0 if not t else sh.common(t.Shape).Volume
 rows.append({'access':lab,'bounds_mm':{'x':[x0,x1],'y':[y0,y1],'z':[z0,z1]},'target_overlap_mm3':ov,'all_targets_reached':all(v>0 for v in ov.values())})
# mutual overlap screens: battery vs sweep should remain separated; tail R/L separate.
objs={lab:doc.getObject('V253_ACCESS_'+lab).Shape for lab,*_ in spec}; pairs={}
for a,b in [('BATTERY','SWEEP'),('TAIL_R','TAIL_L'),('SWEEP','TAIL_R'),('SWEEP','TAIL_L')]: pairs[f'{a}_{b}']=objs[a].common(objs[b]).Volume
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V253_SERVICE_ACCESS_KEEPOUTS','source':src.name,'rows':rows,'access_overlap_mm3':pairs,'architecture':{'keepout_reference_only':True,'battery_hatch_rear_edge_x_mm':428,'sweep_hatch_front_edge_x_mm':430,'bridge_between_battery_and_sweep_mm':2,'tail_servo_hatches_independent':True},'gates':{'all_target_hardware_reached':all(r['all_targets_reached'] for r in rows),'battery_sweep_keepouts_do_not_overlap':pairs['BATTERY_SWEEP']<1e-6,'tail_keepouts_do_not_overlap':pairs['TAIL_R_TAIL_L']<1e-6,'physical_hatch_lip_and_fasteners_designed':False,'shell_cut_release':False,'print_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))