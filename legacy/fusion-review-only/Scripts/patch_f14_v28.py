from pathlib import Path
files=[Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''

def build_robust_datum_clearance_review_v28():
    """Refine only the 68-deg outer-wing pocket in Z, then test dense sweep at +/-1 mm WL uncertainty."""
    build_registered_clearance_keepout_review_v23()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v28_ROBUST_DATUM_CLEARANCE_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    with open(os.path.join(config['export_dir'],'registered_keepout_v23','F14_v23_registered_keepout_audit.json'),encoding='utf-8') as stream: v23=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pz=(s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz)*factor
    fus=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_OML_WL_REGISTERED_v22')
    before=fus.volume
    tools=adsk.core.ObjectCollection.create(); pocket_defs=[]; idx=0
    for rec in v23['intersection_records']:
        if not rec.get('positive_overlap') or 'intersection_bounds_mm' not in rec: continue
        b=rec['intersection_bounds_mm']; mxy=2.0
        mz=3.0 if rec['sweep_deg']==68 and rec['kind']=='outer_wing' else 2.0
        x0,x1=b['x'][0]-mxy,b['x'][1]+mxy; y0,y1=b['y'][0]-mxy,b['y'][1]+mxy; z0,z1=b['z'][0]-mz,b['z'][1]+mz
        idx+=1
        name='ENG_ROBUST_CLEARANCE_%02d_%s_%02d_%s_v28'%(idx,rec['side'],rec['sweep_deg'],rec['kind'])
        body=extrude_poly(root,name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1-z0); body.opacity=0.2; tools.add(body)
        pocket_defs.append(dict(name=name,source_record=rec,margin_xy_mm=mxy,margin_z_mm=mz,bounds_mm=dict(x=[x0,x1],y=[y0,y1],z=[z0,z1])))
    ci=root.features.combineFeatures.createInput(fus,tools); ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation; ci.isKeepToolBodies=True; root.features.combineFeatures.add(ci)
    fus.name='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v28'; after=fus.volume
    temporary=adsk.fusion.TemporaryBRepManager.get(); shifts=[-1.0,-0.5,0.0,0.5,1.0]; sweeps=list(range(20,69,2)); records=[]
    for zshift in shifts:
        fuscopy=temporary.copy(fus); tm=adsk.core.Matrix3D.create(); tm.translation=adsk.core.Vector3D.create(0,0,mm(zshift)); temporary.transform(fuscopy,tm)
        for sweep in sweeps:
            for sign,label in [(1,'R'),(-1,'L')]:
                angle=-sign*math.radians(sweep-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
                wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_')); lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
                for body,kind in [(wing,'outer_wing'),(lug,'root_lug')]:
                    moving=temporary.copy(body); temporary.transform(moving,rot); fixed=temporary.copy(fuscopy)
                    ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=moving.volume if ok and moving.isValid else 0.0
                    records.append(dict(z_shift_mm=zshift,sweep_deg=sweep,side=label,kind=kind,intersection_volume_cm3=iv,positive_overlap=iv>1e-4))
    residual=[r for r in records if r['positive_overlap']]
    audit=dict(status='ROBUST_DENSE_DATUM_CLEARANCE_REVIEW',source_revision='v23',targeted_extra_z_margin_mm=1.0,
      tested_vertical_shifts_mm=shifts,tested_sweep_angles_deg=sweeps,sweep_step_deg=2,pocket_count=len(pocket_defs),pockets=pocket_defs,
      fuselage_volume_before_cm3=before,fuselage_volume_after_cm3=after,removed_volume_cm3=before-after,
      residual_positive_overlaps=residual,max_residual_intersection_volume_cm3=max((r['intersection_volume_cm3'] for r in records),default=0.0),
      robust_dense_clearance_pass=(len(residual)==0),pivot_waterline_original_aircraft_verified=False,source_registration_release=False,
      clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    outdir=os.path.join(config['export_dir'],'robust_clearance_v28'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v28_ROBUST_DATUM_CLEARANCE_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v28 export failed')
    with open(os.path.join(outdir,'F14_v28_robust_datum_clearance_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v28_robust_datum_clearance_review.png'),1600,1000)
    return audit

'''
for path in files:
    s=path.read_text(encoding='utf-8')
    insert=s.index('def build_project_revision():')
    if 'def build_robust_datum_clearance_review_v28()' not in s: s=s[:insert]+fn+s[insert:]
    s=s.replace('return build_vertical_datum_sensitivity_review_v27()','return build_robust_datum_clearance_review_v28()',1)
    path.write_text(s,encoding='utf-8'); print('patched',path)
