"""v131: source-backed D/E/F aft nacelle loft and direct EDF clearance test."""
import adsk.core, adsk.fusion, json, os, hashlib

def mm(v): return v/10.0

def frange(a,b,s):
    n=int((b-a)/s+1e-9); return [a+i*s for i in range(n+1)]
def plane_x(comp,x):
    inp=comp.constructionPlanes.createInput(); inp.setByOffset(comp.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x))); return comp.constructionPlanes.add(inp)
def model_point(sk,x,y,z):
    p=adsk.core.Point3D.create(mm(x),mm(y),mm(z)); q=sk.modelToSketchSpace(p); return q
def add_profile(comp,x,pts,name):
    sk=comp.sketches.add(plane_x(comp,x)); sk.name=name; lines=sk.sketchCurves.sketchLines; pp=[model_point(sk,x,y,z) for y,z in pts]
    for i in range(len(pp)): lines.addByTwoPoints(pp[i],pp[(i+1)%len(pp)])
    if sk.profiles.count<1: raise RuntimeError('no profile '+name)
    return sk.profiles.item(0)
def cyl_x(temp,x0,x1,y,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d/2),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d/2))
def eval_cyl(temp,solid,x0,L,y,z,d):
    c=cyl_x(temp,x0,x0+L,y,z,d); total=c.volume; q=temp.copy(c); ok=temp.booleanOperation(q,temp.copy(solid),adsk.fusion.BooleanTypes.IntersectionBooleanType); inside=min(total,q.volume) if ok and q.isValid else 0.0
    return {'x_start_mm':x0,'x_end_mm':x0+L,'y_abs_mm':abs(y),'z_mm':z,'total_cm3':total,'inside_cm3':inside,'outside_cm3':max(0,total-inside),'containment_fraction':inside/total if total else 0.0}
def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v131_section_inputs.json'),encoding='utf-8'))
    sections=[]; common=float(cfg['common_scale_mm_per_pixel']); refside=float(cfg['reference_axis_side_pixel_y'])
    for s in cfg['sections']:
        for key in ('contour','registration'):
            raw=open(s[key]['path'],'rb').read()
            if hashlib.sha256(raw).hexdigest()!=s[key]['sha256']: raise RuntimeError('hash mismatch '+s['name']+' '+key)
        c=json.load(open(s['contour']['path'],encoding='utf-8')); reg=json.load(open(s['registration']['path'],encoding='utf-8'))
        if c.get('source_image_sha256')!=cfg['source_image_sha256'] or reg.get('source_image_sha256')!=cfg['source_image_sha256']: raise RuntimeError('source raster mismatch '+s['name'])
        fit=float(reg.get('isotropic_multiplier',reg.get('isotropic_section_width_multiplier'))); ax,ay=[float(v) for v in c['source_section_axis_pixel']]; zaxis=(refside-float(s['axis_side_pixel_y']))*common
        pts=[((float(p[0])-ax)*common*fit, -(float(p[1])-ay)*common*fit+zaxis) for p in c['pixel_outline']]
        sections.append({'name':s['name'],'x_mm':float(s['x_mm']),'fit':fit,'z_axis_mm':zaxis,'pts':pts})
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_SOURCE_BACKED_AFT_NACELLE_v131'; design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    section_meta=[]
    for s in sections:
        li.loftSections.add(add_profile(root,s['x_mm'],s['pts'],'SOURCE_'+s['name']+'_v131'))
        ys=[p[0] for p in s['pts']]; zs=[p[1] for p in s['pts']]; section_meta.append({'name':s['name'],'x_mm':s['x_mm'],'fit':s['fit'],'z_axis_mm':s['z_axis_mm'],'bounds_mm':{'y':[min(ys),max(ys)],'z':[min(zs),max(zs)]},'point_count':len(s['pts'])})
    feat=root.features.loftFeatures.add(li)
    if not feat or feat.bodies.count!=1: raise RuntimeError('source aft loft failed')
    aft=feat.bodies.item(0); aft.name='SOURCE_BACKED_AFT_NACELLE_D_E_F_v131'; temp=adsk.fusion.TemporaryBRepManager.get(); xr=[float(v) for v in cfg['x_start_range_mm']]; yr=[float(v) for v in cfg['y_abs_range_mm']]; zr=[float(v) for v in cfg['z_range_mm']]; L=float(cfg['housing_length_mm']); d=float(cfg['clear_diameter_mm'])
    coarse=[]
    for x in frange(*xr):
      for y in frange(*yr):
       for z in frange(*zr): coarse.append(eval_cyl(temp,aft,x,L,y,z,d))
    coarse.sort(key=lambda r:(r['outside_cm3'],-r['containment_fraction'])); seed=coarse[0]; st=float(cfg['refine_step_mm']); hw=float(cfg['refine_half_window_mm']); refined=[]
    for x in frange(seed['x_start_mm']-hw,seed['x_start_mm']+hw,st):
      for y in frange(seed['y_abs_mm']-hw,seed['y_abs_mm']+hw,st):
       for z in frange(seed['z_mm']-hw,seed['z_mm']+hw,st): refined.append(eval_cyl(temp,aft,x,L,y,z,d))
    refined.sort(key=lambda r:(r['outside_cm3'],-r['containment_fraction'])); best=refined[0]; best['pass']=best['outside_cm3']<=float(cfg['containment_tolerance_cm3'])
    for lab,sgn in [('R',1),('L',-1)]:
        b=root.bRepBodies.add(cyl_x(temp,best['x_start_mm'],best['x_end_mm'],sgn*best['y_abs_mm'],best['z_mm'],d)); b.name='EDF_CLEAR_ENVELOPE_'+lab+'_v131'
    audit={'status':'V131_SOURCE_BACKED_AFT_NACELLE_EDF_GATE','source_image_sha256':cfg['source_image_sha256'],'sections':section_meta,'coarse_count':len(coarse),'refined_count':len(refined),'best':best,'top20':refined[:20],'source_loft_valid':True,'geometry_candidate_pass':best['pass'],'v29_dependency':False,'absolute_aircraft_WL_dependency':False,'remaining_axial_reserve_to_F_mm':sections[-1]['x_mm']-best['x_end_mm'],'continuous_source_loft_clearance_verified':best['pass'],'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_SOURCE_BACKED_AFT_NACELLE_v131.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v131_source_aft_nacelle_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v131_source_aft_nacelle_review.png'),1600,1000)
    try:doc.close(False)
    except:pass
    if prior:
      try:prior.activate()
      except:pass
    return audit