"""v179c: find the largest stabilator crank radius that fits the v175 axis inside the source OML."""
import adsk.core, adsk.fusion, json, os, hashlib, math


def run_review(app, builder, mm, outdir):
    oml_path='C:/Users/dezen/Desktop/F14-RC-Model/analysis/independent_reviews/allowanced_inlet_20261015/F14_ALLOWANCED_INLET_WALL_CANDIDATE.f3d'
    oml_sha='cea5f21ed9551991f3b7306ea8ce3df92f02e20bda3bc5f3b5ef61c94f4baf93'
    if hashlib.sha256(open(oml_path,'rb').read()).hexdigest()!=oml_sha:
        raise RuntimeError('v179c OML source changed')
    prior=app.activeDocument
    temp=adsk.fusion.TemporaryBRepManager.get()
    d=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(oml_path))
    r=adsk.fusion.Design.cast(app.activeProduct).rootComponent
    source=temp.copy(next(b for b in r.bRepBodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT'))
    d.close(False)
    x=736.0078983334656; y0=76.0; y1=80.0; z=0.0; tol=1e-5
    radii=[20.0-0.1*i for i in range(31)]
    rows=[]
    for radius in radii:
        sides=[]
        for side,sgn in [('R',1),('L',-1)]:
            body=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(sgn*y0),mm(z)),mm(radius),adsk.core.Point3D.create(mm(x),mm(sgn*y1),mm(z)),mm(radius))
            total=body.volume; inside=temp.copy(body)
            ok=temp.booleanOperation(inside,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType)
            iv=inside.volume if ok and inside.isValid else 0.0
            outside=max(0.0,total-iv)
            sides.append(dict(side=side,outside_source_oml_cm3=outside,pass_=outside<=tol))
        rows.append(dict(radius_mm=radius,diameter_mm=2*radius,sides=sides,bilateral_pass=all(s['pass_'] for s in sides)))
    passing=[r for r in rows if r['bilateral_pass']]
    selected=passing[0] if passing else None
    if selected is None: raise RuntimeError('No passing crank radius down to 17 mm')
    # Existing v148/v168 relations: torque scales inversely with crank radius for fixed servo arm.
    old_radius=20.0; old_throw=17.843481128270785; old_torque=7.809958462640951; servo_arm=8.0; servo_half=math.radians(50.0)
    rr=selected['radius_mm']
    throw=math.degrees(math.asin((servo_arm/rr)*math.sin(servo_half)))
    severe_torque=old_torque*(old_radius/rr)
    audit=dict(status='V179C_MAXIMUM_CONTAINED_STABILATOR_CRANK_RADIUS',source_oml_path=oml_path,source_oml_sha256=oml_sha,
               fixed_axis=dict(x_mm=x,abs_y_range_mm=[y0,y1],z_mm=z),scan_step_mm=0.1,rows=rows,selected_largest_contained_radius=selected,
               linkage_effect=dict(servo_arm_mm=servo_arm,servo_half_travel_deg=50.0,predicted_surface_half_throw_deg=throw,severe_required_servo_torque_kgcm=severe_torque,ratio_to_14kgcm_class=14.0/severe_torque),
               actual_hardware_verified=False,bench_verified=False,print_release=False,flight_release=False,study_source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    os.makedirs(outdir,exist_ok=True)
    json.dump(audit,open(os.path.join(outdir,'F14_v179c_stabilator_crank_radius_scan.json'),'w',encoding='utf-8'),indent=2)
    if prior:
        try: prior.activate()
        except: pass
    return audit
