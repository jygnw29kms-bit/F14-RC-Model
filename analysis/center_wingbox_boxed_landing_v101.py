import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v100=json.loads((root/'analysis/center_wingbox_landing_v100.json').read_text())
b=12.0; h=8.0; t=2.0; L=20.0
bi=b-2*t; hi=h-2*t
A=b*h-bi*hi
I=(b*h**3-bi*hi**3)/12.0
W=I/(h/2.0)
rows=[]
for frame,F in [('front',v100['load_screen']['front_force_N']),('rear',v100['load_screen']['rear_force_N'])]:
    q=F/24.0
    M_uniform=q*L**2/2.0
    sig_uniform=M_uniform/W
    M_tip=F*L
    sig_tip=M_tip/W
    rows.append(dict(frame=frame,force_N=F,line_load_N_per_mm=q,uniform_moment_Nmm=M_uniform,uniform_stress_MPa=sig_uniform,tip_load_moment_Nmm=M_tip,tip_load_stress_MPa=sig_tip,deflection_coeff_uniform_mm_times_E_MPa=q*L**4/(8*I),deflection_coeff_tip_mm_times_E_MPa=F*L**3/(3*I)))
out={
 'status':'V101_BOXED_LANDING_LOADPATH_SCREEN',
 'source_v100':'analysis/center_wingbox_landing_v100.json',
 'section':{'outer_width_mm':b,'outer_height_mm':h,'wall_mm':t,'inner_width_mm':bi,'inner_height_mm':hi,'area_mm2':A,'I_x_mm4':I,'W_x_mm3':W,'I_gain_vs_v100_flat_12x2':I/8.0},
 'cantilever_screen_length_mm':L,
 'cases':rows,
 'interpretation':['closed box is screened conservatively as a free cantilever even though production intent is union/contact with fork and socket','uniform-load case retains the v100 load-distribution assumption; tip-load case is a harsher upper sensitivity bound','material allowable and joint/contact stiffness are not credited'],
 'cad_candidate':{'x_width_mm':12.0,'box_height_mm':8.0,'wall_mm':2.0,'inboard_abs_y_mm':50.0,'outboard_abs_y_mm':72.0,'required_fork_overlap_mm':2.0,'required_socket_overlap_mm':2.0},
 'gates':{'fuselage_containment':False,'fork_union_contact':False,'socket_union_contact':False,'continuous_sweep_clearance':False,'material_allowable_verified':False,'physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False}
}
(root/'analysis/center_wingbox_boxed_landing_v101.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'I_mm4':I,'W_mm3':W,'I_gain':I/8,'cases':rows},indent=2))