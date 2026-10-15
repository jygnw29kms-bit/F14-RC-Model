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
        ends=[]
        for face in body.faces:
            plane=adsk.core.Plane.cast(face.geometry)
            if not plane:continue
            bb=face.boundingBox
            ends.append(dict(x_mm=plane.origin.x*10,area_mm2=face.area*100,y_bounds_mm=[bb.minPoint.y*10,bb.maxPoint.y*10],z_bounds_mm=[bb.minPoint.z*10,bb.maxPoint.z*10],loop_count=face.loops.count,plane_normal=[plane.normal.x,plane.normal.y,plane.normal.z]))
        if not ends:raise RuntimeError('No planar end faces')
        rows.append(dict(body=body.name,minimum_inner_outer_face_gap_mm=result.value*10,conical_faces=len(sides),volume_cm3=body.volume,planar_end_faces=ends))
    if len(rows)!=2:raise RuntimeError('Expected two wall bodies')
    audit=dict(status='NATIVE_INLET_END_INTERFACE_GEOMETRY',input=cfg,measurements=rows,minimum_gap_mm=min(r['minimum_inner_outer_face_gap_mm'] for r in rows),nominal_radial_wall_mm=.8,print_release=False,upstream_and_mount_interfaces_verified=False)
    os.makedirs(outdir,exist_ok=True);json.dump(audit,open(os.path.join(outdir,'F14_inlet_end_interface_audit.json'),'w'),indent=2)
    doc.close(False)
    if prior:prior.activate()
    return audit
