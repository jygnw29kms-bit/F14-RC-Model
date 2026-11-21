from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];paths=[R/'analysis/v192_cap_width_inner_envelope.json',R/'analysis/v192_root_bending_envelope.json',R/'analysis/v192_cap_web_face_contact_audit.json'];basis,loads,contacts=[json.loads(p.read_text()) for p in paths]
assert all(c['total_common_face_area_mm2']>0 for c in contacts['contacts'])
rows=[]
for r in basis['rows']:
 width=r['cap_width_mm'];t=r['assumed_cap_thickness_mm'];h=r['cap_centroid_separation_mm'];I=2*(width*t**3/12+width*t*(h/2)**2);outer=(h+t)/2;Z=I/outer;Q=width*t*h/2
 cases=[]
 for c in loads['cases']:
  F=c['assigned_side_vertical_force_N'];M=F*(loads['reference_y_mm']['wing_tip']-r['y_mm']);q=F*Q/I
  cases.append({'assumed_mass_kg':c['assumed_mass_kg'],'load_factor':c['load_factor'],'side_fraction':c['assigned_side_lift_fraction'],'tip_concentrated_force_N':F,'local_bending_moment_Nmm':M,'cap_only_nominal_outer_fibre_stress_MPa':M/Z,'ideal_cap_web_shear_flow_N_per_mm':q,'nominal_interface_shear_for_0p8mm_contact_width_MPa':q/.8})
 rows.append({'y_mm':r['y_mm'],'cap_width_mm':width,'cap_thickness_mm':t,'cap_centroid_separation_mm':h,'I_two_caps_only_mm4':I,'cap_only_section_modulus_mm3':Z,'Q_one_cap_mm3':Q,'cases':cases})
out={'status':'GEOMETRY_BASED_IDEAL_TAPERED_CAP_LOAD_DEMANDS_NO_STRENGTH_ACCEPTANCE','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'assumptions':['Same nonnegative lift envelope as earlier screen; all assigned side force at Y450 for simultaneous conservative local shear and bending','Two identical caps, 1mm vertical thickness, measured candidate centroid separation; web axial stiffness excluded','Elementary straight beam M/Z and VQ/I applied locally; swept/curved centerline, anisotropy, joint stress concentrations and finite bond length effects excluded','Geometric contact width0.8mm from trial web; no adhesive selected or qualified'],'rows':rows,'limits':['40 idealized station/load combinations; no finite element or aero simulation','Shear flow and nominal interface shear are sizing demands, not bond allowable or proof','No material modulus/strength, FOS, buckling, torsion, fatigue, peel, root transfer or manufacturing release','Candidate exists only Y185..435; root bridge and outer tip load transfer absent'],'print_release':False,'flight_release':False}
p=R/'analysis/v192_tapered_cap_section_demand_screen.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n')
for r in rows:print(r['y_mm'],max(c['cap_only_nominal_outer_fibre_stress_MPa'] for c in r['cases']),max(c['nominal_interface_shear_for_0p8mm_contact_width_MPa'] for c in r['cases']))
