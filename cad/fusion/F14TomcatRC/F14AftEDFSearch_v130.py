"""v130: exploit E-F axial reserve and search aft EDF position before introducing axis tilt."""
import adsk.core, adsk.fusion, json, os, hashlib

def mm(v): return v/10.0

def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2))
def frange(a,b,s):
    n=int((b-a)/s+1e-9); return [a+i*s for i in range(n+1)]
def fus_eval(temp,fus,x0,L,y,z,d):
    c=cyl_x(temp,x0,x0+L,y,z,d); total=c.volume; q=temp.copy(c); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType); inside=q.volume if ok and q.isValid else 0.0
    return {'x_start_mm':x0,'x_end_mm':x0+L,'y_abs_mm':abs(y),'z_mm':z,'total_cm3':total,'inside_cm3':inside,'outside_cm3':max(0,total-inside),'containment_fraction':inside/total if total else 0.0}
def coll_eval(temp,mods,x0,L,y,z,d):
    c=cyl_x(temp,x0,x0+L,y,z,d); out=[]; total=0.0
    for m in mods:
        q=temp.copy(c); ok=temp.booleanOperation(q,temp.copy(m),adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=q.volume if ok and q.isValid else 0.0; total+=iv; out.append({'body':m.name,'intersection_cm3':iv})
    return total,out

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v130_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['path'],'rb').read()).hexdigest()!=src['sha256']: raise RuntimeError('source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['path'])): raise RuntimeError('import failed')
    imported=app.activeDocument; design=adsk.fusion.Design.cast(app.activeProduct); root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get(); bodies=[root.bRepBodies.item(i) for i in range(root.bRepBodies.count)]
    fus=next(b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'); mods=[b for b in bodies if b.name.startswith('MONOLITHIC_LOWER_HARDPOINT_')]
    xr=[float(v) for v in src['x_start_range_mm']]; yr=[float(v) for v in src['y_abs_range_mm']]; zr=[float(v) for v in src['z_range_mm']]; L=float(src['housing_length_mm']); d=float(src['clear_diameter_mm'])
    coarse=[]
    for x in frange(*xr):
      for y in frange(*yr):
       for z in frange(*zr): coarse.append(fus_eval(temp,fus,x,L,y,z,d))
    coarse.sort(key=lambda r:(r['outside_cm3'],-r['containment_fraction']))
    seed=coarse[0]; hx=float(src['refine_half_window_mm']); xs=float(src['refine_x_step_mm']); yz=float(src['refine_yz_step_mm']); refined=[]
    for x in frange(seed['x_start_mm']-hx,seed['x_start_mm']+hx,xs):
      for y in frange(seed['y_abs_mm']-hx,seed['y_abs_mm']+hx,yz):
       for z in frange(seed['z_mm']-hx,seed['z_mm']+hx,yz): refined.append(fus_eval(temp,fus,x,L,y,z,d))
    refined.sort(key=lambda r:(r['outside_cm3'],-r['containment_fraction'])); best=refined[0]
    coll,collrecs=coll_eval(temp,mods,best['x_start_mm'],L,best['y_abs_mm'],best['z_mm'],d); best['fixed_structure_intersection_cm3']=coll; best['collisions']=collrecs; best['pass']=best['outside_cm3']<=float(src['containment_tolerance_cm3']) and coll<=float(src['collision_tolerance_cm3'])
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_EDF_AFT_POSITION_SEARCH_v130'; rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; rr=rd.rootComponent
    b=rr.bRepBodies.add(temp.copy(fus)); b.name=fus.name
    for m in mods: b=rr.bRepBodies.add(temp.copy(m)); b.name=m.name
    for lab,sgn in [('R',1),('L',-1)]: b=rr.bRepBodies.add(cyl_x(temp,best['x_start_mm'],best['x_end_mm'],sgn*best['y_abs_mm'],best['z_mm'],d)); b.name='EDF_CLEAR_ENVELOPE_'+lab+'_v130'
    audit={'status':'V130_AFT_EDF_POSITION_SEARCH','source':src,'coarse_count':len(coarse),'refined_count':len(refined),'best':best,'top20':refined[:20],'geometry_candidate_pass':best['pass'],'remaining_axial_reserve_to_F_mm':754.962281164333-best['x_end_mm'],'axis_tilt_required_next':not best['pass'],'pivot_waterline_dependency':False,'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_EDF_AFT_POSITION_SEARCH_v130.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v130_aft_edf_position_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v130_aft_edf_position_review.png'),1600,1000)
    try:review.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
      try:prior.activate()
      except:pass
    return audit