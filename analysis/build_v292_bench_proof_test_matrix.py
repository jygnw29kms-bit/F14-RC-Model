import json, pathlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
v282=json.load(open(R/'migration/freecad/freecad_v282_three_8x6_wing_joiner_endmodel_audit.json',encoding='utf-8'))
v284=json.load(open(R/'migration/freecad/freecad_v284_light_stabilator_root_fitting_fixed_audit.json',encoding='utf-8'))
v287=json.load(open(R/'migration/freecad/freecad_v287_captive_m3_segment_clamps_audit.json',encoding='utf-8'))
per_tube=v282['load_screen']['seam_moment_per_tube_Nm']; total=per_tube*3
# Proof policies are engineering test factors, not material allowables.
rows=[
 {'test':'WING_JOINER_ASSEMBLY','design_basis':'v282 three 8x6 joiners per wing','design_load':{'seam_moment_Nm':total},'proof_target':{'factor':1.5,'seam_moment_Nm':total*1.5},'pass':['no visible cracking, tube slip or sleeve debond','permanent tip/set after unload <=0.5 mm at measurement point','no clamp/key damage'],'status':'OPEN'},
 {'test':'TAIL_ROOT_FITTING_TORSION','design_basis':'existing severe taileron chain screen / light v284 fitting','design_load':{'torque_Nm':0.67},'proof_target':{'factor':2.0,'torque_Nm':1.34},'pass':['no D-bore slip','no bond-line crack or frame delamination','angular backlash increase <=0.25 deg after unload'],'status':'OPEN'},
 {'test':'SEGMENT_C_RING_CLAMP','design_basis':'v287 captive M3 C-ring retention','proof_target':{'axial_pull_N':100,'cycles':25},'pass':['no rider sleeve axial slip >0.2 mm','no nut-pocket rotation or cracking','M3 fastener remains removable after cycling'],'note':'100 N is a retention/service proof target, not a claimed flight load derived from aero model','status':'OPEN'},
 {'test':'EDF_ADAPTER_RING','design_basis':'v291 split adapter ring family','proof_target':{'thermal_cycles':3,'temperature_range_C':[20,70],'axial_pull_N':50},'pass':['no shroud crushing/ovalisation','no adapter crack or creep preventing removal','measured OD unchanged within 0.1 mm after cycle'],'note':'final temperature target to be checked against actual measured EDF/ESC bay temperature','status':'OPEN'},
]
out={'status':'V292_BENCH_PROOF_TEST_MATRIX','candidate':'v288 + v290/v291 manufacturing gates','rows':rows,'gates':{'all_tests_defined':True,'all_tests_passed':False,'print_release':False,'flight_release':False}}
(R/'analysis/v292_bench_proof_test_matrix.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
md=['# F-14 v292 Bench / Proof Test Matrix','', '> Engineering test plan. These targets do not replace purchased-material certificates or flight test.', '']
for q in rows:
 md += [f"## {q['test']}",f"- Basis: {q['design_basis']}",f"- Proof target: `{json.dumps(q['proof_target'])}`",'- Pass:']+[f"  - {x}" for x in q['pass']]
 if q.get('note'): md += [f"- Note: {q['note']}"]
 md += ['']
(R/'manufacturing/V292_BENCH_PROOF_TEST_MATRIX.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps(out,indent=2))
