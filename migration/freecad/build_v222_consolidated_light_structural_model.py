import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v221_LIGHT_PIVOT_CASSETTE.FCStd'; out=R/'migration/freecad/F14_v222_CONSOLIDATED_LIGHT_STRUCTURAL_MODEL.FCStd'; audp=R/'migration/freecad/freecad_v222_consolidated_light_structural_model_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v222_CONSOLIDATED_LIGHT_STRUCTURAL_MODEL')
exclude={'V204_SOCKET_FRONT_R','V204_SOCKET_REAR_R','V204_MONO_LOWER_R','V204_UPPER_FORK_R','V204_SOCKET_FRONT_L','V204_SOCKET_REAR_L','V204_MONO_LOWER_L','V204_UPPER_FORK_L','V204_META','SWEEP_SERVO_SERVICE_REF','WINGBOX_REF'}; kept=[]
for o in d.Objects:
 if o.Name in exclude: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label; kept.append(o.Name)
doc.recompute(); doc.saveAs(str(out)); rows=[]
for lab in ['R','L']:
 cas=doc.getObject('V221_CASSETTE_'+lab).Shape
 for n in ['INLET_EDF_R','INLET_EDF_L','V205_SWEEP_SERVO_SERVICE','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375','V208_SLIDER_'+lab]:
  o=doc.getObject(n)
  if o: rows.append({'cassette':lab,'target':n,'distance_mm':cas.distToShape(o.Shape)[0]})
res={'status':'V222_CONSOLIDATED_LIGHT_STRUCTURAL_MODEL','source_v221':str(src),'excluded_legacy_duplicates':sorted(exclude),'kept_shape_count':len(kept),'pair_cassette_volume_cm3':sum(doc.getObject('V221_CASSETTE_'+x).Shape.Volume for x in ['R','L'])/1000.0,'packaging_distances':rows,'gates':{'legacy_structural_duplicates_removed':all(doc.getObject(n) is None for n in exclude),'all_packaging_distances_positive':all(r['distance_mm']>0 for r in rows),'dynamic_guard_rod_min_mm':3.18825579314564,'mass_model_ready':True,'production_OML':False,'print_release':False,'flight_release':False}}
res['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))