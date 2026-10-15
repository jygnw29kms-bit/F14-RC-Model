"""v181: conservative packaging scan for the TORQ TCM-1022 stabilator-servo candidate."""
import adsk.core, adsk.fusion, json, os, hashlib


def ivol(temp,a,b):
    q=temp.copy(a)
    ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return q.volume if ok and q.isValid else 0.0


def make_box(temp,mm,x,y,z,dx,dy,dz):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(x),mm(y),mm(z)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(dx),mm(dy),mm(dz))
    return temp.createBox(obb)


def run_review(app,builder,mm,outdir):
    base=os.path.dirname(__file__)
    cfg=json.load(open(os.path.join(base,'F14_v181_servo_candidate.json'),encoding='utf-8'))
    v180='C:/Users/dezen/Desktop/F14-RC-Model/workspace/RC-F14-Tomcat/Fusion/Exports/Current/controls_v180/F14_STABILATOR_CONTAINED_CRANK_v180.f3d'
    v180sha='f8edaa5131101f143cbc1055c8f4d2813df5c721ba558be2549ed01ec2f87cd8'
    oml='C:/Users/dezen/Desktop/F14-RC-Model/analysis/independent_reviews/allowanced_inlet_20261015/F14_ALLOWANCED_INLET_WALL_CANDIDATE.f3d'
    omlsha='cea5f21ed9551991f3b7306ea8ce3df92f02e20bda3bc5f3b5ef61c94f4baf93'
    if hashlib.sha256(open(v180,'rb').read()).hexdigest()!=v180sha: raise RuntimeError('v181 v180 source changed')
    if hashlib.sha256(open(oml,'rb').read()).hexdigest()!=omlsha: raise RuntimeError('v181 OML source changed')
    if cfg['stall_torque_kgcm_at_8p4v'] < cfg['v180_required_servo_torque_kgcm']: raise RuntimeError('v181 servo torque gate failed')
    if cfg['conservative_weight_g'] > cfg['hard_mass_warning_gate_g']: raise RuntimeError('v181 servo mass hard warning exceeded')

    prior=app.activeDocument; temp=adsk.fusion.TemporaryBRepManager.get()
    d=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(v180))
    rr=adsk.fusion.Design.cast(app.activeProduct).rootComponent
    hardware={b.name:temp.copy(b) for b in rr.bRepBodies}
    d.close(False)
    d=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(oml))
    rr=adsk.fusion.Design.cast(app.activeProduct).rootComponent
    source=temp.copy(next(b for b in rr.bRepBodies if b.name=='REFERENCE_INTERPOLATED_SOURCE_LOFT'))
    d.close(False)

    clr=float(cfg['packaging_clearance_each_side_mm'])
    L,W,H=[float(v) for v in cfg['dimensions_mm']]
    orientations=[('A_XL_ZW',(L+2*clr,H+2*clr,W+2*clr)),('B_XW_ZL',(W+2*clr,H+2*clr,L+2*clr))]
    xs=[680.,690.,700.,710.,720.]; ys=[50.,55.,60.,65.]; zs=[-8.,-4.,0.,4.,8.]
    tol=1e-5; itol=1e-8; rows=[]
    for label,(dx,dy,dz) in orientations:
        for x in xs:
            for yabs in ys:
                for z in zs:
                    side_rows=[]; bilateral=True
                    for side,sgn in [('R',1),('L',-1)]:
                        box=make_box(temp,mm,x,sgn*yabs,z,dx,dy,dz)
                        total=box.volume; inside=temp.copy(box)
                        ok=temp.booleanOperation(inside,temp.copy(source),adsk.fusion.BooleanTypes.IntersectionBooleanType)
                        outside=max(0.0,total-(inside.volume if ok and inside.isValid else 0.0))
                        blockers=[]
                        for name,hbody in hardware.items():
                            if ('_'+side+'_') not in name: continue
                            vol=ivol(temp,box,hbody)
                            if vol>itol: blockers.append({'body':name,'intersection_cm3':vol})
                        passed=outside<=tol and not blockers
                        bilateral=bilateral and passed
                        side_rows.append({'side':side,'outside_source_oml_cm3':outside,'blockers':blockers,'pass':passed})
                    face_gap=76.0-(yabs+dy/2.0)
                    rows.append({'orientation':label,'center_mm':[x,yabs,z],'expanded_dims_mm':[dx,dy,dz],
                                 'inboard_face_to_crank_plane_gap_mm':face_gap,'sides':side_rows,'bilateral_pass':bilateral})
    passing=[r for r in rows if r['bilateral_pass'] and r['inboard_face_to_crank_plane_gap_mm']>=0]
    passing.sort(key=lambda r:(abs(r['inboard_face_to_crank_plane_gap_mm']),abs(r['center_mm'][0]-700),abs(r['center_mm'][2]),0 if r['orientation']=='A_XL_ZW' else 1))
    selected=passing[0] if passing else None
    if selected is None: raise RuntimeError('v181 no bilateral servo packaging candidate')

    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_STABILATOR_SERVO_PACKAGING_v181_NO_HARDWARE_FREEZE'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    dx,dy,dz=selected['expanded_dims_mm']; x,yabs,z=selected['center_mm']
    for side,sgn in [('R',1),('L',-1)]:
        b=root.bRepBodies.add(make_box(temp,mm,x,sgn*yabs,z,dx,dy,dz)); b.name='CANDIDATE_TORQ_TCM1022_SERVICE_ENVELOPE_'+side+'_v181'; b.opacity=.35
        for name,hbody in hardware.items():
            if ('_'+side+'_') in name and ('CRANK' in name or 'BEARING' in name or 'SHAFT' in name or 'FITTING' in name):
                rb=root.bRepBodies.add(temp.copy(hbody)); rb.name='REF_'+name+'_v181'; rb.opacity=.12
    audit={'status':'V181_TORQ_TCM1022_SERVO_PACKAGING_CANDIDATE','candidate':cfg,'v180_source_sha256':v180sha,'oml_source_sha256':omlsha,
           'scan_candidate_count':len(rows),'passing_candidate_count':len(passing),'selected':selected,'top_passing_candidates':passing[:10],
           'torque_margin_ratio':cfg['stall_torque_kgcm_at_8p4v']/cfg['v180_required_servo_torque_kgcm'],
           'mass_preferred_gate_pass':cfg['conservative_weight_g']<=cfg['preferred_mass_gate_g'],
           'mass_hard_warning_pass':cfg['conservative_weight_g']<=cfg['hard_mass_warning_gate_g'],
           'mounting_ears_exact_geometry_verified':False,'output_spline_exact_offset_verified':False,'pushrod_path_verified':False,
           'dynamic_linkage_clearance_verified':False,'actual_unit_measured':False,'hardware_frozen':False,'bench_proof_pass':False,'print_release':False,'flight_release':False,
           'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True)
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_STABILATOR_SERVO_PACKAGING_v181.f3d'))): raise RuntimeError('v181 export failed')
    json.dump(audit,open(os.path.join(outdir,'F14_v181_stabilator_servo_packaging_audit.json'),'w',encoding='utf-8'),indent=2)
    app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v181_stabilator_servo_packaging_review.png'),1600,1000)
    if prior:
        try: prior.activate()
        except: pass
    return audit
