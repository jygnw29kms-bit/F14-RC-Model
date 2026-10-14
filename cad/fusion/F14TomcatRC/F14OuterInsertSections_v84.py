"""v84: thin-slab minimum cross-section screen for the complete v83 outer rib/key insert."""
import adsk.core, adsk.fusion, json, os, hashlib

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v84_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get()
    matches=[b for b in root.bRepBodies if b.name=='CANDIDATE_OUTER_INSERT_SWEEP_CLEARED_v83']
    if len(matches)!=1: raise RuntimeError('Expected one v83 insert; got '+repr([b.name for b in root.bRepBodies]))
    body=matches[0]; bb=body.boundingBox
    xmin,xmax=bb.minPoint.x,bb.maxPoint.x; zmin,zmax=bb.minPoint.z,bb.maxPoint.z
    xmid=(xmin+xmax)/2; zmid=(zmin+zmax)/2; xlen=xmax-xmin+0.2; zlen=zmax-zmin+0.2
    th=float(src['slice_thickness_mm']); y=float(src['y_start_mm']); y1=float(src['y_end_mm']); step=float(src['y_step_mm'])
    recs=[]
    while y<=y1+1e-9:
        yc=round(y,6); center=adsk.core.Point3D.create(xmid,mm(yc),zmid)
        obb=adsk.core.OrientedBoundingBox3D.create(center,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),xlen,mm(th),zlen)
        slab=temp.createBox(obb); sample=temp.copy(body)
        ok=temp.booleanOperation(sample,slab,adsk.fusion.BooleanTypes.IntersectionBooleanType)
        if not ok:
            recs.append({'y_mm':yc,'intersection_ok':False,'area_mm2':0.0}); y+=step; continue
        scratch=root.bRepBodies.add(sample); props=scratch.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy); v=props.volume; sbb=scratch.boundingBox
        recs.append({'y_mm':yc,'intersection_ok':True,'area_mm2':v*1000.0/th,'slice_volume_cm3':v,'bbox_x_mm':[sbb.minPoint.x*10,sbb.maxPoint.x*10],'bbox_z_mm':[sbb.minPoint.z*10,sbb.maxPoint.z*10],'centroid_x_mm':props.centerOfMass.x*10,'centroid_z_mm':props.centerOfMass.z*10})
        scratch.deleteMe(); y+=step
    valid=[r for r in recs if r.get('intersection_ok') and r['area_mm2']>0]
    if len(valid)!=len(recs): raise RuntimeError('Missing v84 section(s)')
    mn=min(valid,key=lambda r:r['area_mm2']); mx=max(valid,key=lambda r:r['area_mm2']); avg=sum(r['area_mm2'] for r in valid)/len(valid)
    near_join=min(valid,key=lambda r:abs(r['y_mm']-366.99))
    audit={'status':'V84_COMPLETE_INSERT_MINIMUM_SECTION_SCREEN','source':src,'body_y_bounds_mm':[bb.minPoint.y*10,bb.maxPoint.y*10],'sections':recs,'minimum_section':mn,'maximum_section':mx,'average_area_mm2':avg,'section_near_key_to_rib_join':near_join,'all_sections_present':True,'minimum_insert_section_verified_geometrically':True,'material_allowable_verified':False,'torsion_capacity_verified':False,'fit_coupon_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); json.dump(audit,open(os.path.join(outdir,'F14_v84_insert_section_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v84_insert_section_review.png'),1600,1000)
    if prior: prior.activate()
    return audit