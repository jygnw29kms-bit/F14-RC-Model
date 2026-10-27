from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];caps=R/'migration/freecad/TAPERED_CAPS_UNFROZEN_FIT_TRIAL_ONLY.FCStd';void=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();build=json.loads((R/'analysis/v192_tapered_cap_loft_trial.json').read_text());assert sha(caps)==build['output_sha256'] and sha(void)==build['void_sha256']
out=R/'analysis/v192_tapered_caps_reopen_audit.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(caps));b=App.openDocument(str(void));rows=[]
try:
 objects=[o for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];vs=[o for o in b.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objects)==2 and len(vs)==1;c=vs[0].Shape
 for o in objects:
  s=o.Shape;assert s.isValid() and len(s.Solids)==1;side='lower' if 'LOWER' in o.Name else 'upper';prev=next(r for r in build['rows'] if r['side']==side);assert abs(s.Volume-prev['volume_mm3'])<1e-7
  stage('containment_start',object=o.Name);outside=s.cut(c).Volume;stage('distance_start',object=o.Name);gap,pts,info=s.Shells[0].distToShape(c.Shells[0]);assert outside<=1e-6 and abs(gap-prev['minimum_void_boundary_gap_mm'])<1e-8
  rows.append({'object':o.Name,'valid':True,'solids':1,'volume_mm3':s.Volume,'outside_void_volume_mm3':outside,'minimum_void_boundary_gap_mm':gap,'gap_matches_presave_within_1e_8_mm':True})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert sha(caps)==build['output_sha256'] and sha(void)==build['void_sha256']
out.write_text(json.dumps({'status':'SAVED_CAPS_REOPENED_VALID_AND_CONTAINED','caps_sha256':sha(caps),'void_sha256':sha(void),'rows':rows,'limits':['Reopen and packaging verification only; no structural acceptance or normal clearance requirement frozen','No web, root connection, material, bond, buckling or physical proof'],'print_release':False,'flight_release':False},indent=2)+'\n');stage('complete');print(json.dumps(rows))
