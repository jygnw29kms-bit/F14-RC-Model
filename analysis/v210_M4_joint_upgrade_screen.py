import json,math
from pathlib import Path
src=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v210_A80BHSF_full_stall_mechanism_screen.json").read_text())
F=src['loads']['worst']['dynamic_per_side_N']
pin_d=4.0; hole=4.2
shear=F/(math.pi*pin_d**2/4)
rod_ax=F/(math.pi*4**2/4)
crank_net=F/((14-hole)*5)
crank_bear=F/(pin_d*5)
yoke_bear=F/(pin_d*8)
# 7075 T6 conservative proof stress based on >=460 MPa thin plate / bars typical minimum range, not fatigue release
peak=src['stress_existing_v208']['yoke_neck_1p5x_MPa']; proof=460.;sf=proof/peak
res={'status':'V210_M4_JOINT_AND_7075_YOKE_SCREEN','load_N_per_side_dynamic':F,'joint':{'pin_d_mm':pin_d,'clearance_hole_mm':hole,'pin_single_shear_MPa':shear,'4mm_rod_axial_MPa':rod_ax,'crank_net_section_MPa':crank_net,'crank_bearing_MPa':crank_bear,'yoke_bearing_MPa':yoke_bear},'yoke_7075T6':{'thickness_mm':8,'neck_width_mm':10,'peak_screen_MPa':peak,'conservative_reference_proof_MPa':proof,'screen_SF':sf},'decision':{'upgrade_loaded_crank_yoke_pins_to_M4':True,'retain_4mm_rods':True,'yoke_material_candidate':'EN AW-7075-T6/T651 machined plate/bar','FDM_yoke_rejected':True},'gates':{'exact_stock_cert_verified':False,'fatigue_verified':False,'fastener_grade_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v210_M4_joint_upgrade_screen.json").write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
