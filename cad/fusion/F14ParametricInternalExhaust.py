import adsk.core,adsk.fusion,json,os,math

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_PARAMETRIC_INTERNAL_EXHAUST_CANDIDATE';design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent
    if design.designType!=adsk.fusion.DesignTypes.ParametricDesignType:design.designType=adsk.fusion.DesignTypes.ParametricDesignType
    for name,expr,units in [('fan_ID','50 mm','mm'),('hub_D','28 mm','mm'),('exit_FSA_ratio','0.9',''),('radial_wall','0.83 mm','mm'),('exhaust_start_X','731.5 mm','mm'),('exhaust_end_X','754.962281164333 mm','mm')]:design.userParameters.add(name,adsk.core.ValueInput.createByString(expr),units,'Internal study assumption; no print release')
    planes=[]
    for name in ['exhaust_start_X','exhaust_end_X']:
        ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByString(name if root.yZConstructionPlane.geometry.normal.x>0 else '-'+name));planes.append(root.constructionPlanes.add(ci))
    rows=[]
    for side,sgn in [('R',1),('L',-1)]:
        lofts=[]
        for outer in [True,False]:
            profiles=[]
            for index,plane in enumerate(planes):
                x=731.5 if index==0 else 754.962281164333;sk=root.sketches.add(plane);sk.name='EXHAUST_'+side+('_OUTER' if outer else '_FLOW')+'_'+str(index)
                center=sk.modelToSketchSpace(adsk.core.Point3D.create(mm(x),mm(sgn*65),mm(-10)))
                d=50 if index==0 else math.sqrt(.9*(50**2-28**2));d+=1.66 if outer else 0
                circle=sk.sketchCurves.sketchCircles.addByCenterRadius(center,mm(d/2));circle.centerSketchPoint.isFixed=True
                dim=sk.sketchDimensions.addDiameterDimension(circle,adsk.core.Point3D.create(center.x+mm(30),center.y,0))
                dim.parameter.expression=('fan_ID' if index==0 else 'sqrt(exit_FSA_ratio*(fan_ID^2-hub_D^2))')+('+2*radial_wall' if outer else '')
                if sk.profiles.count!=1:raise RuntimeError('Circle profile missing')
                profiles.append(sk.profiles.item(0))
            li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            for profile in profiles:li.loftSections.add(profile)
            feature=root.features.loftFeatures.add(li)
            if not feature or feature.bodies.count!=1:raise RuntimeError('Parametric exhaust loft failed')
            lofts.append(feature.bodies.item(0))
        tools=adsk.core.ObjectCollection.create();tools.add(lofts[1]);ci=root.features.combineFeatures.createInput(lofts[0],tools);ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation;ci.isKeepToolBodies=False;cut=root.features.combineFeatures.add(ci)
        if not cut or cut.bodies.count!=1:raise RuntimeError('Parametric wall cut failed')
        body=cut.bodies.item(0);body.name='PARAMETRIC_EXHAUST_'+side+'_NOT_RELEASED';faces=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
        if len(faces)!=2 or not body.isValid or not body.isSolid:raise RuntimeError('Invalid parametric wall')
        gap=app.measureManager.measureMinimumDistance(faces[0],faces[1]).value*10;rows.append(dict(side=side,volume_cm3=body.volume,normal_wall_mm=gap))
    audit=dict(status='NATIVE_PARAMETRIC_INTERNAL_EXHAUST_CANDIDATES',user_parameters=[dict(name=u.name,expression=u.expression) for u in design.userParameters],records=rows,axis_yz_fixed_mm=[65,-10],source_containment_rerun=False,parameter_regeneration_verified=False,hardware_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_PARAMETRIC_INTERNAL_EXHAUST_CANDIDATE.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_parametric_exhaust_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_parametric_exhaust_review.png'),1600,1000)
    doc.close(False)
    if prior:prior.activate()
    return audit
