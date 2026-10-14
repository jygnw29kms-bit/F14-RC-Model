"""v75: first production-joint CAD trial: constant-profile bridge from outboard rib toward inboard rib."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument
    base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v75_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    imported=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path']))
    if not imported: raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct)
    temp=adsk.fusion.TemporaryBRepManager.get()
    wanted=[]
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if ('_R_' in b.name and ('CARBON' in b.name or 'HOLLOW_WING' in b.name)) or b.name in ('CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_RIB_ZERO_CLEARANCE_3'):
            wanted.append((b.name,temp.copy(b)))
    if len(wanted)!=7: raise RuntimeError('Expected seven right-side v73 bodies, got '+repr([x[0] for x in wanted]))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_WING_JOINT_BRIDGE_TRIAL_v75'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies=[]
    for name,copy in wanted:
        b=root.bRepBodies.add(copy); b.name=name; bodies.append(b)
    spars=[b for b in bodies if 'CARBON' in b.name]
    skins=[b for b in bodies if 'HOLLOW_WING' in b.name]
    inner=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_-3')
    outer=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_3')
    # Pick the inboard-facing planar end face of the outboard rib (lowest Y plane).
    candidates=[]
    for f in outer.faces:
        pl=adsk.core.Plane.cast(f.geometry)
        if pl and abs(pl.normal.y)>0.999999:
            candidates.append((f.pointOnFace.y*10.0,f,pl.normal.y,f.area*100.0))
    if len(candidates)!=2: raise RuntimeError('Expected two planar outboard rib end faces')
    y0,face,normal_y,face_area=min(candidates,key=lambda x:x[0])
    length=float(src['bridge_length_mm'])
    # Extrude toward -Y independent of face normal orientation.
    signed_cm=mm(length)*(-1.0 if normal_y>0 else 1.0)
    ei=root.features.extrudeFeatures.createInput(face,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(signed_cm))
    feat=root.features.extrudeFeatures.add(ei)
    if not feat or feat.bodies.count<1: raise RuntimeError('Bridge extrusion failed')
    bridges=[]
    for i in range(feat.bodies.count):
        b=feat.bodies.item(i); b.name='CANDIDATE_OUTER_TO_INNER_ALIGNMENT_BRIDGE_v75_'+str(i+1); bridges.append(b)
    bridge_records=[]
    for b in bridges:
        bb=b.boundingBox
        bridge_records.append({'body':b.name,'bbox_y_min_mm':bb.minPoint.y*10.0,'bbox_y_max_mm':bb.maxPoint.y*10.0,'volume_cm3':b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume})
    collisions=[]
    for blocker in skins+spars:
        removed_total=0.0
        for bridge in bridges:
            before=bridge.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume
            cut=temp.copy(bridge)
            if not temp.booleanOperation(cut,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Collision boolean failed: '+blocker.name)
            scratch=root.bRepBodies.add(cut)
            after=scratch.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume
            scratch.deleteMe()
            removed_total += max(0.0,before-after)
        collisions.append({'blocker':blocker.name,'removed_cm3':removed_total,'pass':removed_total<1e-7})
    axial_gap=min(app.measureManager.measureMinimumDistance(bridge,inner).value*10.0 for bridge in bridges)
    by0=min(x['bbox_y_min_mm'] for x in bridge_records); by1=max(x['bbox_y_max_mm'] for x in bridge_records)
    before=sum(x['volume_cm3'] for x in bridge_records)
    audit={
      'status':'V75_CONSTANT_PROFILE_ALIGNMENT_BRIDGE_TRIAL',
      'source':src,
      'bridge':{'origin_face_y_mm':y0,'origin_face_area_mm2':face_area,'length_mm':length,'body_count':len(bridges),'bodies':bridge_records,'bbox_y_min_mm':by0,'bbox_y_max_mm':by1,'volume_cm3':before,'axial_gap_to_inner_rib_mm':axial_gap},
      'collision_checks':collisions,
      'collision_free':all(x['pass'] for x in collisions),
      'axial_gap_screen_pass':abs(axial_gap-float(src['expected_axial_gap_mm']))<=0.03,
      'geometry_candidate_pass':all(x['pass'] for x in collisions) and abs(axial_gap-float(src['expected_axial_gap_mm']))<=0.03,
      'primary_bending_path':'continuous carbon; printed bridge is secondary alignment/torsion path',
      'fit_coupon_verified':False,'torsion_transfer_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,
      'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    }
    os.makedirs(outdir,exist_ok=True)
    export=os.path.join(outdir,'F14_WING_JOINT_BRIDGE_TRIAL_v75.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(export)): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v75_joint_bridge_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v75_joint_bridge_review.png'),1600,1000)
    if prior: prior.activate()
    return audit