from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];src=R/'analysis/v192_root_bending_envelope.json';d=json.loads(src.read_text());rows=[]
for i,c in enumerate(d['cases']):
 M=c['conditional_pivot_bending_upper_bound_Nm']*1000;F=c['assigned_side_vertical_force_N'];ax=F*math.cos(math.radians(1.5))
 for diameter in (6,8,10):
  area=math.pi*diameter**2/4;I=math.pi*diameter**4/64;Z=I/(diameter/2);sigma=M/Z;axial=ax/area
  assert abs(sigma*Z/1000-c['conditional_pivot_bending_upper_bound_Nm'])<1e-12
  assert abs(sigma-32*M/(math.pi*diameter**3))<1e-10
  rows.append({'case_index':i,'hypothetical_solid_shaft_diameter_mm':diameter,'area_mm2':area,'section_modulus_mm3':Z,'full_moment_nominal_bending_MPa':sigma,'nominal_axial_MPa':axial,'worst_outer_fiber_abs_normal_stress_MPa':sigma+axial})
out=R/'analysis/v192_pivot_shaft_nominal_demand_screen.json';assert not out.exists();out.write_text(json.dumps({'status':'CONDITIONAL_FULL_MOMENT_SECTION_DEMAND_NOT_SHAFT_DESIGN','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'model':'Ideal solid circular section, if that section transmits the full inherited pivot bending bound plus axial thrust','rows':rows,'maximum_bending_MPa_by_diameter':{str(n):max(r['full_moment_nominal_bending_MPa'] for r in rows if r['hypothetical_solid_shaft_diameter_mm']==n) for n in (6,8,10)},'limits':['Actual bearing/housing load path can change shaft moment; no real shaft section load verified','No material chosen or allowable compared; no factor of safety or pass/fail','No threads, crossholes, stress concentrations, torsion, contact, shear, fatigue, deflection or buckling included','6mm historical pin is unselected; larger diameters are studies not packaging approvals','No physical proof, structural print or flight release'],'hardware_selected':False,'flight_release':False},indent=2)+'\n');print('24 section cases verified',json.loads(out.read_text())['maximum_bending_MPa_by_diameter'])
