"""v77: tapered wing-joint bridge lofted between validated v73 rib mating profiles."""
import adsk.core, adsk.fusion, json, os, hashlib

def _end_faces(body):
    out=[]
    for f in body.faces:
        pl=adsk.core.Plane.cast(f.geometry)
        if pl and abs(pl.normal.y)>0.999999:
            out.append((f.pointOnFace.y*10.0,f,f.area*100.0))
    return sorted(out,key=lambda x:x[0])

def _volume(body):
    return body.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v77_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted=[]
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if ('_R_' in b.name and ('CARBON' in b.name or 'HOLLOW_WING' in b.name)) or b.name in ('CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_RIB_ZERO_CLEARANCE_3'):
            wanted.append((b.name,temp.copy(b)))
    if len(wanted)!=7: raise RuntimeError('Expected seven right-side v73 bodies, got '+repr([x[0] for x in wanted]))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_WING_JOINT_TAPERED_BRIDGE_v77'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies=[]
    for name,copy in wanted:
        b=root.bRepBodies.add(copy); b.name=name; bodies.append(b)
    spars=[b for b in bodies if 'CARBON' in b.name]; skins=[b for b in bodies if 'HOLLOW_WING' in b.name]
    inner=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_-3')
    outer=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_3')
    inner_ends=_end_faces(inner); outer_ends=_end_faces(outer)
    if len(inner_ends)!=2 or len(outer_ends)!=2: raise RuntimeError('Unexpected rib end-face inventory')
    inner_out_y,inner_face,inner_area=max(inner_ends,key=lambda x:x[0])
    outer_in_y,outer_face,outer_area=min(outer_ends,key=lambda x:x[0])
    # A disposable translated copy supplies the inner loft profile 0.20 mm away from the actual inner rib.
    shifted_copy=temp.copy(inner)
    m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(0,mm(float(src['target_axial_gap_mm'])),0)
    if not temp.transform(shifted_copy,m): raise RuntimeError('Temporary inner-rib shift failed')
    shifted=root.bRepBodies.add(shifted_copy); shifted.name='REFERENCE_SHIFTED_INNER_RIB_v77'
    shifted_ends=_end_faces(shifted)
    target_y,shifted_face,shifted_area=max(shifted_ends,key=lambda x:x[0])
    # Loft directly between the two planar, holed rib faces; both already embody v73 skin/carbon clearances.
    li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    li.isSolid=True
    li.loftSections.add(outer_face)
    li.loftSections.add(shifted_face)
    lf=root.features.loftFeatures.add(li)
    if not lf or lf.bodies.count<1: raise RuntimeError('Tapered bridge loft failed')
    bridge=lf.bodies.item(0); bridge.name='CANDIDATE_TAPERED_ALIGNMENT_BRIDGE_v77'
    if not bridge.isValid or not bridge.isSolid: raise RuntimeError('Tapered bridge body invalid')
    # Remove reference shifted rib before clearance tests.
    shifted.deleteMe()
    vbridge=_volume(bridge); bb=bridge.boundingBox
    collisions=[]
    for blocker in skins+spars:
        cut=temp.copy(bridge)
        if not temp.booleanOperation(cut,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Collision boolean failed: '+blocker.name)
        scratch=root.bRepBodies.add(cut); v=_volume(scratch); scratch.deleteMe()
        removed=max(0.0,vbridge-v)
        collisions.append({'blocker':blocker.name,'removed_cm3':removed,'pass':removed<1e-7})
    # Final axial gap to actual inner rib.
    axial_gap=app.measureManager.measureMinimumDistance(bridge,inner).value*10.0
    # Insertion screen: translate a temporary bridge from +5 mm outboard toward final position in 1 mm increments.
    insertion=[]
    for dy in (5.0,4.0,3.0,2.0,1.0,0.0):
        moving=temp.copy(bridge)
        tr=adsk.core.Matrix3D.create(); tr.translation=adsk.core.Vector3D.create(0,mm(dy),0)
        temp.transform(moving,tr)
        hits=[]
        for blocker in skins+spars+([inner] if dy>0 else []):
            q=temp.copy(moving)
            ok=temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType)
            if not ok: raise RuntimeError('Insertion boolean failed: '+blocker.name)
            scratch=root.bRepBodies.add(q); vv=_volume(scratch); scratch.deleteMe()
            removed=max(0.0,vbridge-vv)
            if removed>=1e-7: hits.append({'blocker':blocker.name,'removed_cm3':removed})
        insertion.append({'outboard_translation_mm':dy,'collision_free':len(hits)==0,'hits':hits})
    final_clear=all(x['pass'] for x in collisions)
    insertion_clear=all(x['collision_free'] for x in insertion)
    gap_pass=abs(axial_gap-float(src['target_axial_gap_mm']))<=0.03
    audit={
      'status':'V77_TAPERED_NATIVE_RIB_PROFILE_BRIDGE',
      'source':src,
      'profiles':{'outer_inboard_face_y_mm':outer_in_y,'outer_area_mm2':outer_area,'inner_original_outboard_face_y_mm':inner_out_y,'shifted_inner_face_y_mm':target_y,'shifted_inner_area_mm2':shifted_area},
      'bridge':{'volume_cm3':vbridge,'bbox_y_min_mm':bb.minPoint.y*10.0,'bbox_y_max_mm':bb.maxPoint.y*10.0,'axial_gap_to_inner_rib_mm':axial_gap},
      'collision_checks_final':collisions,
      'insertion_path_screen':insertion,
      'final_collision_free':final_clear,'insertion_collision_free':insertion_clear,'axial_gap_screen_pass':gap_pass,
      'geometry_candidate_pass':final_clear and insertion_clear and gap_pass,
      'primary_bending_path':'continuous carbon upper/lower caps and web','printed_bridge_role':['alignment','skin step control','local torsion transfer','bond area'],
      'fit_coupon_verified':False,'torsion_transfer_verified':False,'adhesive_system_selected':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,
      'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    }
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_WING_JOINT_TAPERED_BRIDGE_v77.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v77_tapered_bridge_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v77_tapered_bridge_review.png'),1600,1000)
    if prior: prior.activate()
    return audit