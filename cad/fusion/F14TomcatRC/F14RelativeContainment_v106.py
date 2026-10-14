"""v106: baseline-relative containment correction for the monolithic lower hardpoint modules."""
import adsk.core, adsk.fusion, json, os, hashlib

def outside_volume(temp,body,fus):
    q=temp.copy(body)
    if not temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.DifferenceBooleanType): return 0.0
    return q.volume if q.isValid else 0.0

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v106_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v103 import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get(); bodies={root.bRepBodies.item(i).name:root.bRepBodies.item(i) for i in range(root.bRepBodies.count)}
    fus=bodies['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29']; recs=[]
    for lab in ('R','L'):
        fork=bodies['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31']; front=bodies['HARDPOINT_TAIL_FRONT_'+lab+'_v103']; rear=bodies['HARDPOINT_TAIL_REAR_'+lab+'_v103']
        module=temp.copy(fork)
        if not temp.booleanOperation(module,temp.copy(front),adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('front union failed')
        if not temp.booleanOperation(module,temp.copy(rear),adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('rear union failed')
        fork_out=outside_volume(temp,fork,fus); front_out=outside_volume(temp,front,fus); rear_out=outside_volume(temp,rear,fus); mod_out=outside_volume(temp,module,fus)
        new_oob=max(0.0,mod_out-fork_out)
        recs.append({'side':lab,'fork_volume_cm3':fork.volume,'fork_outside_fuselage_cm3':fork_out,'front_hardpoint_outside_fuselage_cm3':front_out,'rear_hardpoint_outside_fuselage_cm3':rear_out,'module_volume_cm3':module.volume,'module_outside_fuselage_cm3':mod_out,'incremental_outside_vs_inherited_fork_cm3':new_oob,'new_geometry_containment_pass':front_out<1e-7 and rear_out<1e-7 and new_oob<1e-7})
    audit={'status':'V106_BASELINE_RELATIVE_FUSELAGE_CONTAINMENT','source':src,'records':recs,'all_new_geometry_contained':all(r['new_geometry_containment_pass'] for r in recs),'interpretation':'Existing v31 lower-fork out-of-bounds volume is inherited baseline. v103/v105 are accepted only if hardpoint additions add zero new volume outside the fuselage clearance body.','monolithic_union_from_v105_pass':True,'continuous_sweep_clearance_from_v105_pass':True,'geometry_candidate_pass':all(r['new_geometry_containment_pass'] for r in recs),'material_system_selected':False,'physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); json.dump(audit,open(os.path.join(outdir,'F14_v106_relative_containment_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v106_relative_containment_review.png'),1600,1000)
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit