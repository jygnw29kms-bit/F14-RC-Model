import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v66=json.loads((root/'analysis/native_span_load_screen_v66.json').read_text())
v63=json.loads((root/'analysis/source_spar_section_properties_v63.json').read_text())
y_joint=363.9687853
# Conservative station: use nearest inboard sampled station to avoid understating moment at joint.
case=max(v66['cases'], key=lambda c:(c['mass_kg'],c['load_factor'],c['assigned_side_fraction']))
inboard=[s for s in case['stations'] if s['y_mm']<=y_joint]
load=max(inboard,key=lambda s:s['y_mm'])
sec=min(v63['stations'], key=lambda s:abs(s['model_y_mm']-y_joint))
d=sec['shifted_and_trimmed']['cap_centroid_separation_mm']
M=load['moment_Nmm']
cap_force=M/d
cap_width=sec['width_mm']
# Bond/engagement sensitivity. This is NOT adhesive approval; it shows required average shear.
lengths=[8,10,12,15,20,25,30]
rows=[]
for L in lengths:
    area=cap_width*L
    tau=cap_force/area
    rows.append({'engagement_mm':L,'one_cap_bond_area_mm2':area,'average_cap_transfer_shear_MPa':tau,'shear_with_SF2_MPa':2*tau,'shear_with_SF3_MPa':3*tau})
# Alignment rib itself is explicitly non-primary. Use 12 mm candidate as compact initial CAD study.
result={
 'status':'V74_JOINT_LOADPATH_SCREEN_CANDIDATE',
 'source_v66':'analysis/native_span_load_screen_v66.json',
 'source_v63':'analysis/source_spar_section_properties_v63.json',
 'joint_y_mm':y_joint,
 'governing_screen_case':{'mass_kg':case['mass_kg'],'load_factor':case['load_factor'],'assigned_side_fraction':case['assigned_side_fraction']},
 'conservative_inboard_sample':load,
 'spar_section_near_joint':{'sample_y_mm':sec['model_y_mm'],'cap_width_mm':cap_width,'cap_centroid_separation_mm':d,'cap_area_total_mm2':sec['shifted_and_trimmed']['cap_area_mm2'],'web_area_mm2':sec['shifted_and_trimmed']['web_area_mm2']},
 'bending_couple_cap_force_N':cap_force,
 'engagement_sensitivity':rows,
 'v74_architecture':{
   'primary_bending_path':'continuous carbon spar/caps across printed segment interface',
   'printed_joint_role':['segment alignment','skin step control','local torsion transfer','assembly indexing'],
   'printed_joint_must_not_be_sized_as_sole_bending_member':True,
   'candidate_axial_engagement_mm':12.0,
   'skin_radial_clearance_mm':0.15,
   'spar_bondline_candidate_mm':0.10,
   'anti_rotation':'two separated keyed/index features, outside spar bond faces',
   'serviceability':'dry-fit before bonding; no forced press fit around carbon path'
 },
 'gates':{
   'adhesive_system_selected':False,
   'coupon_verified':False,
   'torsion_load_verified':False,
   'carbon_continuity_in_CAD_verified':False,
   'joint_geometry_CAD_verified':False,
   'structural_capacity_verified':False,
   'print_release':False,
   'flight_release':False
 },
 'notes':['Moment uses nearest INBOARD v66 sample at y=357.1875 mm, so it is conservative relative to the 363.969 mm joint under the same sampled load model.','Average bond shear is a sensitivity only; no adhesive allowable is assumed or approved.','If the carbon path is interrupted at the print joint, this architecture is invalid and the joint must be redesigned as a structural splice.']
}
(root/'analysis/wing_joint_loadpath_v74.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'M_Nmm':M,'cap_force_N':cap_force,'cap_width_mm':cap_width,'sep_mm':d,'candidate12mm':next(x for x in rows if x['engagement_mm']==12)},indent=2))
