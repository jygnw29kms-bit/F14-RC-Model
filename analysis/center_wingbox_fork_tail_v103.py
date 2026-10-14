import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v100=json.loads((root/'analysis/center_wingbox_landing_v100.json').read_text())
out={'status':'V103_EXTENDED_HARDPOINT_FORK_TAIL_PLAN','source_v102':'analysis/center_wingbox_hardpoint_sleeve_v102.json','geometry':{'socket_abs_y_mm':[50.0,74.0],'tail_outer_abs_y_mm':82.0,'tail_length_mm':8.0,'fork_inner_abs_y_mm':70.0,'total_fork_overlap_mm':12.0,'x_width_mm':12.0,'tail_is_solid_beyond_tube_end':True,'tube_end_abs_y_mm':72.0,'tube_to_solid_tail_gap_mm':2.0},'interface_screen':{},'rules':['source v99 6.4 mm circular bore remains untouched from absY50 to74','solid tail begins only after the 6 mm tube terminates at absY72','tail uses same x/z envelope as each front/rear socket','candidate must remain fully inside fuselage','candidate must retain continuous sweep clearance through 20-68 deg'],'gates':{'fuselage_containment':False,'fork_overlap_12mm':False,'source_socket_preserved':False,'continuous_sweep_clearance':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False}}
for frame,F in [('front',v100['load_screen']['front_force_N']),('rear',v100['load_screen']['rear_force_N'])]:
    area=12.0*12.0
    out['interface_screen'][frame]={'force_N':F,'nominal_overlap_area_mm2':area,'nominal_average_transfer_stress_MPa':F/area,'v100_4mm_overlap_stress_MPa':F/(12*4),'stress_reduction_ratio':(F/area)/(F/(12*4))}
(root/'analysis/center_wingbox_fork_tail_v103.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['interface_screen'],indent=2))