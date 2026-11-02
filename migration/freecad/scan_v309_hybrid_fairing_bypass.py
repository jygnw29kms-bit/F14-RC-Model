import FreeCAD as App, Part, pathlib, json, math, hashlib, itertools
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v307_UNIFIED_TAIL_SERVO_CASSETTE_BASE.FCStd'
aud_path=R/'migration/freecad/freecad_v309_hybrid_fairing_bypass_audit.json'
d=App.openDocument(str(src))
x0=731.5; x1=754.962281164333; L=x1-x0
axis_y=66.28458486059378; axis_z=-10.508688347971937
fan_id=50.0; hub_d=28.0; fsa=math.pi/4.0*(fan_id**2-hub_d**2); dx=0.25
surface_pad=0.5; hardware_outer_pad=1.3
ratios=[0.90,0.95,1.00]
def union_names(names):
    ss=[d.getObject(n).Shape for n in names if d.getObject(n)]
    u=ss[0]
    for s in ss[1:]: u=u.fuse(s)
    return u.removeSplitter()
def dilate(shape,pad):
    copies=[]
    for ox,oy,oz in itertools.product((-pad,0,pad),repeat=3):
        q=shape.copy(); q.translate(App.Vector(ox,oy,oz)); copies.append(q)
    u=copies[0]
    for q in copies[1:]: u=u.fuse(q)
    return u.removeSplitter()
records=[]
for side,sgn in [('R',1),('L',-1)]:
    surfaces=dilate(union_names([f'STABILATOR_{side}',f'VTAIL_{side}',f'VENTRAL_{side}']),surface_pad)
    hardware=dilate(union_names([f'STAB_BEARING_{side}_1',f'STAB_HOUSING_{side}_1',f'STAB_BEARING_{side}_2',f'STAB_HOUSING_{side}_2',f'V234_BEARING_INBOARD_COLLAR_{side}',f'V234_BEARING_OUTER_SHOULDER_{side}',f'V234_SURFACE_INNER_COLLAR_{side}',f'V234_SURFACE_OUTER_WASHER_{side}',f'V234_END_FASTENER_HEAD_{side}',f'V237_D_SHAFT_{side}',f'V241_LIGHT_D_CRANK_{side}',f'V284_LIGHT_D_ROOT_FITTING_{side}']),hardware_outer_pad)
    keep=surfaces.fuse(hardware).removeSplitter(); side_rows=[]
    for ratio in ratios:
        exit_id=math.sqrt(4.0*(fsa*ratio)/math.pi)
        core=Part.makeCone(fan_id/2.0,exit_id/2.0,L,App.Vector(x0,sgn*axis_y,axis_z),App.Vector(1,0,0))
        samples=[]; x=x0
        while x<x1-1e-9:
            w=min(dx,x1-x); slab=Part.makeBox(w,300,300,App.Vector(x,-150,-150)); c=core.common(slab)
            gross=c.Volume/w; block=c.common(keep).Volume/w; clear=max(0.0,gross-block)
            samples.append({'x_mm':x+w/2,'gross_area_mm2':gross,'blocked_area_mm2':block,'net_area_mm2':clear,'net_FSA_ratio':clear/fsa,'block_fraction':block/gross if gross else 0.0}); x+=w
        worst=min(samples,key=lambda q:q['net_FSA_ratio']); maxblock=max(samples,key=lambda q:q['block_fraction'])
        side_rows.append({'nominal_FSA_ratio':ratio,'exit_ID_mm':exit_id,'minimum_net_FSA_ratio':worst['net_FSA_ratio'],'minimum_at_x_mm':worst['x_mm'],'maximum_block_fraction':maxblock['block_fraction'],'maximum_block_at_x_mm':maxblock['x_mm']})
    records.append({'side':side,'ratios':side_rows})
def vals(r): return [next(q for q in s['ratios'] if abs(q['nominal_FSA_ratio']-r)<1e-9)['minimum_net_FSA_ratio'] for s in records]
aud={'status':'V309_HYBRID_FAIRING_STRUCTURAL_BYPASS_POLICY','source_model':src.name,
     'architecture':{'surface_clearance_pad_mm':surface_pad,'hardware_fairing_outer_pad_mm':hardware_outer_pad,'hardware_inner_clearance_planned_mm':0.5,'hardware_fairing_wall_planned_mm':0.8,'structural_zone_x_mm':[x0,x1],'selected_structural_zone_nominal_FSA_ratio':1.0,'final_nozzle_contraction_moved_aft_of_F':True},
     'records':records,
     'decision':{'selected_ratio':1.0,'selected_minimum_net_FSA_ratio':min(vals(1.0)),'reason':'0.95 nominal only barely clears 0.85 net with hybrid fairing; 1.00 retains >0.86 net margin through stabilator/tail structure. Contract to 0.85-0.90 only downstream of station F after aft OML registration.'},
     'gates':{'hybrid_keepout_bilateral_net_FSA_ge_0p86_at_1p00':all(v>=0.86 for v in vals(1.0)),'0p95_has_less_than_0p005_margin_over_0p85':all((v-0.85)<0.005 for v in vals(0.95)),'structural_zone_policy_frozen':True,'downstream_aft_OML_registered':False,'final_nozzle_geometry_defined':False,'actual_EDF_hub_measured':False,'bench_verified':False,'print_release':False,'flight_release':False}}
aud['study_source_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(); aud_path.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))