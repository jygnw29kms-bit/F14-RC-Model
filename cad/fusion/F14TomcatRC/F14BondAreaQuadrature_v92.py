"""v92: conservative pointwise/area-weighted bond-area lower bound for the final v89 insert."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def _cross_mag(a,b):
    x=a.y*b.z-a.z*b.y; y=a.z*b.x-a.x*b.z; z=a.x*b.y-a.y*b.x
    return math.sqrt(x*x+y*y+z*z)

def _sample_face(app, face, skin, ycut_mm, gap_mm, n):
    ev=face.evaluator; pr=ev.parametricRange()
    u0,u1=pr.minPoint.x,pr.maxPoint.x; v0,v1=pr.minPoint.y,pr.maxPoint.y
    du=(u1-u0)/n; dv=(v1-v0)/n
    est_total_cm2=0.0; est_axial_cm2=0.0; est_usable_cm2=0.0
    valid=0; gap_min=1e99; gap_max=0.0
    for iu in range(n):
        u=u0+(iu+0.5)*du
        for iv in range(n):
            v=v0+(iv+0.5)*dv; par=adsk.core.Point2D.create(u,v)
            if not ev.isParameterOnFace(par): continue
            ok,p=ev.getPointAtParameter(par)
            if not ok: continue
            ok,pu,pv=ev.getFirstDerivative(par)
            if not ok: continue
            dA=_cross_mag(pu,pv)*abs(du*dv)
            if not math.isfinite(dA) or dA<=0: continue
            valid+=1; est_total_cm2+=dA
            if p.y*10.0 <= ycut_mm+1e-9:
                est_axial_cm2+=dA
                g=app.measureManager.measureMinimumDistance(p,skin).value*10.0
                gap_min=min(gap_min,g); gap_max=max(gap_max,g)
                if g <= gap_mm+1e-9: est_usable_cm2+=dA
    exact_mm2=face.area*100.0
    total_est_mm2=est_total_cm2*100.0; axial_est_mm2=est_axial_cm2*100.0; usable_est_mm2=est_usable_cm2*100.0
    frac=0.0 if total_est_mm2<=0 else max(0.0,min(1.0,usable_est_mm2/total_est_mm2))
    axial_frac=0.0 if total_est_mm2<=0 else max(0.0,min(1.0,axial_est_mm2/total_est_mm2))
    return {'resolution':n,'valid_samples':valid,'exact_face_area_mm2':exact_mm2,'estimated_total_area_mm2':total_est_mm2,'estimated_axial_area_mm2':axial_est_mm2,'estimated_usable_area_mm2':usable_est_mm2,'usable_fraction_of_face':frac,'axial_fraction_of_face':axial_frac,'gap_min_mm':None if gap_min==1e99 else gap_min,'gap_max_mm':gap_max if gap_min!=1e99 else None}

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v92_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if hashlib.sha256(open(src['v91_audit_path'],'rb').read()).hexdigest()!=src['v91_audit_sha256']: raise RuntimeError('v91 audit hash mismatch')
    v91=json.load(open(src['v91_audit_path'],encoding='utf-8'))
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    insert=None; skin=None
    for i in range(root.bRepBodies.count):
        b=root.bRepBodies.item(i)
        if b.name=='CANDIDATE_OUTER_INSERT_MFG_ENDPOINT_CLEAR_v89': insert=b
        elif b.name=='CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS': skin=b
    if not insert or not skin: raise RuntimeError('Missing v89 insert/inner skin')
    old_candidates=[x for x in v91['faces'] if x['skin_gap_mm']<=float(src['skin_gap_max_mm'])]
    old_candidates.sort(key=lambda x:x['area_mm2'],reverse=True)
    old_total=sum(x['area_mm2'] for x in old_candidates); target=old_total*float(src['dominant_area_fraction'])
    selected=[]; acc=0.0
    for x in old_candidates:
        selected.append(x); acc+=x['area_mm2']
        if acc>=target: break
    resolutions=[int(x) for x in src['resolutions']]
    records=[]; lower_total=0.0; exact_selected=0.0
    for old in selected:
        idx=int(old['face_index'])
        if idx<0 or idx>=insert.faces.count: raise RuntimeError('Face index out of range '+str(idx))
        f=insert.faces.item(idx); exact=f.area*100.0; exact_selected+=exact
        samples=[_sample_face(app,f,skin,float(src['axial_y_max_mm']),float(src['skin_gap_max_mm']),n) for n in resolutions]
        fractions=[s['usable_fraction_of_face'] for s in samples]
        lower_frac=min(fractions) if fractions else 0.0
        credit=exact*lower_frac; lower_total+=credit
        records.append({'face_index':idx,'v91_face_area_mm2':old['area_mm2'],'fusion_exact_face_area_mm2':exact,'v91_min_gap_mm':old['skin_gap_mm'],'v91_point_y_mm':old['sample_y_mm'],'samples':samples,'credited_usable_fraction':lower_frac,'credited_usable_area_mm2':credit})
    force=float(src['torsion_sf3_force_N']); shear=force/lower_total if lower_total>0 else None
    audit={'status':'V92_POINTWISE_BOND_AREA_LOWER_BOUND','source':src,'method':{'description':'dominant v91 candidate faces only; pointwise axial clipping and skin-gap test using UV midpoint quadrature at two resolutions; smaller usable fraction credited per face','selected_v91_faces':len(selected),'selected_v91_area_mm2':acc,'selected_fraction_of_v91_candidate_area':acc/old_total if old_total else 0.0,'ignored_v91_candidate_area_mm2':max(0.0,old_total-acc),'resolutions':resolutions},'v91_claimed_candidate_area_mm2':old_total,'selected_exact_face_area_mm2':exact_selected,'conservative_usable_bond_area_mm2':lower_total,'sf3_equivalent_force_N':force,'required_average_shear_on_lower_bound_MPa':shear,'records':records,'pointwise_area_lower_bound_established':lower_total>0,'adhesive_allowable_verified':False,'coupon_verified':False,'peel_stress_verified':False,'torsion_transfer_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    json.dump(audit,open(os.path.join(outdir,'F14_v92_pointwise_bond_area_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v92_pointwise_bond_area_review.png'),1600,1000)
    if prior: prior.activate()
    return audit