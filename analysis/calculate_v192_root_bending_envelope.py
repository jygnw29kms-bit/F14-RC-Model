from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
paths=[R/'analysis/v192_root_loadpath_preparation.json',R/'analysis/v192_canted_sweep_reference_build.json']
a,b=[json.loads(p.read_text()) for p in paths]
assert a['current_cad_sha256']==b['source_sha256']
pivot=125.20927023775282
bounds=next(r['bounds_mm']['Y'] for r in b['rows'] if r['side']=='R' and r['nominal_label_deg']==20)
root,tip=bounds;assert pivot<root<tip
cases=[]
for c in a['reaction_screen']['cases']:
 F=c['assigned_side_vertical_force_N']
 cases.append({**c,'conditional_root_section_bending_upper_bound_Nm':F*(tip-root)/1000,'conditional_pivot_bending_upper_bound_Nm':F*(tip-pivot)/1000,'ideal_couple_force_from_moment_upper_bound_N_at_assumed_16mm':F*(tip-pivot)/16})
out={'status':'CONDITIONAL_STATIC_POSITIVE_LIFT_LOAD_ENVELOPE_NOT_STRESS_ANALYSIS','inputs_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'current_cad_sha256':b['source_sha256'],'reference_y_mm':{'pivot':pivot,'wing_root':root,'wing_tip':tip},'assumptions':['All assigned vertical lift is nonnegative and acts between root and tip at baseline20 pose','Tip-concentrated force bounds first moment for that nonnegative load; not measured or simulated lift distribution','16mm couple separation is historical unfrozen concept height, not verified contact-center spacing; no shaft or bearing sizing release'],'formulae':['M_root_upper=F*(Ytip-Yroot)','M_pivot_upper=F*(Ytip-Ypivot)','Ideal pure couple member force=M_pivot/h, h=16mm; shear superposition not included'],'cases':cases,'limits':['Does not bound loads with signed span distribution, dynamic impacts, torsion, maneuver asymmetry beyond selected cases, drag or inertial relief','Not material stress, buckling, fatigue, joint strength, FOS, hardware acceptance or proof test','Pivot Z and actual load-transfer contact geometry unresolved','No CAD modification or production release'],'print_release':False,'flight_release':False}
assert len(cases)==8
for c in cases:
 assert abs(c['conditional_pivot_bending_upper_bound_Nm']-c['conditional_root_section_bending_upper_bound_Nm']-c['additional_pivot_moment_from_reference_root_gap_Nm'])<1e-10
outpath=R/'analysis/v192_root_bending_envelope.json';assert not outpath.exists();outpath.write_text(json.dumps(out,indent=2)+'\n')
print('8 cases; maximum pivot moment Nm:',max(c['conditional_pivot_bending_upper_bound_Nm'] for c in cases))
print('Maximum ideal couple member force at assumed16mm N:',max(c['ideal_couple_force_from_moment_upper_bound_N_at_assumed_16mm'] for c in cases))
