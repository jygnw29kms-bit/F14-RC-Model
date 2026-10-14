"""v104: survey the real fork/hardpoint overlap before designing a captured pocket."""
import adsk.core, adsk.fusion, json, os, hashlib

def bb(b):
    q=b.boundingBox
    return {'x_mm':[q.minPoint.x*10,q.maxPoint.x*10],'y_mm':[q.minPoint.y*10,q.maxPoint.y*10],'z_mm':[q.minPoint.z*10,q.maxPoint.z*10],'dx_mm':(q.maxPoint.x-q.minPoint.x)*10,'dy_mm':(q.maxPoint.y-q.minPoint.y)*10,'dz_mm':(q.maxPoint.z-q.minPoint.z)*10}

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v104_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v103 import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get()
    bodies={root.bRepBodies.item(i).name:root.bRepBodies.item(i) for i in range(root.bRepBodies.count)}
    recs=[]
    for fa in ('FRONT','REAR'):
        for lab in ('R','L'):
            cn='HARDPOINT_TAIL_'+fa+'_'+lab+'_v103'; fn='ENG_WINGBOX_FORK_LOWER_'+lab+'_v31'; rn='ENG_RISER_CIRCULAR_'+fa+'_'+lab+'_v99'
            cand=bodies[cn]; fork=bodies[fn]; ris=bodies[rn]
            inter=temp.copy(cand)
            if not temp.booleanOperation(inter,temp.copy(fork),adsk.fusion.BooleanTypes.IntersectionBooleanType): raise RuntimeError('intersection failed '+cn)
            ib=root.bRepBodies.add(inter); ib.name='SURVEY_OVERLAP_'+fa+'_'+lab+'_v104'
            inter_rec={'volume_cm3':ib.volume,'bbox':bb(ib)}
            # Added tail only = candidate minus original riser.
            tail=temp.copy(cand)
            if not temp.booleanOperation(tail,temp.copy(ris),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('tail diff failed '+cn)
            tb=root.bRepBodies.add(tail); tb.name='SURVEY_ADDED_TAIL_'+fa+'_'+lab+'_v104'
            recs.append({'frame':fa,'side':lab,'candidate_bbox':bb(cand),'fork_bbox':bb(fork),'source_riser_bbox':bb(ris),'added_tail_bbox':bb(tb),'added_tail_volume_cm3':tb.volume,'fork_candidate_overlap':inter_rec})
    audit={'status':'V104_FORK_HARDPOINT_CAPTURE_SURVEY','source':src,'records':recs,'minimum_overlap_dz_mm':min(r['fork_candidate_overlap']['bbox']['dz_mm'] for r in recs),'maximum_overlap_dz_mm':max(r['fork_candidate_overlap']['bbox']['dz_mm'] for r in recs),'capture_box_required':True,'pocket_geometry_designed':False,'structural_capacity_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); json.dump(audit,open(os.path.join(outdir,'F14_v104_fork_capture_survey.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v104_fork_capture_survey.png'),1600,1000)
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit