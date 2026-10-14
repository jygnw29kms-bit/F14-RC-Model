import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v97=json.loads((root/'analysis/center_wingbox_crosstie_v97.json').read_text())
v105=json.loads((root/'analysis/center_wingbox_monolithic_module_v105.json').read_text())
front=v97['equal_front_rear_moment_share']['front']['tube_axial_force_N']
rear=v97['equal_front_rear_moment_share']['rear']['tube_axial_force_N']
plan={
 'status':'V107_CENTER_WINGBOX_PHYSICAL_PROOF_PLAN',
 'sources':['analysis/center_wingbox_crosstie_v97.json','analysis/center_wingbox_monolithic_module_v105.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/center_wingbox_v106/F14_v106_relative_containment_audit.json'],
 'test_article':'one complete v105 lower hardpoint module per side, including v99 6.4 mm sockets and v103 fork tails; material/process must match intended production article',
 'fixture':{
   'clamp_zone_abs_y_mm':[95,135],
   'do_not_support_zone_abs_y_mm':[50,90],
   'load_axis':'socket/crosstie Y axis',
   'load_pin':'6.0 mm smooth steel proof pin for module test; actual carbon tube qualified separately',
   'load_measurement':'calibrated >=2 kN load cell or equivalent traceable force measurement',
   'displacement_measurement':'dial indicator or digital indicator at socket center, resolution <=0.01 mm'
 },
 'load_cases':[
   {'id':'FRONT_AXIAL','socket':'front','design_N':front,'proof_1_5x_N':1.5*front,'ultimate_sensitivity_2x_N':2*front},
   {'id':'REAR_AXIAL','socket':'rear','design_N':rear,'proof_1_5x_N':1.5*rear,'ultimate_sensitivity_2x_N':2*rear}
 ],
 'sequence':[
   'inspect and measure bore diameter/ovalization baseline at two orthogonal directions',
   'precondition 10 cycles 0 -> 0.5x design -> 0',
   'record displacement at 0.25x, 0.50x, 0.75x and 1.00x design',
   'unload and record permanent set',
   'apply proof load 1.50x design for 10 s',
   'unload, inspect, remeasure bore and permanent set',
   'repeat a 0.50x design stiffness check and compare with pre-proof stiffness',
   '2.0x case is destructive/sensitivity qualification only, not required on every production article'
 ],
 'provisional_acceptance':{
   'no_crack_delamination_or_layer_separation':True,
   'no_socket_rotation_or_visible_fork_separation':True,
   'max_permanent_set_mm':0.20,
   'max_bore_growth_mm':0.10,
   'max_stiffness_loss_percent':10.0,
   'proof_1_5x_required_without_failure':True
 },
 'safety':['use rigid shielding and stand clear of line-of-fire at >=0.9 kN load','do not use a human-held luggage scale as the reaction structure','compression tests require a short guided proof pin to avoid rod buckling','stop immediately on cracking, progressive displacement, fixture slip or load-cell instability'],
 'gates':{'fixture_CAD_complete':False,'material_system_selected':False,'coupon_material_allowable_verified':False,'front_proof_passed':False,'rear_proof_passed':False,'production_process_repeatability_verified':False,'mechanical_detail_release':False,'print_release':False,'flight_release':False}
}
(root/'analysis/center_wingbox_proof_plan_v107.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'front_proof_N':1.5*front,'rear_proof_N':1.5*rear,'front_proof_kgf':1.5*front/9.80665,'rear_proof_kgf':1.5*rear/9.80665},indent=2))