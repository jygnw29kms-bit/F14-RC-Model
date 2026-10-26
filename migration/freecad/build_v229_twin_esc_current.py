import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v228_DUAL_HV_RECEIVER_RESERVE_CURRENT.FCStd'; out=R/'migration/freecad/F14_v229_TWIN_ESC_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v229_twin_esc_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v229_TWIN_ESC_CURRENT')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
xc=680.0; ay=95.0; zc=25.0; fuse=doc.getObject('FUSELAGE_CURRENT').Shape; rows=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 body=Part.makeBox(60,25,8,App.Vector(xc-30,sign*ay-12.5,zc-4)); service=Part.makeBox(66,31,14,App.Vector(xc-33,sign*ay-15.5,zc-7))
 bo=doc.addObject('PartDesign::Feature','V229_SKYWALKER50A_'+lab); bo.Shape=body; bo.Label='Hobbywing Skywalker 50A V2 '+lab+' / 60x25x8 / 36g'
 so=doc.addObject('PartDesign::Feature','V229_ESC_SERVICE_'+lab); so.Shape=service; so.Label='v229 ESC service/cooling envelope '+lab+' / +3mm'
 inside=body.common(fuse).Volume/body.Volume; sinside=service.common(fuse).Volume/service.Volume
 rec={'side':lab,'body_inside_fraction':inside,'service_inside_fraction':sinside,'distances':{}}
 for n in ['INLET_EDF_'+lab,'V221_CASSETTE_'+lab,'V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','V227_HOBBYWING_UBEC10A_HV','V228_TAIL_UBEC10A_HV','V228_RECEIVER_RESERVE_MAX']:
  o=doc.getObject(n)
  if o: rec['distances'][n]={'body_mm':body.distToShape(o.Shape)[0],'service_mm':service.distToShape(o.Shape)[0]}
 rows.append(rec)
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V229_TWIN_ESC_CURRENT','ESC':{'model':'Hobbywing Skywalker 50A V2','dims_mm':[60,25,8],'weight_g_each':36,'continuous_A':50,'peak_A':70,'input':'3-4S','BEC':'5V/5A switch-mode'},'EDF_candidate':{'model':'XFly Galaxy X5 50mm 4S 4600KV','published_current_A_each':40,'published_thrust_g_each':900,'published_weight_g_each':75,'external_shroud_OD_verified':False},'electrical':{'ESC_R_5V_BEC_to_receiver_candidate':True,'ESC_L_BEC_red_lead_isolated':True,'sweep_and_taileron_HV_domains_independent':True},'rows':rows,'gates':{'ESC_bodies_contained':all(r['body_inside_fraction']>=0.995 for r in rows),'ESC_service_envelopes_contained':all(r['service_inside_fraction']>=0.995 for r in rows),'ESC_service_no_contact':all(v['service_mm']>0 for r in rows for v in r['distances'].values()),'50A_vs_published_40A_EDF_current_margin_pass':50>=1.2*40,'actual_ESC_purchased_verified':False,'EDF_shroud_OD_verified':False,'thermal_airflow_bench_verified':False,'receiver_5V_brownout_bench_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))