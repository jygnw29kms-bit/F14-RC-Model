"""v140: union v139 inlet wall with provisional 8 mm EDF mount transition; validate source containment and annular interfaces."""
import adsk.core, adsk.fusion, json, os, hashlib

def mm(v): return v/10.0

def cone_x(temp,x0,x1,y,z,d0,d1):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y),mm(z)),mm(d0/2.0),adsk.core.Point3D.create(mm(x1),mm(y),mm(z)),mm(d1/2.0))
def intersect_volume(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0
def run_review(app, builder, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v140_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']: raise RuntimeError('v140 source hash mismatch')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])): raise RuntimeError('v139 import failed')
    imported=app.activeDocument; orig=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get(); bodies=[orig.rootComponent.bRepBodies.item(i) for i in range(orig.rootComponent.bRepBodies.count)]
    ref=next((b for b in bodies if b.name=='REFERENCE_SOURCE_SILHOUETTE_GUIDED_AFT_v135'),None); walls={lab:next((b for b in bodies if b.name=='INLET_WALL_COMPLETE_ENDS_'+lab+'_v139'),None) for lab in ('R','L')}
    if ref is None or any(v is None for v in walls.values()): raise RuntimeError('unexpected v139 inventory '+repr([b.name for b in bodies]))
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_INLET_WITH_EDF_MOUNT_INTERFACE_v140'; design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    source=root.bRepBodies.add(temp.copy(ref)); source.name=ref.name; records=[]
    for lab,sgn in [('R',1),('L',-1)]:
        y=sgn*float(cfg['center_abs_y_mm']); z=float(cfg['center_z_mm']); x0=float(cfg['interface_x_mm']); x1=float(cfg['mount_end_x_mm'])
        outer=cone_x(temp,x0,x1,y,z,float(cfg['duct_outer_diameter_mm']),float(cfg['mount_outer_diameter_mm']))
        inner=cone_x(temp,x0,x1,y,z,float(cfg['duct_inner_diameter_mm']),float(cfg['mount_inner_diameter_mm']))
        if not temp.booleanOperation(outer,inner,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('adapter wall difference failed '+lab)
        adapter_volume=outer.volume; adapter_inside=intersect_volume(temp,outer,source); adapter_out=max(0.0,adapter_volume-adapter_inside)
        combined=temp.copy(walls[lab]); before=combined.volume
        union_ok=temp.booleanOperation(combined,temp.copy(outer),adsk.fusion.BooleanTypes.UnionBooleanType)
        if not union_ok or not combined.isValid: raise RuntimeError('duct-adapter union failed '+lab)
        body=root.bRepBodies.add(combined); body.name='INLET_EDF_MOUNT_ASSEMBLY_'+lab+'_v140'
        total=body.volume; inside=intersect_volume(temp,body,source); outside=max(0.0,total-inside)
        cones=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]; gaps=[]
        for i in range(len(cones)):
            for j in range(i+1,len(cones)):
                try:
                    d=app.measureManager.measureMinimumDistance(cones[i],cones[j]).value*10.0
                    if d>1e-5:gaps.append(d)
                except: pass
        planar=[]; xfaces=[]
        for f in body.faces:
            pl=adsk.core.Plane.cast(f.geometry)
            if not pl: continue
            rec={'x_mm':pl.origin.x*10.0,'area_mm2':f.area*100.0,'loop_count':f.loops.count,'normal':[pl.normal.x,pl.normal.y,pl.normal.z]}; planar.append(rec)
            if abs(abs(pl.normal.x)-1.0)<1e-7 and abs(pl.normal.y)<1e-7 and abs(pl.normal.z)<1e-7:xfaces.append(rec)
        xfaces.sort(key=lambda q:q['x_mm']); end_pass=len(xfaces)==2 and all(f['loop_count']==2 for f in xfaces) and abs(xfaces[0]['x_mm']-595.8483908511422)<1e-5 and abs(xfaces[1]['x_mm']-x1)<1e-5
        min_gap=min(gaps) if gaps else None; wall_pass=min_gap is not None and min_gap>=float(cfg['minimum_wall_mm']); contain_pass=outside<=float(cfg['containment_tolerance_cm3']) and adapter_out<=float(cfg['containment_tolerance_cm3'])
        records.append({'side':lab,'adapter_volume_cm3':adapter_volume,'adapter_outside_source_cm3':adapter_out,'combined_volume_cm3':total,'union_volume_gain_cm3':total-before,'combined_outside_source_cm3':outside,'containment_pass':contain_pass,'conical_face_count':len(cones),'minimum_nonzero_conical_face_gap_mm':min_gap,'minimum_wall_pass':wall_pass,'x_plane_end_faces':xfaces,'all_planar_faces':planar,'complete_end_interfaces_pass':end_pass,'pass':contain_pass and wall_pass and end_pass})
    passed=all(r['pass'] for r in records); audit={'status':'V140_PROVISIONAL_EDF_MOUNT_INTERFACE_GATE','source':cfg,'records':records,'bilateral_geometry_pass':passed,'actual_EDF_shroud_measured':False,'hardware_revision_frozen':False,'mount_is_parametric_candidate':True,'installed_thrust_verified':False,'thermal_verified':False,'geometry_candidate_pass':passed,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_INLET_WITH_EDF_MOUNT_INTERFACE_v140.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v140_edf_mount_interface_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v140_edf_mount_interface_review.png'),1600,1000)
    try:doc.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit