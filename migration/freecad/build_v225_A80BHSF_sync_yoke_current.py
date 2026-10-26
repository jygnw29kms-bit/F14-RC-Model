import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v222_CONSOLIDATED_LIGHT_STRUCTURAL_MODEL.FCStd'; out=R/'migration/freecad/F14_v225_A80BHSF_SYNC_YOKE_CURRENT.FCStd'; audp=R/'migration/freecad/freecad_v225_A80BHSF_sync_yoke_current_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v225_A80BHSF_SYNC_YOKE_CURRENT'); remove={'V205_SWEEP_SERVO','V208_SLIDER_R','V208_SLIDER_L'}
for o in d.Objects:
 if o.Name in remove: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
mid=457.3099792190261; x20=471.21391879567443; xmin=443.4060396423778; z0=2.5; z1=10.5
servo=Part.makeBox(40,20,37.5,App.Vector(mid-20,-10,14)); so=doc.addObject('PartDesign::Feature','V225_SERVO_A80BHSF_V2'); so.Shape=servo; so.Label='AGFRC A80BHSF V2 / 40x20x37.5 / 79g / 36kgcm@8.4V'
service=Part.makeBox(46,26,41.5,App.Vector(mid-23,-13,12)); sv=doc.addObject('PartDesign::Feature','V225_SERVO_SERVICE'); sv.Shape=service; sv.Label='v225 A80BHSF conservative service envelope'
profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
pts=[App.Vector(x20+w,y,z0) for y,w in profile]+[App.Vector(x20-w,y,z0) for y,w in reversed(profile)]; yoke=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(App.Vector(0,0,z1-z0)); yoke=yoke.cut(Part.makeBox(5,13,8.4,App.Vector(x20-2.5,7,z0-.2)))
for yy in [65,-65]: yoke=yoke.cut(Part.makeCylinder(2.1,8.4,App.Vector(x20,yy,z0-.2)))
yo=doc.addObject('PartDesign::Feature','V225_SYNC_YOKE_M4_20'); yo.Shape=yoke; yo.Label='v225 synchronized 7075 yoke / M4.2 joints @20deg'
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
checks=[]
for n in ['V221_CASSETTE_R','V221_CASSETTE_L','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','INLET_EDF_R','INLET_EDF_L']:
 o=doc.getObject(n)
 if o: checks.append({'target':n,'servo_service_distance_mm':service.distToShape(o.Shape)[0]})
service_inside=service.common(fuse).Volume/service.Volume
# dynamic yoke translations against fixed current package
kin=json.loads((R/'analysis/F14_sweep_linkage_kinematics_v40.json').read_text()); c=kin['top_candidates'][23]; shift=108.7860812043256; rows=[]; worst=None
fixed=[doc.getObject(n) for n in ['V221_CASSETTE_R','V221_CASSETTE_L','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','V225_SERVO_SERVICE','INLET_EDF_R','INLET_EDF_L'] if doc.getObject(n)]
for r in c['samples']:
 sw=int(r['sweep_deg']); sx=r['slider_x_mm']-shift; sh=yoke.copy(); sh.translate(App.Vector(sx-x20,0,0))
 for f in fixed:
  dist=sh.distToShape(f.Shape)[0]; rec={'sweep_deg':sw,'target':f.Name,'distance_mm':dist}; rows.append(rec); worst=rec if worst is None or dist<worst['distance_mm'] else worst
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V225_A80BHSF_SYNC_YOKE_CURRENT','servo':{'model':'AGFRC A80BHSF V2','dims_mm':[40,20,37.5],'weight_g':79,'stall_kgcm_8p4V':36,'loading_current_A_8p4V':5.0,'travel_deg':180},'service_inside_fuselage_fraction':service_inside,'static_service_checks':checks,'dynamic_yoke_minimum':worst,'dynamic_rows':rows,'gates':{'service_inside_fuselage_ge_99p5pct':service_inside>=0.995,'static_service_no_contact':all(x['servo_service_distance_mm']>0 for x in checks),'dynamic_yoke_clearance_ge_1mm':worst['distance_mm']>=1.0,'servo_datasheet_reverified_current':False,'yoke_material_certificate_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps({k:aud[k] for k in ['status','service_inside_fuselage_fraction','static_service_checks','dynamic_yoke_minimum','gates']},indent=2))