import FreeCAD as App, Part, pathlib, json, math, hashlib, itertools
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v307_UNIFIED_TAIL_SERVO_CASSETTE_BASE.FCStd'
out=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'
audp=R/'migration/freecad/freecad_v310_structural_bypass_freeflow_audit.json'
v309=json.loads((R/'migration/freecad/freecad_v309_hybrid_fairing_bypass_audit.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v310_STRUCTURAL_BYPASS_FREEFLOW')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
x0=731.5; x1=754.962281164333; L=x1-x0
axis_y=66.28458486059378; axis_z=-10.508688347971937
fan_id=50.0; hub_d=28.0; fsa=math.pi/4.0*(fan_id**2-hub_d**2)
ratio=1.0; exit_id=math.sqrt(4.0*(fsa*ratio)/math.pi)
surface_pad=0.5; hardware_outer_pad=1.3; dx=0.25
def union_names(names):
    ss=[doc.getObject(n).Shape for n in names if doc.getObject(n)]
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
rows=[]
for side,sgn in [('R',1),('L',-1)]:
    surfaces=dilate(union_names([f'STABILATOR_{side}',f'VTAIL_{side}',f'VENTRAL_{side}']),surface_pad)
    hardware=dilate(union_names([f'STAB_BEARING_{side}_1',f'STAB_HOUSING_{side}_1',f'STAB_BEARING_{side}_2',f'STAB_HOUSING_{side}_2',f'V234_BEARING_INBOARD_COLLAR_{side}',f'V234_BEARING_OUTER_SHOULDER_{side}',f'V234_SURFACE_INNER_COLLAR_{side}',f'V234_SURFACE_OUTER_WASHER_{side}',f'V234_END_FASTENER_HEAD_{side}',f'V237_D_SHAFT_{side}',f'V241_LIGHT_D_CRANK_{side}',f'V284_LIGHT_D_ROOT_FITTING_{side}']),hardware_outer_pad)
    keep=surfaces.fuse(hardware).removeSplitter()
    core=Part.makeCone(fan_id/2.0,exit_id/2.0,L,App.Vector(x0,sgn*axis_y,axis_z),App.Vector(1,0,0))
    free_raw=core.cut(keep).removeSplitter()
    solids=sorted(list(free_raw.Solids),key=lambda s:s.Volume,reverse=True)
    free=solids[0]
    discarded=sum(s.Volume for s in solids[1:])
    ko=doc.addObject('PartDesign::Feature','V310_HYBRID_KEEPOUT_'+side); ko.Shape=keep; ko.Label='v310 hybrid tail/exhaust keepout '+side
    fo=doc.addObject('PartDesign::Feature','V310_STRUCTURAL_BYPASS_FREEFLOW_'+side); fo.Shape=free; fo.Label='v310 structural-zone main through-flow 1.00 FSA '+side
    oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
    samples=[]; x=x0
    while x<x1-1e-9:
        w=min(dx,x1-x); slab=Part.makeBox(w,300,300,App.Vector(x,-150,-150)); c=core.common(slab)
        gross=c.Volume/w; block=c.common(keep).Volume/w; clear=max(0.0,gross-block)
        samples.append({'x_mm':x+w/2,'gross_area_mm2':gross,'blocked_area_mm2':block,'net_area_mm2':clear,'net_FSA_ratio':clear/fsa}); x+=w
    worst=min(samples,key=lambda q:q['net_FSA_ratio'])
    rows.append({'side':side,'raw_freeflow_solid_count':len(free_raw.Solids),'discarded_dead_pocket_volume_mm3':discarded,'discarded_fraction_of_raw_freeflow':discarded/free_raw.Volume if free_raw.Volume else 0.0,'freeflow_valid':free.isValid(),'freeflow_solid_count':len(free.Solids),'freeflow_shell_count':len(free.Shells),'freeflow_volume_mm3':free.Volume,
                 'freeflow_OML_fraction':free.common(oml).Volume/free.Volume,'keepout_valid':keep.isValid(),'keepout_solid_count':len(keep.Solids),
                 'minimum_net_FSA_ratio':worst['net_FSA_ratio'],'minimum_net_at_x_mm':worst['x_mm'],'exit_inner_diameter_mm':exit_id,
                 'source_v309_minimum_net_FSA_ratio':next(q['minimum_net_FSA_ratio'] for s in v309['records'] if s['side']==side for q in s['ratios'] if abs(q['nominal_FSA_ratio']-1.0)<1e-9)})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V310_STRUCTURAL_BYPASS_FREEFLOW','source_model':src.name,'policy_source':'migration/freecad/freecad_v309_hybrid_fairing_bypass_audit.json',
     'architecture':{'nominal_structural_zone_FSA_ratio':ratio,'fan_ID_mm':fan_id,'hub_D_mm':hub_d,'FSA_mm2':fsa,'exit_ID_mm':exit_id,'structural_zone_x_mm':[x0,x1],'surface_clearance_mm':surface_pad,'internal_hardware_outer_fairing_keepout_mm':hardware_outer_pad,'flow_volume_only_not_printable_duct':True,'downstream_contraction_deferred_until_aft_OML_registered':True},
     'rows':rows,
     'gates':{'bilateral_raw_split_only_tiny_dead_pocket':all(r['raw_freeflow_solid_count']==2 and r['discarded_fraction_of_raw_freeflow']<0.0001 for r in rows),'bilateral_freeflow_valid_single_solid':all(r['freeflow_valid'] and r['freeflow_solid_count']==1 for r in rows),'bilateral_freeflow_single_shell':all(r['freeflow_shell_count']==1 for r in rows),'bilateral_freeflow_OML_ge_0p999':all(r['freeflow_OML_fraction']>=0.999 for r in rows),'bilateral_minimum_net_FSA_ge_0p86':all(r['minimum_net_FSA_ratio']>=0.86 for r in rows),'v309_numeric_reproduction_within_1e_6':all(abs(r['minimum_net_FSA_ratio']-r['source_v309_minimum_net_FSA_ratio'])<=1e-6 for r in rows),'printable_fairing_wall_defined':False,'downstream_aft_OML_registered':False,'final_nozzle_geometry_defined':False,'actual_EDF_hub_measured':False,'bench_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
