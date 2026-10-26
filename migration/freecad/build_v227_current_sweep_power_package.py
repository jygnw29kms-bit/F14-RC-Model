import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v225_A80BHSF_SYNC_YOKE_CURRENT.FCStd'; out=R/'migration/freecad/F14_v227_CURRENT_SWEEP_POWER_PACKAGE.FCStd'; audp=R/'migration/freecad/freecad_v227_current_sweep_power_package_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v227_CURRENT_SWEEP_POWER_PACKAGE')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
xc,yc,zc=330.0,60.0,45.0
bec=Part.makeBox(55,25,12,App.Vector(xc-27.5,yc-12.5,zc-6)); bo=doc.addObject('PartDesign::Feature','V227_HOBBYWING_UBEC10A_HV'); bo.Shape=bec; bo.Label='Hobbywing UBEC 10A HV PN30608000 / 8.4V'
keep=Part.makeSphere(50,App.Vector(xc,yc,zc)); ko=doc.addObject('PartDesign::Feature','V227_RECEIVER_50MM_KEEP_OUT'); ko.Shape=keep; ko.Label='Receiver keep-out >=50mm from UBEC / reference only'
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
iv=bec.common(fuse).Volume; inside=iv/bec.Volume
checks=[]
for n in ['V225_SERVO_SERVICE','V221_CASSETTE_R','V221_CASSETTE_L','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','INLET_EDF_R','INLET_EDF_L']:
 o=doc.getObject(n)
 if o: checks.append({'target':n,'distance_mm':bec.distToShape(o.Shape)[0]})
# check 50mm receiver keep-out against main high-current / moving hardware; overlap here means receiver cannot live in that region, not a failure by itself
keep_checks=[]
for n in ['V225_SERVO_SERVICE','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','INLET_EDF_R','INLET_EDF_L']:
 o=doc.getObject(n)
 if o: keep_checks.append({'target':n,'distance_from_keepout_surface_mm':keep.distToShape(o.Shape)[0],'keepout_intersection_mm3':(lambda s: 0.0 if s.isNull() else s.Volume)(keep.common(o.Shape))})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V227_CURRENT_SWEEP_POWER_PACKAGE','source_v225':str(src),'BEC':{'model':'Hobbywing UBEC 10A HV','PN':'30608000','dims_mm':[55,25,12],'weight_g':35,'input':'3-14S LiPo','output_V':8.4,'continuous_A':10,'instantaneous_A':25,'center_mm':[xc,yc,zc]},'bec_inside_fuselage_fraction':inside,'packaging_distances':checks,'receiver_keepout_radius_mm':50,'receiver_keepout_checks':keep_checks,'gates':{'BEC_contained_ge_99p5pct':inside>=0.995,'BEC_no_contact_with_current_hardware':all(x['distance_mm']>0 for x in checks),'receiver_keepout_modeled':True,'receiver_selected':False,'wiring_harness_designed':False,'EMI_bench_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps({'status':aud['status'],'bec_inside_fuselage_fraction':inside,'packaging_distances':checks,'receiver_keepout_checks':keep_checks,'gates':aud['gates']},indent=2))