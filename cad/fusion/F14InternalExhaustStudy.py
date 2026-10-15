"""Prepared native internal exhaust study; no original nozzle or flight release."""
import adsk.core,adsk.fusion,json,hashlib,os,math

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_internal_exhaust_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Source changed')
    imported=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    source=next(b for b in adsk.fusion.Design.cast(app.activeProduct).rootComponent.bRepBodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT');temp=adsk.fusion.TemporaryBRepManager.get();copy=temp.copy(source)
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_INTERNAL_EXHAUST_STUDY_HUB28_AREA90'
    design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType;root=design.rootComponent;reference=root.bRepBodies.add(copy);reference.name='REFERENCE_CANDIDATE_AFT_LOFT';reference.isVisible=False
    x0=731.5;x1=754.962281164333;exit_d=math.sqrt(.9*(50**2-28**2));wall=.83;records=[]
    for side,sgn in [('R',1),('L',-1)]:
        a=adsk.core.Point3D.create(mm(x0),mm(sgn*65),mm(-10));b=adsk.core.Point3D.create(mm(x1),mm(sgn*65),mm(-10))
        outer=temp.createCylinderOrCone(a,mm(25+wall),b,mm(exit_d/2+wall));inner=temp.createCylinderOrCone(a,mm(25),b,mm(exit_d/2))
        if not temp.booleanOperation(outer,inner,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('Exhaust wall failed')
        body=root.bRepBodies.add(outer);body.name='INTERNAL_EXHAUST_STUDY_'+side+'_NOT_RELEASED'
        if not body.isValid or not body.isSolid:raise RuntimeError('Invalid exhaust')
        cones=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
        if len(cones)!=2:raise RuntimeError('Expected two cone surfaces')
        gap=app.measureManager.measureMinimumDistance(cones[0],cones[1]).value*10;inside=temp.copy(body)
        if not temp.booleanOperation(inside,temp.copy(reference),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Containment query failed')
        records.append(dict(side=side,volume_cm3=body.volume,normal_wall_minimum_mm=gap,outside_candidate_source_cm3=max(0,body.volume-inside.volume)))
    audit=dict(status='NATIVE_INTERNAL_EXHAUST_STUDY',input=cfg,assumed_hub_diameter_mm=28,assumed_fan_ID_mm=50,assumed_exit_to_FSA_ratio=.9,exit_inner_diameter_mm=exit_d,radial_wall_mm=wall,records=records,actual_hardware_verified=False,aerodynamic_exit_ratio_verified=False,original_external_nozzle_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INTERNAL_EXHAUST_STUDY.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_internal_exhaust_study_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_internal_exhaust_study_review.png'),1600,1000)
    doc.close(False);imported.close(False)
    if prior:prior.activate()
    return audit
