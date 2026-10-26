import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v229_TWIN_ESC_CURRENT.FCStd'; out=R/'migration/freecad/F14_v230_EDF_HARDWARE_ACCEPTANCE_CORRIDOR.FCStd'; audp=R/'migration/freecad/freecad_v230_edf_hardware_acceptance_corridor_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v230_EDF_HARDWARE_ACCEPTANCE_CORRIDOR')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fuse=doc.getObject('FUSELAGE_CURRENT').Shape; xface=658.0; length=73.5; free_d=53.6; max_shroud=53.2; carrier_od=55.2; yabs=66.28458486059378; z=-10.508688347971937; rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 axis=App.Vector(xface,sgn*yabs,z); free=Part.makeCylinder(free_d/2,length,axis,App.Vector(1,0,0)); fo=doc.addObject('PartDesign::Feature','V230_EDF_FREE_CORRIDOR_'+lab); fo.Shape=free; fo.Label='v230 EDF free hardware corridor '+lab+' / ID53.6 equivalent / NOT EDF BODY'
 mount=Part.makeCylinder(carrier_od/2,8.0,App.Vector(650,sgn*yabs,z),App.Vector(1,0,0)); mo=doc.addObject('PartDesign::Feature','V230_EDF_MOUNT_OD_'+lab); mo.Shape=mount; mo.Label='v230 EDF carrier OD55.2 mount band '+lab
 inside=free.common(fuse).Volume/free.Volume; mins={'fuselage_inside_fraction':inside}
 for n in ['V229_ESC_SERVICE_'+lab,'V221_CASSETTE_'+lab,'V205_BATTERY_375','V225_SERVO_SERVICE']:
  o=doc.getObject(n)
  if o: mins[n+'_distance_mm']=free.distToShape(o.Shape)[0]
 rows.append({'side':lab,**mins})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V230_EDF_HARDWARE_ACCEPTANCE_CORRIDOR','basis':{'fan_face_x_mm':xface,'body_length_screen_mm':length,'max_shroud_OD_without_changing_carrier_mm':max_shroud,'required_free_ID_mm':free_d,'radial_install_clearance_mm':0.2,'carrier_OD_mm':carrier_od,'axis_abs_y_mm':yabs,'axis_z_mm':z,'axis_absolute_Z_verified':False},'rows':rows,'gates':{'53p6_free_corridor_contained_ge_99p5pct':all(r['fuselage_inside_fraction']>=0.995 for r in rows),'corridor_no_contact_with_current_hardware':all(v>0 for r in rows for k,v in r.items() if k.endswith('_distance_mm')),'XFly_actual_shroud_OD_verified':False,'axis_absolute_Z_verified':False,'actual_EDF_measured':False,'mount_regenerated_to_measured_EDF':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))