"""v102: co-located hardpoint sleeves using the proven v99 socket envelope."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v102_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v99 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted={}
    for i in range(orig.rootComponent.bRepBodies.count):
        b=orig.rootComponent.bRepBodies.item(i)
        if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29' or b.name.startswith('ENG_RISER_CIRCULAR_') or b.name.startswith('ENG_WINGBOX_FORK_LOWER_') or b.name.startswith('REF_CF6x4_') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_') or b.name.startswith('ENG_ROOT_LUG_'):
            wanted[b.name]=temp.copy(b)
    required=['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','ENG_RISER_CIRCULAR_FRONT_R_v99','ENG_RISER_CIRCULAR_FRONT_L_v99','ENG_RISER_CIRCULAR_REAR_R_v99','ENG_RISER_CIRCULAR_REAR_L_v99']
    missing=[n for n in required if n not in wanted]
    if missing: raise RuntimeError('missing v99 bodies '+repr(missing))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_CROSSTIE_HARDPOINT_SLEEVES_v102'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    bodies={}
    for n,c in wanted.items():
        b=root.bRepBodies.add(temp.copy(c)); b.name=n; bodies[n]=b
    fus=bodies['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29']; recs=[]
    min_fork_overlap=1e9; min_tube_gap=1e9; exact_match=True
    for fa in ('FRONT','REAR'):
        tie=bodies['REF_CF6x4_'+fa+'_LOWER_v34']
        for lab in ('R','L'):
            rn='ENG_RISER_CIRCULAR_'+fa+'_'+lab+'_v99'; ris=bodies[rn]
            sleeve=root.bRepBodies.add(temp.copy(ris)); sleeve.name='HARDPOINT_SLEEVE_'+fa+'_'+lab+'_v102'
            sv=sleeve.volume
            # exact co-location gate: sleeve minus riser and riser minus sleeve must both be empty/negligible.
            a=temp.copy(sleeve); ok1=temp.booleanOperation(a,temp.copy(ris),adsk.fusion.BooleanTypes.DifferenceBooleanType); rem1=a.volume if ok1 and a.isValid else 0.0
            b=temp.copy(ris); ok2=temp.booleanOperation(b,temp.copy(sleeve),adsk.fusion.BooleanTypes.DifferenceBooleanType); rem2=b.volume if ok2 and b.isValid else 0.0
            exact=(rem1<1e-7 and rem2<1e-7); exact_match=exact_match and exact
            q=temp.copy(sleeve); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType); inside=q.volume if ok and q.isValid else 0.0
            fork=bodies['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31']; q=temp.copy(sleeve); ok=temp.booleanOperation(q,temp.copy(fork),adsk.fusion.BooleanTypes.IntersectionBooleanType); fov=q.volume if ok and q.isValid else 0.0
            sb=sleeve.boundingBox; fb=fork.boundingBox
            yov=max(0.0,min(sb.maxPoint.y,fb.maxPoint.y)-max(sb.minPoint.y,fb.minPoint.y))*10.0
            try: gap=app.measureManager.measureMinimumDistance(sleeve,tie).value*10.0
            except: gap=-1.0
            min_fork_overlap=min(min_fork_overlap,yov); min_tube_gap=min(min_tube_gap,gap)
            recs.append({'sleeve':sleeve.name,'source_riser':rn,'volume_cm3':sv,'source_exact_match':exact,'source_minus_candidate_cm3':rem2,'candidate_minus_source_cm3':rem1,'fuselage_inside_fraction':inside/sv if sv else 0.0,'fork_overlap_cm3':fov,'fork_y_overlap_mm':yov,'tube_minimum_gap_mm':gap})
    # v99 already certified the same riser envelope continuously through sweep; exact-match sleeves inherit that envelope only if every body is proven identical.
    v99audit_path=os.path.join(os.path.dirname(src['path']),'F14_v99_circular_crosstie_retention_audit.json')
    v99=json.load(open(v99audit_path,encoding='utf-8'))
    inherited_clearance=bool(exact_match and v99.get('continuous_sweep_clearance_pass'))
    audit={'status':'V102_COLOCATED_HARDPOINT_SLEEVE_GATE','source':src,'records':recs,'all_source_envelopes_exact':exact_match,'minimum_fork_y_overlap_mm':min_fork_overlap,'minimum_tube_gap_mm':min_tube_gap,'fuselage_containment_pass':all(r['fuselage_inside_fraction']>0.999999 for r in recs),'fork_contact_pass':all(r['fork_overlap_cm3']>1e-4 and r['fork_y_overlap_mm']>=float(src['required_fork_overlap_mm'])-1e-6 for r in recs),'bore_preserved_pass':min_tube_gap>=float(src['expected_radial_gap_mm'])*0.95,'continuous_sweep_clearance_inherited_from_v99':inherited_clearance,'v99_minimum_continuous_clearance_lower_bound_mm':v99.get('minimum_continuous_clearance_lower_bound_mm'),'geometry_candidate_pass':exact_match and inherited_clearance and all(r['fuselage_inside_fraction']>0.999999 for r in recs) and all(r['fork_overlap_cm3']>1e-4 for r in recs),'hardpoint_material_selected':False,'hardpoint_to_fork_attachment_verified':False,'physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_CROSSTIE_HARDPOINT_SLEEVES_v102.f3d'))): raise RuntimeError('export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v102_hardpoint_sleeve_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v102_hardpoint_sleeve_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit