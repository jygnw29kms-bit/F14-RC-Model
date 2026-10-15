"""v134: compare v133 aft-loft slices against Figure 3.15 plan/side silhouette constraints."""
import adsk.core, adsk.fusion, json, os, hashlib

def mm(v): return v/10.0

def slab(temp,x,t=0.10):
    c=adsk.core.Point3D.create(mm(x),0,0)
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(
        c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),
        mm(t),mm(500.0),mm(500.0)))

def slice_bounds(temp,body,x,t):
    q=temp.copy(body)
    ok=temp.booleanOperation(q,slab(temp,x,t),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    if not ok or not q.isValid or q.volume<=0:
        return None
    b=q.boundingBox
    return {'y_min_mm':b.minPoint.y*10,'y_max_mm':b.maxPoint.y*10,
            'z_min_mm':b.minPoint.z*10,'z_max_mm':b.maxPoint.z*10,'volume_cm3':q.volume}

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument
    base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v134_section_inputs.json'),encoding='utf-8'))
    src=cfg['candidate_v133']['path']
    if hashlib.sha256(open(src,'rb').read()).hexdigest()!=cfg['candidate_v133']['sha256']:
        raise RuntimeError('v133 source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src)):
        raise RuntimeError('v133 import failed')
    imported=app.activeDocument
    design=adsk.fusion.Design.cast(app.activeProduct)
    root=design.rootComponent
    body=next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count)
               if root.bRepBodies.item(i).name=='SOURCE_BACKED_AFT_NACELLE_MATCHED_v133'),None)
    if body is None:
        raise RuntimeError('v133 source body missing: '+repr([root.bRepBodies.item(i).name for i in range(root.bRepBodies.count)]))
    temp=adsk.fusion.TemporaryBRepManager.get()
    bb=body.boundingBox; xmin=bb.minPoint.x*10; xmax=bb.maxPoint.x*10
    t=float(cfg['slice_thickness_mm'])
    plan=[]; side=[]
    for s in cfg['plan_samples']:
        x=float(s['x_model_mm'])
        if x<xmin-0.2 or x>xmax+0.2: continue
        m=slice_bounds(temp,body,x,t)
        if m is None: continue
        measured=max(abs(m['y_min_mm']),abs(m['y_max_mm']))
        err=measured-float(s['expected_half_width_mm'])
        plan.append({'x_model_mm':x,'expected_half_width_mm':s['expected_half_width_mm'],
                     'measured_half_width_mm':measured,'error_mm':err,'abs_error_mm':abs(err),'slice':m})
    for s in cfg['side_samples']:
        x=float(s['x_model_mm'])
        if x<xmin-0.2 or x>xmax+0.2: continue
        m=slice_bounds(temp,body,x,t)
        if m is None: continue
        et=m['z_max_mm']-float(s['expected_z_top_mm'])
        eb=m['z_min_mm']-float(s['expected_z_bottom_mm'])
        side.append({'kind':s['kind'],'name':s.get('name'),'x_model_mm':x,
                     'expected_z_top_mm':s['expected_z_top_mm'],'measured_z_top_mm':m['z_max_mm'],
                     'top_error_mm':et,'top_abs_error_mm':abs(et),
                     'expected_z_bottom_mm':s['expected_z_bottom_mm'],'measured_z_bottom_mm':m['z_min_mm'],
                     'bottom_error_mm':eb,'bottom_abs_error_mm':abs(eb),'slice':m})
    lim=cfg['acceptance']
    pmax=max((r['abs_error_mm'] for r in plan),default=999)
    tmax=max((r['top_abs_error_mm'] for r in side),default=999)
    bmax=max((r['bottom_abs_error_mm'] for r in side),default=999)
    audit={'status':'V134_SOURCE_SILHOUETTE_AUDIT','source':cfg,'candidate_bounds_mm':{'x':[xmin,xmax]},
           'plan_records':plan,'side_records':side,
           'max_half_width_abs_error_mm':pmax,'max_top_abs_error_mm':tmax,'max_bottom_abs_error_mm':bmax,
           'plan_pass':bool(plan) and pmax<=float(lim['half_width_abs_error_mm']),
           'side_top_pass':bool(side) and tmax<=float(lim['z_top_abs_error_mm']),
           'side_bottom_pass':bool(side) and bmax<=float(lim['z_bottom_abs_error_mm']),
           'source_silhouette_gate_pass':False,
           'exterior_fidelity_freeze':False,'print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    audit['source_silhouette_gate_pass']=audit['plan_pass'] and audit['side_top_pass'] and audit['side_bottom_pass']
    os.makedirs(outdir,exist_ok=True)
    json.dump(audit,open(os.path.join(outdir,'F14_v134_source_silhouette_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit()
    app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v134_source_silhouette_review.png'),1600,1000)
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit
