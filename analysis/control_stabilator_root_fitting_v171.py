import json,pathlib,math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v167=json.loads((root/'analysis/control_stabilator_pivot_corridor_v167.json').read_text())
v170=json.loads((root/'analysis/control_stabilator_pivot_axis_v170.json').read_text())
xac=float(v170['area_weighted_quarter_chord_x_mm'])
shaft_r=3.0; min_structure=2.0; inset=shaft_r+min_structure
bands=[]
for b in [{'y_band_mm':[78,110],'common_x_corridor_mm':v167['full_78_110mm_band']['common_x_corridor_mm']}]+v167['candidate_subbands']:
    lo,hi=[float(x) for x in b['common_x_corridor_mm']]
    elo,ehi=lo+inset,hi-inset
    feasible=ehi>=elo
    max_forward_balance=xac-elo if feasible else None
    bands.append({'y_band_mm':b['y_band_mm'],'raw_corridor_mm':[lo,hi],'shaft_plus_structure_inset_each_x_side_mm':inset,'eroded_center_corridor_mm':[elo,ehi] if feasible else None,'max_global_quarter_chord_offset_if_pivot_at_forward_limit_mm':max_forward_balance})
# Choose a 5 mm forward-of-global-AC RC target if structurally available in an outboard engagement band.
target_offset=5.0; target_x=xac-target_offset
eligible=[]
for b in bands:
    if not b['eroded_center_corridor_mm']: continue
    lo,hi=b['eroded_center_corridor_mm']
    if lo<=target_x<=hi: eligible.append(b)
# Prefer the band starting closest to physical root / largest Y width among eligible.
selected=max(eligible,key=lambda b:(b['y_band_mm'][1]-b['y_band_mm'][0],-b['y_band_mm'][0])) if eligible else None
force=33.50791900575004; hinge=force*target_offset/1000; servo=hinge*(8/20)/.7*2; kgcm=servo/.0980665
result={
 'status':'V171_STABILATOR_STEPPED_ROOT_FITTING_ARCHITECTURE',
 'sources':['analysis/control_stabilator_pivot_corridor_v167.json','analysis/control_stabilator_pivot_axis_v170.json','analysis/control_stabilator_pivot_shaft_v149.json'],
 'mechanical_inset':{'shaft_radius_mm':shaft_r,'minimum_surrounding_structure_mm':min_structure,'total_planform_edge_inset_mm':inset},
 'global_area_weighted_quarter_chord_x_mm':xac,
 'eroded_corridors':bands,
 'target_RC_axis':{'pivot_x_mm':target_x,'global_quarter_chord_offset_mm':target_offset,'eligible_root_engagement_bands':eligible,'selected_engagement_band':selected},
 'architecture':{
   'type':'stepped metal/composite root fitting with inboard projecting shaft support',
   'reason':'A full 78-110 mm root-band bore with 5 mm edge inset can place the shaft only about 2.1 mm ahead of global quarter-chord. A fitting engaging from approximately Y=80 mm outward permits the safer X≈736 mm RC axis while the inboard fitting projects under the fuselage fairing.',
   'surface_primary_structure':'stabilator shell/spars bond into root fitting; servo linkage is actuator only',
   'shaft':'6 mm metal precision/shoulder shaft',
   'bearings':'two 6x13x5 radial bearings on fuselage side, separation maximized by packaging',
   'crank':'20 mm radius on inboard shaft/fitting side',
   'servo_arm':'8 mm'
 },
 'severe_screen_at_5mm_offset':{'hinge_moment_Nm':hinge,'required_servo_torque_kgcm_with_8_20_linkage_and_2x':kgcm,'14kgcm_default_class_margin_ratio':14/kgcm},
 'next_gate':'CAD only the stabilator-local root fitting and shaft engagement first. Do not design fuselage bearing mounts until aft fuselage common datum/OML is frozen.',
 'release':{'root_fitting_CAD_verified':False,'bond_load_transfer_verified':False,'fuselage_bearing_mount_verified':False,'servo_crank_packaging_verified':False,'flight_release':False}
}
(root/'analysis/control_stabilator_root_fitting_v171.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'xac':xac,'target_x':target_x,'bands':bands,'selected':selected,'severe_kgcm':kgcm,'margin14':14/kgcm},indent=2))