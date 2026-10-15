"""v133: correspondence-controlled source D/E/F loft and bilateral EDF clearance proof."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def frange(a,b,s):
    n=int((b-a)/s+1e-9)
    return [a+i*s for i in range(n+1)]

def plane_x(comp,x):
    inp=comp.constructionPlanes.createInput()
    inp.setByOffset(comp.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x)))
    return comp.constructionPlanes.add(inp)

def model_point(sk,x,y,z):
    return sk.modelToSketchSpace(adsk.core.Point3D.create(mm(x),mm(y),mm(z)))

def signed_area(pts):
    return 0.5*sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))

def resample_closed(pts,n=96):
    pts=list(pts)
    if signed_area(pts)<0:
        pts.reverse()
    seg=[]; total=0.0
    for i in range(len(pts)):
        a,b=pts[i],pts[(i+1)%len(pts)]
        L=math.hypot(b[0]-a[0],b[1]-a[1])
        seg.append(L); total+=L
    out=[]; j=0; acc=0.0
    for k in range(n):
        t=total*k/n
        while j<len(seg)-1 and acc+seg[j]<t:
            acc+=seg[j]; j+=1
        a,b=pts[j],pts[(j+1)%len(pts)]
        u=0.0 if seg[j]==0 else (t-acc)/seg[j]
        out.append((a[0]+u*(b[0]-a[0]),a[1]+u*(b[1]-a[1])))
    near=[i for i,p in enumerate(out) if abs(p[0])<=5.0]
    anchor=max(near,key=lambda i:out[i][1]) if near else max(range(n),key=lambda i:(-abs(out[i][0]),out[i][1]))
    return out[anchor:]+out[:anchor]

def add_profile(comp,x,pts,name):
    sk=comp.sketches.add(plane_x(comp,x)); sk.name=name
    pp=[model_point(sk,x,y,z) for y,z in pts]
    lines=sk.sketchCurves.sketchLines
    for i in range(len(pp)):
        lines.addByTwoPoints(pp[i],pp[(i+1)%len(pp)])
    if sk.profiles.count<1:
        raise RuntimeError('no profile '+name)
    return sk.profiles.item(0)

def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2))

def one(temp,solid,x0,L,y,z,d):
    c=cyl_x(temp,x0,x0+L,y,z,d); total=c.volume
    q=temp.copy(c)
    ok=temp.booleanOperation(q,temp.copy(solid),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=min(total,q.volume) if ok and q.isValid else 0.0
    return {'inside_cm3':inside,'outside_cm3':max(0,total-inside),'fraction':inside/total if total else 0.0}

def pair_eval(temp,solid,x0,L,y,z,d):
    R=one(temp,solid,x0,L,abs(y),z,d)
    Lf=one(temp,solid,x0,L,-abs(y),z,d)
    return {'x_start_mm':x0,'x_end_mm':x0+L,'y_abs_mm':abs(y),'z_mm':z,
            'right':R,'left':Lf,'worst_outside_cm3':max(R['outside_cm3'],Lf['outside_cm3']),
            'worst_fraction':min(R['fraction'],Lf['fraction'])}

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument
    base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v133_section_inputs.json'),encoding='utf-8'))
    common=float(cfg['common_scale_mm_per_pixel'])
    refside=float(cfg['reference_axis_side_pixel_y'])
    sections=[]
    for s in cfg['sections']:
        for key in ('contour','registration'):
            raw=open(s[key]['path'],'rb').read()
            if hashlib.sha256(raw).hexdigest()!=s[key]['sha256']:
                raise RuntimeError('hash mismatch '+s['name']+' '+key)
        c=json.load(open(s['contour']['path'],encoding='utf-8'))
        reg=json.load(open(s['registration']['path'],encoding='utf-8'))
        fit=float(reg.get('isotropic_multiplier',reg.get('isotropic_section_width_multiplier')))
        ax,ay=[float(v) for v in c['source_section_axis_pixel']]
        zaxis=(refside-float(s['axis_side_pixel_y']))*common
        rawpts=[((float(p[0])-ax)*common*fit,-(float(p[1])-ay)*common*fit+zaxis) for p in c['pixel_outline']]
        pts=resample_closed(rawpts,96)
        sections.append({'name':s['name'],'x_mm':float(s['x_mm']),'raw_count':len(rawpts),'pts':pts})
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name='F14_SOURCE_BACKED_AFT_NACELLE_CORRESPONDENCE_v133'
    design=adsk.fusion.Design.cast(app.activeProduct)
    design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent
    li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    meta=[]
    for s in sections:
        li.loftSections.add(add_profile(root,s['x_mm'],s['pts'],'SOURCE_'+s['name']+'_MATCHED_v133'))
        ys=[p[0] for p in s['pts']]; zs=[p[1] for p in s['pts']]
        meta.append({'name':s['name'],'x_mm':s['x_mm'],'raw_count':s['raw_count'],'resampled_count':len(s['pts']),
                     'signed_area_mm2':signed_area(s['pts']),'anchor_yz_mm':s['pts'][0],
                     'bounds_mm':{'y':[min(ys),max(ys)],'z':[min(zs),max(zs)]}})
    feat=root.features.loftFeatures.add(li)
    if not feat or feat.bodies.count!=1:
        raise RuntimeError('matched loft failed')
    aft=feat.bodies.item(0); aft.name='SOURCE_BACKED_AFT_NACELLE_MATCHED_v133'
    temp=adsk.fusion.TemporaryBRepManager.get()
    L=float(cfg['housing_length_mm']); d=float(cfg['clear_diameter_mm'])
    records=[]
    for x in frange(650.0,666.0,2.0):
        for y in frange(62.0,68.0,1.0):
            for z in frange(-14.0,-8.0,1.0):
                records.append(pair_eval(temp,aft,x,L,y,z,d))
    records.sort(key=lambda r:(r['worst_outside_cm3'],-r['worst_fraction']))
    seed=records[0]; refined=[]
    for x in frange(seed['x_start_mm']-2,seed['x_start_mm']+2,0.5):
        for y in frange(seed['y_abs_mm']-2,seed['y_abs_mm']+2,0.5):
            for z in frange(seed['z_mm']-2,seed['z_mm']+2,0.5):
                refined.append(pair_eval(temp,aft,x,L,y,z,d))
    refined.sort(key=lambda r:(r['worst_outside_cm3'],-r['worst_fraction']))
    best=refined[0]
    tol=float(cfg['containment_tolerance_cm3'])
    best['bilateral_pass']=best['worst_outside_cm3']<=tol
    reserve=0.0; trials=[]
    if best['bilateral_pass']:
        for i in range(1,21):
            extra=i/10.0
            q=pair_eval(temp,aft,best['x_start_mm'],L,best['y_abs_mm'],best['z_mm'],d+2*extra)
            ok=q['worst_outside_cm3']<=tol
            trials.append({'extra_radial_mm':extra,'worst_outside_cm3':q['worst_outside_cm3'],'pass':ok})
            if ok: reserve=extra
            else: break
    for lab,sgn in [('R',1),('L',-1)]:
        b=root.bRepBodies.add(cyl_x(temp,best['x_start_mm'],best['x_end_mm'],sgn*best['y_abs_mm'],best['z_mm'],d))
        b.name='EDF_CLEAR_ENVELOPE_'+lab+'_v133'
    audit={'status':'V133_MATCHED_SOURCE_LOFT_BILATERAL_EDF_GATE','source_image_sha256':cfg['source_image_sha256'],
           'sections':meta,'coarse_count':len(records),'refined_count':len(refined),'best':best,'top20':refined[:20],
           'extra_radial_reserve_mm':reserve,'reserve_trials':trials,'profile_correspondence_controlled':True,
           'bilateral_containment_verified':best['bilateral_pass'],
           'source_station_fidelity':'exact at D/E/F traced profiles; interpolation between stations remains CAD loft, not measured original surface',
           'geometry_candidate_pass':best['bilateral_pass'],'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_SOURCE_BACKED_AFT_NACELLE_MATCHED_v133.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v133_matched_source_aft_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v133_matched_source_aft_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit

