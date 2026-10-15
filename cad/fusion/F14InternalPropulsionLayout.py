import adsk.core,adsk.fusion,json,hashlib,os

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_propulsion_assembly_inputs.json')));temp=adsk.fusion.TemporaryBRepManager.get();copies=[];imports=[]
    for source in cfg:
        if hashlib.sha256(open(source['path'],'rb').read()).hexdigest()!=source['sha256']:raise RuntimeError('Source changed')
        imported=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(source['path']));imports.append(imported)
        for body in adsk.fusion.Design.cast(app.activeProduct).rootComponent.bRepBodies:
            if body.name.startswith('CANDIDATE_JOINED_INLET_') or body.name.startswith('INTERNAL_EXHAUST_STUDY_'):copies.append((body.name,temp.copy(body)))
    if len(copies)!=4:raise RuntimeError('Expected four duct candidates')
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_TWIN_EDF_INTERNAL_LAYOUT_CANDIDATE';design=adsk.fusion.Design.cast(app.activeProduct);design.designType=adsk.fusion.DesignTypes.DirectDesignType;root=design.rootComponent;records=[]
    for name,copy in copies:
        body=root.bRepBodies.add(copy);body.name=name;props=body.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy);center=props.centerOfMass
        records.append(dict(body=name,volume_cm3=props.volume,centroid_mm=[center.x*10,center.y*10,center.z*10]))
    interfaces=[]
    for side,sgn in [('R',1),('L',-1)]:
        housing=root.bRepBodies.add(temp.createCylinderOrCone(adsk.core.Point3D.create(mm(658),mm(sgn*65),mm(-10)),mm(26.25),adsk.core.Point3D.create(mm(731.5),mm(sgn*65),mm(-10)),mm(26.25)));housing.name='REFERENCE_UNMEASURED_EDF_'+side;housing.opacity=.2
        inlet=next(b for b in root.bRepBodies if b.name.startswith('CANDIDATE_JOINED_INLET_'+side));exhaust=next(b for b in root.bRepBodies if b.name.startswith('INTERNAL_EXHAUST_STUDY_'+side))
        gap1=abs(inlet.boundingBox.maxPoint.x*10-658);gap2=abs(exhaust.boundingBox.minPoint.x*10-731.5)
        if gap1>1e-6 or gap2>1e-6:raise RuntimeError('Axial interface mismatch')
        interfaces.append(dict(side=side,inlet_to_housing_axial_gap_mm=gap1,housing_to_exhaust_axial_gap_mm=gap2))
    volume=sum(r['volume_cm3'] for r in records);cg=[sum(r['volume_cm3']*r['centroid_mm'][j] for r in records)/volume for j in range(3)]
    audit=dict(status='NATIVE_TWIN_EDF_INTERNAL_LAYOUT_CANDIDATE',inputs=cfg,ducts=records,interfaces=interfaces,printed_duct_material_volume_cm3=volume,uniform_material_duct_CG_mm=cg,assumed_PLA_density_g_cm3=1.26,analytic_PLA_duct_mass_g=volume*1.26,EDF_mass_included=False,actual_hardware_verified=False,mechanism_collision_verified=False,aircraft_CG_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_TWIN_EDF_INTERNAL_LAYOUT_CANDIDATE.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_internal_layout_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_internal_layout_review.png'),1600,1000)
    doc.close(False)
    for imported in imports:imported.close(False)
    if prior:prior.activate()
    return audit
