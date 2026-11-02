import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
v148=json.loads((R/'analysis/control_linkage_optimization_v148.json').read_text(encoding='utf-8'))
v168=json.loads((R/'analysis/control_servo_torque_gate_v168.json').read_text(encoding='utf-8'))
v241=json.loads((R/'migration/freecad/freecad_v241_light_stabilator_crank_audit.json').read_text(encoding='utf-8'))
v300=json.loads((R/'migration/freecad/freecad_v300_straight_stabilator_pushrod_audit.json').read_text(encoding='utf-8'))
old_arm=8.0; old_crank=20.0; new_crank=float(v241['geometry']['pin_radius_mm']); new_arm=new_crank*(old_arm/old_crank)
servo_half=50.0
ratio_old=old_arm/old_crank; ratio_new=new_arm/new_crank
throw_old=math.degrees(math.asin(ratio_old*math.sin(math.radians(servo_half))))
throw_new=math.degrees(math.asin(ratio_new*math.sin(math.radians(servo_half))))
severe_old=float(v148['default_8mm_arm']['severe_case']['required_servo_torque_kgcm'])
# Same arm/crank ratio and linkage-effectiveness assumption => same torque demand at servo.
severe_new=severe_old*(ratio_new/ratio_old)
pushrod_force=float(v241['load_screen']['pushrod_force_2x_N'])
buckling_sf=min(r['buckling']['buckling_SF'] for r in v300['rows'])
out={
 'status':'V301_CURRENT_STABILATOR_LINKAGE_RATIO_RECONCILED',
 'sources':['analysis/control_linkage_optimization_v148.json','analysis/control_servo_torque_gate_v168.json','migration/freecad/freecad_v241_light_stabilator_crank_audit.json','migration/freecad/freecad_v300_straight_stabilator_pushrod_audit.json'],
 'legacy_baseline':{'servo_arm_mm':old_arm,'stabilator_crank_mm':old_crank,'ratio':ratio_old,'servo_half_travel_deg':servo_half,'predicted_surface_half_throw_deg':throw_old,'severe_required_servo_torque_kgcm':severe_old},
 'current_geometry':{'servo_arm_candidate_mm':new_arm,'stabilator_crank_mm':new_crank,'ratio':ratio_new,'servo_half_travel_deg':servo_half,'predicted_surface_half_throw_deg':throw_new,'severe_required_servo_torque_kgcm':severe_new,'pushrod_force_design_N':pushrod_force,'v300_3mm_CF_pushrod_buckling_SF':buckling_sf},
 'servo_revision_evidence':{'repo_candidate':'TORQ TCM-1022','dims_mm':[23,12,27.5],'spline':'25T','nominal_target_torque_kgcm_8p4V':14.5,'nominal_target_speed_s_60deg_8p4V':0.055,'online_revision_conflict_exists':True,'purchased_unit_label_must_be_verified':True,'exact_spline_axis_offset_must_be_measured':True},
 'decision':{'use_6mm_servo_arm_with_15mm_current_crank':True,'retains_legacy_0p4_ratio':abs(ratio_new-ratio_old)<1e-12,'retains_predicted_half_throw':abs(throw_new-throw_old)<1e-12,'retains_v168_torque_basis':abs(severe_new-severe_old)<1e-12,'intermediate_bellcrank_required':False},
 'gates':{'current_ratio_reconciled':True,'predicted_half_throw_ge_17p8deg':throw_new>=17.8,'14kgcm_class_margin_over_severe_requirement':14.0/severe_new>=1.5,'v300_pushrod_buckling_SF_ge_5':buckling_sf>=5.0,'purchased_servo_revision_verified':False,'exact_servo_spline_axis_measured':False,'6mm_horn_hardware_selected':False,'dynamic_throw_CAD_verified':False,'bench_load_verified':False,'flight_release':False}
}
(R/'analysis/control_linkage_current_ratio_v301.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
