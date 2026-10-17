from pathlib import Path
p=Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py')
text=p.read_text(encoding='utf-8')
backup=p.with_name('F14TomcatRC_pre_v18.py')
backup.write_text(text,encoding='utf-8')
marker='\ndef build_project_revision():\n'
if marker not in text: raise SystemExit('project marker missing')
func=r'''
def build_root_lug_review_v18():
    """Engineering root-lug bridge from source-backed pivot to first Grumman outer-wing section."""
    build_basic_wing_document_v08()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v18_ROOT_LUG_PIVOT_INTERFACE_REVIEW'
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
    root_y=s0['wbl_in']*factor
    root_ref_z=s0['reference_vertical_wl_in']*factor
    root_le=s0['leading_edge_fs_in']*factor
    root_te=s0['trailing_edge_fs_in']*factor
    root_chord=root_te-root_le
    # Bosses and root lugs are engineering envelopes, not scale surface geometry.
    bodies=[]
    temporary=adsk.fusion.TemporaryBRepManager.get()
    checks=[]
    for sign,label in [(1,'R'),(-1,'L')]:
        y_p=sign*py; y_r=sign*root_y
        sk=root.sketches.add(axis_plane(root,'z',pz-10.0)); sk.name='ENG_PIVOT_'+label+'_v18'
        ctr=model_point(sk,px,y_p,pz-10.0); sk.sketchCurves.sketchCircles.addByCenterRadius(ctr,mm(12.0))
        ei=root.features.extrudeFeatures.createInput(sk.profiles.item(0),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(mm(20.0)))
        boss=root.features.extrudeFeatures.add(ei).bodies.item(0); boss.name='ENG_PIVOT_BOSS_'+label+'_24OD_v18'; bodies.append(boss)
        ymin=min(y_p,y_r-sign*1.5); ymax=max(y_p,y_r-sign*1.5)
        # 40-mm chordwise lug centered at pivot FS; 16-mm thick vertically, reaches 1.5 mm into source wing root.
        x0=max(root_le,px-20.0); x1=min(root_te,px+20.0)
        lug=extrude_poly(root,'ENG_ROOT_LUG_'+label+'_v18',[(x0,ymin),(x1,ymin),(x1,ymax),(x0,ymax)],pz-8.0,16.0)
        lug.opacity=0.45; bodies.append(lug)
        wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
        for target_body,kind in [(lug,'lug_to_wing'),(boss,'boss_to_wing')]:
            target=temporary.copy(target_body); tool=temporary.copy(wing)
            ok=temporary.booleanOperation(target,tool,adsk.fusion.BooleanTypes.IntersectionBooleanType)
            iv=target.volume if ok and target.isValid else 0.0
            checks.append(dict(side=label,kind=kind,intersection_succeeded=bool(ok),intersection_volume_cm3=iv,positive_overlap=(iv>1e-4)))
        target=temporary.copy(lug); tool=temporary.copy(boss)
        ok=temporary.booleanOperation(target,tool,adsk.fusion.BooleanTypes.IntersectionBooleanType)
        iv=target.volume if ok and target.isValid else 0.0
        checks.append(dict(side=label,kind='lug_to_boss',intersection_succeeded=bool(ok),intersection_volume_cm3=iv,positive_overlap=(iv>1e-4)))
    root.isSketchFolderLightBulbOn=False; root.isConstructionFolderLightBulbOn=False
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'root_lug_v18'); os.makedirs(outdir,exist_ok=True)
    audit=dict(status='ENGINEERING_ROOT_LUG_PIVOT_INTERFACE_REVIEW',source_pivot_fs_bl_verified=True,
               pivot_waterline_original_aircraft_verified=False,pivot_fullscale_wl_in=pivot_wl_in,
               pivot_model_mm=dict(x=px,y=py,z=pz),first_source_section_mm=dict(y=root_y,leading_edge_x=root_le,trailing_edge_x=root_te,reference_z=root_ref_z,chord=root_chord),
               pivot_to_first_source_section_lateral_gap_mm=root_y-py,checks=checks,
               root_lug_engages_wing_both_sides=all(c['positive_overlap'] for c in checks if c['kind']=='lug_to_wing'),
               root_lug_engages_boss_both_sides=all(c['positive_overlap'] for c in checks if c['kind']=='lug_to_boss'),
               boss_directly_engages_outer_wing=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    target=os.path.join(outdir,'F14_v18_ROOT_LUG_PIVOT_INTERFACE_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v18 export failed')
    with open(os.path.join(outdir,'F14_v18_root_lug_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v18_root_lug_review.png'),1600,1000)
    return audit
'''
text=text.replace(marker,'\n'+func+marker,1)
old='return build_pivot_wingbox_review_v17()'
if old not in text: raise SystemExit('v17 target missing')
text=text.replace(old,'return build_root_lug_review_v18()',1)
p.write_text(text,encoding='utf-8')
print('patched v18')
