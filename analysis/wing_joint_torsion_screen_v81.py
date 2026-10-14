import json, pathlib, math
root=pathlib.Path(r'C:\Users\dezen\Desktop\F14-RC-Model')
wing=json.loads((root/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json').read_text())
v64=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v64_section_audit.json').read_text())
v66=json.loads((root/'analysis/native_span_load_screen_v66.json').read_text())
v79=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v79_carbon_sweep_keys_audit.json').read_text())
v80=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v80_key_section_audit.json').read_text())
factor=900.0/(2.0*wing['sections'][-1]['wbl_in'])
joint_y=363.9687853
section=min(wing['sections'],key=lambda s:abs(s['wbl_in']*factor-joint_y))
le=section['leading_edge_fs_in']*factor
te=section['trailing_edge_fs_in']*factor
chord=te-le
quarter=le+0.25*chord
mid=le+0.5*chord
# interpolate spar x from v64 upper-cap sections around joint
ups=sorted([s for s in v64['sections'] if s['body']=='CANDIDATE_CARBON_R_UPPER_CAP_NOT_STRENGTH_VERIFIED'],key=lambda s:s['y_mm'])
a,b=ups[0],ups[-1]
xa=a['profiles'][0]['centroid_mm'][0]; xb=b['profiles'][0]['centroid_mm'][0]
spar_x=xa+(xb-xa)*(joint_y-a['y_mm'])/(b['y_mm']-a['y_mm'])
# governing v66 case
case=max(v66['cases'],key=lambda c:(c['mass_kg'],c['load_factor'],c['assigned_side_fraction']))
q=case['uniform_load_N_per_mm']; tip_y=max(s['y_mm'] for s in case['stations'])
outboard_force=q*(tip_y-joint_y)
# remove thin-slab boundary artifact using the actual v79 key bounds
key_ymin=v79['keys']['bbox_y_min_mm']; key_ymax=v79['keys']['bbox_y_max_mm']; half=v80['slice_thickness_mm']/2
valid=[s for s in v80['sections'] if s.get('intersection_ok') and s['y_mm']>=key_ymin+half-1e-9 and s['y_mm']<=key_ymax-half+1e-9]
minsec=min(valid,key=lambda s:s['area_mm2'])
A=minsec['area_mm2']; key_cx=minsec['centroid_x_mm']; lever=max(abs(key_cx-spar_x),1e-6)
arms={
    'quarter_chord':abs(spar_x-quarter),
    'mid_chord':abs(spar_x-mid),
    'worst_airfoil_edge':max(abs(spar_x-le),abs(te-spar_x)),
}
cases=[]
for name,arm in arms.items():
    T=outboard_force*arm
    force=T/lever
    tau=force/A
    cases.append({'case':name,'aero_arm_mm':arm,'torsion_Nmm':T,'key_resultant_force_N':force,'required_average_key_shear_MPa':tau,'required_with_SF2_MPa':2*tau,'required_with_SF3_MPa':3*tau})
# extra dynamic sensitivity on worst edge
worst=next(c for c in cases if c['case']=='worst_airfoil_edge')
cases.append({'case':'worst_airfoil_edge_x1.5_dynamic','aero_arm_mm':worst['aero_arm_mm'],'torsion_Nmm':1.5*worst['torsion_Nmm'],'key_resultant_force_N':1.5*worst['key_resultant_force_N'],'required_average_key_shear_MPa':1.5*worst['required_average_key_shear_MPa'],'required_with_SF2_MPa':3*worst['required_average_key_shear_MPa'],'required_with_SF3_MPa':4.5*worst['required_average_key_shear_MPa']})
res={
 'status':'V81_WING_JOINT_TORSION_LOAD_REQUIREMENT_SCREEN',
 'source_files':['NASA_F14_basic_wing_v08.json','F14_v64_section_audit.json','native_span_load_screen_v66.json','F14_v79_carbon_sweep_keys_audit.json','F14_v80_key_section_audit.json'],
 'scale_factor_model_mm_per_source_in':factor,
 'joint_y_mm':joint_y,
 'local_geometry':{'leading_edge_x_mm':le,'trailing_edge_x_mm':te,'local_chord_mm':chord,'quarter_chord_x_mm':quarter,'mid_chord_x_mm':mid,'spar_x_mm':spar_x},
 'governing_load_case':{'mass_kg':case['mass_kg'],'load_factor':case['load_factor'],'assigned_side_fraction':case['assigned_side_fraction'],'uniform_load_N_per_mm':q,'tip_y_mm':tip_y,'outboard_force_from_joint_N':outboard_force},
 'key_geometry':{'interior_min_area_mm2':A,'min_area_y_mm':minsec['y_mm'],'key_centroid_x_mm':key_cx,'spar_to_key_centroid_lever_mm':lever,'raw_boundary_min_excluded_as_slice_edge_artifact':True,'v79_volume_retained_fraction':v79['keys']['volume_retained_fraction']},
 'torsion_cases':cases,
 'interpretation':[
   'The printed v79 key is not credited for primary wing bending; continuous carbon remains the primary bending path.',
   'Average key shear is a load requirement only, not an allowable or a release value.',
   'The worst-airfoil-edge case deliberately puts the entire outboard resultant at the most adverse local airfoil edge and is much more conservative than quarter-chord loading.',
   'A physical printed coupon and selected material/orientation are required before assigning a shear allowable.'
 ],
 'gates':{'geometry_candidate_pass':v79['geometry_candidate_pass'],'minimum_key_section_verified_geometrically':v80['minimum_key_section_verified_geometrically'],'torsion_load_requirement_established':True,'material_allowable_verified':False,'fit_coupon_verified':False,'torsion_transfer_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False}
}
(root/'analysis/wing_joint_torsion_screen_v81.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps({'factor':factor,'chord_mm':chord,'spar_x':spar_x,'quarter_x':quarter,'outboard_force_N':outboard_force,'key_min_area_mm2':A,'key_lever_mm':lever,'torsion_cases':cases},indent=2))