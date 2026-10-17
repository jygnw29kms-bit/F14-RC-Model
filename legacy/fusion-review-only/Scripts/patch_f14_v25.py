from pathlib import Path
files=[
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''

def build_segmented_clearance_pockets_review_v25():
    """Use local intersection-bound pockets instead of broad v23 aggregate keepout boxes."""
    build_registered_clearance_keepout_review_v23()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v25_SEGMENTED_CLEARANCE_POCKETS_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    v23_path=os.path.join(config['export_dir'],'registered_keepout_v23','F14_v23_registered_keepout_audit.json')
    with open(v23_path,encoding='utf-8') as stream: v23=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pivot_wl_in=s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz
    pz=pivot_wl_in*factor
    fus=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_OML_WL_REGISTERED_v22')
    before=fus.volume
    margin=2.0
    tools=adsk.core.ObjectCollection.create(); pocket_defs=[]
    idx=0
    for rec in v23['intersection_records']:
        if not rec.get('positive_overlap') or 'intersection_bounds_mm' not in rec: continue
        b=rec['intersection_bounds_mm']
        x0,x1=b['x'][0]-margin,b['x'][1]+margin
        y0,y1=b['y'][0]-margin,b['y'][1]+margin
        z0,z1=b['z'][0]-margin,b['z'][1]+margin
        idx+=1
        name='ENG_LOCAL_CLEARANCE_%02d_%s_%02d_%s_v25'%(idx,rec['side'],rec['sweep_deg'],rec['kind'])
        body=extrude_poly(root,name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1-z0)
        body.opacity=0.2; tools.add(body)
        pocket_defs.append(dict(name=name,source_record=rec,bounds_mm=dict(x=[x0,x1],y=[y0,y1],z=[z0,z1])))
    ci=root.features.combineFeatures.createInput(fus,tools)
    ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation
    ci.isKeepToolBodies=True
    root.features.combineFeatures.add(ci)
    fus.name='UPC_FUSELAGE_SEGMENTED_CLEARANCE_CUT_v25'
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
                if not temporary.transform(moving,rot): raise RuntimeError('v25 moving body transform failed')
                fixed=temporary.copy(fus)
                ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType)
                iv=moving.volume if ok and moving.isValid else 0.0
                records.append(dict(sweep_deg=sweep,side=label,kind=kind,intersection_volume_cm3=iv,positive_overlap=iv>1e-4))
    residual=[r for r in records if r['positive_overlap']]
    v24_removed=None
    v24_path=os.path.join(config['export_dir'],'engineering_clearance_v24','F14_v24_engineering_clearance_audit.json')
    if os.path.exists(v24_path):
        with open(v24_path,encoding='utf-8') as stream: v24_removed=json.load(stream).get('removed_volume_cm3')
    removed=before-after
    audit=dict(status='SEGMENTED_LOCAL_CLEARANCE_POCKETS_REVIEW',registration_inherited_from='v22',intersection_source='v23',
      pocket_margin_mm=margin,pocket_count=len(pocket_defs),pockets=pocket_defs,
      fuselage_volume_before_cm3=before,fuselage_volume_after_cm3=after,removed_volume_cm3=removed,
      v24_broad_keepout_removed_volume_cm3=v24_removed,
      volume_saved_vs_v24_cm3=(v24_removed-removed if v24_removed is not None else None),
      residual_collision_records=records,residual_positive_overlaps=residual,
      sampled_sweeps_collision_free=(len(residual)==0),
      note='Local rectangular pockets bound each exact sampled intersection plus 2 mm margin. This is an engineering packaging optimization, not final scale glove surface.',
      clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    outdir=os.path.join(config['export_dir'],'segmented_clearance_v25'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v25_SEGMENTED_CLEARANCE_POCKETS_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v25 export failed')
    with open(os.path.join(outdir,'F14_v25_segmented_clearance_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v25_segmented_clearance_review.png'),1600,1000)
    return audit

'''
for path in files:
    s=path.read_text(encoding='utf-8')
    insert=s.index('def build_project_revision():')
    if 'def build_segmented_clearance_pockets_review_v25()' not in s:
        s=s[:insert]+fn+s[insert:]
    s=s.replace('return build_engineering_clearance_cut_review_v24()','return build_segmented_clearance_pockets_review_v25()',1)
    path.write_text(s,encoding='utf-8')
    print('patched',path)
