"""v82: fuse the outboard v73 rib to the v79 sweep-cleared key and test the full moving insert."""
import adsk.core, adsk.fusion, json, os, hashlib

def _vol(b): return b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v82_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted_names=['CANDIDATE_CARBON_SWEEP_CLEARED_KEYS_v79','CANDIDATE_RIB_ZERO_CLEARANCE_3','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    found={}
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if b.name in wanted_names: found[b.name]=temp.copy(b)
    missing=[n for n in wanted_names if n not in found]
    if missing: raise RuntimeError('Missing v79 bodies: '+repr(missing))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_OUTER_RIB_KEY_INSERT_v82'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies={}
    for name,copy in found.items():
        b=root.bRepBodies.add(copy); b.name=name; bodies[name]=b
    keys=bodies['CANDIDATE_CARBON_SWEEP_CLEARED_KEYS_v79']; outer=bodies['CANDIDATE_RIB_ZERO_CLEARANCE_3']; inner=bodies['CANDIDATE_RIB_ZERO_CLEARANCE_-3']
    skin_inner=bodies['CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS']; skin_outer=bodies['CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS']
    spars=[bodies[n] for n in wanted_names if 'CARBON_R_' in n]
    # Slightly overlap the key root into the outboard rib so the printable insert is a true single solid.
    overlap=float(src['root_overlap_mm'])
    k=temp.copy(keys); m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(0,mm(overlap),0); temp.transform(k,m)
    fused=temp.copy(outer)
    if not temp.booleanOperation(fused,k,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('Outer-rib/key union failed')
    insert=root.bRepBodies.add(fused); insert.name='CANDIDATE_OUTER_RIB_KEY_INSERT_v82'
    if not insert.isValid or not insert.isSolid: raise RuntimeError('Fused insert invalid')
    vi=_vol(insert); bb=insert.boundingBox
    axial_gap=app.measureManager.measureMinimumDistance(insert,inner).value*10.0
    final=[]
    for blocker in [skin_inner,skin_outer]+spars:
        q=temp.copy(insert)
        if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Final boolean failed')
        scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed=max(0.0,vi-vv)
        final.append({'blocker':blocker.name,'removed_cm3':removed,'pass':removed<1e-7})
    step=float(src['step_mm']); dist=float(src['insertion_mm']); n=int(round(dist/step)); insertion=[]
    stationary=[skin_inner,inner]+spars
    for kstep in range(n,-1,-1):
        dy=kstep*step; moving=temp.copy(insert); tr=adsk.core.Matrix3D.create(); tr.translation=adsk.core.Vector3D.create(0,mm(dy),0); temp.transform(moving,tr)
        hits=[]
        for blocker in stationary:
            q=temp.copy(moving)
            if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Insertion boolean failed')
            scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed=max(0.0,vi-vv)
            if removed>=1e-7: hits.append({'blocker':blocker.name,'removed_cm3':removed})
        insertion.append({'outboard_translation_mm':dy,'collision_free':not hits,'hits':hits})
    final_clear=all(x['pass'] for x in final); insertion_clear=all(x['collision_free'] for x in insertion); gap_pass=abs(axial_gap-float(src['target_axial_gap_mm']))<=0.04
    audit={'status':'V82_OUTER_RIB_KEY_INSERT_ASSEMBLY_SCREEN','source':src,'insert':{'volume_cm3':vi,'bbox_y_mm':[bb.minPoint.y*10.0,bb.maxPoint.y*10.0],'axial_gap_to_inner_rib_mm':axial_gap,'root_overlap_mm':overlap},'final_collision_checks':final,'insertion_path_screen':insertion,'final_collision_free':final_clear,'insertion_collision_free':insertion_clear,'axial_gap_screen_pass':gap_pass,'geometry_candidate_pass':final_clear and insertion_clear and gap_pass,'primary_bending_path':'continuous carbon','fit_coupon_verified':False,'torsion_capacity_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_OUTER_RIB_KEY_INSERT_v82.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v82_outer_insert_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v82_outer_insert_review.png'),1600,1000)
    if prior: prior.activate()
    return audit