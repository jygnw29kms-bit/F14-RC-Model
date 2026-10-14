import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v100=json.loads((root/'analysis/center_wingbox_landing_v100.json').read_text())
b=12.0; d=6.4; L=20.0
# actual v99 front/rear socket sections: z0 common, bore-center offset from bottom and top from v99 construction
frames={'front':{'h':12.0,'zc_from_bottom':8.0,'F':v100['load_screen']['front_force_N']},
        'rear': {'h':11.0,'zc_from_bottom':7.0,'F':v100['load_screen']['rear_force_N']}}
rows=[]
for name,s in frames.items():
    h=s['h']; zc=s['zc_from_bottom']; F=s['F']
    Ar=b*h; Ac=math.pi*d*d/4; A=Ar-Ac
    zr=h/2; zbar=(Ar*zr-Ac*zc)/A
    Ir=b*h**3/12 + Ar*(zr-zbar)**2
    Ic=math.pi*d**4/64 + Ac*(zc-zbar)**2
    I=Ir-Ic
    c=max(zbar,h-zbar); W=I/c
    q=F/24.0; Mu=q*L**2/2; Mt=F*L
    rows.append({'frame':name,'outer_h_mm':h,'bore_center_from_bottom_mm':zc,'net_area_mm2':A,'centroid_from_bottom_mm':zbar,'I_x_mm4':I,'W_min_mm3':W,'force_N':F,'uniform_moment_Nmm':Mu,'uniform_stress_MPa':Mu/W,'tip_load_moment_Nmm':Mt,'tip_load_stress_MPa':Mt/W,'uniform_deflection_coeff_mm_times_E_MPa':q*L**4/(8*I),'tip_deflection_coeff_mm_times_E_MPa':F*L**3/(3*I)})
out={'status':'V102_CROSSTIE_HARDPOINT_SLEEVE_SCREEN','source_v99':'workspace/RC-F14-Tomcat/Fusion/Exports/Current/center_wingbox_v99/F14_v99_circular_crosstie_retention_audit.json','source_v100':'analysis/center_wingbox_landing_v100.json','architecture':{'outer_width_mm':b,'bore_diameter_mm':d,'supported_y_abs_mm':[50.0,74.0],'nominal_length_mm':24.0,'fork_overlap_target_mm':4.0,'socket_overlap_length_mm':24.0,'role':'structural sleeve/hardpoint surrounding the existing circular crosstie bore; union/contact to lower fork and socket'},'sections':rows,'interpretation':['uses actual v99 front/rear outer section heights and bore offsets','screened as a 20 mm free cantilever even though CAD target is direct union/contact to fork and socket','tip-load case is intentionally harsher than the distributed socket load assumption','no material allowable credited'], 'cad_gates':{'fuselage_containment':False,'socket_union_contact':False,'fork_union_contact':False,'bore_preserved':False,'tube_engagement_preserved':False,'continuous_sweep_clearance':False,'material_allowable_verified':False,'physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False}}
(root/'analysis/center_wingbox_hardpoint_sleeve_v102.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))