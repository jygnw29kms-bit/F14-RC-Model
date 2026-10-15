"""v137: search a source-contained two-segment inlet centerline without reducing flow area."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def cone(temp,a,b,d0,d1):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(a['x']),mm(a['y']),mm(a['z'])),mm(d0/2),adsk.core.Point3D.create(mm(b['x']),mm(b['y']),mm(b['z'])),mm(d1/2))

def contained(temp,body,tool):
    total=tool.volume; q=temp.copy(tool)
    ok=temp.booleanOperation(q,temp.copy(body),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=min(total,q.volume) if ok and q.isValid else 0.0
    return max(0.0,total-inside), inside/total if total else 0.0

def interp_d(d0,d1,x,x0,x1):
    t=(x-x0)/(x1-x0); return d0+t*(d1-d0)

def score(temp,body,D,M,F,d0,d1):
    dm=interp_d(d0,d1,M['x'],D['x'],F['x'])
    a=cone(temp,D,M,d0,dm); b=cone(temp,M,F,dm,d1)
    oa,fa=contained(temp,body,a); ob,fb=contained(temp,body,b)
    return {'mid':dict(M),'mid_outer_diameter_mm':dm,'outside_cm3':oa+ob,'min_fraction':min(fa,fb),'segments':[{'outside_cm3':oa,'fraction':fa},{'outside_cm3':ob,'fraction':fb}]}

def frange(a,b,s):
    n=int(round((b-a)/s)); return [a+i*s for i in range(n+1)]

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v136_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['source_path'],'rb').read()).hexdigest()!=cfg['source_sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])): raise RuntimeError('import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    body=next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count) if root.bRepBodies.item(i).name=='SOURCE_SILHOUETTE_GUIDED_AFT_v135'),None)
    if body is None: raise RuntimeError('v135 body missing')
    temp=adsk.fusion.TemporaryBRepManager.get(); D=dict(cfg['D_center_local_mm']); F=dict(cfg['fan_face_center_local_mm']); duct=cfg['duct']
    D={k:float(v) for k,v in D.items()}; F={k:float(v) for k,v in F.items()}; d0=float(duct['D_outer_diameter_mm']); d1=float(duct['fan_outer_diameter_mm'])
    coarse=[]
    for x in [615.0,625.0,635.0]:
        for y in frange(54.0,66.0,2.0):
            for z in frange(-12.0,0.0,2.0):
                coarse.append(score(temp,body,D,{'x':x,'y':y,'z':z},F,d0,d1))
    coarse.sort(key=lambda r:(r['outside_cm3'],-r['min_fraction']))
    seed=coarse[0]; sm=seed['mid']; refined=[]
    for x in [sm['x']-2.5,sm['x'],sm['x']+2.5]:
        for y in frange(sm['y']-2.0,sm['y']+2.0,0.5):
            for z in frange(sm['z']-2.0,sm['z']+2.0,0.5):
                refined.append(score(temp,body,D,{'x':x,'y':y,'z':z},F,d0,d1))
    refined.sort(key=lambda r:(r['outside_cm3'],-r['min_fraction']))
    best=refined[0]
    # Bilateral and inner-flow validation for the selected path.
    validations=[]
    for lab,sgn in [('R',1),('L',-1)]:
        dD={'x':D['x'],'y':sgn*abs(D['y']),'z':D['z']}; dF={'x':F['x'],'y':sgn*abs(F['y']),'z':F['z']}; dM={'x':best['mid']['x'],'y':sgn*abs(best['mid']['y']),'z':best['mid']['z']}
        odM=best['mid_outer_diameter_mm']; idM=interp_d(float(duct['D_inner_diameter_mm']),float(duct['fan_inner_diameter_mm']),dM['x'],dD['x'],dF['x'])
        out1=cone(temp,dD,dM,d0,odM); out2=cone(temp,dM,dF,odM,d1)
        in1=cone(temp,dD,dM,float(duct['D_inner_diameter_mm']),idM); in2=cone(temp,dM,dF,idM,float(duct['fan_inner_diameter_mm']))
        vals=[]
        for kind,obj in [('outer_1',out1),('outer_2',out2),('flow_1',in1),('flow_2',in2)]:
            outside,fraction=contained(temp,body,obj); vals.append({'kind':kind,'outside_cm3':outside,'fraction':fraction})
        validations.append({'side':lab,'records':vals,'pass':all(v['outside_cm3']<=1e-5 for v in vals)})
    bilateral=all(v['pass'] for v in validations)
    # Geometry diagnostics.
    m=best['mid']
    def angle(a,b): return math.degrees(math.atan2(math.hypot(b['y']-a['y'],b['z']-a['z']),b['x']-a['x']))
    path={'D_to_mid_angle_deg':angle(D,m),'mid_to_fan_angle_deg':angle(m,F),'mid':m}
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_INLET_PATH_SEARCH_v137'
    rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; rr=rd.rootComponent
    rb=rr.bRepBodies.add(temp.copy(body)); rb.name=body.name
    for lab,sgn in [('R',1),('L',-1)]:
        dD={'x':D['x'],'y':sgn*abs(D['y']),'z':D['z']}; dF={'x':F['x'],'y':sgn*abs(F['y']),'z':F['z']}; dM={'x':m['x'],'y':sgn*abs(m['y']),'z':m['z']}; dm=best['mid_outer_diameter_mm']
        for idx,obj in enumerate([cone(temp,dD,dM,d0,dm),cone(temp,dM,dF,dm,d1)],1):
            q=rr.bRepBodies.add(obj); q.name=f'DUCT_OUTER_{lab}_{idx}_v137'
    audit={'status':'V137_INLET_CENTERLINE_PATH_SEARCH','source_v136':cfg,'coarse_count':len(coarse),'refined_count':len(refined),
           'best':best,'top20':refined[:20],'bilateral_validation':validations,'bilateral_containment_pass':bilateral,
           'path_geometry':path,'flow_area_preserved':bool(duct['minimum_flow_area_policy_pass']),
           'requires_smooth_v138_loft':True,'geometry_candidate_pass':bilateral and bool(duct['minimum_flow_area_policy_pass']),
           'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INLET_PATH_SEARCH_v137.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v137_inlet_path_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v137_inlet_path_review.png'),1600,1000)
    try: review.close(False)
    except: pass
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit
