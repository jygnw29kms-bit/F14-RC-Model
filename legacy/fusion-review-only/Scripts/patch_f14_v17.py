from pathlib import Path
p=Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py')
text=p.read_text(encoding='utf-8')
backup=p.with_name('F14TomcatRC_pre_v17.py')
backup.write_text(text,encoding='utf-8')
marker='\ndef build_project_revision():\n'
if marker not in text:
    raise SystemExit('build_project_revision marker not found')
func=r'''
def build_pivot_wingbox_review_v17():
    """Engineering pivot/wingbox datum review. Pivot WL is source-section extrapolation, not original-aircraft verification."""
    build_basic_wing_document_v08()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v17_PIVOT_WINGBOX_ENGINEERING_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream:
        data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream:
        pivot=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pivot_wl_in=s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz
    pz=pivot_wl_in*factor
    for n,val,c in [
        ('SourcePivotFS_v17',px,'source-backed pivot FS'),('SourcePivotBL_v17',py,'source-backed pivot BL'),
        ('EngineeringPivotWL_v17',pz,'linear extrapolation of two inboard Grumman wing reference WL stations')]:
        try: design.userParameters.add(n,adsk.core.ValueInput.createByReal(mm(val)),'mm',c)
        except: pass
    bodies=[]
    # Central wing-box engineering envelope: deliberately conservative and separate from OML.
    box_x0,box_x1=px-38.0,px+45.0
    box_y0,box_y1=-py-28.0,py+28.0
    box_z0,box_h=pz-13.0,26.0
    box=_box_body(root,'ENG_WINGBOX_v17_NOT_FLIGHT_RELEASED',box_x0,box_x1,box_y0,box_y1,box_z0,box_h)
    box.opacity=0.35; bodies.append(box)
    # Pivot bosses around source-backed FS/BL with extrapolated vertical datum.
    for sign,label in [(1,'R'),(-1,'L')]:
        y=sign*py
        sk=root.sketches.add(axis_plane(root,'z',pz-10.0))
        sk.name='ENG_PIVOT_'+label+'_v17'
        ctr=model_point(sk,px,y,pz-10.0)
        sk.sketchCurves.sketchCircles.addByCenterRadius(ctr,mm(12.0))
        if sk.profiles.count!=1: raise RuntimeError('Pivot profile failed '+label)
        ex=root.features.extrudeFeatures
        ei=ex.createInput(sk.profiles.item(0),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(mm(20.0)))
        body=ex.add(ei).bodies.item(0); body.name='ENG_PIVOT_BOSS_'+label+'_24OD_v17'; bodies.append(body)
    # Check pivot boss intersection with each source wing: non-zero overlap is required for a mechanically meaningful root datum.
    temporary=adsk.fusion.TemporaryBRepManager.get()
    checks=[]
    for label in ['R','L']:
        wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
        boss=next(b for b in root.bRepBodies if b.name=='ENG_PIVOT_BOSS_'+label+'_24OD_v17')
        target=temporary.copy(boss); tool=temporary.copy(wing)
        ok=temporary.booleanOperation(target,tool,adsk.fusion.BooleanTypes.IntersectionBooleanType)
        iv=target.volume if ok and target.isValid else 0.0
        checks.append(dict(side=label,intersection_succeeded=bool(ok),intersection_volume_cm3=iv,pivot_engages_source_wing=(iv>0.01)))
    root.isSketchFolderLightBulbOn=False
    root.isConstructionFolderLightBulbOn=False
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'pivot_wingbox_v17'); os.makedirs(outdir,exist_ok=True)
    audit=dict(status='ENGINEERING_PIVOT_WINGBOX_DATUM_REVIEW',source_pivot_fs_bl_verified=True,
               pivot_waterline_method='linear extrapolation from two inboard Grumman source reference-WL stations',
               pivot_waterline_original_aircraft_verified=False,pivot_fullscale_wl_in=pivot_wl_in,
               pivot_model_mm=dict(x=px,y=py,z=pz),pivot_boss_od_mm=24.0,wingbox_bounds_mm=dict(x=[box_x0,box_x1],y=[box_y0,box_y1],z=[box_z0,box_z0+box_h]),
               pivot_wing_intersection=checks,mechanical_detail_release=False,body_glove_collision_checked=False,
               print_release=False,flight_release=False)
    target=os.path.join(outdir,'F14_v17_PIVOT_WINGBOX_ENGINEERING_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)):
        raise RuntimeError('v17 archive export failed')
    with open(os.path.join(outdir,'F14_v17_pivot_wingbox_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit()
    _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v17_pivot_wingbox_review.png'),1600,1000)
    return audit
'''
text=text.replace(marker,'\n'+func+marker,1)
old="return build_pivot_kinematic_review_v16()"
if old not in text:
    raise SystemExit('old project revision target not found')
text=text.replace(old,"return build_pivot_wingbox_review_v17()",1)
p.write_text(text,encoding='utf-8')
print('patched',p)
print('backup',backup)
