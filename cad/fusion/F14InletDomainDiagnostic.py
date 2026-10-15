import adsk.core,adsk.fusion,json,hashlib,os

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument
    cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_inlet_domain_inputs.json')))
    for key in ('archive','audit'):
        if hashlib.sha256(open(cfg[key],'rb').read()).hexdigest()!=cfg[key+'_sha256']:raise RuntimeError('Source changed')
    a=json.load(open(cfg['audit'])); points=a['chosen_path']; xmin=points[0]['x']; xmax=points[-1]['x']
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['archive']))
    design=adsk.fusion.Design.cast(app.activeProduct)
    solids=[b for b in design.rootComponent.bRepBodies if not b.name.startswith('DUCT_CORRIDOR_')]
    if len(solids)!=1:raise RuntimeError('Ambiguous source body')
    temp=adsk.fusion.TemporaryBRepManager.get()
    box=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm((xmin+xmax)/2),0,0),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(xmax-xmin),mm(1000),mm(1000))
    clip=temp.createBox(box); records=[]
    for l,r in zip(points,points[1:]):
        for side,sgn in [('R',1),('L',-1)]:
            for kind in ('outer','inner'):
                obj=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(l['x']),mm(sgn*abs(l['y'])),mm(l['z'])),mm(l[kind+'_diameter_mm']/2),adsk.core.Point3D.create(mm(r['x']),mm(sgn*abs(r['y'])),mm(r['z'])),mm(r[kind+'_diameter_mm']/2))
                original=obj.volume; q=temp.copy(obj)
                if not temp.booleanOperation(q,temp.copy(clip),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Domain clip failed')
                clipped=q.volume; inside=temp.copy(q)
                if not temp.booleanOperation(inside,temp.copy(solids[0]),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Containment query failed')
                residual=max(0,clipped-inside.volume)
                records.append(dict(x0_mm=l['x'],x1_mm=r['x'],side=side,kind=kind,original_cm3=original,excluded_domain_cm3=original-clipped,common_domain_outside_cm3=residual))
    result=dict(status='INDEPENDENT_NATIVE_COMMON_DOMAIN_CONTAINMENT',inputs=cfg,records=records,maximum_common_domain_outside_cm3=max(x['common_domain_outside_cm3'] for x in records),source_OML_original_fidelity_verified=False,upstream_geometry_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);json.dump(result,open(os.path.join(outdir,'F14_inlet_common_domain_audit.json'),'w'),indent=2)
    doc.close(False)
    if prior:prior.activate()
    return result
