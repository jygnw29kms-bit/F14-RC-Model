"""v165: corrected retention-compatible battery tray with split-height terminal hardpoints."""
import adsk.core,adsk.fusion,json,os,hashlib,math

def mm(v): return v/10.0
def box(temp,cx,cy,cz,l,w,h):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h)); return temp.createBox(obb)
def ivol(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0
def unite(temp,target,other):
    if not temp.booleanOperation(target,other,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('union failed')
def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v165_section_inputs.json'),encoding='utf-8'))
    for pathkey,hashkey in [('source_path','source_sha256'),('v164_path','v164_sha256')]:
        if hashlib.sha256(open(cfg[pathkey],'rb').read()).hexdigest()!=cfg[hashkey]: raise RuntimeError('hash mismatch '+pathkey)
    v164=json.load(open(cfg['v164_path'],encoding='utf-8'))
    if not v164.get('all_70mm_travel_positions_have_two_positive_stops'): raise RuntimeError('v164 retention index did not pass')
    if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path'])): raise RuntimeError('source import failed')
    imp=app.activeDocument; d0=adsk.fusion.Design.cast(app.activeProduct); r0=d0.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get(); bodies=[r0.bRepBodies.item(i) for i in range(r0.bRepBodies.count)]
    fus=next((b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'),None)
    if fus is None: raise RuntimeError('fuselage missing')
    blockers=[b for b in bodies if b is not fus and (b.name.startswith('MONOLITHIC_') or b.name.startswith('ENG_') or b.name.startswith('REF_CF') or 'WINGBOX' in b.name or 'HARDPOINT' in b.name)]
    x0,x1=[float(x) for x in cfg['tray_x_range_mm']]; L=x1-x0; bz=float(cfg['base_z_mm']); rail_h=float(cfg['rail_height_mm']); rail_in=float(cfg['rail_inner_y_mm']); rail_out=float(cfg['rail_outer_y_mm']); rail_w=float(cfg['rail_width_mm']); rcy=(rail_in+rail_out)/2
    pieces=[]
    for s in (-1,1): pieces.append(box(temp,(x0+x1)/2,s*rcy,bz+rail_h/2,L,rail_w,rail_h))
    fsw=float(cfg['floor_strip_width_mm']); fst=float(cfg['floor_strip_thickness_mm']); fcy=float(cfg['floor_strip_center_abs_y_mm'])
    for s in (-1,1): pieces.append(box(temp,(x0+x1)/2,s*fcy,bz+fst/2,L,fsw,fst))
    for x in cfg['crossbar_x_mm']: pieces.append(box(temp,float(x),0,bz+float(cfg['crossbar_z_thickness_mm'])/2,float(cfg['crossbar_x_thickness_mm']),float(cfg['crossbar_y_length_mm']),float(cfg['crossbar_z_thickness_mm'])))
    # Terminal hardpoints are outboard of battery sidewalls and support both stop and frame bores.
    hp_l,hp_w,hp_h=[float(v) for v in cfg['end_hardpoint_size_mm']]; hp_y=float(cfg['end_hardpoint_center_abs_y_mm']); hp_z=float(cfg['end_hardpoint_center_z_mm'])
    for x in cfg['end_hardpoint_x_mm']:
        for s in (-1,1): pieces.append(box(temp,float(x),s*hp_y,hp_z,hp_l,hp_w,hp_h))
    tray=pieces[0]
    for p in pieces[1:]: unite(temp,tray,p)
    # Stop-pin holes traverse both rails/end hardpoints.
    stop_d=float(cfg['stop_pin_hole_diameter_mm']); stop_z=float(cfg['stop_pin_axis_z_mm']); holes=[]
    for x in cfg['retention_hole_x_mm']:
        x=float(x); cyl=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(-rail_out-1),mm(stop_z)),mm(stop_d/2),adsk.core.Point3D.create(mm(x),mm(rail_out+1),mm(stop_z)),mm(stop_d/2))
        if not temp.booleanOperation(tray,cyl,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('stop hole cut failed %.3f'%x)
        holes.append(x)
    # M3 frame holes are vertically separated and only traverse each outboard end-hardpoint.
    frame_d=float(cfg['frame_hole_diameter_mm']); frame_z=float(cfg['frame_hole_axis_z_mm']); ya,yb=[float(v) for v in cfg['frame_hole_y_span_mm']]; interfaces=[]
    for x in cfg['end_hardpoint_x_mm']:
        for side,s in [('R',1),('L',-1)]:
            p0=adsk.core.Point3D.create(mm(float(x)),mm(s*ya),mm(frame_z)); p1=adsk.core.Point3D.create(mm(float(x)),mm(s*yb),mm(frame_z))
            cyl=temp.createCylinderOrCone(p0,mm(frame_d/2),p1,mm(frame_d/2))
            if not temp.booleanOperation(tray,cyl,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('frame hole cut failed')
            interfaces.append({'x_mm':float(x),'side':side,'y_span_mm':[s*ya,s*yb],'z_mm':frame_z,'hole_d_mm':frame_d})
    total=tray.volume; inside=ivol(temp,tray,fus); outside=max(0,total-inside); collisions=[]
    for b in blockers:
        v=ivol(temp,tray,b)
        if v>float(cfg['collision_tolerance_cm3']): collisions.append({'body':b.name,'intersection_cm3':v})
    # Re-check pack travel against full corrected tray.
    pl,pw,ph=[float(v) for v in cfg['reference_pack_mm']]; pz=float(cfg['floor_top_z_mm'])+ph/2; packs=[]
    for px in cfg['battery_center_positions_mm']:
        px=float(px); pack=box(temp,px,0,pz,pl,pw,ph); ov=ivol(temp,pack,tray); inf=ivol(temp,pack,fus)
        packs.append({'center_x_mm':px,'x_range_mm':[px-pl/2,px+pl/2],'tray_overlap_cm3':ov,'fuselage_inside_fraction':inf/pack.volume,'pass':ov<=float(cfg['collision_tolerance_cm3']) and abs(inf-pack.volume)<=float(cfg['containment_tolerance_cm3'])})
    # Geometric ligament checks at terminal hardpoint.
    axis_sep=abs(frame_z-stop_z); nominal_surface_ligament=axis_sep-(frame_d+stop_d)/2
    end_x=float(cfg['end_hardpoint_x_mm'][0]); hp_left=end_x-hp_l/2; stop_edge_ligament=(end_x-stop_d/2)-hp_left
    hp_top=hp_z+hp_h/2; frame_top_ligament=hp_top-(frame_z+frame_d/2)
    pass_geom=outside<=float(cfg['containment_tolerance_cm3']) and not collisions and all(x['pass'] for x in packs) and nominal_surface_ligament>=3.0 and stop_edge_ligament>=4.0 and frame_top_ligament>=2.0
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_BATTERY_TRAY_RETENTION_CORRECTED_v165'; rd=adsk.fusion.Design.cast(app.activeProduct); rd.designType=adsk.fusion.DesignTypes.DirectDesignType; root=rd.rootComponent
    rf=root.bRepBodies.add(temp.copy(fus)); rf.name=fus.name
    for b in blockers:
        try: rb=root.bRepBodies.add(temp.copy(b)); rb.name=b.name
        except: pass
    tb=root.bRepBodies.add(temp.copy(tray)); tb.name='BATTERY_TRAY_RETENTION_CORRECTED_v165_NO_PRINT_RELEASE'
    audit={'status':'V165_CORRECTED_BATTERY_RETENTION_TRAY','source':cfg,'geometry':{'tray_volume_cm3':total,'outside_fuselage_cm3':outside,'containment_fraction':inside/total if total else 0,'fixed_structure_collisions':collisions,'retention_hole_x_mm':holes,'frame_interfaces':interfaces,'stop_to_frame_axis_separation_mm':axis_sep,'nominal_surface_ligament_between_bores_mm':nominal_surface_ligament,'terminal_stop_hole_x_edge_ligament_mm':stop_edge_ligament,'frame_hole_top_ligament_mm':frame_top_ligament},'battery_travel_checks':packs,'v164_retention_position_checks':v164['battery_position_checks'],'geometry_candidate_pass':pass_geom,'stop_shoe_designed':False,'mating_internal_frames_designed':False,'retention_proof_pass':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_BATTERY_TRAY_RETENTION_CORRECTED_v165.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v165_battery_retention_tray_audit.json'),'w'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v165_battery_retention_tray_review.png'),1600,1000)
    try: doc.close(False); imp.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit