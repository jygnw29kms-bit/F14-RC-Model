from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(src);build=json.loads((R/'analysis/v192_fullspan_spar_reference_build.json').read_text());assert before==build['output_sha256']
out=R/'analysis/v192_inboard_extended_bond_contact_audit.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as f:f.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
def normal(f):
 u,v,s,t=f.ParameterRange;return f.normalAt((u+v)/2,(s+t)/2)
d=App.openDocument(str(src));contacts=[]
try:
 objs=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==5
 for o in objs:assert o.Shape.isValid() and len(o.Shape.Solids)==1
 for side in ('LOWER','UPPER'):
  bond=d.getObject('GEOMETRIC_'+side+'_BOND_0p1').Shape
  for target in ('CONTINUOUS_'+side+'_CAP_REFERENCE','UNFROZEN_FLANGED_WEB'):
   other=d.getObject(target).Shape;rows=[];stage('face_pairs',side=side,target=target)
   for i,f in enumerate(bond.Faces):
    if f.BoundBox.YLength<1:continue
    for j,g in enumerate(other.Faces):
     if g.BoundBox.YLength<1 or min(f.BoundBox.YMax,g.BoundBox.YMax)-max(f.BoundBox.YMin,g.BoundBox.YMin)<1:continue
     if abs(normal(f).dot(normal(g)))<.999999:continue
     dist=f.distToShape(g)[0]
     if dist>1e-7:continue
     c=f.common(g)
     if c.Area>1e-8:rows.append({'bond_face_index':i,'target_face_index':j,'common_area_mm2':c.Area,'common_faces':len(c.Faces),'y_interval_mm':[f.BoundBox.YMin,f.BoundBox.YMax]})
   contacts.append({'bond_side':side,'target':target,'face_pairs':rows,'total_common_face_area_mm2':sum(r['common_area_mm2'] for r in rows),'solid_distance_mm':bond.distToShape(other)[0],'solid_overlap_volume_mm3':bond.common(other).Volume})
finally:App.closeDocument(d.Name)
assert sha(src)==before
r={'status':'SAVED_Y149_435_FIVE_BODY_REOPEN_AND_BOND_INTERFACE_GEOMETRY_ONLY','source_sha256':before,'valid_single_solids_reopened':5,'contacts':contacts,'limits':['Geometric bond-layer faces only, no adhesive strength, surface preparation, cure or physical proof','0.1mm vertical thickness is not constant normal film thickness','No shear transfer, peel, flange bending, buckling, material, root or print release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print([(c['bond_side'],c['target'],len(c['face_pairs']),c['total_common_face_area_mm2']) for c in contacts])
