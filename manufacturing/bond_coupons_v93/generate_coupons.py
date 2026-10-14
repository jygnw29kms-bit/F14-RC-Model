import json, pathlib, struct, math
ROOT=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
V92=ROOT/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v92_pointwise_bond_area_audit.json'
a=json.loads(V92.read_text())
req=float(a['required_average_shear_on_lower_bound_MPa'])
force=float(a['sf3_equivalent_force_N'])
area=15.0*10.0
coupon_force=req*area
kgf=coupon_force/9.80665
base_dynamic_torsion=747.3921304468803 # v81 worst-airfoil-edge x1.5 dynamic, before SF3
sf3_torsion=base_dynamic_torsion*3.0
flight_proof=base_dynamic_torsion*1.5
out={
 'status':'V93_PHYSICAL_BOND_QUALIFICATION_PLAN',
 'source_v92':str(V92),
 'model_requirement':{
   'conservative_usable_bond_area_mm2':a['conservative_usable_bond_area_mm2'],
   'sf3_equivalent_force_N':force,
   'required_average_bond_shear_MPa':req,
   'v81_dynamic_worst_torsion_Nmm':base_dynamic_torsion,
   'sacrificial_joint_sf3_torsion_Nmm':sf3_torsion,
   'flight_article_nondestructive_proof_torsion_Nmm':flight_proof,
 },
 'flat_coupon':{
   'bar_length_mm':70.0,'bar_width_mm':15.0,'bar_thickness_mm':2.4,
   'overlap_length_mm':10.0,'bond_area_mm2':area,
   'minimum_failure_load_N':coupon_force,'minimum_failure_load_kgf':kgf,
   'replicates_per_process_condition':5,
   'acceptance':['all 5 specimens >= minimum_failure_load_N','no adhesive-interface separation below the minimum load','coefficient of variation <= 20 percent; otherwise repeat/process-control review'],
 },
 'process_matrix':{
   'print_material':['actual flight-print material only; test PETG and ASA separately if both remain candidates'],
   'surface_preparation':['as-printed cleaned','lightly abraded + cleaned'],
   'adhesive':['each candidate adhesive/system tested as a separate process; do not pool results'],
   'bondline_mm':[0.15,0.20,0.25],
   'conditioning':['full manufacturer cure at room condition','warm-condition screen at 40 C after cure'],
 },
 'representative_joint':{
   'sacrificial_destructive_gate_Nm':sf3_torsion/1000.0,
   'flight_article_nondestructive_proof_Nm':flight_proof/1000.0,
   'requirements':['no slip, crack, whitening, bond separation or permanent set at proof load','sacrificial representative joint must survive SF3 torque before flight release','inspect carbon continuity before and after test'],
 },
 'gates':{'fit_coupon_verified':False,'adhesive_process_verified':False,'environmental_condition_verified':False,'representative_joint_torsion_verified':False,'flight_article_proof_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False}
}
(ROOT/'analysis/bond_qualification_v93.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

def stl_box(path, sx, sy, sz, name):
    x0,y0,z0=0.0,0.0,0.0; x1,y1,z1=sx,sy,sz
    v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    tris=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),(1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
    with open(path,'w',newline='\n') as f:
        f.write('solid '+name+'\n')
        for a,b,c in tris:
            f.write(' facet normal 0 0 0\n  outer loop\n')
            for i in (a,b,c): f.write('   vertex %.6f %.6f %.6f\n'%v[i])
            f.write('  endloop\n endfacet\n')
        f.write('endsolid '+name+'\n')

outdir=ROOT/'manufacturing/bond_coupons_v93'
stl_box(outdir/'F14_v93_lap_bar_70x15x2p4.stl',70,15,2.4,'F14_v93_lap_bar')
for gap in (0.15,0.20,0.25):
    tag=str(gap).replace('.','p')
    stl_box(outdir/f'F14_v93_optional_gap_shim_{tag}mm.stl',20,5,gap,f'F14_v93_gap_shim_{tag}')
print(json.dumps({'required_shear_MPa':req,'coupon_area_mm2':area,'coupon_min_load_N':coupon_force,'coupon_min_load_kgf':kgf,'joint_sf3_Nm':sf3_torsion/1000,'flight_proof_Nm':flight_proof/1000},indent=2))