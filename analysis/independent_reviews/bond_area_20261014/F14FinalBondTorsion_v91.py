"""v91: final v89 insert bond-area and torsion-transfer requirement screen."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v91_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    names=['CANDIDATE_OUTER_INSERT_MFG_ENDPOINT_CLEAR_v89','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_RIB_ZERO_CLEARANCE_-3']
    bodies={}
    for i in range(root.bRepBodies.count):
        b=root.bRepBodies.item(i)
        if b.name in names: bodies[b.name]=b
    miss=[n for n in names if n not in bodies]
    if miss: raise RuntimeError('Missing v89 bodies '+repr(miss))
    ins=bodies[names[0]]; skin=bodies[names[1]]; rib=bodies[names[2]]; ycut=float(src['insert_y_max_mm']); maxgap=float(src['skin_gap_candidate_max_mm'])
    faces=[]; candidate=0.0; bins={'0_0.15':0.0,'0.15_0.20':0.0,'0.20_0.25':0.0,'gt_0.25':0.0}
    for i,f in enumerate(ins.faces):
        y=f.pointOnFace.y*10.0
        if y>ycut+0.05: continue
        area=f.area*100.0; sg=app.measureManager.measureMinimumDistance(f,skin).value*10.0; rg=app.measureManager.measureMinimumDistance(f,rib).value*10.0
        faces.append({'face_index':i,'sample_y_mm':y,'area_mm2':area,'skin_gap_mm':sg,'inner_rib_gap_mm':rg})
        if sg<=maxgap:
            candidate+=area
            if sg<=0.15: bins['0_0.15']+=area
            elif sg<=0.20: bins['0.15_0.20']+=area
            else: bins['0.20_0.25']+=area
        else: bins['gt_0.25']+=area
    if candidate<=0: raise RuntimeError('No bond candidate area')
    force=float(src['torsion_sf3_force_N']); shear=force/candidate
    audit={'status':'V91_FINAL_BOND_TORSION_INTERFACE_SCREEN','source':src,'insert_region_face_count':len(faces),'candidate_skin_bond_area_mm2':candidate,'skin_gap_area_bins_mm2':bins,'minimum_skin_gap_mm':min(x['skin_gap_mm'] for x in faces),'maximum_candidate_skin_gap_mm':max(x['skin_gap_mm'] for x in faces if x['skin_gap_mm']<=maxgap),'minimum_inner_rib_gap_mm':min(x['inner_rib_gap_mm'] for x in faces),'torsion_requirement':{'equivalent_key_force_with_SF3_N':force,'required_average_bond_shear_MPa':shear},'faces':faces,'geometry_bond_area_established':True,'adhesive_allowable_verified':False,'coupon_verified':False,'torsion_transfer_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); json.dump(audit,open(os.path.join(outdir,'F14_v91_final_bond_torsion_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v91_final_bond_torsion_review.png'),1600,1000)
    if prior: prior.activate()
    return audit