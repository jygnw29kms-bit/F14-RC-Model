"""v87: manufacture-clearance sweep envelope for the full outboard insert."""
import adsk.core, adsk.fusion, json, os, hashlib

def _vol(b): return b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def _shift(temp, body, dx, dy, dz, mm):
    c=temp.copy(body); m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(mm(dx),mm(dy),mm(dz)); temp.transform(c,m); return c

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    src=json.load(open(os.path.join(base,'F14_v87_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    names=['CANDIDATE_OUTER_RIB_KEY_INSERT_v82','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    found={}
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if b.name in names: found[b.name]=temp.copy(b)
    miss=[n for n in names if n not in found]
    if miss: raise RuntimeError('Missing v82 bodies '+repr(miss))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_OUTER_INSERT_MANUFACTURING_CLEARANCE_v87'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; bodies={}
    for name,copy in found.items():
        b=root.bRepBodies.add(copy); b.name=name; bodies[name]=b
    insert=bodies[names[0]]; inner=bodies[names[1]]; skin=bodies[names[2]]; spars=[bodies[n] for n in names[3:]]
    raw=_vol(insert); carved=temp.copy(insert)
    dist=float(src['insertion_mm']); step=float(src['carve_step_mm']); n=int(round(dist/step)); cc=float(src['carbon_clearance_mm']); sc=float(src['skin_clearance_mm'])
    carbon_offsets=[(dx,dz) for dx in (-cc,0.0,cc) for dz in (-cc,0.0,cc)]
    skin_offsets=[(dx,dz) for dx in (-sc,0.0,sc) for dz in (-sc,0.0,sc)]
    ops=0
    for k in range(n+1):
        dy=-k*step
        for spar in spars:
            for dx,dz in carbon_offsets:
                cutter=_shift(temp,spar,dx,dy,dz,mm)
                if not temp.booleanOperation(carved,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Carbon clearance carve failed')
                ops+=1
        for dx,dz in skin_offsets:
            cutter=_shift(temp,skin,dx,dy,dz,mm)
            if not temp.booleanOperation(carved,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Skin clearance carve failed')
            ops+=1
    cleared=root.bRepBodies.add(carved); cleared.name='CANDIDATE_OUTER_INSERT_MFG_CLEARANCE_v87'
    if not cleared.isValid or not cleared.isSolid: raise RuntimeError('v87 cleared insert invalid')
    vc=_vol(cleared); bb=cleared.boundingBox
    # Fine verification at half the carve step.
    vs=float(src['verify_step_mm']); nv=int(round(dist/vs)); rows=[]
    for k in range(nv,-1,-1):
        dy=k*vs; moved=_shift(temp,cleared,0,dy,0,mm); scratch=root.bRepBodies.add(moved)
        skin_gap=app.measureManager.measureMinimumDistance(scratch,skin).value*10.0
        carbon=[app.measureManager.measureMinimumDistance(scratch,s).value*10.0 for s in spars]
        rib_gap=app.measureManager.measureMinimumDistance(scratch,inner).value*10.0
        rows.append({'outboard_translation_mm':dy,'skin_gap_mm':skin_gap,'minimum_carbon_gap_mm':min(carbon),'carbon_gaps_mm':carbon,'inner_rib_gap_mm':rib_gap})
        scratch.deleteMe()
    min_skin=min(x['skin_gap_mm'] for x in rows); min_carbon=min(x['minimum_carbon_gap_mm'] for x in rows); min_rib=min(x['inner_rib_gap_mm'] for x in rows)
    axial=app.measureManager.measureMinimumDistance(cleared,inner).value*10.0
    skin_pass=min_skin>=sc*0.95; carbon_pass=min_carbon>=cc*0.95; axial_pass=abs(axial-float(src['target_axial_gap_mm']))<=0.04
    audit={'status':'V87_MANUFACTURING_CLEARANCE_SWEEP','source':src,'carve_boolean_operations':ops,'insert':{'raw_volume_cm3':raw,'cleared_volume_cm3':vc,'volume_retained_fraction':vc/raw,'bbox_y_mm':[bb.minPoint.y*10.0,bb.maxPoint.y*10.0],'axial_gap_mm':axial},'verification':rows,'minimum_skin_gap_mm':min_skin,'minimum_carbon_gap_mm':min_carbon,'minimum_inner_rib_gap_mm':min_rib,'skin_clearance_pass':skin_pass,'carbon_clearance_pass':carbon_pass,'axial_gap_pass':axial_pass,'manufacturing_clearance_candidate_pass':skin_pass and carbon_pass and axial_pass,'minimum_section_verified_after_clearance':False,'fit_coupon_verified':False,'torsion_capacity_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_OUTER_INSERT_MANUFACTURING_CLEARANCE_v87.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v87_manufacturing_clearance_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v87_manufacturing_clearance_review.png'),1600,1000)
    if prior: prior.activate()
    return audit