"""v139: extend inlet cone beyond D/fan planes, clip back to X-domain, verify complete annular interfaces."""
import adsk.core, adsk.fusion, json, os, hashlib, math

def mm(v): return v/10.0

def lerp(a,b,t): return a+(b-a)*t

def point_at(a,b,x):
    t=(x-float(a['x']))/(float(b['x'])-float(a['x']))
    return {'x':x,'y':lerp(float(a['y']),float(b['y']),t),'z':lerp(float(a['z']),float(b['z']),t),
            'outer_diameter_mm':lerp(float(a['outer_diameter_mm']),float(b['outer_diameter_mm']),t),
            'inner_diameter_mm':lerp(float(a['inner_diameter_mm']),float(b['inner_diameter_mm']),t)}

def cone(temp,a,b,key):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(a['x']),mm(a['y']),mm(a['z'])),mm(a[key]/2.0),
                                     adsk.core.Point3D.create(mm(b['x']),mm(b['y']),mm(b['z'])),mm(b[key]/2.0))

def xclip(temp,x0,x1):
    c=adsk.core.Point3D.create(mm((x0+x1)/2),0,0)
    box=adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(x1-x0),mm(1000),mm(1000))
    return temp.createBox(box)

def containment(temp,body,source):
    total=body.volume; q=temp.copy(body)
    ok=temp.booleanOperation(q,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    inside=q.volume if ok and q.isValid else 0.0
    return total,inside,max(0.0,total-inside)

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v139_section_inputs.json'),encoding='utf-8'))
    for p,h in ((cfg['source_path'],cfg['source_sha256']),(cfg['corridor_audit_path'],cfg['corridor_audit_sha256'])):
        if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: raise RuntimeError('v139 source hash mismatch '+p)
    corridor=json.load(open(cfg['corridor_audit_path'],encoding='utf-8')); pts=corridor['chosen_path']; a=pts[0]; b=pts[-1]
    x0=float(a['x']); x1=float(b['x']); ext=float(cfg['extension_each_end_mm']); ae=point_at(a,b,x0-ext); be=point_at(a,b,x1+ext)
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])): raise RuntimeError('v135 import failed')
    imported=app.activeDocument; od=adsk.fusion.Design.cast(app.activeProduct); temp=adsk.fusion.TemporaryBRepManager.get()
    source=next((od.rootComponent.bRepBodies.item(i) for i in range(od.rootComponent.bRepBodies.count) if od.rootComponent.bRepBodies.item(i).name=='SOURCE_SILHOUETTE_GUIDED_AFT_v135'),None)
    if source is None: raise RuntimeError('source body missing')
    source_copy=temp.copy(source)
    review=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); review.name='F14_COMPLETE_ANNULAR_INLET_ENDS_v139'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    ref=root.bRepBodies.add(temp.copy(source_copy)); ref.name='REFERENCE_SOURCE_SILHOUETTE_GUIDED_AFT_v135'
    clip=xclip(temp,x0,x1); records=[]
    for lab,sgn in [('R',1),('L',-1)]:
        aa=dict(ae); bb=dict(be); aa['y']=sgn*abs(float(aa['y'])); bb['y']=sgn*abs(float(bb['y']))
        outer=cone(temp,aa,bb,'outer_diameter_mm'); inner=cone(temp,aa,bb,'inner_diameter_mm')
        if not temp.booleanOperation(outer,inner,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('wall difference failed '+lab)
        if not temp.booleanOperation(outer,temp.copy(clip),adsk.fusion.BooleanTypes.IntersectionBooleanType): raise RuntimeError('domain clip failed '+lab)
        body=root.bRepBodies.add(outer); body.name='INLET_WALL_COMPLETE_ENDS_'+lab+'_v139'
        if not body.isValid or not body.isSolid: raise RuntimeError('invalid wall '+lab)
        total,inside,outside=containment(temp,body,ref)
        cones=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
        if len(cones)!=2: raise RuntimeError('expected two conical faces '+lab+' got '+str(len(cones)))
        gap=app.measureManager.measureMinimumDistance(cones[0],cones[1]).value*10.0
        xends=[]; other_planar=[]
        for f in body.faces:
            pl=adsk.core.Plane.cast(f.geometry)
            if not pl: continue
            nx,ny,nz=pl.normal.x,pl.normal.y,pl.normal.z; rec={'x_mm':pl.origin.x*10.0,'area_mm2':f.area*100.0,'loop_count':f.loops.count,'normal':[nx,ny,nz]}
            if abs(abs(nx)-1.0)<1e-7 and abs(ny)<1e-7 and abs(nz)<1e-7: xends.append(rec)
            else: other_planar.append(rec)
        xends.sort(key=lambda r:r['x_mm'])
        end_pass=len(xends)==2 and all(r['loop_count']==2 for r in xends) and abs(xends[0]['x_mm']-x0)<1e-5 and abs(xends[1]['x_mm']-x1)<1e-5 and len(other_planar)==0
        thick_pass=abs(gap-float(cfg['wall_mm']))<=float(cfg['thickness_tolerance_mm'])
        contain_pass=outside<=float(cfg['containment_tolerance_cm3'])
        records.append({'side':lab,'volume_cm3':total,'inside_source_cm3':inside,'outside_source_cm3':outside,'containment_pass':contain_pass,
                        'minimum_inner_outer_face_gap_mm':gap,'thickness_pass':thick_pass,'x_plane_end_faces':xends,'other_planar_faces':other_planar,
                        'complete_annular_end_interfaces_pass':end_pass,'pass':contain_pass and thick_pass and end_pass})
    audit={'status':'V139_COMPLETE_ANNULAR_X_PLANE_INLET_INTERFACES','source':cfg,'domain_x_mm':[x0,x1],'extended_generation_endpoints':{'start':ae,'end':be},
           'records':records,'bilateral_pass':all(r['pass'] for r in records),'geometry_candidate_pass':all(r['pass'] for r in records),
           'upstream_original_inlet_geometry_verified':False,'fan_hardware_dimensions_frozen':False,'print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_COMPLETE_ANNULAR_INLET_ENDS_v139.f3d')))
    json.dump(audit,open(os.path.join(outdir,'F14_v139_complete_annular_ends_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v139_complete_annular_ends_review.png'),1600,1000)
    try:review.close(False)
    except:pass
    try:imported.close(False)
    except:pass
    if prior:
        try:prior.activate()
        except:pass
    return audit