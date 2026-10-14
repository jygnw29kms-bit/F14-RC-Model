"""v98: extend lower crosstie riser sockets inboard for 22 mm actual CF tube engagement."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def box(temp,x0,x1,y0,y1,z0,z1):
    c=adsk.core.Point3D.create(mm((x0+x1)/2),mm((y0+y1)/2),mm((z0+z1)/2))
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(x1-x0),mm(y1-y0),mm(z1-z0)))

def vol(b): return b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume

def _bbrec(b):
    bb=b.boundingBox
    return {'x':[bb.minPoint.x*10.0,bb.maxPoint.x*10.0],'y':[bb.minPoint.y*10.0,bb.maxPoint.y*10.0],'z':[bb.minPoint.z*10.0,bb.maxPoint.z*10.0]}

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v98_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['v34_path'],'rb').read()).hexdigest()!=src['v34_sha256']: raise RuntimeError('v34 hash mismatch')
    if hashlib.sha256(open(src['v97_path'],'rb').read()).hexdigest()!=src['v97_sha256']: raise RuntimeError('v97 hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['v34_path'])): raise RuntimeError('v34 import failed')
    orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    needed=['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','SOURCE_GRUMMAN_BASIC_WING_R_v08','SOURCE_GRUMMAN_BASIC_WING_L_v08','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19']
    # Wing names can carry suffix details; resolve by prefix below.
    found={}
    for i in range(orig.rootComponent.bRepBodies.count):
        b=orig.rootComponent.bRepBodies.item(i)
        if b.name in needed or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_R_') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_L_'):
            found[b.name]=temp.copy(b)
    def getexact(n):
        if n in found: return found[n]
        if n.startswith('SOURCE_GRUMMAN_BASIC_WING_R'): return next(v for k,v in found.items() if k.startswith('SOURCE_GRUMMAN_BASIC_WING_R_'))
        if n.startswith('SOURCE_GRUMMAN_BASIC_WING_L'): return next(v for k,v in found.items() if k.startswith('SOURCE_GRUMMAN_BASIC_WING_L_'))
        raise RuntimeError('missing '+n)
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_EXTENDED_CROSSTIE_RETENTION_v98'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; bodies={}
    for n in ['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19']:
        b=root.bRepBodies.add(temp.copy(getexact(n))); b.name=n; bodies[n]=b
    for label in ('R','L'):
        key='SOURCE_GRUMMAN_BASIC_WING_'+label
        b=root.bRepBodies.add(temp.copy(getexact(key))); b.name=key+'_v98_REF'; bodies[key]=b
    # Derive pivot and routed centers from checked project data.
    data=json.load(open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8')); pivot=json.load(open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8'))
    factor=900.0/(2.0*data['sections'][-1]['wbl_in']); px=pivot['derived_full_scale_pivot_fs_in']*factor; py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]; dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in']); pz=(s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz)*factor
    routes={'FRONT':{'xc':px-16.0,'zc':pz-4.5},'REAR':{'xc':px+16.0,'zc':pz-5.5}}
    z0=pz-12.5; yi=float(src['socket_inner_abs_y_mm']); yo=float(src['socket_outer_abs_y_mm']); xw=float(src['socket_x_width_mm']); ch=float(src['channel_size_mm'])
    risers=[]; containment=[]; interfaces=[]
    fus=bodies['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29']
    for fa,r in routes.items():
        tie=bodies['REF_CF6x4_'+fa+'_LOWER_v34']; xc,zc=r['xc'],r['zc']; z1=zc+4.0
        for sign,label in ((1,'R'),(-1,'L')):
            y0,y1=(yi,yo) if sign>0 else (-yo,-yi)
            raw=box(temp,xc-xw/2,xc+xw/2,y0,y1,z0,z1)
            channel=box(temp,xc-ch/2,xc+ch/2,y0-0.1,y1+0.1,zc-ch/2,zc+ch/2)
            if not temp.booleanOperation(raw,channel,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('channel cut failed')
            riser=root.bRepBodies.add(raw); riser.name='ENG_RISER_SOCKET_'+fa+'_'+label+'_v98'; risers.append(riser)
            rv=vol(riser); q=temp.copy(riser); ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=vol(q) if ok and q.isValid else 0.0
            containment.append({'riser':riser.name,'volume_cm3':rv,'inside_fuselage_volume_cm3':iv,'inside_fraction':iv/rv if rv else 0.0})
            fork=bodies['ENG_WINGBOX_FORK_LOWER_'+label+'_v31']; q=temp.copy(riser); ok=temp.booleanOperation(q,temp.copy(fork),adsk.fusion.BooleanTypes.IntersectionBooleanType); fv=vol(q) if ok and q.isValid else 0.0
            # actual axial tube engagement from bounding spans
            tbb=tie.boundingBox; rbb=riser.boundingBox
            if sign>0: eng=max(0.0,min(tbb.maxPoint.y,rbb.maxPoint.y)-max(tbb.minPoint.y,rbb.minPoint.y))*10.0
            else: eng=max(0.0,min(tbb.maxPoint.y,rbb.maxPoint.y)-max(tbb.minPoint.y,rbb.minPoint.y))*10.0
            interfaces.append({'riser':riser.name,'fork_overlap_cm3':fv,'fork_engaged':fv>1e-4,'tube_axial_engagement_mm':eng})
    # dense moving geometry collision screen
    fixed=risers+[bodies['REF_CF6x4_FRONT_LOWER_v34'],bodies['REF_CF6x4_REAR_LOWER_v34']]; checks=[]
    for sweep in range(int(src['sweep_min_deg']),int(src['sweep_max_deg'])+1,int(src['sweep_step_deg'])):
        for sign,label in ((1,'R'),(-1,'L')):
            ang=-sign*math.radians(sweep-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            for mov,kind in ((bodies['SOURCE_GRUMMAN_BASIC_WING_'+label],'outer_wing'),(bodies['ENG_ROOT_LUG_'+label+'_v19'],'root_lug')):
                mc=temp.copy(mov); temp.transform(mc,rot)
                for fp in fixed:
                    q=temp.copy(mc); ok=temp.booleanOperation(q,temp.copy(fp),adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=vol(q) if ok and q.isValid else 0.0
                    checks.append({'sweep_deg':sweep,'side':label,'moving_kind':kind,'fixed_part':fp.name,'intersection_cm3':iv,'collision':iv>1e-4})
    residual=[x for x in checks if x['collision']]; v97=json.load(open(src['v97_path'],encoding='utf-8')); engage=min(x['tube_axial_engagement_mm'] for x in interfaces); area=math.pi*float(src['tube_od_mm'])*engage
    loads={k:{'force_N':v['tube_axial_force_N'],'required_average_interface_shear_MPa':v['tube_axial_force_N']/area} for k,v in v97['equal_front_rear_moment_share'].items()}
    debug_bboxes={n:_bbrec(b) for n,b in bodies.items()}; debug_bboxes.update({r.name:_bbrec(r) for r in risers})
    audit={'status':'V98_EXTENDED_CROSSTIE_RETENTION_PACKAGING','debug_bboxes':debug_bboxes,'source':src,'geometry':{'pivot_mm':[px,py,pz],'routes':routes,'socket_abs_y_span_mm':[yi,yo],'socket_length_mm':yo-yi,'minimum_actual_tube_engagement_mm':engage,'cylindrical_interface_area_mm2':area},'riser_containment':containment,'interfaces':interfaces,'minimum_inside_fraction':min(x['inside_fraction'] for x in containment),'all_forks_engaged':all(x['fork_engaged'] for x in interfaces),'sweep_checks':checks,'residual_collisions':residual,'dense_sweep_clearance_pass':not residual,'equal_share_interface_screen':loads,'no_transverse_tube_hole':True,'adhesive_process_verified':False,'clamp_cap_designed':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); target=os.path.join(outdir,'F14_EXTENDED_CROSSTIE_RETENTION_v98.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v98_extended_crosstie_retention_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v98_extended_crosstie_retention_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit