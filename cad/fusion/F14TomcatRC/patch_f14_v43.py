from pathlib import Path

TARGETS=[
 Path(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\cad\fusion\F14TomcatRC\F14TomcatRC.py'),
 Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py')]

FUNC=r'''
def build_packaging_diagnostic_v43():
    """Diagnose v42 packaging and search a mechanically valid split-plane crank/link arrangement."""
    design=adsk.fusion.Design.cast(_app.activeProduct); root=design.rootComponent if design else None
    if not root or not any(b.name=='REF_UPC_FUSELAGE_OUTER_OML_v37' for b in root.bRepBodies):
        build_inboard_sweep_crank_scan_v38(); design=adsk.fusion.Design.cast(_app.activeProduct); root=design.rootComponent
    _app.activeDocument.name='F14_v43_PACKAGING_DIAGNOSTIC_SPLIT_PLANE'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as f:pivot=json.load(f)
    with open(os.path.join(base,'F14_sweep_linkage_kinematics_v40.json'),encoding='utf-8') as f:kin=json.load(f)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as f:config=json.load(f)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as f:data=json.load(f)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in']); px=pivot['derived_full_scale_pivot_fs_in']*factor; py=pivot['derived_full_scale_pivot_bl_in']*factor
    outer=next(b for b in root.bRepBodies if b.name=='REF_UPC_FUSELAGE_OUTER_OML_v37'); temporary=adsk.fusion.TemporaryBRepManager.get()
    wings={label:next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_')) for label in ['R','L']}
    fixed=[b for b in root.bRepBodies if (b.name.startswith('ENG_RISER_SOCKET_') and b.name.endswith('_v34')) or b.name in ['REF_CF6x4_FRONT_LOWER_v34','REF_CF6x4_REAR_LOWER_v34','REF_CF6x4_FRONT_UPPER_v35','REF_CF6x4_REAR_UPPER_v35']]
    service=next((b for b in root.bRepBodies if b.name=='RC_SWEEP_SERVO_SERVICE_ENVELOPE_v35'),None)
    if service: fixed.append(service)
    c=kin['top_candidates'][1]; link_z=196.0; sy=c['slider_attach_y_mm']; dx0,dy0=c['crank_vector_at_20deg_mm']; samples={r['sweep_deg']:r for r in c['samples'] if r['sweep_deg']%4==0}
    def ivol(a_body,b_body):
        a=temporary.copy(a_body); b=temporary.copy(b_body); ok=temporary.booleanOperation(a,b,adsk.fusion.BooleanTypes.IntersectionBooleanType); return a.volume if ok and a.isValid else 0.0
    def bbox(body):
        b=body.boundingBox; return {'xmin_mm':b.minPoint.x*10,'ymin_mm':b.minPoint.y*10,'zmin_mm':b.minPoint.z*10,'xmax_mm':b.maxPoint.x*10,'ymax_mm':b.maxPoint.y*10,'zmax_mm':b.maxPoint.z*10}
    bounds={'outer':bbox(outer),'wings':{k:bbox(v) for k,v in wings.items()},'fixed':{b.name:bbox(b) for b in fixed}}
    # Slider audit per obstacle and z-plane. This separates a real collision from an intentionally overlapping service envelope.
    xmin,xmax=c['slider_x_min_mm'],c['slider_x_max_mm']; slider_scan=[]
    for zc in [188.0,192.0,196.0,200.0,204.0]:
        slider=extrude_poly(root,'TMP43_SLIDER_%03d'%int(zc),[(xmin-4,-sy-6),(xmax+4,-sy-6),(xmax+4,sy+6),(xmin-4,sy+6)],zc-2.5,5.0); slider.isLightBulbOn=False
        hits={p.name:ivol(slider,p) for p in fixed}; ov=slider.volume; oi=ivol(slider,outer)/ov if ov else 0.0
        slider_scan.append({'z_mm':zc,'outer_inside_fraction':oi,'total_fixed_collision_cm3':sum(hits.values()),'hits_cm3':hits}); slider.deleteMe()
    # Search crank plane independently. The rod may connect by a vertical M3 shoulder/ball stud; max offset screened to 20 mm.
    crank_scan=[]
    for crank_z in [176.0,180.0,184.0,188.0,192.0,196.0,200.0]:
        min_allowed=1.0; max_hit=0.0; checks=[]
        for label,sgn in [('R',1),('L',-1)]:
            yp=sgn*py; arm=_link_rod_body_v37(root,'TMP43_CRANK_%s_%03d'%(label,int(crank_z)),(px,yp),(px+dx0,sgn*(py+dy0)),crank_z,8.0,4.0); arm.isLightBulbOn=False
            for sweep in range(20,69,4):
                ang=-sgn*math.radians(sweep-20.0); rot=adsk.core.Matrix3D.create(); rot.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(yp),mm(crank_z)))
                crank=temporary.copy(arm); temporary.transform(crank,rot); cv=crank.volume
                wing=temporary.copy(wings[label]); # wing geometry is defined at its source datum and rotates about the same XY pivot
                rw=adsk.core.Matrix3D.create(); rw.setToRotation(ang,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(yp),0)); temporary.transform(wing,rw)
                io=ivol(crank,outer); iw=ivol(crank,wing); allowed=min(1.0,(io+iw)/cv) if cv else 0.0
                hits={p.name:ivol(crank,p) for p in fixed}; hit=sum(hits.values())
                min_allowed=min(min_allowed,allowed); max_hit=max(max_hit,hit); checks.append({'side':label,'sweep_deg':sweep,'allowed_fraction':allowed,'fixed_collision_cm3':hit})
            arm.deleteMe()
        crank_scan.append({'crank_z_mm':crank_z,'link_z_mm':link_z,'vertical_stud_offset_mm':abs(link_z-crank_z),'min_allowed_fraction':min_allowed,'max_fixed_collision_cm3':max_hit,'checks':checks})
    # Prefer fully-contained, collision-free solutions; then smallest stud offset and highest containment.
    crank_scan.sort(key=lambda r:(0 if (r['min_allowed_fraction']>=0.985 and r['max_fixed_collision_cm3']<1e-4 and r['vertical_stud_offset_mm']<=20) else 1,r['vertical_stud_offset_mm'],-r['min_allowed_fraction'],r['max_fixed_collision_cm3']))
    best_crank=crank_scan[0]
    best_slider=min(slider_scan,key=lambda r:(r['total_fixed_collision_cm3'],abs(r['z_mm']-link_z),-r['outer_inside_fraction']))
    audit={'status':'V43_PACKAGING_DIAGNOSTIC_SPLIT_PLANE','source_revision':'v42','candidate_index':1,'link_z_mm':link_z,'bounds':bounds,'best_crank_plane':best_crank,'best_slider_plane':best_slider,'crank_scan':crank_scan,'slider_scan':slider_scan,'mechanical_detail_release':False,'print_release':False,'flight_release':False}
    outdir=os.path.join(config['export_dir'],'packaging_diagnostic_v43'); os.makedirs(outdir,exist_ok=True)
    with open(os.path.join(outdir,'F14_v43_packaging_diagnostic_audit.json'),'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v43_packaging_diagnostic_review.png'),1600,1000)
    return audit
'''

for p in TARGETS:
    txt=p.read_text(encoding='utf-8')
    if 'def build_packaging_diagnostic_v43():' not in txt:
        txt=txt.replace('def build_project_revision():',FUNC+'\n\ndef build_project_revision():',1)
    txt=txt.replace('return build_root_union_crank_packaging_v42()','return build_packaging_diagnostic_v43()',1)
    p.write_text(txt,encoding='utf-8')
    print('patched',p)
