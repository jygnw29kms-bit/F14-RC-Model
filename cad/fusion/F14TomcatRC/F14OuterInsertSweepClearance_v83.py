"""v83: carve the full outer-rib/key insert for the stationary continuous-carbon insertion envelope."""
import adsk.core, adsk.fusion, json, os, hashlib

def _vol(b): return b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v83_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted=['CANDIDATE_OUTER_RIB_KEY_INSERT_v82','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    found={}
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if b.name in wanted: found[b.name]=temp.copy(b)
    miss=[n for n in wanted if n not in found]
    if miss: raise RuntimeError('Missing v82 bodies '+repr(miss))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_OUTER_INSERT_SWEEP_CLEARED_v83'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies={}
    for name,copy in found.items():
        b=root.bRepBodies.add(copy); b.name=name; bodies[name]=b
    insert=bodies['CANDIDATE_OUTER_RIB_KEY_INSERT_v82']; inner=bodies['CANDIDATE_RIB_ZERO_CLEARANCE_-3']
    skin_inner=bodies['CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS']; skin_outer=bodies['CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS']
    spars=[bodies[n] for n in wanted if 'CARBON_R_' in n]
    raw_volume=_vol(insert)
    carved=temp.copy(insert)
    step=float(src['step_mm']); dist=float(src['insertion_mm']); n=int(round(dist/step)); carve_samples=[]
    # Equivalent to moving the insert +dy over fixed carbon: carve carbon shifted -dy from final insert coordinates.
    for k in range(n+1):
        dy=k*step
        removed_before=None
        for spar in spars:
            cutter=temp.copy(spar); m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(0,mm(-dy),0); temp.transform(cutter,m)
            if not temp.booleanOperation(carved,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Sweep carve failed at '+str(dy)+' '+spar.name)
        carve_samples.append({'relative_carbon_shift_mm':-dy})
    cleared=root.bRepBodies.add(carved); cleared.name='CANDIDATE_OUTER_INSERT_SWEEP_CLEARED_v83'
    if not cleared.isValid or not cleared.isSolid: raise RuntimeError('Cleared insert invalid')
    vc=_vol(cleared); bb=cleared.boundingBox
    axial_gap=app.measureManager.measureMinimumDistance(cleared,inner).value*10.0
    final=[]
    for blocker in [skin_inner,skin_outer]+spars:
        q=temp.copy(cleared)
        if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Final boolean failed')
        scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed=max(0.0,vc-vv)
        final.append({'blocker':blocker.name,'removed_cm3':removed,'pass':removed<1e-7})
    stationary=[skin_inner,inner]+spars; insertion=[]
    for k in range(n,-1,-1):
        dy=k*step; moving=temp.copy(cleared); m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(0,mm(dy),0); temp.transform(moving,m)
        hits=[]
        for blocker in stationary:
            q=temp.copy(moving)
            if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Insertion boolean failed')
            scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed=max(0.0,vc-vv)
            if removed>=1e-7: hits.append({'blocker':blocker.name,'removed_cm3':removed})
        insertion.append({'outboard_translation_mm':dy,'collision_free':not hits,'hits':hits})
    final_clear=all(x['pass'] for x in final); insertion_clear=all(x['collision_free'] for x in insertion); gap_pass=abs(axial_gap-float(src['target_axial_gap_mm']))<=0.04
    audit={'status':'V83_FULL_OUTER_INSERT_CARBON_SWEEP_CLEARANCE','source':src,'insert':{'raw_volume_cm3':raw_volume,'cleared_volume_cm3':vc,'volume_retained_fraction':vc/raw_volume,'bbox_y_mm':[bb.minPoint.y*10.0,bb.maxPoint.y*10.0],'face_count':cleared.faces.count,'axial_gap_to_inner_rib_mm':axial_gap},'carve_samples':carve_samples,'final_collision_checks':final,'insertion_path_screen':insertion,'final_collision_free':final_clear,'insertion_collision_free':insertion_clear,'axial_gap_screen_pass':gap_pass,'geometry_candidate_pass':final_clear and insertion_clear and gap_pass,'primary_bending_path':'continuous carbon','minimum_insert_section_verified':False,'fit_coupon_verified':False,'torsion_capacity_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_OUTER_INSERT_SWEEP_CLEARED_v83.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v83_outer_insert_sweep_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v83_outer_insert_sweep_review.png'),1600,1000)
    if prior: prior.activate()
    return audit