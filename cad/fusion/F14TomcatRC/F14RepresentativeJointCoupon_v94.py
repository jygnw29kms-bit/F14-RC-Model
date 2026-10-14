"""v94: build a local geometry-representative printed wing-joint coupon from v89 + v82 lineage."""
import adsk.core, adsk.fusion, json, os, hashlib, re

def _mm(v): return v/10.0

def _safe(name): return re.sub(r'[^A-Za-z0-9_.-]+','_',name)

def _copy_named(design,names,temp):
    out={}
    for i in range(design.rootComponent.bRepBodies.count):
        b=design.rootComponent.bRepBodies.item(i)
        if b.name in names: out[b.name]=temp.copy(b)
    return out

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v94_section_inputs.json'),encoding='utf-8'))
    for p,h in ((src['v89_path'],src['v89_sha256']),(src['v82_path'],src['v82_sha256'])):
        if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: raise RuntimeError('Source hash mismatch '+p)
    temp=adsk.fusion.TemporaryBRepManager.get(); imp=app.importManager
    if not imp.importToNewDocument(imp.createFusionArchiveImportOptions(src['v89_path'])): raise RuntimeError('v89 import failed')
    doc89=app.activeDocument; d89=adsk.fusion.Design.cast(app.activeProduct)
    names89=['CANDIDATE_OUTER_INSERT_MFG_ENDPOINT_CLEAR_v89','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    c89=_copy_named(d89,names89,temp); miss=[n for n in names89 if n not in c89]
    if miss: raise RuntimeError('Missing v89 bodies '+repr(miss))
    if not imp.importToNewDocument(imp.createFusionArchiveImportOptions(src['v82_path'])): raise RuntimeError('v82 import failed')
    doc82=app.activeDocument; d82=adsk.fusion.Design.cast(app.activeProduct)
    outer_name='CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS'; c82=_copy_named(d82,[outer_name],temp)
    if outer_name not in c82: raise RuntimeError('Missing v82 outer skin')
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_REPRESENTATIVE_JOINT_COUPON_v94'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    source={**c89,**c82}
    # Build one common crop box around all source geometry, limited only in Y.
    bbs=[b.boundingBox for b in source.values()]
    xmin=min(b.minPoint.x for b in bbs)-0.2; xmax=max(b.maxPoint.x for b in bbs)+0.2
    zmin=min(b.minPoint.z for b in bbs)-0.2; zmax=max(b.maxPoint.z for b in bbs)+0.2
    y0=float(src['crop_y_min_mm']); y1=float(src['crop_y_max_mm']); yc=(y0+y1)/2.0
    center=adsk.core.Point3D.create((xmin+xmax)/2.0,_mm(yc),(zmin+zmax)/2.0)
    box=adsk.core.OrientedBoundingBox3D.create(center,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),xmax-xmin,_mm(y1-y0),zmax-zmin)
    slab=temp.createBox(box)
    made={}; rec=[]
    for name,b in source.items():
        q=temp.copy(b)
        ok=temp.booleanOperation(q,temp.copy(slab),adsk.fusion.BooleanTypes.IntersectionBooleanType)
        if not ok: raise RuntimeError('Crop failed '+name)
        body=root.bRepBodies.add(q); body.name='COUPON_'+name; made[name]=body
        bb=body.boundingBox; props=body.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy)
        rec.append({'source_body':name,'coupon_body':body.name,'volume_cm3':props.volume,'bbox_mm':{'x':[bb.minPoint.x*10,bb.maxPoint.x*10],'y':[bb.minPoint.y*10,bb.maxPoint.y*10],'z':[bb.minPoint.z*10,bb.maxPoint.z*10]}})
    insert=made['CANDIDATE_OUTER_INSERT_MFG_ENDPOINT_CLEAR_v89']; inner_skin=made['CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS']; outer_skin=made[outer_name]; inner_rib=made['CANDIDATE_RIB_ZERO_CLEARANCE_-3']
    spars=[made[n] for n in names89 if 'CARBON_R_' in n]
    gaps={
      'insert_to_inner_skin_mm':app.measureManager.measureMinimumDistance(insert,inner_skin).value*10.0,
      'insert_to_outer_skin_mm':app.measureManager.measureMinimumDistance(insert,outer_skin).value*10.0,
      'insert_to_inner_rib_mm':app.measureManager.measureMinimumDistance(insert,inner_rib).value*10.0,
      'skin_segment_min_gap_mm':app.measureManager.measureMinimumDistance(inner_skin,outer_skin).value*10.0,
      'insert_to_carbon_mm':[app.measureManager.measureMinimumDistance(insert,b).value*10.0 for b in spars]
    }
    # Carbon must span both sides of the local coupon window; record actual retained span.
    carbon=[]
    for b in spars:
        bb=b.boundingBox; carbon.append({'body':b.name,'y_min_mm':bb.minPoint.y*10.0,'y_max_mm':bb.maxPoint.y*10.0,'span_mm':(bb.maxPoint.y-bb.minPoint.y)*10.0})
    os.makedirs(outdir,exist_ok=True); stldir=os.path.join(outdir,'representative_joint_coupon_v94_stl'); os.makedirs(stldir,exist_ok=True)
    printable=[inner_skin,outer_skin,insert,inner_rib]; stls=[]
    for b in printable:
        fn=os.path.join(stldir,_safe(b.name)+'.stl'); opt=design.exportManager.createSTLExportOptions(b,fn); opt.sendToPrintUtility=False
        if not design.exportManager.execute(opt): raise RuntimeError('STL export failed '+b.name)
        stls.append(fn)
    f3d=os.path.join(outdir,'F14_REPRESENTATIVE_JOINT_COUPON_v94.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(f3d)): raise RuntimeError('F3D export failed')
    audit={'status':'V94_REPRESENTATIVE_PRINTED_JOINT_COUPON','source':src,'crop_y_mm':[y0,y1],'bodies':rec,'assembly_gaps':gaps,'carbon_references':carbon,'printable_stl_files':stls,'test_requirement':{'sacrificial_sf3_torsion_Nm':src['sf3_torsion_Nm'],'flight_article_nondestructive_proof_Nm':src['flight_proof_Nm']},'coordinate_lineage_compatible':True,'geometry_coupon_created':True,'adhesive_process_verified':False,'carbon_material_installed_in_coupon':False,'representative_joint_torsion_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    json.dump(audit,open(os.path.join(outdir,'F14_v94_representative_joint_coupon_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v94_representative_joint_coupon_review.png'),1600,1000)
    # Close imported/reference documents to prevent Fusion session-recovery accumulation.
    doc.activate();
    try: doc89.close(False)
    except: pass
    try: doc82.close(False)
    except: pass
    try: doc.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit