import adsk.core,adsk.fusion,json,hashlib,os

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_joined_inlet_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Source changed')
    imported=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']))
    source=adsk.fusion.Design.cast(app.activeProduct).rootComponent;temp=adsk.fusion.TemporaryBRepManager.get();unions=[]
    for side in ['R','L']:
        adapter=next(b for b in source.bRepBodies if b.name.startswith('CANDIDATE_ADAPTER_'+side))
        wall=next(b for b in source.bRepBodies if b.name.startswith('CANDIDATE_INLET_WALL_'+side))
        union=temp.copy(wall)
        if not temp.booleanOperation(union,temp.copy(adapter),adsk.fusion.BooleanTypes.UnionBooleanType):raise RuntimeError('Union failed')
        unions.append((side,union))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_JOINED_INLET_ADAPTER_CANDIDATES'
    design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType;root=design.rootComponent;records=[]
    for side,union in unions:
        body=root.bRepBodies.add(union);body.name='CANDIDATE_JOINED_INLET_'+side+'_NO_PRINT_RELEASE'
        if not body.isValid or not body.isSolid:raise RuntimeError('Invalid joined wall')
        graph={f.tempId:set() for f in body.faces}; bad=[]
        for edge in body.edges:
            if edge.coEdges.count!=2:bad.append(edge.tempId)
            ids=[f.tempId for f in edge.faces]
            for one in ids:graph[one].update(ids)
        visited=set();pending=[next(iter(graph))]
        while pending:
            one=pending.pop()
            if one in visited:continue
            visited.add(one);pending.extend(graph[one]-visited)
        if bad or len(visited)!=len(graph):raise RuntimeError('Disconnected or nonmanifold wall')
        records.append(dict(side=side,volume_cm3=body.volume,face_count=len(graph),edge_count=body.edges.count,all_edges_two_coedges=True,face_graph_connected=True))
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_JOINED_INLET_ADAPTER_CANDIDATES.f3d'))):raise RuntimeError('Archive failed')
    audit=dict(status='NATIVE_JOINED_INLET_ADAPTER_CONNECTIVITY',input=cfg,bodies=records,manufacturing_fit_verified=False,actual_hardware_verified=False,print_release=False)
    json.dump(audit,open(os.path.join(outdir,'F14_joined_inlet_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_joined_inlet_review.png'),1600,1000)
    doc.close(False);imported.close(False)
    if prior:prior.activate()
    return audit
