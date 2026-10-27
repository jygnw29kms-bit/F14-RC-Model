from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];paths=[R/'analysis/v192_tapered_cap_section_demand_screen.json',R/'analysis/v192_flanged_web_bondline_trial.json',R/'analysis/v192_flanged_bond_face_contact_audit.json'];old,geom,face=[json.loads(p.read_text()) for p in paths]
width=geom['dimensions_mm']['flange_width'];assert width==4 and len(face['contacts'])==4 and all(len(c['face_pairs'])==4 for c in face['contacts'])
rows=[]
for r in old['rows']:
 cases=[]
 for c in r['cases']:
  q=c['ideal_cap_web_shear_flow_N_per_mm'];previous=c['nominal_interface_shear_for_0p8mm_contact_width_MPa'];new=q/width;assert abs(previous/new-5)<1e-12
  cases.append({'assumed_mass_kg':c['assumed_mass_kg'],'load_factor':c['load_factor'],'side_fraction':c['side_fraction'],'cap_only_nominal_outer_fibre_stress_MPa':c['cap_only_nominal_outer_fibre_stress_MPa'],'ideal_cap_web_shear_flow_N_per_mm':q,'nominal_bond_shear_for_4mm_width_MPa':new,'previous_nominal_bond_shear_for_0p8mm_width_MPa':previous})
 rows.append({'y_mm':r['y_mm'],'cases':cases})
r={'status':'UPDATED_NOMINAL_BOND_WIDTH_DEMAND_ONLY_NOT_FLANGED_SECTION_ANALYSIS','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'contact_width_mm':width,'nominal_shear_reduction_factor_from_width_only':5,'rows':rows,'assumptions':['Reuses earlier ideal cap-only M/Z and VQ/I tip-concentrated-load demands','Only uniform nominal interface shear denominator changes from0.8to4mm; no peak stress reduction asserted','New flange/core/bond stiffness is not included; web-to-flange corner still transfers shear and needs local analysis'],'limits':['Not a complete flanged composite section calculation or laminate analysis','No adhesive allowable, peel, shear lag, flange bending, corner concentration, buckling, cure or proof test','No safety factor or structural pass/fail','Outermost Y435 sizing station is not physical spar tip load-transfer validation'],'print_release':False,'flight_release':False}
p=R/'analysis/v192_flanged_bond_load_demand_update.json';assert not p.exists();p.write_text(json.dumps(r,indent=2)+'\n')
print('40 width-only comparisons; max nominal4mm interface MPa',max(c['nominal_bond_shear_for_4mm_width_MPa'] for r in rows for c in r['cases']))
