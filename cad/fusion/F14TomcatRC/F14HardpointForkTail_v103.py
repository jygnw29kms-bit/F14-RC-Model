"""v103: extend v99 circular crosstie hardpoint sleeves with a solid 8 mm fork tail."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def box(temp,x0,x1,y0,y1,z0,z1):
    c=adsk.core.Point3D.create(mm((x0+x1)/2),mm((y0+y1)/2),mm((z0+z1)/2))
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(x1-x0),mm(y1-y0),mm(z1-z0)))

def rmax_xy(body,px,py):
    bb=body.boundingBox; xs=[bb.minPoint.x*10,bb.maxPoint.x*10]; ys=[bb.minPoint.y*10,bb.maxPoint.y*10]
    return max(math.hypot(x-px,y-py) for x in xs for y in ys)

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v103_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v99 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get(); found={}
    for i in range(orig.rootComponent.bRepBodies.count):
        b=orig.rootComponent.bRepBodies.item(i)
        if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29' or b.name.startswith('ENG_RISER_CIRCULAR_') or b.name.startswith('ENG_WINGBOX_FORK_LOWER_') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_') or b.name.startswith('ENG_ROOT_LUG_'):
            found[b.name]=temp.copy(b)
    req=['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','ENG_RISER_CIRCULAR_FRONT_R_v99','ENG_RISER_CIRCULAR_FRONT_L_v99','ENG_RISER_CIRCULAR_REAR_R_v99','ENG_RISER_CIRCULAR_REAR_L_v99','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19']
    miss=[n for n in req if n not in found]
    if miss: raise RuntimeError('missing bodies '+repr(miss))
    def wing(lab):
        return next(v for k,v in found.items() if k.startswith('SOURCE_GRUMMAN_BASIC_WING_'+lab))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_EXTENDED_HARDPOINT_FORK_TAILS_v103'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; bodies={}
    for n,c in found.items(): b=root.bRepBodies.add(temp.copy(c)); b.name=n; bodies[n]=b
    fus=bodies['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29']; candidates=[]; recs=[]
    for fa in ('FRONT','REAR'):
        for lab,sgn in (('R',1),('L',-1)):
            rn='ENG_RISER_CIRCULAR_'+fa+'_'+lab+'_v99'; ris=bodies[rn]; rb=ris.boundingBox
            x0,x1=rb.minPoint.x*10,rb.maxPoint.x*10; z0,z1=rb.minPoint.z*10,rb.maxPoint.z*10
            if sgn>0: y0,y1=rb.minPoint.y*10,float(src['tail_outer_abs_y_mm'])
            else: y0,y1=-float(src['tail_outer_abs_y_mm']),rb.maxPoint.y*10
            cand=temp.copy(ris)
            # Tail starts with tiny overlap to make robust boolean union; tube already ends before the tail.
            if sgn>0: tail=box(temp,x0,x1,rb.maxPoint.y*10-0.1,y1,z0,z1)
            else: tail=box(temp,x0,x1,y0,rb.minPoint.y*10+0.1,z0,z1)
            if not temp.booleanOperation(cand,tail,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('tail union failed '+rn)
            cb=root.bRepBodies.add(cand); cb.name='HARDPOINT_TAIL_'+fa+'_'+lab+'_v103'; candidates.append(cb)
            cv=cb.volume; q=temp.copy(cb); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=q.volume if ok and q.isValid else 0.0
            fork=bodies['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31']; q=temp.copy(cb); ok=temp.booleanOperation(q,temp.copy(fork),adsk.fusion.BooleanTypes.IntersectionBooleanType); fv=q.volume if ok and q.isValid else 0.0
            fb=fork.boundingBox; bb=cb.boundingBox; yov=max(0,min(bb.maxPoint.y,fb.maxPoint.y)-max(bb.minPoint.y,fb.minPoint.y))*10
            # Source riser must remain wholly embedded in candidate; this proves bore/socket geometry was not removed.
            q=temp.copy(ris); ok=temp.booleanOperation(q,temp.copy(cb),adsk.fusion.BooleanTypes.DifferenceBooleanType); missing=q.volume if ok and q.isValid else 0.0
            recs.append({'candidate':cb.name,'source_riser':rn,'volume_cm3':cv,'source_riser_missing_from_candidate_cm3':missing,'source_socket_preserved':missing<1e-7,'fuselage_inside_fraction':iv/cv if cv else 0,'fork_overlap_cm3':fv,'fork_y_overlap_mm':yov,'bbox_y_mm':[bb.minPoint.y*10,bb.maxPoint.y*10]})
    # Continuous sweep clearance against the new tails only.
    pivot=[613.1323905812828,125.20927023775282,187.59240693460868]; px,py,pz=pivot; step=float(src['sweep_step_deg']); pairs={}; sample_count=0
    n=int(round((float(src['sweep_max_deg'])-float(src['sweep_min_deg']))/step))
    for ii in range(n+1):
        sw=float(src['sweep_min_deg'])+ii*step
        for lab,sgn in (('R',1),('L',-1)):
            ang=-sgn*math.radians(sw-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sgn*py),mm(pz)))
            movs=[(wing(lab),'outer_wing'),(bodies['ENG_ROOT_LUG_'+lab+'_v19'],'root_lug')]
            for mov,kind in movs:
                mc=temp.copy(mov); temp.transform(mc,rot); sample_count+=1
                for fp in candidates:
                    key=lab+'|'+kind+'|'+fp.name
                    try: dist=app.measureManager.measureMinimumDistance(mc,fp).value*10.0
                    except:
                        s=root.bRepBodies.add(temp.copy(mc)); dist=app.measureManager.measureMinimumDistance(s,fp).value*10.0; s.deleteMe()
                    rr=pairs.setdefault(key,{'side':lab,'moving_kind':kind,'fixed_part':fp.name,'minimum_sampled_clearance_mm':1e99,'at_sweep_deg':None})
                    if dist<rr['minimum_sampled_clearance_mm']: rr['minimum_sampled_clearance_mm']=dist; rr['at_sweep_deg']=sw
    cert=[]
    for k,rec in pairs.items():
        mov=wing(rec['side']) if rec['moving_kind']=='outer_wing' else bodies['ENG_ROOT_LUG_'+rec['side']+'_v19']; rr=rmax_xy(mov,px,(1 if rec['side']=='R' else -1)*py); bound=2*rr*math.sin(math.radians(step)/4); margin=rec['minimum_sampled_clearance_mm']-bound; rec.update({'moving_rmax_mm':rr,'half_step_motion_bound_mm':bound,'continuous_clearance_lower_bound_mm':margin,'continuous_pass':margin>float(src['continuous_margin_required_mm'])}); cert.append(rec)
    audit={'status':'V103_EXTENDED_HARDPOINT_FORK_TAIL_GATE','source':src,'records':recs,'all_source_sockets_preserved':all(r['source_socket_preserved'] for r in recs),'minimum_fuselage_inside_fraction':min(r['fuselage_inside_fraction'] for r in recs),'minimum_fork_y_overlap_mm':min(r['fork_y_overlap_mm'] for r in recs),'all_fork_contacts':all(r['fork_overlap_cm3']>1e-4 for r in recs),'clearance_certificate':cert,'sampled_moving_states':sample_count,'continuous_sweep_clearance_pass':all(r['continuous_pass'] for r in cert),'minimum_continuous_clearance_lower_bound_mm':min(r['continuous_clearance_lower_bound_mm'] for r in cert),'geometry_candidate_pass':all(r['source_socket_preserved'] and r['fuselage_inside_fraction']>0.999999 and r['fork_y_overlap_mm']>=float(src['required_fork_overlap_mm'])-1e-6 and r['fork_overlap_cm3']>1e-4 for r in recs) and all(r['continuous_pass'] for r in cert),'hardpoint_material_selected':False,'hardpoint_to_fork_attachment_verified':False,'physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_EXTENDED_HARDPOINT_FORK_TAILS_v103.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v103_extended_hardpoint_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v103_extended_hardpoint_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit