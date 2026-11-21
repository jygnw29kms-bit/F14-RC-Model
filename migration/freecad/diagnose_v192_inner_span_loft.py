from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(src.read_bytes()).hexdigest();out=R/'analysis/v192_inner_span_loft_diagnostic.json';assert not out.exists();d=App.openDocument(str(src));r=dict(status='INNER_SPAN_LOFT_DIAGNOSTIC_ONLY',source_sha256=before,stations=[],print_release=False,flight_release=False)
try:
 wing=d.getObject('WING_R').Shape;wires=[]
 for y in (180,220):
  row=dict(y_mm=y);section=wing.slice(App.Vector(0,1,0),y);row['section_wires']=len(section)
  if len(section)!=1:raise RuntimeError('section wire count '+str(len(section)))
  row.update(source_edges=len(section[0].Edges),source_closed=section[0].isClosed(),source_valid=section[0].isValid())
  off=section[0].makeOffset2D(-.43,0,False,False,False);row.update(offset_valid=off.isValid(),offset_wires=len(off.Wires),offset_edges=len(off.Edges))
  if len(off.Wires)!=1:raise RuntimeError('offset wire count '+str(len(off.Wires)))
  w=off.Wires[0];row.update(offset_closed=w.isClosed(),offset_face_valid=Part.Face(w).isValid());wires.append(w);r['stations'].append(row)
 loft=Part.makeLoft(wires,True,True);r.update(loft_valid=loft.isValid(),loft_solids=len(loft.Solids),loft_faces=len(loft.Faces),loft_volume_mm3=loft.Volume)
 if r['loft_valid'] and r['loft_solids']==1:
  outer=wing.slice(App.Vector(0,1,0),200);inner=loft.slice(App.Vector(0,1,0),200);r.update(midpoint_outer_wires=len(outer),midpoint_inner_wires=len(inner))
except Exception as err:r['error_type']=type(err).__name__;r['error']=str(err)
finally:App.closeDocument(d.Name)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before;r['limits']=['Diagnostic only; no shell/containment/normal-thickness verification.','No automatic geometry repair or vertex reordering performed; master unchanged.'];out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
