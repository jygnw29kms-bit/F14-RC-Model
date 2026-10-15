import adsk.core,adsk.fusion,json,os,hashlib

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument; cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_adapter_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Source changed')
    imported=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    src=adsk.fusion.Design.cast(app.activeProduct);temp=adsk.fusion.TemporaryBRepManager.get();copies=[(b.name,temp.copy(b)) for b in src.rootComponent.bRepBodies]
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_ELLIPSE_TO_CIRCLE_ADAPTER_CANDIDATE'
    design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent
    base=root.features.baseFeatures.add();base.startEdit()
    bodies=[]
    for name,copy in copies:
        body=root.bRepBodies.add(copy,base);body.name=name;bodies.append(body)
    base.finishEdit();records=[]
    for side,sgn in [('R',1),('L',-1)]:
        wall=next(b for b in bodies if b.name.startswith('CANDIDATE_INLET_WALL_'+side))
        face=next(f for f in wall.faces if adsk.core.Plane.cast(f.geometry) and abs(adsk.core.Plane.cast(f.geometry).origin.x*10-650)<1e-6)
        loops=sorted(list(face.loops),key=lambda q:sum(e.length for e in q.edges),reverse=True)
        if len(loops)!=2:raise RuntimeError('Expected annular interface')
        targets=[]
        for idx,loop in enumerate(loops):
            start_ci=root.constructionPlanes.createInput();start_ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(650)/root.yZConstructionPlane.geometry.normal.x));start_plane=root.constructionPlanes.add(start_ci)
            sk=root.sketches.add(start_plane);sk.name='ADAPTER_'+side+('_OUTER' if idx==0 else '_INNER')
            for edge in loop.edges:sk.project(edge)
            if sk.profiles.count!=1:raise RuntimeError('Interface ellipse projection ambiguous')
            ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(658)/root.yZConstructionPlane.geometry.normal.x));plane=root.constructionPlanes.add(ci)
            end=root.sketches.add(plane);center=end.modelToSketchSpace(adsk.core.Point3D.create(mm(658),mm(sgn*65),mm(-10)))
            end.sketchCurves.sketchCircles.addByCenterRadius(center,mm(25.81 if idx==0 else 25))
            li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation);li.loftSections.add(sk.profiles.item(0));li.loftSections.add(end.profiles.item(0));loft=root.features.loftFeatures.add(li)
            if not loft or loft.bodies.count!=1:raise RuntimeError('Adapter loft failed')
            targets.append(loft.bodies.item(0))
        cut=temp.copy(targets[0])
        if not temp.booleanOperation(cut,temp.copy(targets[1]),adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('Adapter hollow failed')
        base2=root.features.baseFeatures.add();base2.startEdit();adapter=root.bRepBodies.add(cut,base2);base2.finishEdit();adapter=base2.bodies.item(0);adapter.name='CANDIDATE_ADAPTER_'+side+'_UNMEASURED_FAN'
        if not adapter.isValid or not adapter.isSolid:raise RuntimeError('Adapter invalid')
        source=next(b for b in bodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT')
        inside=temp.copy(adapter)
        if not temp.booleanOperation(inside,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Adapter containment query failed')
        records.append(dict(side=side,volume_cm3=adapter.volume,outside_candidate_source_cm3=max(0,adapter.volume-inside.volume),valid_solid=True))
        for target in targets:target.isVisible=False
    audit=dict(status='NATIVE_ELLIPSE_TO_CIRCLE_ADAPTER_CANDIDATES',input=cfg,adapters=records,x_span_mm=[650,658],fan_inner_diameter_assumed_mm=50,fan_outer_diameter_candidate_mm=51.62,normal_wall_thickness_verified=False,actual_hardware_fit_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_ELLIPSE_CIRCLE_ADAPTER_CANDIDATE.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_adapter_candidate_audit.json'),'w'),indent=2)
    app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_adapter_candidate_review.png'),1600,1000)
    doc.close(False);imported.close(False)
    if prior:prior.activate()
    return audit
