import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v239_STABILATOR_CRANK_M3_PIN.FCStd'; out=R/'migration/freecad/F14_v240_STABILATOR_PUSHROD_CORRIDOR.FCStd'; audp=R/'migration/freecad/freecad_v240_stabilator_pushrod_corridor_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v240_STABILATOR_PUSHROD_CORRIDOR')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fuse=doc.getObject('FUSELAGE_CURRENT').Shape; rows=[]
# Conservative reserve begins just outside servo service y-face and spans all possible crank pin z motion plus body/spline uncertainty.
for lab,sgn in [('R',1),('L',-1)]:
 x0=686.5; x1=753.0; z0=-10; z1=10; ya=75.8; yb=80.2; y0=ya if sgn>0 else -yb
 corridor=Part.makeBox(x1-x0,yb-ya,z1-z0,App.Vector(x0,y0,z0)); o=doc.addObject('PartDesign::Feature','V240_PUSHROD_RESERVE_'+lab); o.Shape=corridor; o.Label='v240 stabilator pushrod reserved corridor '+lab+' / NOT ROD GEOMETRY'
 inside=corridor.common(fuse).Volume/corridor.Volume; checks={}
 for n in ['STAB_HOUSING_'+lab+'_1','STAB_HOUSING_'+lab+'_2','V235_D_ROOT_FITTING_'+lab,'V234_BEARING_INBOARD_COLLAR_'+lab,'V234_BEARING_OUTER_SHOULDER_'+lab,'INLET_EDF_'+lab,'V229_ESC_SERVICE_'+lab,'V228_TAIL_UBEC10A_HV','V227_HOBBYWING_UBEC10A_HV','V221_CASSETTE_'+lab]:
  q=doc.getObject(n)
  if q: checks[n]=corridor.distToShape(q.Shape)[0]
 rows.append({'side':lab,'inside_fraction':inside,'distances_mm':checks})
doc.recompute();doc.saveAs(str(out))
aud={'status':'V240_STABILATOR_PUSHROD_CORRIDOR','reserve_bounds':{'x_mm':[686.5,753.0],'abs_y_mm':[75.8,80.2],'z_mm':[-10,10]},'basis':{'servo_service_outer_abs_y_mm':75.75,'crank_abs_y_mm':[76,80],'crank_pin_radius_mm':15.0,'predicted_surface_half_throw_deg':18.92,'servo_spline_offset_still_unknown':True},'rows':rows,'gates':{'corridor_fuselage_containment_ge_99pct':all(r['inside_fraction']>=0.99 for r in rows),'corridor_clear_of_non_actuator_hardware':all(v>0 for r in rows for v in r['distances_mm'].values()),'actual_pushrod_centerline_frozen':False,'servo_spline_measured':False,'ball_link_selected':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))