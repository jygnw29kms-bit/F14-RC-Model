"""v99: circular 6.4 mm crosstie sockets plus distance-based continuous sweep-clearance certificate."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def box(temp,x0,x1,y0,y1,z0,z1):
    c=adsk.core.Point3D.create(mm((x0+x1)/2),mm((y0+y1)/2),mm((z0+z1)/2))
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(x1-x0),mm(y1-y0),mm(z1-z0)))

def cyl_y(temp,x,y0,y1,z,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(y0),mm(z)),mm(d/2.0),adsk.core.Point3D.create(mm(x),mm(y1),mm(z)),mm(d/2.0))

def bbrec(b):
    q=b.boundingBox; return {'x':[q.minPoint.x*10,q.maxPoint.x*10],'y':[q.minPoint.y*10,q.maxPoint.y*10],'z':[q.minPoint.z*10,q.maxPoint.z*10]}

def rmax_xy(body,px,py):
    bb=body.boundingBox; xs=[bb.minPoint.x*10,bb.maxPoint.x*10]; ys=[bb.minPoint.y*10,bb.maxPoint.y*10]
    return max(math.hypot(x-px,y-py) for x in xs for y in ys)

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v99_section_inputs.json'),encoding='utf-8'))
    for p,h in ((src['v34_path'],src['v34_sha256']),(src['v97_path'],src['v97_sha256'])):
        if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: raise RuntimeError('source hash mismatch '+p)
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(src['v34_path'])): raise RuntimeError('v34 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    found={}
    for i in range(orig.rootComponent.bRepBodies.count):
        b=orig.rootComponent.bRepBodies.item(i)
        if b.name in ('UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_R_') or b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_L_'):
            found[b.name]=temp.copy(b)
    def get(n):
        if n in found:return found[n]
        return next(v for k,v in found.items() if k.startswith(n+'_'))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_CIRCULAR_CROSSTIE_RETENTION_v99'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; bodies={}
    for n in ('UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29','REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','ENG_WINGBOX_FORK_LOWER_R_v31','ENG_WINGBOX_FORK_LOWER_L_v31','ENG_ROOT_LUG_R_v19','ENG_ROOT_LUG_L_v19'):
        b=root.bRepBodies.add(temp.copy(get(n)));b.name=n;bodies[n]=b
    for lab in ('R','L'):
        n='SOURCE_GRUMMAN_BASIC_WING_'+lab; b=root.bRepBodies.add(temp.copy(get(n)));b.name=n+'_v99_REF';bodies[n]=b
    data=json.load(open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8')); pivot=json.load(open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8'))
    factor=900.0/(2.0*data['sections'][-1]['wbl_in']);px=pivot['derived_full_scale_pivot_fs_in']*factor;py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1];dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in']);pz=(s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz)*factor
    routes={'FRONT':{'xc':px-16.0,'zc':pz-4.5},'REAR':{'xc':px+16.0,'zc':pz-5.5}};z0=pz-12.5;yi=float(src['socket_inner_abs_y_mm']);yo=float(src['socket_outer_abs_y_mm']);d=float(src['round_bore_diameter_mm']);xw=float(src['socket_x_width_mm'])
    fus=bodies['UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'];risers=[];contain=[];interfaces=[]
    for fa,r in routes.items():
        tie=bodies['REF_CF6x4_'+fa+'_LOWER_v34'];xc,zc=r['xc'],r['zc'];z1=zc+4.0
        for sign,lab in ((1,'R'),(-1,'L')):
            ya,yb=(yi,yo) if sign>0 else (-yo,-yi); raw=box(temp,xc-xw/2,xc+xw/2,ya,yb,z0,z1); bore=cyl_y(temp,xc,ya-0.1,yb+0.1,zc,d)
            if not temp.booleanOperation(raw,bore,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('round bore cut failed')
            ris=root.bRepBodies.add(raw);ris.name='ENG_RISER_CIRCULAR_'+fa+'_'+lab+'_v99';risers.append(ris)
            rv=ris.volume;q=temp.copy(ris);ok=temp.booleanOperation(q,temp.copy(fus),adsk.fusion.BooleanTypes.IntersectionBooleanType);iv=q.volume if ok and q.isValid else 0
            fork=bodies['ENG_WINGBOX_FORK_LOWER_'+lab+'_v31']; q2=temp.copy(ris);ok2=temp.booleanOperation(q2,temp.copy(fork),adsk.fusion.BooleanTypes.IntersectionBooleanType);fv=q2.volume if ok2 and q2.isValid else 0
            tb=tie.boundingBox;rb=ris.boundingBox;eng=max(0,min(tb.maxPoint.y,rb.maxPoint.y)-max(tb.minPoint.y,rb.minPoint.y))*10
            contain.append({'riser':ris.name,'volume_cm3':rv,'inside_fraction':iv/rv if rv else 0,'inside_cm3':iv});interfaces.append({'riser':ris.name,'fork_overlap_cm3':fv,'fork_engaged':fv>1e-4,'tube_engagement_mm':eng})
    fixed=risers+[bodies['REF_CF6x4_FRONT_LOWER_v34'],bodies['REF_CF6x4_REAR_LOWER_v34']]
    step=float(src['sweep_step_deg']);s0deg=float(src['sweep_min_deg']);s1deg=float(src['sweep_max_deg']);pairs={}; sample_count=0
    n=int(round((s1deg-s0deg)/step))
    for ii in range(n+1):
        sweep=s0deg+ii*step
        for sign,lab in ((1,'R'),(-1,'L')):
            ang=-sign*math.radians(sweep-20.0);rot=adsk.core.Matrix3D.create();rot.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            for mov,kind in ((bodies['SOURCE_GRUMMAN_BASIC_WING_'+lab],'outer_wing'),(bodies['ENG_ROOT_LUG_'+lab+'_v19'],'root_lug')):
                mc=temp.copy(mov);temp.transform(mc,rot); sample_count+=1
                for fp in fixed:
                    key=lab+'|'+kind+'|'+fp.name
                    try: dist=app.measureManager.measureMinimumDistance(mc,fp).value*10.0
                    except: 
                        scratch=root.bRepBodies.add(temp.copy(mc));dist=app.measureManager.measureMinimumDistance(scratch,fp).value*10.0;scratch.deleteMe()
                    rec=pairs.setdefault(key,{'side':lab,'moving_kind':kind,'fixed_part':fp.name,'minimum_sampled_clearance_mm':1e99,'at_sweep_deg':None})
                    if dist<rec['minimum_sampled_clearance_mm']:rec['minimum_sampled_clearance_mm']=dist;rec['at_sweep_deg']=sweep
    cert=[]
    for key,rec in pairs.items():
        mov=bodies['SOURCE_GRUMMAN_BASIC_WING_'+rec['side']] if rec['moving_kind']=='outer_wing' else bodies['ENG_ROOT_LUG_'+rec['side']+'_v19']; rr=rmax_xy(mov,px,(1 if rec['side']=='R' else -1)*py); bound=2*rr*math.sin(math.radians(step)/4.0); margin=rec['minimum_sampled_clearance_mm']-bound
        rec.update({'moving_rmax_mm':rr,'half_step_motion_bound_mm':bound,'continuous_clearance_lower_bound_mm':margin,'continuous_pass':margin>float(src['continuous_margin_required_mm'])});cert.append(rec)
    eng=min(x['tube_engagement_mm'] for x in interfaces);geom_area=math.pi*float(src['tube_od_mm'])*eng; v97=json.load(open(src['v97_path'],encoding='utf-8'));loads={k:{'force_N':v['tube_axial_force_N'],'geometric_annulus_interface_area_mm2':geom_area,'required_average_shear_MPa':v['tube_axial_force_N']/geom_area} for k,v in v97['equal_front_rear_moment_share'].items()}
    audit={'status':'V99_CIRCULAR_CROSSTIE_RETENTION_CONTINUOUS_CLEARANCE','source':src,'geometry':{'pivot_mm':[px,py,pz],'socket_length_mm':yo-yi,'minimum_tube_engagement_mm':eng,'bore_diameter_mm':d,'tube_od_mm':src['tube_od_mm'],'nominal_radial_bondline_mm':(d-float(src['tube_od_mm']))/2,'geometric_cylindrical_interface_area_mm2':geom_area},'containment':contain,'interfaces':interfaces,'minimum_inside_fraction':min(x['inside_fraction'] for x in contain),'all_forks_engaged':all(x['fork_engaged'] for x in interfaces),'clearance_certificate':cert,'sweep_step_deg':step,'sampled_moving_states':sample_count,'continuous_sweep_clearance_pass':all(x['continuous_pass'] for x in cert),'minimum_continuous_clearance_lower_bound_mm':min(x['continuous_clearance_lower_bound_mm'] for x in cert),'equal_share_interface_screen':loads,'full_360_bond_coverage_geometrically_available':True,'adhesive_fill_and_surface_process_verified':False,'material_allowable_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); f3d=os.path.join(outdir,'F14_CIRCULAR_CROSSTIE_RETENTION_v99.f3d');design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(f3d));json.dump(audit,open(os.path.join(outdir,'F14_v99_circular_crosstie_retention_audit.json'),'w',encoding='utf-8'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v99_circular_crosstie_retention_review.png'),1600,1000)
    try:doc.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit