import json, math, pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
plan=json.loads((R/'analysis/torsion_fixture_v96.json').read_text())
audit=json.loads((R/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v96_torsion_fixture_audit.json').read_text())
ix0,ix1=map(float,plan['inner_skin_bbox_mm']['x']); ox0,ox1=map(float,plan['outer_skin_bbox_mm']['x'])
inner_half=(ix1-ix0)/2; outer_half=(ox1-ox0)/2
fixed_clear=51-2.3-inner_half; moving_clear=49-2.3-outer_half
fixed_raw=112*18*8/1000; holevol=4*math.pi*(4.6/2)**2*8/1000; moving_raw=108*18*8/1000
parts={p['body']:p for p in audit['parts']}
val={
 'status':'V96_FIXTURE_DIMENSION_VALIDATION',
 'fixed_plate_raw_volume_cm3':fixed_raw,
 'fixed_expected_hole_volume_cm3':holevol,
 'fixed_expected_net_cm3':fixed_raw-holevol,
 'fixed_fusion_net_cm3':parts['FIXED_TOP_v96']['volume_cm3'],
 'fixed_volume_error_cm3':parts['FIXED_TOP_v96']['volume_cm3']-(fixed_raw-holevol),
 'moving_bottom_expected_net_cm3':moving_raw-holevol,
 'moving_bottom_fusion_net_cm3':parts['MOVING_BOTTOM_v96']['volume_cm3'],
 'moving_volume_error_cm3':parts['MOVING_BOTTOM_v96']['volume_cm3']-(moving_raw-holevol),
 'minimum_fixed_hole_edge_clearance_from_skin_mm':fixed_clear,
 'minimum_moving_hole_edge_clearance_from_skin_mm':moving_clear,
 'fixed_clamp_y_range_mm':[float(plan['assembly']['fixed_clamp_y_center_mm'])-9,float(plan['assembly']['fixed_clamp_y_center_mm'])+9],
 'moving_clamp_y_range_mm':[float(plan['assembly']['moving_clamp_y_center_mm'])-9,float(plan['assembly']['moving_clamp_y_center_mm'])+9],
 'joint_clearance_each_side_mm':1.0,
 'pass':abs(parts['FIXED_TOP_v96']['volume_cm3']-(fixed_raw-holevol))<1e-6 and abs(parts['MOVING_BOTTOM_v96']['volume_cm3']-(moving_raw-holevol))<1e-6 and fixed_clear>5 and moving_clear>5,
}
(R/'analysis/torsion_fixture_v96_validation.json').write_text(json.dumps(val,indent=2),encoding='utf-8')
print(json.dumps(val,indent=2))