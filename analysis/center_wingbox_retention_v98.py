import json,math,pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
i=json.loads((R/'cad/fusion/F14TomcatRC/F14_v98_section_inputs.json').read_text()); v97=json.loads(pathlib.Path(i['v97_path']).read_text())
eng=i['tie_end_abs_y_mm']-i['socket_inner_abs_y_mm']; area=math.pi*i['tube_od_mm']*eng
loads={}
for k,v in v97['equal_front_rear_moment_share'].items(): loads[k]={'tie_force_N':v['tube_axial_force_N'],'engagement_mm':eng,'cylindrical_interface_area_mm2':area,'required_average_interface_shear_MPa':v['tube_axial_force_N']/area}
worst=[]
for v in v97['single_frame_worst_case']: worst.append({'frame':v['frame'],'tie_force_N':v['force_N'],'required_average_interface_shear_MPa':v['force_N']/area})
o={'status':'V98_EXTENDED_RISER_RETENTION_PLAN','socket_span_abs_y_mm':[i['socket_inner_abs_y_mm'],i['socket_outer_abs_y_mm']],'actual_tube_engagement_mm':eng,'tube_cylindrical_interface_area_mm2':area,'equal_share_interface_screen':loads,'single_frame_interface_screen':worst,'retention_policy':['no transverse drilling of 6x4 carbon tube','bonded cylindrical/saddle interface plus non-damaging clamp/end-stop may be used','actual adhesive/process must be qualified separately for carbon-to-socket interface'],'geometry_gate_pending':True,'material_allowable_verified':False,'retention_detail_release':False,'print_release':False,'flight_release':False}
(R/'analysis/center_wingbox_retention_v98.json').write_text(json.dumps(o,indent=2),encoding='utf-8'); print(json.dumps(o,indent=2))