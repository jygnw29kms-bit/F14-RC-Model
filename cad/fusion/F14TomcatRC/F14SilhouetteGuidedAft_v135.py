"""v135: source-silhouette-guided D/E/F aft loft with bilateral EDF and exterior audits."""
import adsk.core, adsk.fusion, json, os, hashlib

def mm(v): return v/10.0

def plane_x(comp,x):
    inp=comp.constructionPlanes.createInput()
    inp.setByOffset(comp.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x)))
    return comp.constructionPlanes.add(inp)

def add_profile(comp,x,pts,name):
    sk=comp.sketches.add(plane_x(comp,x)); sk.name=name
    pp=[sk.modelToSketchSpace(adsk.core.Point3D.create(mm(x),mm(y),mm(z))) for y,z in pts]
    lines=sk.sketchCurves.sketchLines
    for i in range(len(pp)):
        lines.addByTwoPoints(pp[i],pp[(i+1)%len(pp)])
    if sk.profiles.count<1: raise RuntimeError('no profile '+name)
    return sk.profiles.item(0)

def slab(temp,x,t=0.10):
    c=adsk.core.Point3D.create(mm(x),0,0)
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(t),mm(500),mm(500)))

def slice_bounds(temp,body,x,t):
    q=temp.copy(body)
    ok=temp.booleanOperation(q,slab(temp,x,t),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    if not ok or not q.isValid or q.volume<=0: return None
    b=q.boundingBox
    return {'y_min_mm':b.minPoint.y*10,'y_max_mm':b.maxPoint.y*10,'z_min_mm':b.minPoint.z*10,'z_max_mm':b.maxPoint.z*10}

def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2))

def cyl_containment(temp,solid,x0,L,y,z,d):
    c=cyl_x(temp,x0,x0+L,y,z,d); total=c.volume
    q=temp.copy(c)
    ok=temp.booleanOperation(q,temp.copy(solid),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=min(total,q.volume) if ok and q.isValid else 0.0
    return {'inside_cm3':inside,'outside_cm3':max(0,total-inside),'fraction':inside/total if total else 0.0}

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    profiles=json.load(open(os.path.join(base,'F14_v135_profile_set.json'),encoding='utf-8'))
    cons=json.load(open(os.path.join(base,'F14_v134_section_inputs.json'),encoding='utf-8'))
    if profiles['source_image_sha256']!=cons['source_image_sha256']:
        raise RuntimeError('v135/v134 source mismatch')
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name='F14_SOURCE_SILHOUETTE_GUIDED_AFT_v135'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent
    byname={p['name']:p for p in profiles['base_profiles']}
    for p in profiles['guide_profiles']: byname[p['name']]=p
    order=profiles['profile_order']
    li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    meta=[]
    for name in order:
        p=byname[name]
        li.loftSections.add(add_profile(root,float(p['x_mm']),p['points'],'V135_'+name))
        ys=[q[0] for q in p['points']]; zs=[q[1] for q in p['points']]
        meta.append({'name':name,'x_mm':p['x_mm'],'bounds_mm':{'y':[min(ys),max(ys)],'z':[min(zs),max(zs)]},
                     'guide':name.startswith('GUIDE_')})
    feat=root.features.loftFeatures.add(li)
    if not feat or feat.bodies.count!=1: raise RuntimeError('v135 loft failed')
    body=feat.bodies.item(0); body.name='SOURCE_SILHOUETTE_GUIDED_AFT_v135'
    temp=adsk.fusion.TemporaryBRepManager.get(); bb=body.boundingBox; xmin=bb.minPoint.x*10; xmax=bb.maxPoint.x*10
    t=float(cons['slice_thickness_mm']); plan=[]; side=[]
    for s in cons['plan_samples']:
        x=float(s['x_model_mm'])
        if x<xmin-0.2 or x>xmax+0.2: continue
        m=slice_bounds(temp,body,x,t)
        if not m: continue
        measured=max(abs(m['y_min_mm']),abs(m['y_max_mm'])); err=measured-float(s['expected_half_width_mm'])
        plan.append({'x_model_mm':x,'expected_half_width_mm':s['expected_half_width_mm'],'measured_half_width_mm':measured,
                     'error_mm':err,'abs_error_mm':abs(err)})
    for s in cons['side_samples']:
        x=float(s['x_model_mm'])
        if x<xmin-0.2 or x>xmax+0.2: continue
        m=slice_bounds(temp,body,x,t)
        if not m: continue
        et=m['z_max_mm']-float(s['expected_z_top_mm']); eb=m['z_min_mm']-float(s['expected_z_bottom_mm'])
        side.append({'kind':s['kind'],'name':s.get('name'),'x_model_mm':x,
                     'top_error_mm':et,'top_abs_error_mm':abs(et),'bottom_error_mm':eb,'bottom_abs_error_mm':abs(eb),
                     'expected_z_top_mm':s['expected_z_top_mm'],'measured_z_top_mm':m['z_max_mm'],
                     'expected_z_bottom_mm':s['expected_z_bottom_mm'],'measured_z_bottom_mm':m['z_min_mm']})
    lim=cons['acceptance']; pmax=max((r['abs_error_mm'] for r in plan),default=999); tmax=max((r['top_abs_error_mm'] for r in side),default=999); bmax=max((r['bottom_abs_error_mm'] for r in side),default=999)
    silhouette_pass=bool(plan) and bool(side) and pmax<=float(lim['half_width_abs_error_mm']) and tmax<=float(lim['z_top_abs_error_mm']) and bmax<=float(lim['z_bottom_abs_error_mm'])
    candidates=[]; L=73.5; d=55.6
    for x in [648.0,648.5,649.0,650.0,651.0,652.0,653.0,654.0]:
        for y in [63.5,64.0,64.5,65.0]:
            for z in [-12.0,-11.5,-11.0,-10.5,-10.0]:
                R=cyl_containment(temp,body,x,L,y,z,d); Lf=cyl_containment(temp,body,x,L,-y,z,d)
                candidates.append({'x_start_mm':x,'x_end_mm':x+L,'y_abs_mm':y,'z_mm':z,'right':R,'left':Lf,
                                   'worst_outside_cm3':max(R['outside_cm3'],Lf['outside_cm3']),'worst_fraction':min(R['fraction'],Lf['fraction'])})
    candidates.sort(key=lambda r:(r['worst_outside_cm3'],-r['worst_fraction']))
    best=candidates[0]; best['bilateral_pass']=best['worst_outside_cm3']<=1e-5
    reserve=0.0; reserve_trials=[]
    if best['bilateral_pass']:
        for i in range(1,21):
            extra=i/10.0
            R=cyl_containment(temp,body,best['x_start_mm'],L,best['y_abs_mm'],best['z_mm'],d+2*extra)
            Lf=cyl_containment(temp,body,best['x_start_mm'],L,-best['y_abs_mm'],best['z_mm'],d+2*extra)
            worst=max(R['outside_cm3'],Lf['outside_cm3']); ok=worst<=1e-5
            reserve_trials.append({'extra_radial_mm':extra,'worst_outside_cm3':worst,'pass':ok})
            if ok: reserve=extra
            else: break
    for lab,sgn in [('R',1),('L',-1)]:
        b=root.bRepBodies.add(cyl_x(temp,best['x_start_mm'],best['x_end_mm'],sgn*best['y_abs_mm'],best['z_mm'],d))
        b.name='EDF_CLEAR_ENVELOPE_'+lab+'_v135'
    audit={'status':'V135_SILHOUETTE_GUIDED_AFT_GATE','source_image_sha256':cons['source_image_sha256'],'profiles':meta,
           'plan_records':plan,'side_records':side,'max_half_width_abs_error_mm':pmax,'max_top_abs_error_mm':tmax,'max_bottom_abs_error_mm':bmax,
           'source_silhouette_gate_pass':silhouette_pass,'edf_best':best,'edf_extra_radial_reserve_mm':reserve,'edf_reserve_trials':reserve_trials,
           'bilateral_edf_pass':best['bilateral_pass'],'geometry_candidate_pass':silhouette_pass and best['bilateral_pass'],
           'source_fidelity':'D/E/F traced profiles plus silhouette-constrained interpolated guide profiles; guide profiles are not independently measured sections',
           'exterior_fidelity_freeze':False,'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_SOURCE_SILHOUETTE_GUIDED_AFT_v135.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v135_silhouette_guided_aft_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v135_silhouette_guided_aft_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit
