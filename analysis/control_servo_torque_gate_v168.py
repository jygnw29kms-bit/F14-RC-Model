import json,pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v146=json.loads((root/'analysis/control_stabilator_torque_v146.json').read_text())
v148=json.loads((root/'analysis/control_linkage_optimization_v148.json').read_text())
v147=json.loads((root/'analysis/control_servo_power_acceptance_v147.json').read_text())
req=float(v148['default_8mm_arm']['severe_case']['required_servo_torque_kgcm'])
default=14.0
legacy_min=10.0
result={
 'status':'V168_STABILATOR_SERVO_TORQUE_GATE_RECONCILIATION',
 'sources':['analysis/control_stabilator_torque_v146.json','analysis/control_linkage_optimization_v148.json','analysis/control_servo_power_acceptance_v147.json','analysis/control_stabilator_pivot_corridor_v167.json'],
 'optimized_linkage':{'servo_arm_mm':8,'stabilator_crank_mm':20,'linkage_effectiveness':0.7,'predicted_half_throw_deg':v148['default_8mm_arm']['severe_case']['predicted_stabilator_half_travel_deg'],'severe_required_servo_torque_kgcm_including_existing_2x_factor':req},
 'rating_margins':{
   '10kgcm_class_ratio_to_severe_requirement':legacy_min/req,
   '14kgcm_class_ratio_to_severe_requirement':default/req,
   'note':'Published servo torque is commonly a stall rating, not a continuous flight-load allowable. Rating ratio is not itself flight qualification.'
 },
 'reconciled_gate':{
   'default_nominal_torque_class_min_kgcm':default,
   '10_to_13p9kgcm_allowed_only_by_full_bench_exception':True,
   'below_10kgcm_rejected_for_baseline':True,
   'operating_voltage':'7.4-8.4 V HV preferred, exact voltage matched to receiver/BEC/servo hardware',
   'preferred_mass_each_g_max':20,
   'hard_mass_warning_each_g':25,
   'metal_gears':True,'metal_output_interface':True,'dual_output_bearing_preferred':True
 },
 'bench_exception_for_10_to_13p9kgcm':{
   'must_pass_v147_hinge_moment_Nm':0.67,
   'cycles_each_direction':100,
   'supply_test':'worst-case regulated bus voltage under simultaneous taileron reversal + sweep load + EDF throttle transient',
   'minimum_receiver_bus_voltage_V':6.8,
   'max_total_neutral_freeplay_deg':0.5,
   'max_permanent_neutral_shift_deg':0.25,
   'no_spline_slip':True,'no_abnormal_temperature_or_gear_noise':True
 },
 'decision':{
   'v147_10kgcm_default_is_superseded':True,
   'v148_linkage_geometry_retained':True,
   '14kgcm_default_does_not_change_linkage_geometry':True,
   'servo_model_freeze_waits_for_packaging_and_bench':True
 },
 'release':{'servo_model_frozen':False,'linkage_packaging_verified':False,'bench_load_verified':False,'brownout_verified':False,'flutter_verified':False,'flight_release':False}
}
(root/'analysis/control_servo_torque_gate_v168.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))