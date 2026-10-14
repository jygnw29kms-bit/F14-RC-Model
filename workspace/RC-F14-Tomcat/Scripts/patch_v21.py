from pathlib import Path
paths=[Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''
def build_fuselage_sweep_collision_review_v21():
    """Cross-source UPC fuselage vs NASA/Grumman moving wing BRep intersection review."""
    build_root_lug_review_v19()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v21_UPC_FUSELAGE_SWEEP_COLLISION_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    full_length_from_scale_mm=748.5*factor
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pz=(s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz)*factor
    fus=build_upc_fuselage_oml(root)
    fus.name='UPC_FUSELAGE_OML_CROSS_SOURCE_v21'
    temporary=adsk.fusion.TemporaryBRepManager.get()
    results=[]
    for sweep in [20,30,40,50,60,68]:
        sides=[]
        for sign,label in [(1,'R'),(-1,'L')]:
            wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
            lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
            angle=-sign*math.radians(sweep-20.0)
            tr=adsk.core.Matrix3D.create(); tr.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            checks=[]
            for body,kind in [(wing,'outer_wing_to_fuselage'),(lug,'root_lug_to_fuselage')]:
                moving=temporary.copy(body)
                if not temporary.transform(moving,tr): raise RuntimeError('v21 transform failed')
                fixed=temporary.copy(fus)
                ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType)
                iv=moving.volume if ok and moving.isValid else 0.0
                checks.append(dict(kind=kind,intersection_succeeded=bool(ok),intersection_volume_cm3=iv,positive_overlap=iv>1e-4))
            sides.append(dict(side=label,checks=checks))
        results.append(dict(sweep_deg=sweep,sides=sides))
    bb=fus.boundingBox
    audit=dict(status='CROSS_SOURCE_FUSELAGE_SWEEP_COLLISION_REVIEW',
      fuselage_source='UPC Figure 5.3 extracted fuselage guide stations; section shaping uses documented UPC examples',
      wing_source='NASA/Grumman basic outer-wing source dataset',
      source_registration_frozen=False,
      registration_note='Longitudinal/scale consistency is close, but final common aircraft datum registration remains required before clearance release.',
      wing_scale_implied_full_length_mm=full_length_from_scale_mm,upc_fuselage_length_mm=879.0,
      length_scale_difference_mm=879.0-full_length_from_scale_mm,
      fuselage_bounds_mm={a:[getattr(bb.minPoint,a)*10,getattr(bb.maxPoint,a)*10] for a in ['x','y','z']},
      pivot_model_mm=dict(x=px,y=py,z=pz),sweep_collision_results=results,
      body_glove_collision_checked=True,clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'fuselage_collision_v21'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v21_UPC_FUSELAGE_SWEEP_COLLISION_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v21 export failed')
    with open(os.path.join(outdir,'F14_v21_fuselage_sweep_collision_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v21_fuselage_sweep_collision_review.png'),1600,1000)
    return audit

'''
for p in paths:
 s=p.read_text(encoding='utf-8')
 marker='def build_project_revision():'
 i=s.index(marker)
 s=s[:i]+fn+s[i:]
 old='return build_sweep_envelope_review_v20()'
 s=s.replace(old,'return build_fuselage_sweep_collision_review_v21()',1)
 p.write_text(s,encoding='utf-8')
 print('patched',p)
