"""v76: extend the outboard joint rib inboard by direct face offset; test taper clearances."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v76_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    wanted=[]
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if ('_R_' in b.name and ('CARBON' in b.name or 'HOLLOW_WING' in b.name)) or b.name in ('CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_RIB_ZERO_CLEARANCE_3'):
            wanted.append((b.name,temp.copy(b)))
    if len(wanted)!=7: raise RuntimeError('Expected seven right-side v73 bodies')
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_WING_JOINT_EXTENDED_RIB_v76'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType
    root=design.rootComponent; bodies=[]
    for name,copy in wanted:
        b=root.bRepBodies.add(copy); b.name=name; bodies.append(b)
    spars=[b for b in bodies if 'CARBON' in b.name]; skins=[b for b in bodies if 'HOLLOW_WING' in b.name]
    inner=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_-3')
    outer=next(b for b in bodies if b.name=='CANDIDATE_RIB_ZERO_CLEARANCE_3')
    ends=[]
    for f in outer.faces:
        pl=adsk.core.Plane.cast(f.geometry)
        if pl and abs(pl.normal.y)>0.999999: ends.append((f.pointOnFace.y*10.0,f,pl.normal.y,f.area*100.0))
    if len(ends)!=2: raise RuntimeError('Expected two planar outboard rib end faces')
    y0,face,normal_y,area=min(ends,key=lambda x:x[0])
    length=float(src['bridge_length_mm'])
    # Positive offset follows face normal. Choose sign that moves this face toward -Y.
    signed_mm=length*(-1.0/normal_y)
    before=outer.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume
    inp=root.features.offsetFacesFeatures.createInput([face],adsk.core.ValueInput.createByReal(mm(signed_mm)))
    feat=root.features.offsetFacesFeatures.add(inp)
    if not feat or feat.bodies.count<1: raise RuntimeError('Rib face extension failed')
    outer_result=feat.bodies.item(0)
    if not outer_result.isValid or not outer_result.isSolid: raise RuntimeError('Extended result body invalid')
    outer_result.name='CANDIDATE_EXTENDED_OUTBOARD_RIB_v76'
    after=outer_result.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume
    bb=outer_result.boundingBox; y_min=bb.minPoint.y*10.0; y_max=bb.maxPoint.y*10.0
    axial_gap=app.measureManager.measureMinimumDistance(outer_result,inner).value*10.0
    collisions=[]
    for blocker in skins+spars:
        cut=temp.copy(outer_result)
        if not temp.booleanOperation(cut,temp.copy(blocker),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Collision boolean failed')
        scratch=root.bRepBodies.add(cut); v=scratch.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume; scratch.deleteMe()
        removed=max(0.0,after-v)
        collisions.append({'blocker':blocker.name,'removed_cm3':removed,'pass':removed<1e-7})
    direction_pass=abs(y_min-float(src['expected_y_min_mm']))<=0.03
    gap_pass=abs(axial_gap-float(src['expected_axial_gap_mm']))<=0.03
    collision_free=all(x['pass'] for x in collisions)
    audit={'status':'V76_EXTENDED_OUTBOARD_RIB_BRIDGE_TRIAL','source':src,'extension':{'origin_y_mm':y0,'origin_face_area_mm2':area,'normal_y':normal_y,'signed_offset_mm':signed_mm,'before_cm3':before,'after_cm3':after,'added_cm3':after-before,'bbox_y_min_mm':y_min,'bbox_y_max_mm':y_max,'axial_gap_to_inner_rib_mm':axial_gap},'collision_checks':collisions,'direction_screen_pass':direction_pass,'axial_gap_screen_pass':gap_pass,'collision_free':collision_free,'geometry_candidate_pass':direction_pass and gap_pass and collision_free,'primary_bending_path':'continuous carbon','fit_coupon_verified':False,'torsion_transfer_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_WING_JOINT_EXTENDED_RIB_v76.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v76_extended_rib_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v76_extended_rib_review.png'),1600,1000)
    if prior: prior.activate()
    return audit