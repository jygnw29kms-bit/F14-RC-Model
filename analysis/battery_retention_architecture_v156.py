import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
mass_kg=0.240; g=9.81; accel_g=20; proof=mass_kg*g*accel_g; sf=2.0; design=proof*sf
pin_d=4.0; rail_t=4.0
pin_area_double=2*math.pi*pin_d**2/4
pin_shear=proof/pin_area_double
pin_shear_design=design/pin_area_double
rail_bearing_each=(proof/2)/(pin_d*rail_t)
rail_bearing_design=(design/2)/(pin_d*rail_t)
shoe_area=30*10
result={
 'status':'V156_BATTERY_RETENTION_ARCHITECTURE',
 'sources':['analysis/cg_battery_tray_v152.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v153/F14_v153_battery_tray_audit.json','workspace/RC-F14-Tomcat/Fusion/Exports/Current/cg_v155/F14_v155_battery_tray_structural_envelope_audit.json'],
 'loads':{'hard_pack_mass_g':240,'proof_acceleration_g':20,'retention_proof_force_N':proof,'hardware_sizing_factor':sf,'hardware_sizing_force_N':design},
 'architecture':{
   'fixed_tray':'two longitudinal side rails plus open/skeleton support floor',
   'usable_battery_center_travel_mm':70,
   'clear_battery_travel_envelope_mm':[176,38,27],
   'verified_structural_service_envelope_mm':[196,46,34],
   'vertical_lateral_restraint':'two independent approximately 15 mm hook-and-loop straps wrapped around the tray and pack; either strap alone must retain full proof load',
   'fore_aft_restraint':'two removable positive cross-pins, one ahead and one behind pack, indexed along rails; friction and connector not credited',
   'stop_interface':'compliant/wide stop shoe on each pin to avoid concentrated load on LiPo pouch',
   'undertray_strap_clearance_mm':2.0,
   'candidate_pin_diameter_mm':4.0,
   'candidate_rail_wall_thickness_mm':4.0,
   'candidate_index_pitch_mm':10.0,
   'candidate_stop_shoe_contact_mm':[30,10]
 },
 'screens':{
   '4mm_pin_double_shear_MPa_at_20g':pin_shear,
   '4mm_pin_double_shear_MPa_at_2x_sizing':pin_shear_design,
   'rail_hole_bearing_each_side_MPa_at_20g':rail_bearing_each,
   'rail_hole_bearing_each_side_MPa_at_2x_sizing':rail_bearing_design,
   'stop_shoe_average_pressure_MPa_at_20g':proof/shoe_area,
   'stop_shoe_average_pressure_MPa_at_2x_sizing':design/shoe_area
 },
 'rules':['battery connector carries no restraint load','tray anchors must terminate in internal frames/structure, never shell skin alone','no sharp printed edge contacts LiPo','all pin holes require adequate edge distance and are proof-tested in print orientation','battery dimensions and strap hardware remain unfrozen until measured'],
 'proof_gate':{'directions':['forward','aft','up','down','left','right'],'minimum_applied_force_N':round(proof,2),'maximum_pack_motion_mm':1.0,'repeat_cycles_each_direction':3,'visual_damage_allowed':False,'permanent_deformation_allowed':False,'single_strap_full_load_check_required':True,'pin_stop_full_load_check_required':True},
 'release':{'tray_CAD_designed':False,'internal_frame_anchors_designed':False,'strap_hardware_verified':False,'pin_material_verified':False,'retention_proof_pass':False,'print_release':False,'flight_release':False}
}
(root/'analysis/battery_retention_architecture_v156.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result['screens'],indent=2))