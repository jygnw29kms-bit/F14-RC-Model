"""v157: skeleton battery tray candidate inside the v155 verified structural/service envelope."""
import adsk.core,adsk.fusion,json,os,hashlib,math

def mm(v): return v/10.0
def make_box(temp,cx,cy,cz,l,w,h):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h)); return temp.createBox(obb)
def ivol(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0
def union_into(temp,target,other):
    if not temp.booleanOperation(target,other,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('union failed')
def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v157_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(cfg['source_path'],'rb').read()).hexdigest()!=cfg['source_sha256']: raise RuntimeError('source hash mismatch')
    if hashlib.sha256(open(cfg['v155_audit'],'rb').read()).hexdigest()!=cfg['v155_audit_sha256']: raise RuntimeError('v155 audit hash mismatch')
    v155=json.load(open(cfg['v155_audit'],encoding='utf-8'))
    if not v155.get('geometry_candidate_pass'): raise RuntimeError('v155 envelope is not a pass')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])): raise RuntimeError('source import failed')
    imp=app.activeDocument; design0=adsk.fusion.Design.cast(app.activeProduct); root0=design0.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get(); bodies=[root0.bRepBodies.item(i) for i in range(root0.bRepBodies.count)]
    fus=next((b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'),None)
    if fus is None: raise RuntimeError('fuselage missing')
    blockers=[b for b in bodies if b is not fus and (b.name.startswith('MONOLITHIC_') or b.name.startswith('ENG_') or b.name.startswith('REF_CF') or 'WINGBOX' in b.name or 'HARDPOINT' in b.name)]
    x0,x1=[float(x) for x in cfg['tray_x_range_mm']]; L=x1-x0; basez=float(cfg['base_z_mm']); rail_h=float(cfg['rail_height_mm']); rail_w=float(cfg['rail_width_mm']); outer_y=float(cfg['rail_outer_y_mm']); inner_y=float(cfg['rail_inner_y_mm'])
    # Build unioned skeleton in temp BRep.
    pieces=[]
    rail_cy=(outer_y+inner_y)/2.0
    for s in (-1,1): pieces.append(make_box(temp,(x0+x1)/2,s*rail_cy,basez+rail_h/2,L,rail_w,rail_h))
    fsw=float(cfg['floor_strip_width_mm']); fst=float(cfg['floor_strip_thickness_mm']); fcy=float(cfg['floor_strip_center_abs_y_mm'])
    for s in (-1,1): pieces.append(make_box(temp,(x0+x1)/2,s*fcy,basez+fst/2,L,fsw,fst))
    for x in cfg['crossbar_x_mm']: pieces.append(make_box(temp,float(x),0,basez+float(cfg['crossbar_z_thickness_mm'])/2,float(cfg['crossbar_x_thickness_mm']),float(cfg['crossbar_y_length_mm']),float(cfg['crossbar_z_thickness_mm'])))
    tray=pieces[0]
    for p in pieces[1:]: union_into(temp,tray,p)
    # Indexed positive-stop holes through both rails.
    d=float(cfg['pin_hole_diameter_mm']); zpin=float(cfg['pin_center_z_mm']); first=float(cfg['pin_first_x_mm']); last=float(cfg['pin_last_x_mm']); pitch=float(cfg['pin_hole_pitch_mm']); holes=[]; x=first
    while x<=last+1e-9:
        cyl=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(-outer_y-1),mm(zpin)),mm(d/2),adsk.core.Point3D.create(mm(x),mm(outer_y+1),mm(zpin)),mm(d/2))
        if not temp.booleanOperation(tray,cyl,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('pin hole cut failed at %.3f'%x)
        holes.append(x); x+=pitch
    total=tray.volume; inside=ivol(temp,tray,fus); outside=max(0,total-inside)
    collision_records=[]
    for b in blockers:
        v=ivol(temp,tray,b)
        if v>1e-9: collision_records.append({'body':b.name,'intersection_cm3':v})
    # Reference battery positions, bottom seated on floor top. Contact/touching is allowed, positive overlap is not.
    pl,pw,ph=[float(x) for x in cfg['reference_pack_mm']]; floor_top=float(cfg['floor_top_z_mm']); pz=floor_top+ph/2; cx=float(cfg['reference_pack_center_x_mm']); travel=float(cfg['battery_travel_mm']); pack_records=[]
    for label,px in [('forward',cx-travel/2),('center',cx),('aft',cx+travel/2)]:
        pack=make_box(temp,px,0,pz,pl,pw,ph); ov=ivol(temp,pack,tray); inf=ivol(temp,pack,fus); pack_records.append({'position':label,'center_x_mm':px,'x_range_mm':[px-pl/2,px+pl/2],'tray_positive_overlap_cm3':ov,'inside_fuselage_fraction':inf/pack.volume if pack.volume else 0,'pass':ov<1e-6 and abs(inf-pack.volume)<1e-5})
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_BATTERY_SKELETON_TRAY_v157'; rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; root=rd.rootComponent
    ref=root.bRepBodies.add(temp.copy(fus)); ref.name=fus.name
    for b in blockers:
        try: rb=root.bRepBodies.add(temp.copy(b)); rb.name=b.name
        except: pass
    tb=root.bRepBodies.add(temp.copy(tray)); tb.name='BATTERY_SKELETON_TRAY_v157_NO_PRINT_RELEASE'
    # Reference pack at center and reference stop pins at nearest useful holes around 106 mm pack.
    pack=root.bRepBodies.add(make_box(temp,cx,0,pz,pl,pw,ph)); pack.name='REF_BATTERY_106x36x25_v157'; pack.opacity=0.35
    front_pin=max(h for h in holes if h < cx-pl/2); aft_pin=min(h for h in holes if h > cx+pl/2)
    for name,px in [('FRONT',front_pin),('AFT',aft_pin)]:
        pin=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(px),mm(-outer_y),mm(zpin)),mm(2.0),adsk.core.Point3D.create(mm(px),mm(outer_y),mm(zpin)),mm(2.0)); pb=root.bRepBodies.add(pin); pb.name='REF_4MM_STOP_PIN_'+name+'_v157'; pb.opacity=0.5
    audit={'status':'V157_BATTERY_SKELETON_TRAY_CANDIDATE','source':cfg,'geometry':{'tray_volume_cm3':total,'outside_fuselage_cm3':outside,'containment_fraction':inside/total if total else 0,'fixed_structure_collisions':collision_records,'pin_hole_count':len(holes),'pin_hole_x_mm':holes,'reference_stop_pins_mm':[front_pin,aft_pin],'undertray_strap_clearance_mm':cfg['strap_undertray_clearance_mm']},'reference_pack_travel_checks':pack_records,'geometry_candidate_pass':outside<1e-5 and not collision_records and all(x['pass'] for x in pack_records),'frame_anchor_interfaces_designed':False,'strap_hardware_verified':False,'stop_pin_hardware_verified':False,'retention_proof_pass':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_BATTERY_SKELETON_TRAY_v157.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v157_battery_skeleton_tray_audit.json'),'w'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v157_battery_skeleton_tray_review.png'),1600,1000)
    try: doc.close(False); imp.close(False)
    except: pass
    if prior:
      try: prior.activate()
      except: pass
    return audit