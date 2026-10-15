"""v129: direct twin-EDF clearance-envelope search in registered v105 fuselage/wingbox CAD."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2.0),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2.0))

def frange(a,b,s):
    n=int(round((b-a)/s)); return [a+i*s for i in range(n+1)]

def evaluate(temp,fus,mods,x0,x1,y,z,d,contain_tol,coll_tol):
    c=cyl_x(temp,x0,x1,y,z,d); total=c.volume
    q=temp.copy(c); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=q.volume if ok and q.isValid else 0.0; outside=max(0.0,total-inside)
    collisions=[]; coll_total=0.0
    for m in mods:
        q=temp.copy(c); ok=temp.booleanOperation(q,temp.copy(m),adsk.fusion.BooleanTypes.IntersectionBooleanType)
        iv=q.volume if ok and q.isValid else 0.0; coll_total+=iv; collisions.append({'body':m.name,'intersection_cm3':iv})
    passed=outside<=contain_tol and coll_total<=coll_tol
    return {'y_abs_mm':abs(y),'z_mm':z,'total_cm3':total,'inside_fuselage_cm3':inside,'outside_fuselage_cm3':outside,'containment_fraction':inside/total if total else 0.0,'fixed_structure_intersection_cm3':coll_total,'collisions':collisions,'pass':passed}

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v129_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('v129 source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('v105 import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get()
    bodies=[root.bRepBodies.item(i) for i in range(root.bRepBodies.count)]
    fus=next((b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'),None)
    mods=[b for b in bodies if b.name.startswith('MONOLITHIC_LOWER_HARDPOINT_')]
    if fus is None or len(mods)!=2: raise RuntimeError('unexpected v105 inventory '+repr([b.name for b in bodies]))
    x0=float(src['x_start_mm']); x1=x0+float(src['housing_length_mm']); d=float(src['clear_diameter_mm']); ct=float(src['containment_tolerance_cm3']); mt=float(src['collision_tolerance_cm3'])
    ya,yb,ys=[float(x) for x in src['coarse_y_abs_mm']]; za,zb,zs=[float(x) for x in src['coarse_z_mm']]
    records=[]
    for y in frange(ya,yb,ys):
        for z in frange(za,zb,zs): records.append(evaluate(temp,fus,mods,x0,x1,y,z,d,ct,mt))
    records.sort(key=lambda r:(not r['pass'],r['outside_fuselage_cm3']+r['fixed_structure_intersection_cm3'],-r['containment_fraction']))
    seed=records[0]; step=float(src['refine_step_mm']); hw=float(src['refine_half_window_mm']); refined=[]
    for y in frange(seed['y_abs_mm']-hw,seed['y_abs_mm']+hw,step):
        for z in frange(seed['z_mm']-hw,seed['z_mm']+hw,step): refined.append(evaluate(temp,fus,mods,x0,x1,y,z,d,ct,mt))
    refined.sort(key=lambda r:(not r['pass'],r['outside_fuselage_cm3']+r['fixed_structure_intersection_cm3'],-r['containment_fraction']))
    best=refined[0]
    # For a passing nominal envelope, estimate extra radial reserve in 0.1 mm radius increments.
    reserve=0.0; reserve_trials=[]
    if best['pass']:
        for extra in [i/10.0 for i in range(1,21)]:
            rr=evaluate(temp,fus,mods,x0,x1,best['y_abs_mm'],best['z_mm'],d+2*extra,ct,mt); reserve_trials.append({'extra_radial_mm':extra,'pass':rr['pass'],'outside_cm3':rr['outside_fuselage_cm3'],'collision_cm3':rr['fixed_structure_intersection_cm3']})
            if rr['pass']: reserve=extra
            else: break
    # Create visible R/L envelopes only for review.
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_TWIN_EDF_DIRECT_CLEARANCE_v129'; rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; rr=rd.rootComponent
    rf=rr.bRepBodies.add(temp.copy(fus)); rf.name=fus.name
    for m in mods: b=rr.bRepBodies.add(temp.copy(m)); b.name=m.name
    for lab,sgn in [('R',1),('L',-1)]:
        b=rr.bRepBodies.add(cyl_x(temp,x0,x1,sgn*best['y_abs_mm'],best['z_mm'],d)); b.name='EDF_CLEAR_ENVELOPE_'+lab+'_v129'
    audit={'status':'V129_DIRECT_EDF_CLEARANCE_SEARCH','source':src,'inventory':[b.name for b in bodies],'search':{'coarse_count':len(records),'refined_count':len(refined),'best':best,'top10':refined[:10]},'extra_radial_reserve_mm':reserve,'reserve_trials':reserve_trials,'symmetric_twin_assumption':True,'geometry_candidate_pass':bool(best['pass']),'pivot_waterline_dependency':False,'continuous_inlet_duct_verified':False,'exhaust_duct_verified':False,'installed_thrust_verified':False,'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); target=os.path.join(outdir,'F14_TWIN_EDF_DIRECT_CLEARANCE_v129.f3d'); rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(target)); json.dump(audit,open(os.path.join(outdir,'F14_v129_direct_edf_clearance_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v129_direct_edf_clearance_review.png'),1600,1000)
    try:review.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit