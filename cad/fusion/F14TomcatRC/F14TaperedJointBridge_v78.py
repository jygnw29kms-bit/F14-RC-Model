"""v78: deterministic sketch-profile loft for the tapered wing-joint bridge."""
import adsk.core, adsk.fusion, json, os, hashlib

def _end_faces(body):
    out=[]
    for f in body.faces:
        pl=adsk.core.Plane.cast(f.geometry)
        if pl and abs(pl.normal.y)>0.999999:
            out.append((f.pointOnFace.y*10.0,f,f.area*100.0))
    return sorted(out,key=lambda x:x[0])

def _vol(body):
    return body.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def _profile_from_face(root, face, target_area_mm2, name):
    sk=root.sketches.add(face)
    sk.name=name
    for e in face.edges:
        sk.project(e)
    if sk.profiles.count<1: raise RuntimeError('No sketch profile from '+name)
    candidates=[]
    for p in sk.profiles:
        props=p.areaProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy)
        candidates.append((abs(props.area*100.0-target_area_mm2),props.area*100.0,p,p.profileLoops.count))
    candidates.sort(key=lambda x:x[0])
    err,area,p,loops=candidates[0]
    if err>1.0: raise RuntimeError('Projected profile area mismatch '+name+': '+repr([(x[1],x[3]) for x in candidates]))
    return p,area,loops

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v78_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted=[]
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if ('_R_' in b.name and ('CARBON' in b.name or 'HOLLOW_WING' in b.name)) or b.name in ('CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_RIB_ZERO_CLEARANCE_3'):
            wanted.append((b.name,temp.copy(b)))
    if len(wanted)!=7: raise RuntimeError('Expected seven right-side v73 bodies')
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_WING_JOINT_TAPERED_BRIDGE_v78'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies=[]
    for name,copy in wanted:
        b=root.bRepBodies.add(copy); b.name=name; bodies.append(b)
    spars=[b for b in bodies if 'CARBON' in b.name]
    skin_inner=next(b for b in bodies if b.name=='CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS')
    skin_outer=next(b for b in bodies if b.name=='CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS')
    inner=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_-3')
    outer=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_3')
    inner_out_y,inner_face,inner_area=max(_end_faces(inner),key=lambda x:x[0])
    outer_in_y,outer_face,outer_area=min(_end_faces(outer),key=lambda x:x[0])
    shifted_copy=temp.copy(inner)
    m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(0,mm(float(src['target_axial_gap_mm'])),0)
    if not temp.transform(shifted_copy,m): raise RuntimeError('Shift inner reference failed')
    shifted=root.bRepBodies.add(shifted_copy); shifted.name='REFERENCE_SHIFTED_INNER_RIB_v78'
    target_y,shifted_face,shifted_area=max(_end_faces(shifted),key=lambda x:x[0])
    p_outer,a_outer,l_outer=_profile_from_face(root,outer_face,outer_area,'BRIDGE_OUTER_PROFILE_v78')
    p_inner,a_inner,l_inner=_profile_from_face(root,shifted_face,shifted_area,'BRIDGE_INNER_PROFILE_v78')
    li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    li.isSolid=True; li.loftSections.add(p_outer); li.loftSections.add(p_inner)
    lf=root.features.loftFeatures.add(li)
    if not lf or lf.bodies.count<1: raise RuntimeError('No tapered bridge loft bodies')
    candidates=[]
    for i in range(lf.bodies.count):
        b=lf.bodies.item(i)
        if not b.isValid or not b.isSolid: continue
        bb=b.boundingBox; rec={'body':b,'volume_cm3':_vol(b),'y_min_mm':bb.minPoint.y*10.0,'y_max_mm':bb.maxPoint.y*10.0}
        rec['span_mm']=rec['y_max_mm']-rec['y_min_mm']
        candidates.append(rec)
    bridges=[]; bridge_records=[]
    for rec in candidates:
        if 4.95<=rec['span_mm']<=5.05:
            b=rec['body']; b.name='CANDIDATE_TAPERED_ALIGNMENT_BRIDGE_v78'; bridges.append(b)
            bridge_records.append({'body':b.name,'volume_cm3':rec['volume_cm3'],'y_min_mm':rec['y_min_mm'],'y_max_mm':rec['y_max_mm'],'span_mm':rec['span_mm']})
    shifted.deleteMe()
    if len(bridges)!=1: raise RuntimeError('Expected one 5 mm loft bridge; candidates='+repr([{k:v for k,v in x.items() if k!='body'} for x in candidates]))
    vb=sum(x['volume_cm3'] for x in bridge_records)
    final_collisions=[]
    for blocker in [skin_inner,skin_outer]+spars:
        removed=0.0
        for bridge in bridges:
            q=temp.copy(bridge)
            if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Final boolean failed')
            scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed += max(0.0,_vol(bridge)-vv)
        final_collisions.append({'blocker':blocker.name,'removed_cm3':removed,'pass':removed<1e-7})
    axial_gap=min(app.measureManager.measureMinimumDistance(bridge,inner).value*10.0 for bridge in bridges)
    # Assembly model: the outboard printed segment and bridge move together over the stationary inner segment and already-installed continuous carbon spar.
    stationary=[skin_inner,inner]+spars
    insertion=[]
    for dy in (5.0,4.0,3.0,2.0,1.0,0.0):
        moving=temp.copy(bridge); tr=adsk.core.Matrix3D.create(); tr.translation=adsk.core.Vector3D.create(0,mm(dy),0); temp.transform(moving,tr)
        hits=[]
        for blocker in stationary:
            q=temp.copy(moving)
            if not temp.booleanOperation(q,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Insertion boolean failed')
            scratch=root.bRepBodies.add(q); vv=_vol(scratch); scratch.deleteMe(); removed=max(0.0,vb-vv)
            if removed>=1e-7: hits.append({'blocker':blocker.name,'removed_cm3':removed})
        insertion.append({'outboard_translation_mm':dy,'collision_free':not hits,'hits':hits})
    final_clear=all(x['pass'] for x in final_collisions); insertion_clear=all(x['collision_free'] for x in insertion)
    gap_pass=abs(axial_gap-float(src['target_axial_gap_mm']))<=0.03
    audit={'status':'V78_DETERMINISTIC_TAPERED_BRIDGE','source':src,'profiles':{'outer_y_mm':outer_in_y,'outer_face_area_mm2':outer_area,'outer_profile_area_mm2':a_outer,'outer_loops':l_outer,'inner_original_y_mm':inner_out_y,'inner_shifted_y_mm':target_y,'inner_face_area_mm2':shifted_area,'inner_profile_area_mm2':a_inner,'inner_loops':l_inner},'bridge':{'body_count':len(bridges),'bodies':bridge_records,'total_volume_cm3':vb,'axial_gap_to_inner_rib_mm':axial_gap},'final_collision_checks':final_collisions,'insertion_path_model':'outer segment plus bridge moves over stationary inner segment and continuous carbon spar','insertion_path_screen':insertion,'final_collision_free':final_clear,'insertion_collision_free':insertion_clear,'axial_gap_screen_pass':gap_pass,'geometry_candidate_pass':final_clear and insertion_clear and gap_pass,'primary_bending_path':'continuous carbon upper/lower caps and web','fit_coupon_verified':False,'torsion_transfer_verified':False,'adhesive_system_selected':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_WING_JOINT_TAPERED_BRIDGE_v78.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v78_tapered_bridge_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v78_tapered_bridge_review.png'),1600,1000)
    if prior: prior.activate()
    return audit