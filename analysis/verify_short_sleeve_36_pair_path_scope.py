from pathlib import Path
import json,hashlib,itertools
R=Path(__file__).resolve().parents[1]
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports={}
def read(n):
 p=R/'analysis'/n;d=json.loads(p.read_text());reports[n]=H(p);return d
poses=read('v192_short_sleeve_tip_subassembly_poses.json')
a=read('v192_short_sleeve_auxiliary_optimal_bounds.json')
b=read('v192_short_sleeve_tip_skin_local_bounds.json')
c=read('v192_tip_skin_spar_continuous_clearance_resumed.json')
v=read('v192_tip_skin_spar_interval_coverage_verification.json')
assert v['input_report_sha256']==reports['v192_tip_skin_spar_continuous_clearance_resumed.json']
inputs={}
for d in [poses,a,b,c]:
 for n,h in d['input_sha256_unchanged'].items():
  assert n not in inputs or inputs[n]==h
  assert H(R/'migration/freecad'/n)==h
  inputs[n]=h
assert a['translation_range_mm']==b['translation_range_mm']==c['translation_range_y_mm']==[0,5]
assert not c['pending_intervals']
intervals=sorted(c['covered_intervals']);assert intervals[0][0]==0 and intervals[-1][1]==5
assert all(x[1]==y[0] for x,y in zip(intervals,intervals[1:]))
covered=[s for s in c['samples'] if s['covered']]
assert sorted(s['interval'] for s in covered)==intervals
for s in covered:
 lo,hi=s['interval'];assert s['mid_translation_mm']==(lo+hi)/2
 assert s['lipschitz_radius_mm']==(hi-lo)/2
 assert s['native_distance_mm']-(hi-lo)/2>c['native_distance_margin_mm']
fixed=poses['fixed_objects'];moving=poses['moving_objects'];pairs={}
def add(m,f,method):
 if f=='SLEEVE':f='GENERIC_4OD_2p2ID_SLEEVE'
 assert (m,f) not in pairs;pairs[m,f]=method
for row in a['rows']:
 for t in row['tests']:
  assert t['covered']
  if t['method']=='disjointY':assert t['gap_lower_bound_mm']>1e-6
  elif t['method']=='optimalGeometryBoundsDisjointXWithinSweptYSlab':assert t['x_gap_lower_bound_mm']>1e-6
  elif t['method']=='radial_exclusion_invariant_underYtranslation':assert abs(t['overlap_long_radius2_cylinder_mm3'])<1e-7
  else:assert t['method']=='noSolidInSweptYSlab'
  add(row['moving'],t['fixed'],t['method'])
for t in b['rows']:
 assert t['covered']
 if 'gap_lower_bound_mm' in t:assert t['gap_lower_bound_mm']>1e-6
 else:assert abs(t['tip_overlap_cylinder_mm3'])<1e-7 and abs(t['sleeve_outside_cylinder_mm3'])<1e-7
 add('TIP_SKIN',t['fixed'],t['method'])
# The short sleeve containment in radius2 is measured by report b; same CAD hash
# supplies the fixed sleeve used for all three auxiliary radial exclusions.
for f in c['input_sha256_unchanged']:
 if f.startswith('FULLSPAN'):spar_file=f
spar_names=[f for f in fixed if f not in [t['fixed'] for t in b['rows']]]
assert len(spar_names)==5
for f in spar_names:add('TIP_SKIN',f,'midpoint_distance_1_Lipschitz_vs_compound_of_all_spar_objects')
assert set(pairs)==set(itertools.product(moving,fixed)) and len(pairs)==36
out=R/'analysis/v192_short_sleeve_36_pair_path_scope_verification.json';assert not out.exists()
out.write_text(json.dumps({'status':'DECLARED_36_PAIR_RIGID_PATH_SCOPE_AND_HASH_LINKS_VERIFIED','translation_global_y_mm':[0,5],'input_cad_sha256':inputs,'evidence_report_sha256':reports,'moving_objects':moving,'fixed_objects':fixed,'pair_count':len(pairs),'pairs':[{'moving':m,'fixed':f,'method':method} for (m,f),method in sorted(pairs.items())],'limits':['Report consistency and numerical bounds verified; not independent reexecution of every CAD operation','Only listed objects: root wing skin, rest of aircraft, tools and access are outside this scope','Rigid adhesive placeholders; contact allowed by zero-volume screens; no physical assembly process acceptance','No material, strength, tolerance, cure or flight validation; short sleeve bond area reduced 61.2 percent and unqualified','Source partition volume gate remains blocked; no master promotion'],'print_release':False,'flight_release':False},indent=2)+'\n')
print('Verified unique complete declared Cartesian scope:',len(pairs),'pairs')
