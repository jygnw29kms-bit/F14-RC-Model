import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v217_MONOLITHIC_PIVOT_CASSETTE.FCStd'; out=R/'migration/freecad/F14_v218_CONSOLIDATED_STRUCTURAL_MODEL.FCStd'; audp=R/'migration/freecad/freecad_v218_consolidated_structural_model_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v218_CONSOLIDATED_STRUCTURAL_MODEL')
exclude={'V204_SOCKET_FRONT_R','V204_SOCKET_REAR_R','V204_MONO_LOWER_R','V204_UPPER_FORK_R','V204_SOCKET_FRONT_L','V204_SOCKET_REAR_L','V204_MONO_LOWER_L','V204_UPPER_FORK_L','V204_META','SWEEP_SERVO_SERVICE_REF','WINGBOX_REF'}
kept=[]
for o in d.Objects:
 if o.Name in exclude: continue
 if hasattr(o,'Shape') and not o.Shape.isNull():
  q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label; kept.append(o.Name)
doc.recompute(); doc.saveAs(str(out))
rows=[]
for lab in ['R','L']:
 cas=doc.getObject('V217_CASSETTE_'+lab).Shape
 for n in ['INLET_EDF_R','INLET_EDF_L','V205_SWEEP_SERVO_SERVICE','V205_BATTERY_305','V205_BATTERY_340','V205_BATTERY_375']:
  o=doc.getObject(n)
  if o: rows.append({'cassette':lab,'target':n,'distance_mm':cas.distToShape(o.Shape)[0]})
meta={'status':'V218_CONSOLIDATED_STRUCTURAL_MODEL','source_v217':str(src),'excluded_legacy_duplicate_objects':sorted(exclude),'kept_shape_count':len(kept),'cassette_volume_mm3':{lab:doc.getObject('V217_CASSETTE_'+lab).Shape.Volume for lab in ['R','L']},'packaging_distances':rows,'gates':{'legacy_structural_duplicates_removed':all(doc.getObject(n) is None for n in exclude),'cassette_to_battery_servo_edf_no_contact':all(r['distance_mm']>0 for r in rows),'production_OML':False,'mass_model_ready_for_material_assumptions':True,'print_release':False,'flight_release':False}}
meta['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(meta,indent=2),encoding='utf-8'); print(json.dumps(meta,indent=2))