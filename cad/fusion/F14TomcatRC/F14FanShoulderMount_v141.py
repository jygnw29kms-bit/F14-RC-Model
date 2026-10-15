"""v141: overlapping fan shoulder/collar eliminates face-only v140 mount union."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def ring_x(temp,x0,x1,y0,z0,y1,z1,od0,od1,id0,id1):
    outer=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(od0/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(od1/2))
    inner=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(id0/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(id1/2))
    if not temp.booleanOperation(outer,inner,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('ring difference failed')
    return outer

def ivol(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0

def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v141_section_inputs.json'),encoding='utf-8'))
    for p,h in ((cfg['path'],cfg['sha256']),(cfg['v139_audit_path'],cfg['v139_audit_sha256'])):
        if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: raise RuntimeError('v141 source hash mismatch '+p)
    a139=json.load(open(cfg['v139_audit_path'],encoding='utf-8')); inherited_min=min(float(r['minimum_inner_outer_face_gap_mm']) for r in a139['records'])
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])): raise RuntimeError('v139 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get(); srcb=[orig.rootComponent.bRepBodies.item(i) for i in range(orig.rootComponent.bRepBodies.count)]
    ref=next(b for b in srcb if b.name=='REFERENCE_SOURCE_SILHOUETTE_GUIDED_AFT_v135'); walls={lab:next(b for b in srcb if b.name=='INLET_WALL_COMPLETE_ENDS_'+lab+'_v139') for lab in ('R','L')}
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_INLET_FAN_SHOULDER_MOUNT_v141'; design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; source=root.bRepBodies.add(temp.copy(ref)); source.name=ref.name
    xif=float(cfg['interface_x_mm']); xf=float(cfg['flange_start_x_mm']); xe=float(cfg['sleeve_end_x_mm']); records=[]
    # v139 centerline D->fan is linear; evaluate center one mm upstream from fixed fan face.
    D={'x':595.8483908511422,'y':56.30470783882318,'z':-6.556713425255683}; F={'x':650.0,'y':float(cfg['center_abs_y_mm']),'z':float(cfg['center_z_mm'])}
    t=(xf-D['x'])/(F['x']-D['x']); yf=D['y']+(F['y']-D['y'])*t; zf=D['z']+(F['z']-D['z'])*t
    for lab,sgn in [('R',1),('L',-1)]:
        wall=temp.copy(walls[lab]); flange=ring_x(temp,xf,xif,sgn*yf,zf,sgn*F['y'],F['z'],float(cfg['flange_outer_diameter_mm']),float(cfg['flange_outer_diameter_mm']),float(cfg['flange_inner_diameter_mm']),float(cfg['flange_inner_diameter_mm']))
        sleeve=ring_x(temp,xif,xe,sgn*F['y'],F['z'],sgn*F['y'],F['z'],float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']))
        mount=temp.copy(flange)
        if not temp.booleanOperation(mount,temp.copy(sleeve),adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('mount union failed '+lab)
        mount_vol=mount.volume; mount_out=max(0.0,mount_vol-ivol(temp,mount,source))
        before=wall.volume
        if not temp.booleanOperation(wall,temp.copy(mount),adsk.fusion.BooleanTypes.UnionBooleanType) or not wall.isValid: raise RuntimeError('overlap union failed '+lab)
        body=root.bRepBodies.add(wall); body.name='INLET_FAN_SHOULDER_ASSEMBLY_'+lab+'_v141'; total=body.volume; outside=max(0.0,total-ivol(temp,body,source))
        planar=[]; xfaces=[]
        for f in body.faces:
            pl=adsk.core.Plane.cast(f.geometry)
            if not pl: continue
            rec={'x_mm':pl.origin.x*10.0,'area_mm2':f.area*100.0,'loop_count':f.loops.count,'normal':[pl.normal.x,pl.normal.y,pl.normal.z]}; planar.append(rec)
            if abs(abs(pl.normal.x)-1)<1e-7 and abs(pl.normal.y)<1e-7 and abs(pl.normal.z)<1e-7:xfaces.append(rec)
        xfaces.sort(key=lambda q:q['x_mm']); physical_ends=[f for f in xfaces if abs(f['x_mm']-595.8483908511422)<1e-5 or abs(f['x_mm']-xe)<1e-5]
        internal_at_interface=[f for f in xfaces if abs(f['x_mm']-xif)<1e-5]
        end_pass=len(physical_ends)==2 and all(f['loop_count']==2 for f in physical_ends)
        contain_pass=mount_out<=float(cfg['containment_tolerance_cm3']) and outside<=float(cfg['containment_tolerance_cm3'])
        mount_radial_wall=(float(cfg['sleeve_outer_diameter_mm'])-float(cfg['sleeve_inner_diameter_mm']))/2; flange_radial=(float(cfg['flange_outer_diameter_mm'])-float(cfg['flange_inner_diameter_mm']))/2; min_wall=min(inherited_min,mount_radial_wall,flange_radial); wall_pass=min_wall>=float(cfg['minimum_wall_mm'])
        records.append({'side':lab,'mount_volume_cm3':mount_vol,'mount_outside_source_cm3':mount_out,'combined_volume_cm3':total,'overlap_union_gain_cm3':total-before,'combined_outside_source_cm3':outside,'containment_pass':contain_pass,'inherited_v139_min_wall_mm':inherited_min,'sleeve_radial_wall_mm':mount_radial_wall,'flange_radial_wall_mm':flange_radial,'governing_wall_mm':min_wall,'minimum_wall_pass':wall_pass,'physical_x_end_faces':physical_ends,'residual_interface_faces_x650':internal_at_interface,'complete_physical_end_interfaces_pass':end_pass,'pass':contain_pass and wall_pass and end_pass})
    passed=all(r['pass'] for r in records); audit={'status':'V141_OVERLAPPING_FAN_SHOULDER_MOUNT','source':cfg,'records':records,'bilateral_geometry_pass':passed,'flow_throat_diameter_mm':float(cfg['flange_inner_diameter_mm']),'provisional_shroud_sleeve_ID_mm':float(cfg['sleeve_inner_diameter_mm']),'hardware_measurement_required':True,'actual_EDF_shroud_measured':False,'hardware_revision_frozen':False,'geometry_candidate_pass':passed,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INLET_FAN_SHOULDER_MOUNT_v141.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v141_fan_shoulder_mount_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v141_fan_shoulder_mount_review.png'),1600,1000)
    try:doc.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit