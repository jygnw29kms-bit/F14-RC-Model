from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];paths=[R/'analysis/v192_root_bending_envelope.json',R/'analysis/v192_straight_spar_packaging_trial.json',R/'docs/09_ENGINEERING_AUDIT_20261004.md'];loads=json.loads(paths[0].read_text());fit=json.loads(paths[1].read_text());assert loads['current_cad_sha256']==fit['source_sha256']
sections=[]
for outer,inner,label in [(4,0,'4mm solid circle packaging envelope'),(4,2,'4x2mm hollow circle hypothetical'),(4,3,'4x3mm hollow circle hypothetical')]:
 I=math.pi*(outer**4-inner**4)/64;Z=I/(outer/2)
 cases=[]
 for c in loads['cases']:
  cases.append({'mass_kg':c['assumed_mass_kg'],'load_factor':c['load_factor'],'side_fraction':c['assigned_side_lift_fraction'],'root_moment_upper_bound_Nm':c['conditional_root_section_bending_upper_bound_Nm'],'conditional_nominal_outer_fibre_stress_upper_bound_MPa':c['conditional_root_section_bending_upper_bound_Nm']*1000/Z})
 sections.append({'label':label,'outer_diameter_mm':outer,'inner_diameter_mm':inner,'I_mm4':I,'section_modulus_mm3':Z,'cases':cases})
r={'status':'CONDITIONAL_SECTION_DEMAND_SCREEN_NO_MATERIAL_ACCEPTANCE','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'formulae':['I=pi*(D^4-d^4)/64','Z=I/(D/2)','sigma_nominal=M/Z; M from conditional nonnegative lift upper bound'], 'sections':sections,'finding':'Geometric fit of a 4mm cylinder does not establish a viable primary spar. Nominal elastic stress demand must be checked against selected orthotropic hardware and a justified load model; no allowable is supplied here.','limits':['Circular section ideal beam model only; composite tube layup, shear, ovalization, local buckling, joints and defects excluded','No material strength, elastic modulus, safety factor or pass/fail inferred','Uses root-section moment upper bound; earlier pivot moment also requires separate root bridge','Historical 16x1mm carbon caps are a separate unfrozen topology, not replaced by this fit trial','Fit trial starts Y155 while root bound is at Y148.826; root transfer remains absent'],'mechanical_release':False,'print_release':False,'flight_release':False}
out=R/'analysis/v192_spar_section_demand_screen.json';assert not out.exists();out.write_text(json.dumps(r,indent=2)+'\n')
for s in sections:print(s['label'], 'Z',s['section_modulus_mm3'],'max conditional MPa',max(c['conditional_nominal_outer_fibre_stress_upper_bound_MPa'] for c in s['cases']))
