import adsk.core,adsk.fusion,json,os,hashlib

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument; cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_inlet_thickness_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Archive changed')
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    design=adsk.fusion.Design.cast(app.activeProduct);rows=[]
    for body in design.rootComponent.bRepBodies:
        if not body.name.startswith('CANDIDATE_INLET_WALL_'):continue
        sides=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
        if len(sides)!=2:raise RuntimeError('Expected inner and outer conical faces')
        result=app.measureManager.measureMinimumDistance(sides[0],sides[1])
        if not result:raise RuntimeError('Cone face distance failed')
        rows.append(dict(body=body.name,minimum_inner_outer_face_gap_mm=result.value*10,conical_faces=len(sides),volume_cm3=body.volume))
    if len(rows)!=2:raise RuntimeError('Expected two wall bodies')
    audit=dict(status='NATIVE_INLET_CONICAL_FACE_THICKNESS',input=cfg,measurements=rows,minimum_gap_mm=min(r['minimum_inner_outer_face_gap_mm'] for r in rows),nominal_radial_wall_mm=.8,print_release=False,upstream_and_mount_interfaces_verified=False)
    os.makedirs(outdir,exist_ok=True);json.dump(audit,open(os.path.join(outdir,'F14_inlet_thickness_audit.json'),'w'),indent=2)
    doc.close(False)
    if prior:prior.activate()
    return audit
