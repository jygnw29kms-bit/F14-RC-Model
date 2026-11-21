from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=[R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd',R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd',R/'analysis/v192_cap_width_inner_envelope.json'];inputs={str(p):sha(p) for p in paths};out=R/'analysis/v192_socket_continuous_insertion_audit.json';assert not out.exists();a=App.openDocument(str(paths[0]));b=App.openDocument(str(paths[1]));rows=[]
def joined(shapes):
 s=shapes[0]
 for t in shapes[1:]:s=s.fuse(t)
 print('joined',s.isValid(),len(s.Solids),flush=True);assert s.isValid() and len(s.Solids)==1;return s
try:
 socket=next(o.Shape for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull());print('socket ymax',socket.BoundBox.YMax,flush=True);assert socket.BoundBox.YMax<185-1e-6
 cap=b.getObject('CONTINUOUS_LOWER_CAP_REFERENCE').Shape;rf=next(f for f in cap.Faces if abs(f.BoundBox.YMin-149)<1e-7 and f.BoundBox.YLength<1e-7);x0=(rf.BoundBox.XMin+rf.BoundBox.XMax)/2;x185=json.loads(paths[2].read_text())['rows'][0]['x_center_mm'];slope=(x185-x0)/36
 clip=Part.makeBox(2000,36,2000,App.Vector(-1000,149,-1000))
 for o in b.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull():continue
  print('object',o.Name,flush=True);shape=o.Shape;rootfaces=[f for f in shape.Faces if abs(f.BoundBox.YMin-149)<1e-7 and f.BoundBox.YLength<1e-7];assert rootfaces
  initial=joined([f.extrude(App.Vector(slope*36,36,0)) for f in rootfaces]);actual=shape.common(clip);diff=initial.cut(actual).Volume+actual.cut(initial).Volume;assert diff<=1e-6, str(diff)
  # Exact translation sweep for this prismatic segment: 36mm segment +26mm travel.
  swept=joined([f.extrude(App.Vector(slope*62,62,0)) for f in rootfaces]);overlap=swept.common(socket).Volume
  rows.append({'object':o.Name,'root_face_count':len(rootfaces),'inboard_segment_symmetric_difference_volume_mm3':diff,'swept_envelope_valid':swept.isValid(),'swept_envelope_volume_mm3':swept.Volume,'socket_swept_overlap_volume_mm3':overlap})
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items()) and len(rows)==5
r={'status':'CONTINUOUS_IDEAL_TRANSLATION_SOCKET_OVERLAP_CHECK','input_sha256':inputs,'translation_y_interval_mm':[0,26],'inboard_prismatic_segment_y_interval_mm':[149,185],'swept_inboard_y_interval_mm':[149,211],'socket_y_max_mm':socket.BoundBox.YMax,'rows':rows,'all_swept_overlap_volumes_below_1e_6_mm3':all(r['socket_swept_overlap_volume_mm3']<=1e-6 for r in rows),'reasoning':['Saved Y149..185 segment independently matched to extruded root section by symmetric volume differences','Exact ideal translation sweep of that prismatic segment is root-face extrusion over36+26mm','Saved geometry atY>=185 stays beyond actual socket bounding Ymax, which is below185 for all nonnegative Y translations; cannot intersect socket','This establishes only no positive-volume socket collision for the ideal rigid translation model, within boolean tolerance'],'limits':['End-stop contact allowed; no positive clearance or insertion force claimed','No manufacturing tolerances, adhesive process, surrounding wing/body/access, bearing/shaft installation or physical proof','Original outside body/glove packaging still rejected; no production or flight acceptance'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows))
