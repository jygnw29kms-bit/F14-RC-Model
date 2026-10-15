import adsk.core,adsk.fusion,json,os,hashlib

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_shifted_edf_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Source changed')
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    root=adsk.fusion.Design.cast(app.activeProduct).rootComponent;temp=adsk.fusion.TemporaryBRepManager.get();source=next(b for b in root.bRepBodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT');rows=[]
    for side,sgn in [('R',1),('L',-1)]:
        for kind,diameter,length in [('housing',52.5,73.5),('housing_skin_service',54.5,73.5),('mount',55.2,8)]:
            obj=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(658),mm(sgn*65),mm(-10)),mm(diameter/2),adsk.core.Point3D.create(mm(658+length),mm(sgn*65),mm(-10)),mm(diameter/2));total=obj.volume;inside=temp.copy(obj)
            if not temp.booleanOperation(inside,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Containment query failed')
            outside=max(0,total-inside.volume)
            rows.append(dict(side=side,kind=kind,x_start_mm=658,x_end_mm=658+length,diameter_mm=diameter,outside_candidate_source_cm3=outside,containment_screen_pass=outside<1e-5))
    audit=dict(status='NATIVE_SHIFTED_EDF_INTERFACE_PACKAGING_SCREEN',input=cfg,records=rows,all_candidate_containment_pass=all(r['containment_screen_pass'] for r in rows),fan_face_candidate_x_mm=658,housing_length_assumed_mm=73.5,housing_OD_assumed_mm=52.5,skin_radial_allowance_mm=.8,service_radial_allowance_mm=.2,actual_hardware_verified=False,source_fidelity_verified=False,mechanism_clearance_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);json.dump(audit,open(os.path.join(outdir,'F14_shifted_edf_interface_audit.json'),'w'),indent=2)
    doc.close(False)
    if prior:prior.activate()
    return audit
