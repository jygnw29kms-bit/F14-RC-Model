"""v136: D-to-EDF integral inlet transition and first fan-mount packaging gate."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def cone(temp,a,b,d0,d1):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(a['x']),mm(a['y']),mm(a['z'])),mm(d0/2.0),adsk.core.Point3D.create(mm(b['x']),mm(b['y']),mm(b['z'])),mm(d1/2.0))

def cylinder_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2.0),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2.0))

def contained(temp,body,tool):
    total=tool.volume
    q=temp.copy(tool)
    ok=temp.booleanOperation(q,temp.copy(body),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=min(total,q.volume) if ok and q.isValid else 0.0
    return {'total_cm3':total,'inside_cm3':inside,'outside_cm3':max(0.0,total-inside),'fraction':inside/total if total else 0.0}

def shell_from(temp,outer,inner):
    q=temp.copy(outer)
    if not temp.booleanOperation(q,temp.copy(inner),adsk.fusion.BooleanTypes.DifferenceBooleanType):
        raise RuntimeError('shell boolean failed')
    return q

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v136_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['source_path'],'rb').read()).hexdigest()!=cfg['source_sha256']:
        raise RuntimeError('v135 source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])):
        raise RuntimeError('v135 import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent
    body=next((root.bRepBodies.item(i) for i in range(root.bRepBodies.count) if root.bRepBodies.item(i).name=='SOURCE_SILHOUETTE_GUIDED_AFT_v135'),None)
    if body is None: raise RuntimeError('v135 body missing')
    temp=adsk.fusion.TemporaryBRepManager.get()
    D=dict(cfg['D_center_local_mm']); F=dict(cfg['fan_face_center_local_mm']); duct=cfg['duct']; mount=cfg['fan_mount_candidate']
    records=[]; visible=[]
    for lab,sgn in [('R',1),('L',-1)]:
        a={'x':float(D['x']),'y':sgn*abs(float(D['y'])),'z':float(D['z'])}
        b={'x':float(F['x']),'y':sgn*abs(float(F['y'])),'z':float(F['z'])}
        outer=cone(temp,a,b,float(duct['D_outer_diameter_mm']),float(duct['fan_outer_diameter_mm']))
        inner=cone(temp,a,b,float(duct['D_inner_diameter_mm']),float(duct['fan_inner_diameter_mm']))
        flow=contained(temp,body,inner); outer_fit=contained(temp,body,outer)
        shell=shell_from(temp,outer,inner)
        x0=float(mount['x_start_mm']); x1=x0+float(mount['length_mm']); y=b['y']; z=b['z']
        mo=cylinder_x(temp,x0,x1,y,z,float(mount['mount_OD_mm']))
        mi=cylinder_x(temp,x0,x1,y,z,float(mount['mount_ID_mm']))
        mfit=contained(temp,body,mo); mshell=shell_from(temp,mo,mi)
        records.append({'side':lab,'transition_outer':outer_fit,'transition_flow':flow,'mount_outer':mfit,
                        'transition_shell_volume_cm3':shell.volume,'mount_shell_volume_cm3':mshell.volume})
        visible.append((lab,'DUCT',shell)); visible.append((lab,'MOUNT',mshell))
    pass_outer=all(r['transition_outer']['outside_cm3']<=1e-5 for r in records)
    pass_flow=all(r['transition_flow']['outside_cm3']<=1e-5 for r in records)
    pass_mount=all(r['mount_outer']['outside_cm3']<=1e-5 for r in records)
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_INLET_TRANSITION_AND_MOUNT_v136'
    rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; rr=rd.rootComponent
    rb=rr.bRepBodies.add(temp.copy(body)); rb.name=body.name
    for lab,kind,b in visible:
        q=rr.bRepBodies.add(temp.copy(b)); q.name=kind+'_'+lab+'_v136'
    audit={'status':'V136_D_TO_EDF_TRANSITION_AND_MOUNT_GATE','source':cfg,'records':records,
           'transition_outer_containment_pass':pass_outer,'transition_flow_containment_pass':pass_flow,
           'fan_mount_outer_containment_pass':pass_mount,'bilateral_pass':pass_outer and pass_flow and pass_mount,
           'minimum_flow_area_policy_pass':bool(duct['minimum_flow_area_policy_pass']),
           'shared_skin_architecture_at_D':True,
           'hardware_dimensions_frozen':False,'installed_thrust_verified':False,'thermal_verified':False,
           'geometry_candidate_pass':pass_outer and pass_flow and pass_mount and bool(duct['minimum_flow_area_policy_pass']),
           'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INLET_TRANSITION_AND_MOUNT_v136.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v136_inlet_transition_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v136_inlet_transition_review.png'),1600,1000)
    try: review.close(False)
    except: pass
    try: imported.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit
