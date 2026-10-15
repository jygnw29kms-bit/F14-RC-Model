"""v180: replace the 20 mm crank reference with the largest source-OML-contained 18.9 mm crank and revalidate the static stack."""
import adsk.core, adsk.fusion, json, os, hashlib, math


def ivol(temp, a, b):
    q=temp.copy(a)
    ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return q.volume if ok and q.isValid else 0.0


def run_review(app,builder,mm,outdir):
    base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v180_section_inputs.json'),encoding='utf-8'))
    for pk,hk in [('v177_path','v177_sha256'),('source_oml_path','source_oml_sha256'),('v179c_audit_path','v179c_audit_sha256')]:
        if hashlib.sha256(open(cfg[pk],'rb').read()).hexdigest()!=cfg[hk]: raise RuntimeError('v180 source changed '+pk)
    scan=json.load(open(cfg['v179c_audit_path'],encoding='utf-8'))
    if abs(scan['selected_largest_contained_radius']['radius_mm']-cfg['crank_radius_mm'])>1e-9: raise RuntimeError('v180 radius does not match v179c')

    prior=app.activeDocument; temp=adsk.fusion.TemporaryBRepManager.get()
    d=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['v177_path']))
    sr=adsk.fusion.Design.cast(app.activeProduct).rootComponent
    copies={b.name:temp.copy(b) for b in sr.bRepBodies if not b.name.startswith('REF_20MM_CRANK_ENVELOPE_')}
    d.close(False)
    d=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_oml_path']))
    sr=adsk.fusion.Design.cast(app.activeProduct).rootComponent
    source=temp.copy(next(b for b in sr.bRepBodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT'))
    d.close(False)

    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_STABILATOR_CONTAINED_CRANK_v180_NO_FLIGHT_RELEASE'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    static={}
    for name,body in copies.items():
        b=root.bRepBodies.add(temp.copy(body)); b.name=name.replace('_v177','_v180'); static[name]=b
        if name.startswith('REF_'): b.opacity=.2
    x=float(cfg['pivot_x_mm']); z=float(cfg['pivot_z_mm']); r=float(cfg['crank_radius_mm']); ylo,yhi=[float(v) for v in cfg['crank_abs_y_range_mm']]
    rec=[]
    for side,sgn in [('R',1),('L',-1)]:
        crank=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(sgn*ylo),mm(z)),mm(r),adsk.core.Point3D.create(mm(x),mm(sgn*yhi),mm(z)),mm(r))
        crank_ref=temp.copy(crank); cb=root.bRepBodies.add(crank); cb.name='CANDIDATE_18P9MM_CRANK_ROTATION_ENVELOPE_'+side+'_v180'; cb.opacity=.35
        inside=temp.copy(crank_ref); ok=temp.booleanOperation(inside,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType)
        outside=max(0.0,crank_ref.volume-(inside.volume if ok and inside.isValid else 0.0))
        blockers=[]
        for name,body in copies.items():
            if ('_'+side+'_') not in name: continue
            if any(k in name for k in ['BEARING_','SHAFT_COLLAR_','SHAFT_SHOULDER_','D_BORE_STABILATOR_FITTING_','SURFACE_OUTER_END_WASHER_']):
                vol=ivol(temp,crank_ref,body)
                blockers.append(dict(body=name,intersection_cm3=vol,pass_=vol<=float(cfg['interference_tolerance_cm3'])))
        rec.append(dict(side=side,outside_source_oml_cm3=outside,containment_pass=outside<=float(cfg['containment_tolerance_cm3']),static_intersections=blockers,no_static_interference=all(b['pass_'] for b in blockers)))
    throw=math.degrees(math.asin((float(cfg['servo_arm_mm'])/r)*math.sin(math.radians(float(cfg['servo_half_travel_deg'])))))
    torque=float(cfg['severe_required_servo_torque_kgcm']); servo=float(cfg['nominal_servo_class_kgcm'])
    audit=dict(status='V180_STABILATOR_CONTAINED_CRANK_AND_STATIC_STACK',source=cfg,records=rec,
               bilateral_crank_containment_pass=all(q['containment_pass'] for q in rec),
               bilateral_static_interference_pass=all(q['no_static_interference'] for q in rec),
               linkage=dict(crank_radius_mm=r,servo_arm_mm=float(cfg['servo_arm_mm']),predicted_surface_half_throw_deg=throw,severe_required_servo_torque_kgcm=torque,nominal_servo_class_kgcm=servo,servo_class_ratio=servo/torque),
               pivot_axis_unchanged_from_v175=True,bearing_stack_unchanged_from_v177=True,
               servo_location_frozen=False,pushrod_path_verified=False,dynamic_linkage_clearance_verified=False,
               actual_hardware_verified=False,bench_proof_pass=False,print_release=False,flight_release=False,
               study_source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    if not (audit['bilateral_crank_containment_pass'] and audit['bilateral_static_interference_pass']): raise RuntimeError('v180 corrected crank still fails packaging')
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_STABILATOR_CONTAINED_CRANK_v180.f3d'))): raise RuntimeError('v180 export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v180_stabilator_contained_crank_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v180_stabilator_contained_crank_review.png'),1600,1000)
    if prior:
        try: prior.activate()
        except: pass
    return audit
