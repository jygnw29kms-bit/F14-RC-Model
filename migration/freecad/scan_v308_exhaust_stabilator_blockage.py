import FreeCAD as App, Part, pathlib, json, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v307_UNIFIED_TAIL_SERVO_CASSETTE_BASE.FCStd'
aud_path=R/'migration/freecad/freecad_v308_exhaust_stabilator_blockage_audit.json'
d=App.openDocument(str(src))
x0=731.5; x1=754.962281164333; L=x1-x0
axis_y=66.28458486059378; axis_z=-10.508688347971937
fan_id=50.0; hub_d=28.0
fsa=math.pi/4.0*(fan_id**2-hub_d**2)
ratios=[0.85,0.90,0.95,1.00]
dx=0.25
base_names=['STAB_BEARING_{s}_1','STAB_HOUSING_{s}_1','STAB_BEARING_{s}_2','STAB_HOUSING_{s}_2',
            'V234_BEARING_INBOARD_COLLAR_{s}','V234_BEARING_OUTER_SHOULDER_{s}',
            'V234_SURFACE_INNER_COLLAR_{s}','V234_SURFACE_OUTER_WASHER_{s}','V234_END_FASTENER_HEAD_{s}',
            'V237_D_SHAFT_{s}','V241_LIGHT_D_CRANK_{s}','V284_LIGHT_D_ROOT_FITTING_{s}']
records=[]
for side,sgn in [('R',1),('L',-1)]:
    names=[n.format(s=side) for n in base_names]
    shapes=[d.getObject(n).Shape for n in names if d.getObject(n)]
    hw=shapes[0]
    for sh in shapes[1:]: hw=hw.fuse(sh)
    hw=hw.removeSplitter()
    side_rows=[]
    for ratio in ratios:
        exit_id=math.sqrt(4.0*(fsa*ratio)/math.pi)
        core=Part.makeCone(fan_id/2.0,exit_id/2.0,L,App.Vector(x0,sgn*axis_y,axis_z),App.Vector(1,0,0))
        samples=[]; x=x0
        while x < x1-1e-9:
            w=min(dx,x1-x)
            slab=Part.makeBox(w,300.0,300.0,App.Vector(x,-150.0,-150.0))
            c=core.common(slab); core_area=c.Volume/w if w else 0.0
            block_area=c.common(hw).Volume/w if w else 0.0
            clear_area=max(0.0,core_area-block_area)
            samples.append({'x_mm':x+w/2.0,'gross_core_area_mm2':core_area,'hardware_block_area_mm2':block_area,
                            'net_clear_area_mm2':clear_area,'net_clear_FSA_ratio':clear_area/fsa if fsa else 0.0,
                            'block_fraction_of_gross':block_area/core_area if core_area else 0.0})
            x+=w
        worst=min(samples,key=lambda q:q['net_clear_FSA_ratio'])
        maxblock=max(samples,key=lambda q:q['block_fraction_of_gross'])
        intersections=[]
        for n in names:
            o=d.getObject(n)
            if o:
                iv=core.common(o.Shape).Volume
                if iv>1e-6: intersections.append({'object':n,'intersection_mm3':iv})
        oml=d.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
        side_rows.append({'nominal_exit_FSA_ratio':ratio,'exit_inner_diameter_mm':exit_id,
                          'gross_core_OML_fraction':core.common(oml).Volume/core.Volume,
                          'minimum_net_clear_FSA_ratio':worst['net_clear_FSA_ratio'],'minimum_net_at_x_mm':worst['x_mm'],
                          'maximum_local_block_fraction':maxblock['block_fraction_of_gross'],'maximum_block_at_x_mm':maxblock['x_mm'],
                          'intersecting_hardware':intersections})
    records.append({'side':side,'ratios':side_rows})
def row(side,ratio):
    return next(q for q in next(x for x in records if x['side']==side)['ratios'] if abs(q['nominal_exit_FSA_ratio']-ratio)<1e-9)
r90=[row('R',0.90),row('L',0.90)]
aud={'status':'V308_EXHAUST_STABILATOR_BLOCKAGE_NET_FSA_AUDIT','source_model':src.name,
     'architecture':{'fan_inner_diameter_assumed_mm':fan_id,'hub_diameter_assumed_mm':hub_d,'fan_swept_area_mm2':fsa,
                     'exhaust_start_x_mm':x0,'exhaust_end_x_mm':x1,'axis_abs_y_mm':axis_y,'axis_z_mm':axis_z,
                     'sample_dx_mm':dx,'candidate_nominal_4S_exit_FSA_ratio':0.90,
                     'intent':'retain current stabilator architecture; shape exhaust/fairing around hardware rather than relocate validated linkage'},
     'records':records,
     'decision':{'nominal_0p90_net_min_FSA_ratio':min(q['minimum_net_clear_FSA_ratio'] for q in r90),
                 'nominal_0p90_effective_within_original_4S_target_band_0p85_to_0p90':all(0.85<=q['minimum_net_clear_FSA_ratio']<=0.90 for q in r90),
                 'straight_unrelieved_exhaust_shell_allowed':False,
                 'next_gate':'v309 hardware-relieved exhaust wall / aerodynamic fairing candidate'},
     'gates':{'gross_core_bilateral_OML_ge_0p999':all(q['gross_core_OML_fraction']>=0.999 for s in records for q in s['ratios']),
              'nominal_0p90_net_min_FSA_ge_0p85':all(q['minimum_net_clear_FSA_ratio']>=0.85 for q in r90),
              'nominal_0p90_net_min_FSA_le_0p90':all(q['minimum_net_clear_FSA_ratio']<=0.90 for q in r90),
              'straight_core_zero_hardware_intersection':all(len(q['intersecting_hardware'])==0 for s in records for q in s['ratios']),
              'hardware_fairing_defined':False,'actual_EDF_hub_measured':False,'bench_thrust_current_temperature_verified':False,
              'print_release':False,'flight_release':False}}
aud['study_source_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
aud_path.write_text(json.dumps(aud,indent=2),encoding='utf-8')
print(json.dumps({'status':aud['status'],'decision':aud['decision'],'gates':aud['gates'],
                  'R':[{k:q[k] for k in ['nominal_exit_FSA_ratio','exit_inner_diameter_mm','minimum_net_clear_FSA_ratio','maximum_local_block_fraction']} for q in records[0]['ratios']]},indent=2))