from pathlib import Path
files=[
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''

def build_engineering_clearance_cut_review_v24():
    """Cut conservative v23 keepout envelopes from registered fuselage and re-check residual sweep collisions."""
    build_registered_clearance_keepout_review_v23()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v24_ENGINEERING_CLEARANCE_CUT_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pivot_wl_in=s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz
    pz=pivot_wl_in*factor
    fus=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_OML_WL_REGISTERED_v22')
    before=fus.volume
    tools=adsk.core.ObjectCollection.create()
    for label in ['R','L']:
        tools.add(next(b for b in root.bRepBodies if b.name=='ENG_SWEEP_KEEPOUT_'+label+'_v23_NOT_CUT_GEOMETRY'))
    ci=root.features.combineFeatures.createInput(fus,tools)
    ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation
    ci.isKeepToolBodies=True
    root.features.combineFeatures.add(ci)
    fus.name='UPC_FUSELAGE_ENGINEERING_CLEARANCE_CUT_v24'
    after=fus.volume
    temporary=adsk.fusion.TemporaryBRepManager.get()
    records=[]
    for sweep in [20,30,40,50,60,68]:
        for sign,label in [(1,'R'),(-1,'L')]:
            angle=-sign*math.radians(sweep-20.0)
            rot=adsk.core.Matrix3D.create(); rot.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
            lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
            for body,kind in [(wing,'outer_wing'),(lug,'root_lug')]:
                moving=temporary.copy(body)
                if not temporary.transform(moving,rot): raise RuntimeError('v24 moving body transform failed')
                fixed=temporary.copy(fus)
                ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType)
                iv=moving.volume if ok and moving.isValid else 0.0
                records.append(dict(sweep_deg=sweep,side=label,kind=kind,intersection_volume_cm3=iv,positive_overlap=iv>1e-4))
    residual=[r for r in records if r['positive_overlap']]
    audit=dict(status='ENGINEERING_CLEARANCE_CUT_RESIDUAL_COLLISION_REVIEW',registration_inherited_from='v22',keepout_inherited_from='v23',
      pivot_waterline_original_aircraft_verified=False,fuselage_volume_before_cm3=before,fuselage_volume_after_cm3=after,
      removed_volume_cm3=before-after,residual_collision_records=records,residual_positive_overlaps=residual,
      sampled_sweeps_collision_free=(len(residual)==0),
      note='Conservative v23 keepout boxes cut from provisional registered UPC fuselage. This validates packaging logic only; final glove surface and source registration remain unreleased.',
      clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'engineering_clearance_v24'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v24_ENGINEERING_CLEARANCE_CUT_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v24 export failed')
    with open(os.path.join(outdir,'F14_v24_engineering_clearance_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v24_engineering_clearance_review.png'),1600,1000)
    return audit

'''
for path in files:
    s=path.read_text(encoding='utf-8')
    insert=s.index('def build_project_revision():')
    if 'def build_engineering_clearance_cut_review_v24()' not in s:
        s=s[:insert]+fn+s[insert:]
    s=s.replace('return build_registered_clearance_keepout_review_v23()','return build_engineering_clearance_cut_review_v24()',1)
    path.write_text(s,encoding='utf-8')
    print('patched',path)
