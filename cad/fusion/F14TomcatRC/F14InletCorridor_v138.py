"""v138: map the bilateral admissible inlet-center corridor and validate a multi-segment path."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2))

def cone(temp,a,b,d0,d1):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(a['x']),mm(a['y']),mm(a['z'])),mm(d0/2),adsk.core.Point3D.create(mm(b['x']),mm(b['y']),mm(b['z'])),mm(d1/2))

def outside(temp,body,obj):
    total=obj.volume; q=temp.copy(obj)
    ok=temp.booleanOperation(q,temp.copy(body),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=min(total,q.volume) if ok and q.isValid else 0.0
    return max(0.0,total-inside)

def lerp(a,b,t): return a+t*(b-a)

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v136_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['source_path'],'rb').read()).hexdigest()!=cfg['source_sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])): raise RuntimeError('import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    body=next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count) if root.bRepBodies.item(i).name=='SOURCE_SILHOUETTE_GUIDED_AFT_v135'),None)
    if body is None: raise RuntimeError('v135 body missing')
    temp=adsk.fusion.TemporaryBRepManager.get(); D={k:float(v) for k,v in cfg['D_center_local_mm'].items()}; F={k:float(v) for k,v in cfg['fan_face_center_local_mm'].items()}; duct=cfg['duct']
    d0=float(duct['D_outer_diameter_mm']); d1=float(duct['fan_outer_diameter_mm']); id0=float(duct['D_inner_diameter_mm']); id1=float(duct['fan_inner_diameter_mm'])
    xs=[D['x'],605.0,615.0,625.0,635.0,645.0,F['x']]
    stations=[]; chosen=[]
    for idx,x in enumerate(xs):
        t=(x-D['x'])/(F['x']-D['x']); target_y=lerp(D['y'],F['y'],t); target_z=lerp(D['z'],F['z'],t); d=lerp(d0,d1,t)
        if idx==0:
            candidates=[{'y':D['y'],'z':D['z'],'outside_cm3':0.0,'cost':0.0}]
        elif idx==len(xs)-1:
            candidates=[{'y':F['y'],'z':F['z'],'outside_cm3':0.0,'cost':0.0}]
        else:
            candidates=[]
            for yi in range(-4,5):
                y=target_y+yi*1.0
                for zi in range(-4,5):
                    z=target_z+zi*1.0
                    oR=outside(temp,body,cyl_x(temp,x-0.10,x+0.10,y,z,d))
                    oL=outside(temp,body,cyl_x(temp,x-0.10,x+0.10,-y,z,d))
                    o=max(oR,oL); cost=(y-target_y)**2+(z-target_z)**2
                    if o<=1e-6:
                        candidates.append({'y':y,'z':z,'outside_cm3':o,'cost':cost})
            candidates.sort(key=lambda q:(q['cost'],q['outside_cm3']))
            if not candidates:
                raise RuntimeError('no bilateral corridor center at x='+str(x))
        c=candidates[0]
        point={'x':x,'y':c['y'],'z':c['z'],'outer_diameter_mm':d,'inner_diameter_mm':lerp(id0,id1,t)}
        chosen.append(point)
        stations.append({'x_mm':x,'target_linear_center':{'y':target_y,'z':target_z},'outer_diameter_mm':d,'valid_count':len(candidates),'chosen':point,'top_candidates':candidates[:10]})
    segs=[]; bilateral=True
    for a,b in zip(chosen,chosen[1:]):
        vals=[]
        for lab,sgn in [('R',1),('L',-1)]:
            aa={'x':a['x'],'y':sgn*abs(a['y']),'z':a['z']}; bb={'x':b['x'],'y':sgn*abs(b['y']),'z':b['z']}
            outer=cone(temp,aa,bb,a['outer_diameter_mm'],b['outer_diameter_mm'])
            inner=cone(temp,aa,bb,a['inner_diameter_mm'],b['inner_diameter_mm'])
            oo=outside(temp,body,outer); oi=outside(temp,body,inner)
            vals.append({'side':lab,'outer_outside_cm3':oo,'flow_outside_cm3':oi})
            if oo>1e-5 or oi>1e-5: bilateral=False
        segs.append({'x0_mm':a['x'],'x1_mm':b['x'],'records':vals})
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_INLET_CORRIDOR_v138'
    rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; rr=rd.rootComponent
    rb=rr.bRepBodies.add(temp.copy(body)); rb.name=body.name
    for a,b in zip(chosen,chosen[1:]):
        for lab,sgn in [('R',1),('L',-1)]:
            aa={'x':a['x'],'y':sgn*abs(a['y']),'z':a['z']}; bb={'x':b['x'],'y':sgn*abs(b['y']),'z':b['z']}
            q=rr.bRepBodies.add(cone(temp,aa,bb,a['outer_diameter_mm'],b['outer_diameter_mm']))
            q.name=f'DUCT_CORRIDOR_{lab}_{a["x"]:.0f}_{b["x"]:.0f}_v138'
    audit={'status':'V138_BILATERAL_INLET_CENTER_CORRIDOR','source_v136':cfg,'stations':stations,'chosen_path':chosen,
           'segment_validation':segs,'bilateral_segment_pass':bilateral,'flow_area_preserved':bool(duct['minimum_flow_area_policy_pass']),
           'geometry_candidate_pass':bilateral and bool(duct['minimum_flow_area_policy_pass']),
           'next_gate':'v139 smooth multi-section duct loft with curvature/area audit','print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INLET_CORRIDOR_v138.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v138_inlet_corridor_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v138_inlet_corridor_review.png'),1600,1000)
    try: review.close(False)
    except: pass
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit
