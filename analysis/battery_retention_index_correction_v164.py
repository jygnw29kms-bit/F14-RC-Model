import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
pack_len=106.0
centers=[305.0,340.0,375.0]
pin_r=2.0
hard_clear=1.0
max_shoe_reach=12.0
holes=[249.0]+[259.0+10*i for i in range(17)]+[431.0]  # 249, 259..419, 431
checks=[]
for c in centers:
    front_edge=c-pack_len/2; aft_edge=c+pack_len/2
    front_candidates=[]; aft_candidates=[]
    for h in holes:
        # pin cylinder occupies x h+-2; require 1 mm gap to bare pack
        if h+pin_r <= front_edge-hard_clear:
            gap=front_edge-(h+pin_r)
            front_candidates.append((gap,h))
        if h-pin_r >= aft_edge+hard_clear:
            gap=(h-pin_r)-aft_edge
            aft_candidates.append((gap,h))
    f=min(front_candidates) if front_candidates else None
    a=min(aft_candidates) if aft_candidates else None
    rec={'battery_center_x_mm':c,'pack_x_range_mm':[front_edge,aft_edge],
         'front_stop':None if f is None else {'pin_x_mm':f[1],'hard_gap_to_pack_mm':f[0],'shoe_reach_required_mm':f[0]},
         'aft_stop':None if a is None else {'pin_x_mm':a[1],'hard_gap_to_pack_mm':a[0],'shoe_reach_required_mm':a[0]}}
    rec['pass']=f is not None and a is not None and f[0]<=max_shoe_reach and a[0]<=max_shoe_reach
    checks.append(rec)
# Separation between stop pin axis z195 and raised frame fastener z203.
stop_z=195.0; m3_z=203.0; m3_r=3.3/2
axis_sep=abs(m3_z-stop_z); surface_ligament=axis_sep-(pin_r+m3_r)
result={
 'status':'V164_RETENTION_INDEX_AND_FASTENER_SEPARATION_CORRECTION',
 'corrects':['v157 stop-hole end coverage','v158 near-coincident frame/stop fastener axes'],
 'retention_hole_x_mm':holes,
 'stop_pin_diameter_mm':4.0,
 'minimum_bare_pack_clearance_mm':hard_clear,
 'maximum_compliant_stop_shoe_reach_mm':max_shoe_reach,
 'battery_position_checks':checks,
 'all_70mm_travel_positions_have_two_positive_stops':all(x['pass'] for x in checks),
 'frame_interface_revision':{
   'anchor_x_mm':[249,431],
   'stop_pin_axis_z_mm':stop_z,
   'M3_frame_hole_axis_z_mm':m3_z,
   'M3_clearance_hole_d_mm':3.3,
   'axis_separation_mm':axis_sep,
   'minimum_surface_ligament_between_nominal_holes_mm':surface_ligament,
   'M3_hole_y_span_mm':[20,28],
   'reason':'Separate frame-fastener bore from the terminal stop-pin bore while keeping both inside the v155 structural/service envelope.'
 },
 'next_CAD_gate':'v165 regenerate tray holes and frame pads with corrected terminal stops and raised M3 frame fastener axes',
 'release':{'corrected_CAD_verified':False,'stop_shoe_designed':False,'retention_proof_pass':False,'print_release':False,'flight_release':False}
}
(root/'analysis/battery_retention_index_correction_v164.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))