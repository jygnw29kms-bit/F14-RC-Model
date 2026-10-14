"""v85: quantify actual insert-to-inner-skin / inner-rib bond-interface area for torsion transfer."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v85_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    wanted=['CANDIDATE_OUTER_INSERT_SWEEP_CLEARED_v83','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    bodies={}
    for i in range(root.bRepBodies.count):
        b=root.bRepBodies.item(i)
        if b.name in wanted: bodies[b.name]=b
    miss=[n for n in wanted if n not in bodies]
    if miss: raise RuntimeError('Missing v83 bodies '+repr(miss))
    ins=bodies['CANDIDATE_OUTER_INSERT_SWEEP_CLEARED_v83']; skin=bodies['CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS']; rib=bodies['CANDIDATE_RIB_ZERO_CLEARANCE_-3']
    spars=[bodies[n] for n in wanted if 'CARBON_R_' in n]
    ycut=float(src['insert_y_max_mm']); maxgap=float(src['skin_gap_candidate_max_mm'])
    faces=[]; skin_candidate_area=0.0; near_rib_area=0.0
    gap_bins={'0_0.10':0.0,'0.10_0.20':0.0,'0.20_0.30':0.0,'gt_0.30':0.0}
    for i,f in enumerate(ins.faces):
        p=f.pointOnFace; y=p.y*10.0
        if y>ycut+0.05: continue
        area=f.area*100.0
        skin_gap=app.measureManager.measureMinimumDistance(f,skin).value*10.0
        rib_gap=app.measureManager.measureMinimumDistance(f,rib).value*10.0
        carbon_gap=min(app.measureManager.measureMinimumDistance(f,s).value*10.0 for s in spars)
        rec={'face_index':i,'sample_y_mm':y,'area_mm2':area,'skin_gap_mm':skin_gap,'inner_rib_gap_mm':rib_gap,'nearest_carbon_gap_mm':carbon_gap}
        faces.append(rec)
        if skin_gap<=maxgap:
            skin_candidate_area+=area
            if skin_gap<=0.10: gap_bins['0_0.10']+=area
            elif skin_gap<=0.20: gap_bins['0.10_0.20']+=area
            else: gap_bins['0.20_0.30']+=area
        else: gap_bins['gt_0.30']+=area
        if rib_gap<=0.30: near_rib_area+=area
    if not faces: raise RuntimeError('No insert-region faces')
    # conservative torsion requirement from v81 worst dynamic case with SF3
    torsion_req_Nmm=747.3921304468803
    sf3_force_N=36.94816950685162*3.0
    avg_bond_shear_MPa=sf3_force_N/skin_candidate_area if skin_candidate_area>0 else None
    audit={
      'status':'V85_INSERT_BOND_INTERFACE_SCREEN',
      'source':src,
      'insert_region_face_count':len(faces),
      'insert_region_total_area_mm2':sum(x['area_mm2'] for x in faces),
      'skin_candidate_area_mm2_le_0p30_gap':skin_candidate_area,
      'skin_gap_area_bins_mm2':gap_bins,
      'inner_rib_near_area_mm2_le_0p30_gap':near_rib_area,
      'minimum_skin_gap_mm':min(x['skin_gap_mm'] for x in faces),
      'maximum_skin_gap_within_candidate_mm':max((x['skin_gap_mm'] for x in faces if x['skin_gap_mm']<=maxgap), default=None),
      'minimum_carbon_gap_mm':min(x['nearest_carbon_gap_mm'] for x in faces),
      'minimum_inner_rib_gap_mm':min(x['inner_rib_gap_mm'] for x in faces),
      'torsion_requirement':{'worst_dynamic_torsion_Nmm':torsion_req_Nmm,'equivalent_key_force_with_SF3_N':sf3_force_N,'required_average_bond_shear_if_all_candidate_skin_area_used_MPa':avg_bond_shear_MPa},
      'faces':faces,
      'geometry_bond_area_established':skin_candidate_area>0,
      'adhesive_allowable_verified':False,
      'coupon_verified':False,
      'torsion_transfer_verified':False,
      'structural_capacity_verified':False,
      'print_release':False,
      'flight_release':False,
      'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    }
    os.makedirs(outdir,exist_ok=True)
    json.dump(audit,open(os.path.join(outdir,'F14_v85_insert_bond_interface_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v85_insert_bond_interface_review.png'),1600,1000)
    if prior: prior.activate()
    return audit