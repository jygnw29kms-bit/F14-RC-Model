from pathlib import Path
files=[Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')]
fn=r'''

def _link_rod_body_v37(root,name,p1,p2,zcenter,width=4.0,height=4.0):
    x1,y1=p1; x2,y2=p2; dx=x2-x1; dy=y2-y1; L=math.hypot(dx,dy)
    if L<1e-6: raise RuntimeError('zero length linkage')
    nx=-dy/L*width/2.0; ny=dx/L*width/2.0
    poly=[(x1+nx,y1+ny),(x2+nx,y2+ny),(x2-nx,y2-ny),(x1-nx,y1-ny)]
    return extrude_poly(root,name,poly,zcenter-height/2.0,height)

def build_linkage_plane_scan_v37():
    """Scan vertical linkage planes for the v36 synchronized slider/rod geometry."""
    build_sweep_servo_packaging_review_v35()
    design=adsk.fusion.Design.cast(_app.activeProduct); root=design.rootComponent
    _app.activeDocument.name='F14_v37_LINKAGE_PLANE_SCAN'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    with open(os.path.join(base,'F14_sweep_linkage_kinematics_v36.json'),encoding='utf-8') as stream: kin=json.load(stream)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in']); px=pivot['derived_full_scale_pivot_fs_in']*factor; py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]; dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in']); pz=(s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz)*factor
    fus_cut=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29')
    # Build a fresh uncut outer reference OML for containment only.
    outer=build_upc_fuselage_oml(root); outer.name='REF_UPC_FUSELAGE_OUTER_OML_v37'; move=root.features.moveFeatures; coll=adsk.core.ObjectCollection.create(); coll.add(outer); tr=adsk.core.Matrix3D.create(); tr.translation=adsk.core.Vector3D.create(0,0,mm(pz)); mi=move.createInput2(coll); mi.defineAsFreeMove(tr); move.add(mi); outer.opacity=0.03
    temporary=adsk.fusion.TemporaryBRepManager.get()
    servo=next(b for b in root.bRepBodies if b.name=='RC_SWEEP_SERVO_ENVELOPE_v35'); service=next(b for b in root.bRepBodies if b.name=='RC_SWEEP_SERVO_SERVICE_ENVELOPE_v35')
    fixed=[b for b in root.bRepBodies if (b.name.startswith('ENG_WINGBOX_FORK_') and b.name.endswith('_v31')) or (b.name.startswith('ENG_RISER_SOCKET_') and b.name.endswith('_v34')) or b.name in ['REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','REF_CF6x4_FRONT_UPPER_v35','REF_CF6x4_REAR_UPPER_v35']]
    sample_by_sweep={r['sweep_deg']:r for r in kin['samples']}
    z_candidates=[184.0,236.0,240.0,244.0,248.0]
    scans=[]; review_bodies=[]
    xmin=kin['geometry']['slider_x_min_mm']; xmax=kin['geometry']['slider_x_max_mm']; sy=kin['geometry']['slider_attach_y_mm']
    for zc in z_candidates:
        # Conservative full travel envelope of a 6 mm fore-aft slider crossbar spanning both rod pins.
        slider=extrude_poly(root,'REF_SLIDER_KEEP_OUT_Z%03d_v37'%round(zc),[(xmin-3,-sy-4),(xmax+3,-sy-4),(xmax+3,sy+4),(xmin-3,sy+4)],zc-2.5,5.0); slider.opacity=0.04; review_bodies.append(slider)
        sv=slider.volume; sc=temporary.copy(slider); oc=temporary.copy(outer); ok=temporary.booleanOperation(sc,oc,adsk.fusion.BooleanTypes.IntersectionBooleanType); siv=sc.volume if ok and sc.isValid else 0.0
        structural_hits=[]; structural_iv=0.0
        for part in fixed+[service]:
            a=temporary.copy(slider); b=temporary.copy(part); ok2=temporary.booleanOperation(a,b,adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=a.volume if ok2 and a.isValid else 0.0
            structural_iv+=iv
            if iv>1e-4: structural_hits.append(dict(kind='slider',part=part.name,intersection_volume_cm3=iv))
        rod_inside=[]; rod_hits=[]; moving_checks=[]
        for sweep in range(20,69,4):
            rec=sample_by_sweep[sweep]; sx=rec['slider_x_mm']; ax,ay=rec['wing_attach_right_mm']
            for side,sgn in [('R',1),('L',-1)]:
                rod=_link_rod_body_v37(root,'REF_LINK_%s_%02d_Z%03d_v37'%(side,sweep,round(zc)),(sx,sgn*sy),(ax,sgn*ay),zc,4.0,4.0); rod.opacity=0.025; review_bodies.append(rod)
                rv=rod.volume; rc=temporary.copy(rod); oc=temporary.copy(outer); ok3=temporary.booleanOperation(rc,oc,adsk.fusion.BooleanTypes.IntersectionBooleanType); riv=rc.volume if ok3 and rc.isValid else 0.0; rod_inside.append(riv/rv if rv else 0.0)
                for part in fixed+[service]:
                    a=temporary.copy(rod); b=temporary.copy(part); ok4=temporary.booleanOperation(a,b,adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=a.volume if ok4 and a.isValid else 0.0
                    if iv>1e-4: rod_hits.append(dict(sweep_deg=sweep,side=side,part=part.name,intersection_volume_cm3=iv))
                # Check rod against opposite moving wing only; own-wing endpoint contact is intentional.
                oside='L' if side=='R' else 'R'; osgn=-sgn
                wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+oside+'_')); lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+oside+'_v19')
                angle=-osgn*math.radians(sweep-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(osgn*py),mm(pz)))
                for mov,kind in [(wing,'opposite_outer_wing'),(lug,'opposite_root_lug')]:
                    a=temporary.copy(mov); temporary.transform(a,rot); b=temporary.copy(rod); ok5=temporary.booleanOperation(a,b,adsk.fusion.BooleanTypes.IntersectionBooleanType); iv=a.volume if ok5 and a.isValid else 0.0
                    if iv>1e-4: moving_checks.append(dict(sweep_deg=sweep,rod_side=side,kind=kind,intersection_volume_cm3=iv))
        good=(siv/sv>0.995 and structural_iv<1e-4 and not rod_hits and not moving_checks and min(rod_inside)>0.97)
        scans.append(dict(z_center_mm=zc,slider_inside_fraction=(siv/sv if sv else 0.0),slider_structural_intersection_cm3=structural_iv,structural_hits=structural_hits,min_rod_outer_oml_inside_fraction=min(rod_inside),rod_structural_hits=rod_hits,opposite_moving_hits=moving_checks,fully_packaged=good))
    good=[r for r in scans if r['fully_packaged']]; chosen=min(good,key=lambda r:r['z_center_mm']) if good else max(scans,key=lambda r:(r['min_rod_outer_oml_inside_fraction'],r['slider_inside_fraction'],-r['slider_structural_intersection_cm3']))
    for b in review_bodies:
        visible=('Z%03d_v37'%round(chosen['z_center_mm'])) in b.name
        b.isLightBulbOn=visible
        if visible: b.opacity=0.25
    audit=dict(status='SWEEP_LINKAGE_PLANE_PACKAGING_SCAN',source_revision='v35',kinematics_source='v36',candidate_results=scans,chosen_candidate=chosen,chosen_fully_packaged=chosen['fully_packaged'],
      linkage_plane_z_mm=chosen['z_center_mm'],slider_travel_mm=kin['geometry']['slider_travel_mm'],rod_length_mm=kin['geometry']['rod_length_mm'],vertical_wing_bellcrank_required=True,
      wing_bellcrank_geometry_verified=False,slider_guide_geometry_verified=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    outdir=os.path.join(config['export_dir'],'linkage_plane_v37'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v37_LINKAGE_PLANE_SCAN.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v37 export failed')
    with open(os.path.join(outdir,'F14_v37_linkage_plane_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v37_linkage_plane_review.png'),1600,1000)
    return audit

'''
for path in files:
    s=path.read_text(encoding='utf-8'); insert=s.index('def build_project_revision():')
    if 'def build_linkage_plane_scan_v37()' not in s: s=s[:insert]+fn+s[insert:]
    s=s.replace('return build_sweep_servo_packaging_review_v35()','return build_linkage_plane_scan_v37()',1)
    path.write_text(s,encoding='utf-8'); print('patched',path)
