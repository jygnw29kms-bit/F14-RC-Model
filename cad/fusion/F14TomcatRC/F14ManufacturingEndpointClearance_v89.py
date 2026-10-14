"""v89: extend manufacturing clearance sweep envelopes beyond both Y endpoints."""
import adsk.core, adsk.fusion, json, os, hashlib

def _vol(b): return b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def _shift(temp,b,dx,dy,dz,mm):
    c=temp.copy(b); m=adsk.core.Matrix3D.create(); m.translation=adsk.core.Vector3D.create(mm(dx),mm(dy),mm(dz)); temp.transform(c,m); return c

def run_review(app, build_source_wings, mm, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v89_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('Source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('Archive import failed')
    original=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    names=['CANDIDATE_OUTER_INSERT_MFG_REFINED_v88','CANDIDATE_RIB_ZERO_CLEARANCE_-3','CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS','CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_LOWER_CAP_NOT_STRENGTH_VERIFIED','CANDIDATE_CARBON_R_WEB_NOT_STRENGTH_VERIFIED']
    found={}
    for i in range(original.rootComponent.bRepBodies.count):
        b=original.rootComponent.bRepBodies.item(i)
        if b.name in names: found[b.name]=temp.copy(b)
    miss=[n for n in names if n not in found]
    if miss: raise RuntimeError('Missing v88 bodies '+repr(miss))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_OUTER_INSERT_MFG_ENDPOINT_CLEARANCE_v89'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; bodies={}
    for name,copy in found.items(): b=root.bRepBodies.add(copy); b.name=name; bodies[name]=b
    insert=bodies[names[0]]; inner=bodies[names[1]]; skin=bodies[names[2]]; spars=[bodies[n] for n in names[3:]]
    before=_vol(insert); carved=temp.copy(insert); dist=float(src['insertion_mm']); cc=float(src['carbon_clearance_mm']); sc=float(src['skin_clearance_mm']); ops=0
    # Existing v87/v88 covers blocker shifts from 0 through -dist. Add 3D clearance envelopes beyond both ends.
    for spar in spars:
        offsets=[(dx,dz) for dx in (-cc,0.0,cc) for dz in (-cc,0.0,cc)]
        for dy in (cc,-dist-cc):
            for dx,dz in offsets:
                if not temp.booleanOperation(carved,_shift(temp,spar,dx,dy,dz,mm),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Carbon endpoint carve failed')
                ops+=1
    offsets=[(dx,dz) for dx in (-sc,0.0,sc) for dz in (-sc,0.0,sc)]
    for dy in (sc,-dist-sc):
        for dx,dz in offsets:
            if not temp.booleanOperation(carved,_shift(temp,skin,dx,dy,dz,mm),adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Skin endpoint carve failed')
            ops+=1
    cleared=root.bRepBodies.add(carved); cleared.name='CANDIDATE_OUTER_INSERT_MFG_ENDPOINT_CLEAR_v89'
    if not cleared.isValid or not cleared.isSolid: raise RuntimeError('v89 insert invalid')
    after=_vol(cleared); vs=float(src['verify_step_mm']); nv=int(round(dist/vs)); rows=[]
    for k in range(nv,-1,-1):
        dy=k*vs; scratch=root.bRepBodies.add(_shift(temp,cleared,0,dy,0,mm))
        sg=app.measureManager.measureMinimumDistance(scratch,skin).value*10.0; cg=[app.measureManager.measureMinimumDistance(scratch,s).value*10.0 for s in spars]; rg=app.measureManager.measureMinimumDistance(scratch,inner).value*10.0
        rows.append({'outboard_translation_mm':dy,'skin_gap_mm':sg,'minimum_carbon_gap_mm':min(cg),'carbon_gaps_mm':cg,'inner_rib_gap_mm':rg}); scratch.deleteMe()
    mins=min(x['skin_gap_mm'] for x in rows); minc=min(x['minimum_carbon_gap_mm'] for x in rows); minr=min(x['inner_rib_gap_mm'] for x in rows); axial=app.measureManager.measureMinimumDistance(cleared,inner).value*10.0
    st=float(src['skin_target_mm']); ct=float(src['carbon_target_mm']); sp=mins>=st*0.95; cp=minc>=ct*0.95; ap=abs(axial-float(src['target_axial_gap_mm']))<=0.04
    audit={'status':'V89_MANUFACTURING_ENDPOINT_CLEARANCE','source':src,'endpoint_boolean_operations':ops,'insert':{'before_cm3':before,'after_cm3':after,'incremental_retained_fraction':after/before,'axial_gap_mm':axial},'verification':rows,'minimum_skin_gap_mm':mins,'minimum_carbon_gap_mm':minc,'minimum_inner_rib_gap_mm':minr,'skin_clearance_pass':sp,'carbon_clearance_pass':cp,'axial_gap_pass':ap,'manufacturing_clearance_candidate_pass':sp and cp and ap,'minimum_section_verified_after_endpoint_clearance':False,'fit_coupon_verified':False,'torsion_capacity_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_OUTER_INSERT_MFG_ENDPOINT_CLEARANCE_v89.f3d'))): raise RuntimeError('Export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v89_manufacturing_endpoint_clearance_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v89_manufacturing_endpoint_clearance_review.png'),1600,1000)
    if prior: prior.activate()
    return audit