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
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    review.name='F14_ALLOWANCED_INLET_WALL_CANDIDATE'
    rd=adsk.fusion.Design.cast(app.activeProduct);rd.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=rd.rootComponent; sourcebody=root.bRepBodies.add(temp.copy(solids[0]));sourcebody.name='REFERENCE_INTERPOLATED_SOURCE_LOFT'
    shell_records=[]
    original_l,original_r=dict(points[0]),dict(points[-1])
    original_l['inner_diameter_mm']-=.02
    original_r['inner_diameter_mm']-=.02
    span=original_r['x']-original_l['x']
    def extend(t):
        return {key:original_l[key]+t*(original_r[key]-original_l[key]) for key in ('x','y','z','outer_diameter_mm','inner_diameter_mm')}
    l,r=extend(-10/span),extend(1+10/span)
    for side,sgn in [('R',1),('L',-1)]:
        ends=[adsk.core.Point3D.create(mm(t['x']),mm(sgn*abs(t['y'])),mm(t['z'])) for t in (l,r)]
        outer=temp.createCylinderOrCone(ends[0],mm(l['outer_diameter_mm']/2),ends[1],mm(r['outer_diameter_mm']/2))
        inner=temp.createCylinderOrCone(ends[0],mm(l['inner_diameter_mm']/2),ends[1],mm(r['inner_diameter_mm']/2))
        if not temp.booleanOperation(outer,inner,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('Duct wall difference failed')
        if not temp.booleanOperation(outer,temp.copy(clip),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Wall domain clip failed')
        body=root.bRepBodies.add(outer);body.name='CANDIDATE_INLET_WALL_'+side+'_NO_PRINT_RELEASE'
        if not body.isValid or not body.isSolid:raise RuntimeError('Invalid wall body')
        inside=temp.copy(body)
        if not temp.booleanOperation(inside,temp.copy(sourcebody),adsk.fusion.BooleanTypes.IntersectionBooleanType):raise RuntimeError('Wall containment query failed')
        outside=max(0,body.volume-inside.volume)
        ends=[f for f in body.faces if adsk.core.Plane.cast(f.geometry)]
        if len(ends)!=2 or any(f.loops.count!=2 or abs(adsk.core.Plane.cast(f.geometry).normal.x)<.999999 for f in ends):raise RuntimeError('Incomplete X annular end')
        cones=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
        if len(cones)!=2:raise RuntimeError('Expected two conical wall faces')
        thickness=app.measureManager.measureMinimumDistance(cones[0],cones[1]).value*10
        if thickness<.8:raise RuntimeError('Normal wall thickness below 0.8 mm')
        shell_records.append(dict(side=side,wall_material_volume_cm3=body.volume,outside_candidate_source_cm3=outside,valid_solid=True,complete_X_annular_ends=True,end_loop_counts=[f.loops.count for f in ends],normal_wall_minimum_mm=thickness,end_dimensions=[dict(x_mm=adsk.core.Plane.cast(f.geometry).origin.x*10,y_bounds_mm=[f.boundingBox.minPoint.y*10,f.boundingBox.maxPoint.y*10],z_bounds_mm=[f.boundingBox.minPoint.z*10,f.boundingBox.maxPoint.z*10],area_mm2=f.area*100) for f in ends]))
    result['wall_candidates']=shell_records
    result['wall_thickness_radius_difference_mm']=.81
    result['minimum_normal_wall_thickness_verified']=True
    result['inlet_ends_planar_X_domain_clips']=True
    if not rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_ALLOWANCED_INLET_WALL_CANDIDATE.f3d'))):raise RuntimeError('Wall archive export failed')
    json.dump(result,open(os.path.join(outdir,'F14_allowanced_inlet_wall_audit.json'),'w'),indent=2)
    app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_allowanced_inlet_wall_review.png'),1600,1000)
    review.close(False)
    doc.close(False)
    if prior:prior.activate()
    return result
