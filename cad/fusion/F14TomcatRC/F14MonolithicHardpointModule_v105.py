"""v105: union lower fork and front/rear hardpoint tails into one structural module per side."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def rmax_xy(body,px,py):
    bb=body.boundingBox; xs=[bb.minPoint.x*10,bb.maxPoint.x*10]; ys=[bb.minPoint.y*10,bb.maxPoint.y*10]
    return max(math.hypot(x-px,y-py) for x in xs for y in ys)

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v105_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v103 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get(); found={}
    for i in range(orig.rootComponent.bRepBodies.count):
        b=orig.rootComponent.bRepBodies.item(i)
        if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29' or b.name.startswith('ENG_WINGBOX_FORK_LOWER_') or b.name.startswith('HARDPOINT_TAIL_') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_') or b.name.startswith('ENG_ROOT_LUG_'):
            found[b.name]=temp.copy(b)
    req=['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','HARDPOINT_TAIL_FRONT_R_v103','HARDPOINT_TAIL_REAR_R_v103','HARDPOINT_TAIL_FRONT_L_v103','HARDPOINT_TAIL_REAR_L_v103','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19']
    miss=[n for n in req if n not in found]
    if miss: raise RuntimeError('missing bodies '+repr(miss))
    def wing(lab): return next(v for k,v in found.items() if k.startswith('SOURCE_GRUMMAN_BASIC_WING_'+lab))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_MONOLITHIC_LOWER_HARDPOINT_MODULES_v105'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    fus=root.bRepBodies.add(temp.copy(found['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'])); fus.name='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'
    modules={}; records=[]
    for lab in ('R','L'):
        fork=temp.copy(found['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31'])
        source_names=['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31','HARDPOINT_TAIL_FRONT_'+lab+'_v103','HARDPOINT_TAIL_REAR_'+lab+'_v103']
        for n in source_names[1:]:
            if not temp.booleanOperation(fork,temp.copy(found[n]),adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('module union failed '+lab+' '+n)
        mod=root.bRepBodies.add(fork); mod.name='MONOLITHIC_LOWER_HARDPOINT_'+lab+'_v105'; modules[lab]=mod
        mv=mod.volume; q=temp.copy(mod); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=q.volume if ok and q.isValid else 0.0
        preserv=[]
        for n in source_names:
            q=temp.copy(found[n]); ok=temp.booleanOperation(q,temp.copy(mod),adsk.fusion.BooleanTypes.DifferenceBooleanType); rem=q.volume if ok and q.isValid else 0.0
            preserv.append({'source':n,'missing_from_module_cm3':rem,'preserved':rem<1e-7})
        bb=mod.boundingBox
        records.append({'side':lab,'module':mod.name,'volume_cm3':mv,'bbox_mm':{'x':[bb.minPoint.x*10,bb.maxPoint.x*10],'y':[bb.minPoint.y*10,bb.maxPoint.y*10],'z':[bb.minPoint.z*10,bb.maxPoint.z*10]},'fuselage_inside_fraction':iv/mv if mv else 0.0,'source_preservation':preserv})
    # continuous sweep screen of both moving wing/root-lug bodies against both monolithic modules
    px,py,pz=613.1323905812828,125.20927023775282,187.59240693460868; step=float(src['sweep_step_deg']); pairs={}; sample_count=0
    n=int(round((float(src['sweep_max_deg'])-float(src['sweep_min_deg']))/step))
    for ii in range(n+1):
        sw=float(src['sweep_min_deg'])+ii*step
        for lab,sgn in (('R',1),('L',-1)):
            ang=-sgn*math.radians(sw-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sgn*py),mm(pz)))
            for mov,kind in ((wing(lab),'outer_wing'),(found['ENG_ROOT_LUG_'+lab+'_v19'],'root_lug')):
                mc=temp.copy(mov); temp.transform(mc,rot); sample_count+=1
                for mlab,mod in modules.items():
                    key=lab+'|'+kind+'|'+mlab
                    try: dist=app.measureManager.measureMinimumDistance(mc,mod).value*10.0
                    except:
                        s=root.bRepBodies.add(temp.copy(mc)); dist=app.measureManager.measureMinimumDistance(s,mod).value*10.0; s.deleteMe()
                    rec=pairs.setdefault(key,{'side':lab,'moving_kind':kind,'module_side':mlab,'minimum_sampled_clearance_mm':1e99,'at_sweep_deg':None})
                    if dist<rec['minimum_sampled_clearance_mm']:rec['minimum_sampled_clearance_mm']=dist;rec['at_sweep_deg']=sw
    cert=[]
    for k,rec in pairs.items():
        mov=wing(rec['side']) if rec['moving_kind']=='outer_wing' else found['ENG_ROOT_LUG_'+rec['side']+'_v19']; rr=rmax_xy(mov,px,(1 if rec['side']=='R' else -1)*py); bound=2*rr*math.sin(math.radians(step)/4); margin=rec['minimum_sampled_clearance_mm']-bound; rec.update({'moving_rmax_mm':rr,'half_step_motion_bound_mm':bound,'continuous_clearance_lower_bound_mm':margin,'continuous_pass':margin>float(src['continuous_margin_required_mm'])});cert.append(rec)
    all_preserved=all(p['preserved'] for r in records for p in r['source_preservation']); inside=min(r['fuselage_inside_fraction'] for r in records); sweep=all(c['continuous_pass'] for c in cert)
    audit={'status':'V105_MONOLITHIC_LOWER_HARDPOINT_MODULE_GATE','source':src,'records':records,'all_source_geometry_preserved':all_preserved,'minimum_fuselage_inside_fraction':inside,'clearance_certificate':cert,'sampled_moving_states':sample_count,'continuous_sweep_clearance_pass':sweep,'minimum_continuous_clearance_lower_bound_mm':min(c['continuous_clearance_lower_bound_mm'] for c in cert),'monolithic_union_pass':all_preserved and all(r['volume_cm3']>0 for r in records),'geometry_candidate_pass':all_preserved and inside>0.999999 and sweep,'material_system_selected':False,'material_allowable_verified':False,'proof_fixture_defined':False,'physical_proof_passed':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_MONOLITHIC_LOWER_HARDPOINT_MODULES_v105.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v105_monolithic_module_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v105_monolithic_module_review.png'),1600,1000)
    try:doc.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit