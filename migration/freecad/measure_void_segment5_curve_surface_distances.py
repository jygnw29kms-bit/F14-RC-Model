from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepLib import BRepLib_CheckCurveOnSurface
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_void_segment5_curve_surface_distances.json';assert not out.exists();D=A.openDocument(str(p));s=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);lookup={}
for i,e in enumerate(s.Edges,1):lookup.setdefault(e.hashCode(),[]).append((i,e))
rows=[]
for fi,f in enumerate(s.Faces,1):
 face=topods.Face(Part.__toPythonOCC__(f))
 for e in f.Edges:
  ids=[i for i,g in lookup[e.hashCode()] if e.isSame(g)];assert len(ids)==1;edge=topods.Edge(Part.__toPythonOCC__(e));check=BRepLib_CheckCurveOnSurface(edge,face);check.Perform();done=check.IsDone();row={'face_one_based':fi,'edge_one_based':ids[0],'done':done,'error_status':check.ErrorStatus(),'stored_edge_tolerance_mm':BRep_Tool.Tolerance(edge)}
  if done:row.update(max_distance_mm=check.MaxDistance(),parameter_at_max=check.MaxParameter())
  rows.append(row)
assert H(p)==h;done=[r for r in rows if r['done'] and r['error_status']==0]
out.write_text(json.dumps({'status':'SEGMENT5_NATIVE_EDGE_FACE_MAX_DISTANCES_MEASURED','input_sha256_unchanged':h,'object':'VOID_TOOL_5','edge_count':len(s.Edges),'face_count':len(s.Faces),'pair_count':len(rows),'completed_pair_count':len(done),'max_distance_mm':max(r['max_distance_mm'] for r in done),'pairs_exceeding_stored_edge_tolerance':[r for r in done if r['max_distance_mm']>r['stored_edge_tolerance_mm']],'rows':rows,'limits':['Native numerical max-distance algorithm, not exact arithmetic or rigorous global bound','Curve/surface mismatch alone does not prove flux error cause or bound volume error','No changes to curves, SameParameter flags, geometry or tolerances; no release'],'print_release':False,'flight_release':False},indent=2)+'\n');print('pairs',len(rows),'completed',len(done),'max',max(r['max_distance_mm'] for r in done),'exceed',sum(r['max_distance_mm']>r['stored_edge_tolerance_mm'] for r in done),flush=True)
