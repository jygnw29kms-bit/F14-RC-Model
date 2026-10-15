"""v158: add four M3 frame-interface pads to the validated v157 battery skeleton tray."""
import adsk.core,adsk.fusion,json,os,hashlib,math

def mm(v): return v/10.0
def make_box(temp,cx,cy,cz,l,w,h):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h)); return temp.createBox(obb)
def ivol(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0
def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v158_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']: raise RuntimeError('v158 source hash')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])): raise RuntimeError('v157 import')
    imp=app.activeDocument; d=adsk.fusion.Design.cast(app.activeProduct); root0=d.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get(); bodies=[root0.bRepBodies.item(i) for i in range(root0.bRepBodies.count)]
    fus=next((b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'),None); tray0=next((b for b in bodies if b.name=='BATTERY_SKELETON_TRAY_v157_NO_PRINT_RELEASE'),None)
    if fus is None or tray0 is None: raise RuntimeError('required v157 bodies missing')
    blockers=[b for b in bodies if b is not fus and b is not tray0 and (b.name.startswith('MONOLITHIC_') or b.name.startswith('ENG_') or b.name.startswith('REF_CF') or 'WINGBOX' in b.name or 'HARDPOINT' in b.name)]
    tray=temp.copy(tray0); lx,wy,hz=[float(x) for x in cfg['anchor_pad_size_mm']]; cy=float(cfg['anchor_pad_center_abs_y_mm']); cz=float(cfg['anchor_center_z_mm']); interfaces=[]
    for x in cfg['anchor_x_mm']:
      for side,sgn in [('R',1),('L',-1)]:
        pad=make_box(temp,float(x),sgn*cy,cz,lx,wy,hz)
        if not temp.booleanOperation(tray,pad,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('anchor pad union failed')
        ya,yb=[float(v) for v in cfg['mount_hole_axis_y_span_mm']]
        p0=adsk.core.Point3D.create(mm(float(x)),mm(sgn*ya),mm(cz)); p1=adsk.core.Point3D.create(mm(float(x)),mm(sgn*yb),mm(cz))
        hole=temp.createCylinderOrCone(p0,mm(float(cfg['mount_hole_diameter_mm'])/2),p1,mm(float(cfg['mount_hole_diameter_mm'])/2))
        if not temp.booleanOperation(tray,hole,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('mount hole cut failed')
        interfaces.append({'x_mm':float(x),'side':side,'outer_interface_y_mm':sgn*(cy+wy/2),'z_mm':cz,'hole_d_mm':float(cfg['mount_hole_diameter_mm'])})
    total=tray.volume; inside=ivol(temp,tray,fus); outside=max(0,total-inside); coll=[]
    for b in blockers:
      v=ivol(temp,tray,b)
      if v>1e-9: coll.append({'body':b.name,'intersection_cm3':v})
    force=float(cfg['hardware_sizing_force_N']); dmm=float(cfg['mount_hole_diameter_mm']); pad_h=hz
    # conservative printed-hole bearing screen if one interface momentarily sees whole sizing force
    bearing=force/(dmm*pad_h)
    # M3 nominal shank shear screen, using 3 mm rather than clearance-hole diameter
    m3_area=math.pi*3.0**2/4; m3_shear=force/m3_area
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_BATTERY_TRAY_FRAME_INTERFACES_v158'; rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; root=rd.rootComponent
    rf=root.bRepBodies.add(temp.copy(fus)); rf.name=fus.name
    for b in blockers:
      try: rb=root.bRepBodies.add(temp.copy(b)); rb.name=b.name
      except: pass
    tb=root.bRepBodies.add(temp.copy(tray)); tb.name='BATTERY_TRAY_WITH_FRAME_INTERFACES_v158_NO_PRINT_RELEASE'
    audit={'status':'V158_BATTERY_TRAY_FRAME_INTERFACE_CANDIDATE','source':cfg,'geometry':{'tray_with_interfaces_volume_cm3':total,'outside_fuselage_cm3':outside,'containment_fraction':inside/total if total else 0,'fixed_structure_collisions':coll,'interfaces':interfaces},'load_screens':{'single_interface_full_2x_sizing_force_N':force,'printed_hole_bearing_MPa':bearing,'M3_nominal_shank_single_shear_MPa':m3_shear},'geometry_candidate_pass':outside<1e-5 and not coll,'frame_anchor_interfaces_designed':True,'mating_internal_frames_designed':False,'frame_fastener_hardware_verified':False,'retention_proof_pass':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_BATTERY_TRAY_FRAME_INTERFACES_v158.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v158_battery_tray_frame_interfaces_audit.json'),'w'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v158_battery_tray_frame_interfaces_review.png'),1600,1000)
    try: doc.close(False); imp.close(False)
    except: pass
    if prior:
      try: prior.activate()
      except: pass
    return audit