from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/NASA_20DEG_EIGHT_SECTION_OUTBOARD_R2_REFERENCE_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/original_front_sources/NASA_outboard_r2_native_edge_samples.json';assert not out.exists();d=A.openDocument(str(p))
try:
 s=d.Objects[0].Shape;assert s.isValid();edges=[[[v.x,v.y,v.z] for v in e.discretize(Number=5)] for e in s.Edges]
finally:A.closeDocument(d.Name)
assert hashlib.sha256(p.read_bytes()).hexdigest()==h;out.write_text(json.dumps({'source_sha256_unchanged':h,'edges':edges,'limits':'Native edge sampling only; not CAD screenshot or surface clearance/OML acceptance'},indent=2)+'\n');print(len(edges))
