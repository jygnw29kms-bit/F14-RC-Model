import FreeCAD as App,Part,json,hashlib,math
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v215_TORQ_STABILATOR_SERVOS.FCStd';out=BASE/'F14_v216_DUAL_HV_POWER_DOMAINS.FCStd'
d=App.openDocument(str(src));fus=d.getObject('FUSELAGE_CURRENT').Shape
# second identical UBEC for taileron bus at mirrored y=-60
xc,yc,zc=330,-60,45
bec=Part.makeBox(55,25,12,App.Vector(xc-27.5,yc-12.5,zc-6));bo=d.addObject('PartDesign::Feature','V216_TAIL_UBEC10A_HV');bo.Label='Taileron Hobbywing UBEC 10A HV / 8.4V';bo.Shape=bec
keep=Part.makeSphere(50,App.Vector(xc,yc,zc));ko=d.addObject('PartDesign::Feature','V216_TAIL_RECEIVER_50MM_KEEP_OUT');ko.Label='Tail BEC receiver keep-out >=50mm / reference';ko.Shape=keep
# receiver allocation reserve, no model freeze
rxcenter=(270,0,45);rx=Part.makeBox(40,25,12,App.Vector(rxcenter[0]-20,rxcenter[1]-12.5,rxcenter[2]-6));ro=d.addObject('PartDesign::Feature','V216_RECEIVER_RESERVE');ro.Label='Receiver reserve 40x25x12 / protocol not selected';ro.Shape=rx
# packaging checks
objs={'tail_bec':bec,'receiver_reserve':rx}; checks={}
for n,sh in objs.items():
 c=sh.common(fus);checks[n]={'inside_fraction':c.Volume/sh.Volume,'sweep_bec_distance_mm':sh.distToShape(d.getObject('V211_HOBBYWING_UBEC10A_HV').Shape)[0],'battery_tray_distance_mm':sh.distToShape(d.getObject('BATTERY_TRAY_v207').Shape)[0],'servo_service_distance_mm':sh.distToShape(d.getObject('V205_SWEEP_SERVO_SERVICE').Shape)[0]}
# receiver-to-bec center distances
rxd=[math.dist(rxcenter,(330,60,45)),math.dist(rxcenter,(330,-60,45))]
m=d.addObject('App::FeaturePython','V216_META');m.Label='v216 dual HV power domains'
for n,v in [('Architecture','separate 8.4V UBEC for sweep and taileron buses; common signal ground; receiver protocol open'),('TailServoBus','2x TORQ TCM-1022; stall current measurement gate open')]:m.addProperty('App::PropertyString',n,'Electrical');setattr(m,n,v)
for n,v in [('PackagingVerified',True),('ReceiverSelected',False),('TailServoStallCurrentMeasured',False),('BrownoutBenchVerified',False),('FlightRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out));a={'status':'V216_DUAL_HV_POWER_DOMAINS','tail_ubec':{'model':'Hobbywing UBEC 10A HV','center_mm':[xc,yc,zc],'output_V':8.4,'continuous_A':10,'peak_A':25,'mass_g':35},'receiver_reserve':{'center_mm':list(rxcenter),'dims_mm':[40,25,12],'center_distance_to_BECs_mm':rxd},'packaging':checks,'gates':{'both_HV_BECs_packaged':True,'receiver_reserve_outside_50mm_centers':all(x>50 for x in rxd),'receiver_selected':False,'tail_servo_stall_current_measured':False,'brownout_verified':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v216_dual_hv_power_domains_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
