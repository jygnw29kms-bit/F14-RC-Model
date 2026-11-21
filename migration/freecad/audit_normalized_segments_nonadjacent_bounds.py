from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_NORMALIZED_SHARED_PROFILE_SEGMENTS_STUDY_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_normalized_segments_nonadjacent_bounds.json';assert not out.exists();D=A.openDocument(str(p));bounds=[]
for i in range(17):
 s=D.getObject('NORMALIZED_VOID_SEG_'+str(i)).Shape;b=Bnd_Box();brepbndlib.AddOptimal(Part.__toPythonOCC__(s),b,False,True);v=b.Get();bounds.append({'index':i,'optimal_y_bounds_mm':[v[1],v[4]]})
A.closeDocument(D.Name);rows=[]
for i in range(17):
 for j in range(i+2,17):
  a,b=bounds[i]['optimal_y_bounds_mm'];c,d=bounds[j]['optimal_y_bounds_mm'];gap=max(c-b,a-d);rows.append({'left_index':i,'right_index':j,'y_separation_lower_bound_mm':gap,'covered':gap>1e-6})
assert len(rows)==120 and H(p)==h
out.write_text(json.dumps({'status':'120_NONADJACENT_SEGMENT_Y_BOUNDS_MEASURED','input_sha256_unchanged':h,'bounds':bounds,'rows':rows,'all_nonadjacent_pairs_disjoint_by_Y':all(r['covered'] for r in rows),'limits':['Native optimal bounds include shape tolerances; not exact arithmetic certificate','Adjacent pairs handled by separate face/volume audit','No fusion, original-shape deviation or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print('120 pairs; min separation',min(r['y_separation_lower_bound_mm'] for r in rows))
