import json, math, pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v30=json.loads((R/'analysis/F14_pivot_cassette_screen_v30.json').read_text())
v33=json.loads((R/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/lower_crosstie_routing_v33/F14_v33_lower_crosstie_routing_audit.json').read_text())
M=v30['root_bending_moment_Nm']*1000.0 # Nmm
do,di=6.0,4.0
A=math.pi/4*(do**2-di**2)
I=math.pi/64*(do**4-di**4)
L=144.0
E=70000.0 # MPa=N/mm2 candidate
allow=350.0
zu=199.09240693460868
zf=v33['chosen_routes']['FRONT']['z_center_mm']; zr=v33['chosen_routes']['REAR']['z_center_mm']
seps={'front':zu-zf,'rear':zu-zr}
rows={}
for k,sep in seps.items():
    force=(M/2.0)/sep
    stress=force/A
    pcr=math.pi**2*E*I/L**2
    rows[k]={'vertical_couple_separation_mm':sep,'moment_share_Nmm':M/2,'tube_axial_force_N':force,'tube_axial_stress_MPa':stress,'candidate_material_strength_FOS':allow/stress,'euler_pinned_pcr_N':pcr,'compression_buckling_FOS':pcr/force}
# pessimistic single fore/aft frame taking all root moment
worst=[]
for k,sep in seps.items():
    f=M/sep; stress=f/A; pcr=math.pi**2*E*I/L**2
    worst.append({'frame':k,'force_N':f,'stress_MPa':stress,'strength_FOS':allow/stress,'buckling_FOS':pcr/f})
res={'status':'V97_CENTER_WINGBOX_CROSSTIE_LOAD_SCREEN','source_v30':'analysis/F14_pivot_cassette_screen_v30.json','source_v33':'v33 routed cross ties','design_case':{'review_mass_kg':v30['review_mass_kg'],'load_factor_g':v30['load_factor_g'],'asymmetric_high_side_fraction':v30['asymmetric_high_side_fraction'],'root_bending_moment_Nm':v30['root_bending_moment_Nm']},'tube_candidate':{'od_mm':do,'id_mm':di,'length_mm':L,'area_mm2':A,'I_mm4':I,'E_candidate_GPa':E/1000,'strength_allowable_candidate_MPa':allow,'material_values_verified':False},'equal_front_rear_moment_share':rows,'single_frame_worst_case':worst,'interpretation':['Cross ties are screened as axial tension/compression members reacting roll-axis root bending through upper/lower vertical separation.','Equal 50/50 front/rear moment share is the intended center-box load path; single-frame cases are included as a fault/sensitivity bound.','Euler pinned-end buckling is conservative for a socketed tube if end restraint is real, but actual carbon tube modulus/strength and socket stiffness remain unverified.','Do not drill transverse retention holes through the 6x4 carbon tube; retention should preserve the tube section.'],'gates':{'tube_material_datasheet_verified':False,'socket_load_transfer_verified':False,'retention_detail_designed':False,'center_box_physical_proof_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False}}
(R/'analysis/center_wingbox_crosstie_v97.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps({'A_mm2':A,'I_mm4':I,'Pcr_N':math.pi**2*E*I/L**2,'equal_share':rows,'single_frame':worst},indent=2))