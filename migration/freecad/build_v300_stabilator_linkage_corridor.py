import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v299_TAIL_SERVO_RELOCATION_CANDIDATE.FCStd'
out=R/'migration/freecad/F14_v300_STRAIGHT_STABILATOR_PUSHROD.FCStd'
audp=R/'migration/freecad/freecad_v300_straight_stabilator_pushrod_audit.json'
v241=json.loads((R/'migration/freecad/freecad_v241_light_stabilator_crank_audit.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v300_STRAIGHT_STABILATOR_PUSHROD')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
start_x=723.5; start_y=20.0; start_z=12.0
end_x=751.0078983334656; end_y=76.0; end_z=0.0
rod_d=3.0; service_d=4.0
force_N=float(v241['load_screen']['pushrod_force_2x_N'])
E_MPa=50000.0  # conservative lower-screen value for pultruded carbon rod; purchased stock still needs verification

def cyl_between(a,b,r):
    v=b.sub(a); return Part.makeCylinder(r,v.Length,a,v.normalize())
rows=[]
for side,sgn in [('R',1),('L',-1)]:
    p0=App.Vector(start_x,sgn*start_y,start_z); p1=App.Vector(end_x,sgn*end_y,end_z)
    rod=cyl_between(p0,p1,rod_d/2.0); svc=cyl_between(p0,p1,service_d/2.0)
    ro=doc.addObject('PartDesign::Feature','V300_CF_PUSHROD_'+side); ro.Shape=rod; ro.Label='v300 3mm CF stabilator pushrod '+side
    so=doc.addObject('PartDesign::Feature','V300_PUSHROD_SERVICE_'+side); so.Shape=svc; so.Label='v300 4mm static pushrod service corridor '+side
    edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape
    fit=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    crank=doc.getObject('V241_LIGHT_D_CRANK_'+side).Shape
    L=p0.distanceToPoint(p1)
    I=math.pi*rod_d**4/64.0
    pcr=math.pi**2*E_MPa*I/(L**2)
    rows.append({'side':side,'horn_tip_target_mm':[p0.x,p0.y,p0.z],'crank_pin_target_mm':[p1.x,p1.y,p1.z],'pushrod_length_mm':L,
                 'rod_OML_containment':rod.common(oml).Volume/rod.Volume,'service_OML_containment':svc.common(oml).Volume/svc.Volume,
                 'rod_EDF_clearance_mm':rod.distToShape(edf)[0],'service_EDF_clearance_mm':svc.distToShape(edf)[0],
                 'rod_EDF_intersection_mm3':rod.common(edf).Volume,'service_EDF_intersection_mm3':svc.common(edf).Volume,
                 'service_root_fitting_clearance_mm':svc.distToShape(fit)[0],'rod_crank_intersection_mm3':rod.common(crank).Volume,
                 'buckling':{'rod_diameter_mm':rod_d,'screen_E_MPa':E_MPa,'second_moment_mm4':I,'pinned_pinned_Pcr_N':pcr,'design_pushrod_force_N':force_N,'buckling_SF':pcr/force_N}})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V300_STRAIGHT_STABILATOR_PUSHROD_CANDIDATE','source_model':src.name,
     'architecture':{'direct_pushrod':True,'intermediate_bellcrank_required':False,'rod_diameter_mm':rod_d,'static_service_corridor_diameter_mm':service_d,
                     'servo_horn_tip_target_abs_y_mm':start_y,'servo_horn_tip_target_x_mm':start_x,'servo_horn_tip_target_z_mm':start_z,
                     'exact_servo_spline_offset_measured':False,'exact_horn_geometry_open':True,'M3_or_ball_link_joint_selection_open':True},
     'rows':rows,
     'gates':{'bilateral_rod_OML_containment_ge_0p999':all(r['rod_OML_containment']>=0.999 for r in rows),
              'bilateral_service_OML_containment_ge_0p999':all(r['service_OML_containment']>=0.999 for r in rows),
              'zero_EDF_intersection':all(r['rod_EDF_intersection_mm3']<1e-6 and r['service_EDF_intersection_mm3']<1e-6 for r in rows),
              'service_EDF_clearance_ge_1p5mm':all(r['service_EDF_clearance_mm']>=1.5 for r in rows),
              'service_root_fitting_clearance_ge_5mm':all(r['service_root_fitting_clearance_mm']>=5.0 for r in rows),
              'conservative_buckling_SF_ge_5':all(r['buckling']['buckling_SF']>=5.0 for r in rows),
              'exact_servo_spline_offset_measured':False,'carbon_stock_E_verified':False,'joint_hardware_selected':False,'dynamic_throw_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
