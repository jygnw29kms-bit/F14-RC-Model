import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v231_CURRENT_ENDMODEL_HARDWARE_STATE.FCStd'; out=R/'migration/freecad/F14_v233_TCM1022_STABILATOR_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v233_TCM1022_stabilator_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v233_TCM1022_STABILATOR_CURRENT'); remove={'STAB_SERVO_ENV_R','STAB_SERVO_ENV_L'}
for o in d.Objects:
 if o.Name in remove: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fuse=doc.getObject('FUSELAGE_CURRENT').Shape; rows=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 body=Part.makeBox(23,27.5,12,App.Vector(700-11.5,sign*60-13.75,-6)); env=Part.makeBox(27,31.5,16,App.Vector(700-13.5,sign*60-15.75,-8))
 bo=doc.addObject('PartDesign::Feature','V233_TORQ_TCM1022_'+lab); bo.Shape=body; bo.Label='TORQ TCM-1022 '+lab+' / 23x12x27.5 / 22g / 14.5kgcm@8.4V'
 eo=doc.addObject('PartDesign::Feature','V233_TORQ_SERVICE_'+lab); eo.Shape=env; eo.Label='v233 TCM-1022 service envelope '+lab
 rec={'side':lab,'body_inside_fraction':body.common(fuse).Volume/body.Volume,'service_inside_fraction':env.common(fuse).Volume/env.Volume,'distances':{}}
 for n in ['STAB_CRANK_'+lab,'STAB_HOUSING_'+lab+'_1','STAB_HOUSING_'+lab+'_2','INLET_EDF_'+lab,'V229_ESC_SERVICE_'+lab,'V228_TAIL_UBEC10A_HV','V227_HOBBYWING_UBEC10A_HV','V221_CASSETTE_'+lab,'V205_BATTERY_375']:
  o=doc.getObject(n)
  if o: rec['distances'][n]={'body_mm':body.distToShape(o.Shape)[0],'service_mm':env.distToShape(o.Shape)[0]}
 rows.append(rec)
doc.recompute();doc.saveAs(str(out))
aud={'status':'V233_TCM1022_STABILATOR_CURRENT','source_v231':str(src),'servo':{'model':'TORQ TCM-1022','dims_mm':[23,12,27.5],'mass_g_each':22,'stall_kgcm_8p4V':14.5,'speed_s_60_8p4V':0.055,'spline':'25T'},'service_dims_mm':[27,31.5,16],'rows':rows,'gates':{'servo_bodies_contained':all(r['body_inside_fraction']>=0.999 for r in rows),'service_envelopes_contained':all(r['service_inside_fraction']>=0.999 for r in rows),'servo_body_no_contact':all(v['body_mm']>0 for r in rows for v in r['distances'].values()),'service_no_contact':all(v['service_mm']>0 for r in rows for v in r['distances'].values()),'v232_torque_gate_pass':True,'stall_current_known':False,'mounting_ears_measured':False,'spline_offset_measured':False,'bench_proof':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))