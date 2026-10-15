import adsk.core,adsk.fusion,json,hashlib,os

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_adapter_thickness_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Archive changed')
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    root=adsk.fusion.Design.cast(app.activeProduct).rootComponent;temp=adsk.fusion.TemporaryBRepManager.get();rows=[]
    for side in ['R','L']:
        options=[b for b in root.bRepBodies if b.name.startswith('CANDIDATE_ADAPTER_'+side)]
        if len(options)!=1:raise RuntimeError('Adapter names: '+repr([b.name for b in root.bRepBodies]))
        adapter=options[0]
        wall=next(b for b in root.bRepBodies if b.name.startswith('CANDIDATE_INLET_WALL_'+side))
        sides=[f for f in adapter.faces if not adsk.core.Plane.cast(f.geometry)]
        if len(sides)!=2:raise RuntimeError('Unexpected adapter surface count')
        gap=app.measureManager.measureMinimumDistance(sides[0],sides[1]).value*10
        united=temp.copy(wall)
        success=temp.booleanOperation(united,temp.copy(adapter),adsk.fusion.BooleanTypes.UnionBooleanType)
        rows.append(dict(side=side,minimum_loft_face_gap_mm=gap,minimum_0p8mm_screen_pass=gap>=.8,wall_adapter_distance_mm=app.measureManager.measureMinimumDistance(wall,adapter).value*10,union_operation_success=success,union_valid_solid=bool(success and united.isValid and united.isSolid),union_volume_cm3=united.volume if success else None,component_volume_sum_cm3=wall.volume+adapter.volume))
    audit=dict(status='NATIVE_ADAPTER_THICKNESS_AND_UNION_SCREEN',input=cfg,measurements=rows,actual_hardware_verified=False,union_connectivity_independently_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);json.dump(audit,open(os.path.join(outdir,'F14_adapter_thickness_union_audit.json'),'w'),indent=2)
    doc.close(False)
    if prior:prior.activate()
    return audit
