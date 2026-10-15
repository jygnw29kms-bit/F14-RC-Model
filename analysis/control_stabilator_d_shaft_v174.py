import json,math,pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v173=json.loads((root/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/controls_v173/F14_v173_stabilator_root_fitting_audit.json').read_text())
shaft_d=6.0; shaft_r=3.; flat_depth=.6; shaft_flat_x=shaft_r-flat_depth
bore_r=3.05; flat_clear=.05; bore_flat_x=shaft_flat_x+flat_clear
length=24.0
def chord(r,x):return 2*math.sqrt(max(0,r*r-x*x))
shaft_chord=chord(shaft_r,shaft_flat_x); bore_chord=chord(bore_r,bore_flat_x)
area=shaft_chord*length
proofT=.6701583801150008; designT=2*proofT
force=designT*1000/shaft_r
press=force/area
J=math.pi*shaft_d**4/32
solid_tau=designT*1000*shaft_r/J
stress_concentration_screen=1.5*solid_tau
result={'status':'V174_STABILATOR_D_SHAFT_TORQUE_TRANSFER_SCREEN','sources':['workspace/RC-F14-Tomcat/Fusion/Exports/Current/controls_v173/F14_v173_stabilator_root_fitting_audit.json','analysis/control_stabilator_pivot_shaft_v149.json'],'geometry':{'shaft_diameter_mm':shaft_d,'shaft_flat_depth_mm':flat_depth,'shaft_flat_plane_from_center_mm':shaft_flat_x,'bore_nominal_radius_mm':bore_r,'bore_flat_plane_from_center_mm':bore_flat_x,'radial_clearance_mm':bore_r-shaft_r,'flat_clearance_mm':bore_flat_x-shaft_flat_x,'effective_D_engagement_length_mm':length,'shaft_flat_chord_width_mm':shaft_chord,'bore_flat_chord_width_mm':bore_chord,'nominal_flat_contact_area_mm2':area},'load_screen':{'severe_surface_hinge_moment_Nm':proofT,'screen_design_moment_Nm_2x':designT,'equivalent_tangential_force_at_3mm_radius_N':force,'average_D_flat_bearing_pressure_MPa':press,'solid_6mm_shaft_nominal_torsional_shear_MPa_at_2x':solid_tau,'1p5x_stress_concentration_screen_MPa':stress_concentration_screen,'steel_500MPa_yield_screen_SF':500/stress_concentration_screen},'architecture':{'torque_transfer':'matching D-flat in local shaft region and root-fitting bore','shaft_bearing_regions':'remain round 6 mm for standard radial bearings','no_transverse_shaft_hole':True,'axial_retention':'separate shoulder/collar/end-fastener; not provided by D-flat','manufacturing':'flat may be machined/ground only after shaft and bearing hardware are selected; gauge before assembly'},'decision':{'D_flat_candidate_passes_preliminary_stress_and_bearing_screen':True,'transverse_cross_pin_rejected_for_baseline':True,'next_CAD_gate':'replace v173 round bore/reference shaft with matching D geometry and verify fitting remains valid'},'release':{'D_geometry_CAD_verified':False,'actual_shaft_material_verified':False,'axial_retention_designed':False,'root_fitting_proof_pass':False,'flight_release':False}}
(root/'analysis/control_stabilator_d_shaft_v174.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))