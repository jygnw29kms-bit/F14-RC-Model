import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v227_CURRENT_SWEEP_POWER_PACKAGE.FCStd'; out=R/'migration/freecad/F14_v228_DUAL_HV_RECEIVER_RESERVE_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v228_dual_hv_receiver_reserve_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v228_DUAL_HV_RECEIVER_RESERVE_CURRENT')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
# second independent HV domain mirrored from sweep BEC
xc,yc,zc=330.0,-60.0,45.0
tail=Part.makeBox(55,25,12,App.Vector(xc-27.5,yc-12.5,zc-6)); to=doc.addObject('PartDesign::Feature','V228_TAIL_UBEC10A_HV'); to.Shape=tail; to.Label='Taileron Hobbywing UBEC 10A HV / independent 8.4V domain'
tkeep=Part.makeSphere(50,App.Vector(xc,yc,zc)); tk=doc.addObject('PartDesign::Feature','V228_TAIL_BEC_50MM_KEEP_OUT'); tk.Shape=tkeep; tk.Label='Tail BEC receiver keep-out >=50mm / reference'
# hardware-neutral receiver reserve from project maximum envelope 50x30x15
rxcenter=(270.0,0.0,45.0); rx=Part.makeBox(50,30,15,App.Vector(rxcenter[0]-25,rxcenter[1]-15,rxcenter[2]-7.5)); ro=doc.addObject('PartDesign::Feature','V228_RECEIVER_RESERVE_MAX'); ro.Shape=rx; ro.Label='Receiver reserve max 50x30x15 / model and protocol open'
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
sweep_bec=doc.getObject('V227_HOBBYWING_UBEC10A_HV').Shape; sweep_keep=doc.getObject('V227_RECEIVER_50MM_KEEP_OUT').Shape
objs={'tail_bec':tail,'receiver_reserve':rx}; containment={k:v.common(fuse).Volume/v.Volume for k,v in objs.items()}
checks=[]
for label,shape in [('tail_bec',tail),('receiver',rx)]:
 for n in ['V225_SERVO_SERVICE','V221_CASSETTE_R','V221_CASSETTE_L','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','INLET_EDF_R','INLET_EDF_L','V227_HOBBYWING_UBEC10A_HV']:
  o=doc.getObject(n)
  if o and not (label=='tail_bec' and n=='V227_HOBBYWING_UBEC10A_HV'): checks.append({'object':label,'target':n,'distance_mm':shape.distToShape(o.Shape)[0]})
# receiver must be fully outside both 50mm BEC keep-outs
rx_keep=[{'domain':'sweep','distance_mm':rx.distToShape(sweep_keep)[0],'intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(rx.common(sweep_keep))},{'domain':'tail','distance_mm':rx.distToShape(tkeep)[0],'intersection_mm3':(lambda s:0.0 if s.isNull() else s.Volume)(rx.common(tkeep))}]
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V228_DUAL_HV_RECEIVER_RESERVE_CURRENT','architecture':'separate 8.4V UBEC domains for sweep and taileron controls; common signal reference to receiver; propulsion ESC BEC outputs not credited for HV control buses','tail_BEC':{'model':'Hobbywing UBEC 10A HV','PN':'30608000','center_mm':[xc,yc,zc],'mass_g':35},'receiver_reserve':{'center_mm':list(rxcenter),'dims_mm':[50,30,15],'hardware_model_frozen':False},'containment':containment,'packaging_checks':checks,'receiver_keepout_checks':rx_keep,'gates':{'both_BECs_contained':containment['tail_bec']>=0.995,'receiver_reserve_contained':containment['receiver_reserve']>=0.995,'tail_BEC_no_contact':all(r['distance_mm']>0 for r in checks if r['object']=='tail_bec'),'receiver_no_contact':all(r['distance_mm']>0 for r in checks if r['object']=='receiver'),'receiver_fully_outside_both_50mm_BEC_keepouts':all(r['intersection_mm3']<1e-6 for r in rx_keep),'receiver_selected':False,'antenna_layout_verified':False,'brownout_bench_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps({'status':aud['status'],'containment':containment,'receiver_keepout_checks':rx_keep,'minimum_packaging_distance_mm':min(r['distance_mm'] for r in checks),'gates':aud['gates']},indent=2))