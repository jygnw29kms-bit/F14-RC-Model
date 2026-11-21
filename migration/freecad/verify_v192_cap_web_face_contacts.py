from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/CAP_WEB_UNFROZEN_TRIAL_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(src);build=json.loads((R/'analysis/v192_cap_shear_web_trial.json').read_text());assert before==build['output_sha256']
out=R/'analysis/v192_cap_web_face_contact_audit.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as f:f.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
d=App.openDocument(str(src));contacts=[]
try:
 objs=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==3
 for o in objs:assert o.Shape.isValid() and len(o.Shape.Solids)==1
 web=d.getObject('UNFROZEN_WEB_0p8').Shape
 for capname in ('UNFROZEN_LOWER_CAP','UNFROZEN_UPPER_CAP'):
  cap=d.getObject(capname).Shape;rows=[];stage('face_pairs_start',cap=capname)
  for i,f in enumerate(web.Faces):
   if f.BoundBox.YLength<1:continue
   for j,g in enumerate(cap.Faces):
    if g.BoundBox.YLength<1:continue
    if min(f.BoundBox.YMax,g.BoundBox.YMax)-max(f.BoundBox.YMin,g.BoundBox.YMin)<1:continue
    u,v=f.ParameterRange[:2];v0,v1=f.ParameterRange[2:];n=f.normalAt((u+v)/2,(v0+v1)/2)
    u,v=g.ParameterRange[:2];v0,v1=g.ParameterRange[2:];m=g.normalAt((u+v)/2,(v0+v1)/2)
    if abs(n.dot(m))<.999999:continue
    dist=f.distToShape(g)[0]
    if dist>1e-7:continue
    common=f.common(g)
    if common.Area>1e-8:rows.append({'web_face_index':i,'cap_face_index':j,'distance_mm':dist,'common_area_mm2':common.Area,'common_faces':len(common.Faces),'web_face_y_interval_mm':[f.BoundBox.YMin,f.BoundBox.YMax]})
  contacts.append({'cap':capname,'positive_area_face_pairs':rows,'total_common_face_area_mm2':sum(r['common_area_mm2'] for r in rows)})
finally:App.closeDocument(d.Name)
assert sha(src)==before
r={'status':'SAVED_THREE_BODY_REOPEN_AND_FACE_LEVEL_CONTACT_AUDIT','source_sha256':before,'reopened_valid_single_solids':3,'contacts':contacts,'limits':['Only geometric face coincidence, no adhesive film, surface preparation, bond strength or shear-transfer proof','Normals filtered parallel within 1e-6; positive face common areas reported explicitly','Solid common returned no faces in earlier study; this audit uses individual face intersections','No structural, material, buckling, root connection or manufacturing release'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(contacts))
