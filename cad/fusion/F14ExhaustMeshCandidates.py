import adsk.core,adsk.fusion,json,os,hashlib

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_exhaust_mesh_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Archive changed')
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    design=adsk.fusion.Design.cast(app.activeProduct);os.makedirs(outdir,exist_ok=True);rows=[]
    for body in design.rootComponent.bRepBodies:
        if not body.name.startswith('INTERNAL_EXHAUST_STUDY_'):continue
        side='R' if '_R_' in body.name else 'L';path=os.path.join(outdir,'F14_EXHAUST_'+side+'_CANDIDATE_NOT_RELEASED.stl')
        opt=design.exportManager.createSTLExportOptions(body,path);opt.unitType=adsk.fusion.DistanceUnits.MillimeterDistanceUnits;opt.isBinaryFormat=True;opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        if not design.exportManager.execute(opt):raise RuntimeError('STL export failed')
        bb=body.boundingBox;rows.append(dict(side=side,path=path,native_volume_mm3=body.volume*1000,native_bounds_mm=[[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10]],sha256=hashlib.sha256(open(path,'rb').read()).hexdigest()))
    if len(rows)!=2:raise RuntimeError('Expected two exports')
    audit=dict(status='NATIVE_STL_MILLIMETER_CANDIDATE_EXPORTS',input=cfg,files=rows,print_release=False,slicer_verified=False)
    json.dump(audit,open(os.path.join(outdir,'F14_exhaust_STL_export_audit.json'),'w'),indent=2);doc.close(False)
    if prior:prior.activate()
    return audit
