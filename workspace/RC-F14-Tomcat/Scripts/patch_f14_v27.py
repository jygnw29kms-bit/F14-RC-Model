from pathlib import Path
files=[
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''

def build_vertical_datum_sensitivity_review_v27():
    """Stress v25 clearance against +/-1 mm common-WL registration uncertainty."""
    build_segmented_clearance_pockets_review_v25()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v27_VERTICAL_DATUM_SENSITIVITY_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pivot_wl_in=s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz
    pz=pivot_wl_in*factor
    # Sensitivity of linear regression choice across retained Grumman stations.
    fit_values=[]
    xs=[float(s['wbl_in']) for s in data['sections']]
    zs=[float(s['reference_vertical_wl_in']) for s in data['sections']]
    for n in [2,3,4,5,8]:
        xm=sum(xs[:n])/n; zm=sum(zs[:n])/n
        slope=sum((x-xm)*(z-zm) for x,z in zip(xs[:n],zs[:n]))/sum((x-xm)**2 for x in xs[:n])
        wl=zm+slope*(pivot['derived_full_scale_pivot_bl_in']-xm)
        fit_values.append(dict(first_n=n,pivot_wl_fullscale_in=wl,pivot_wl_model_mm=wl*factor))
    fit_spread=max(v['pivot_wl_model_mm'] for v in fit_values)-min(v['pivot_wl_model_mm'] for v in fit_values)
    fus=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_SEGMENTED_CLEARANCE_CUT_v25')
    temporary=adsk.fusion.TemporaryBRepManager.get()
    shifts=[-1.0,-0.5,0.0,0.5,1.0]
    sweeps=list(range(20,69,4))
    records=[]
    for zshift in shifts:
        fuscopy=temporary.copy(fus)
        tm=adsk.core.Matrix3D.create(); tm.translation=adsk.core.Vector3D.create(0,0,mm(zshift))
        if not temporary.transform(fuscopy,tm): raise RuntimeError('v27 fuselage datum shift failed')
        for sweep in sweeps:
            for sign,label in [(1,'R'),(-1,'L')]:
                angle=-sign*math.radians(sweep-20.0)
                rot=adsk.core.Matrix3D.create(); rot.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
                wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
                lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
                for body,kind in [(wing,'outer_wing'),(lug,'root_lug')]:
                    moving=temporary.copy(body)
                    if not temporary.transform(moving,rot): raise RuntimeError('v27 moving body transform failed')
                    fixed=temporary.copy(fuscopy)
                    ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType)
                    iv=moving.volume if ok and moving.isValid else 0.0
                    records.append(dict(z_shift_mm=zshift,sweep_deg=sweep,side=label,kind=kind,intersection_volume_cm3=iv,positive_overlap=iv>1e-4))
    residual=[r for r in records if r['positive_overlap']]
    audit=dict(status='VERTICAL_DATUM_REGISTRATION_SENSITIVITY_REVIEW',source_revision='v25',
      pivot_waterline_original_aircraft_verified=False,
      two_station_engineering_pivot_wl_model_mm=pz,linear_fit_variants=fit_values,
      linear_fit_spread_model_mm=fit_spread,tested_vertical_shifts_mm=shifts,
      tested_sweep_angles_deg=sweeps,sweep_step_deg=4,
      residual_collision_records=records,residual_positive_overlaps=residual,
      max_residual_intersection_volume_cm3=max((r['intersection_volume_cm3'] for r in records),default=0.0),
      clearance_robust_within_plusminus_1mm=(len(residual)==0),
      note='The Grumman/NASA wing vertical references are airplane-coordinate values, but no explicit pivot WL has been found. This test deliberately exceeds the observed 0.546 mm model-scale extrapolation spread with +/-1 mm datum shifts.',
      source_registration_release=False,clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    outdir=os.path.join(config['export_dir'],'datum_sensitivity_v27'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v27_VERTICAL_DATUM_SENSITIVITY_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v27 export failed')
    with open(os.path.join(outdir,'F14_v27_vertical_datum_sensitivity_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v27_vertical_datum_sensitivity_review.png'),1600,1000)
    return audit

'''
for path in files:
    s=path.read_text(encoding='utf-8')
    insert=s.index('def build_project_revision():')
    if 'def build_vertical_datum_sensitivity_review_v27()' not in s:
        s=s[:insert]+fn+s[insert:]
    s=s.replace('return build_dense_sweep_clearance_review_v26()','return build_vertical_datum_sensitivity_review_v27()',1)
    path.write_text(s,encoding='utf-8')
    print('patched',path)
