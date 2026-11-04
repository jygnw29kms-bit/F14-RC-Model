from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
R=Path(__file__).resolve().parents[2];names=['WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd','Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps]
out=R/'analysis/v192_short_sleeve_root_skin_path_bounds.json';assert not out.exists()
def bounds(s):
 b=Bnd_Box();brepbndlib.AddOptimal(Part.__toPythonOCC__(s),b,False,True);return b.Get()
D=A.openDocument(str(ps[0]));sh=[o.Shape.copy() for o in D.Objects];A.closeDocument(D.Name)
tip=next(s for s in sh if min(v.Point.y for v in s.Vertexes)>299.999);root=next(s for s in sh if min(v.Point.y for v in s.Vertexes)<299)
# Finite boxes contain the full bounded input geometry on the respective side.
low=Part.makeBox(4000,1300,4000,A.Vector(-1000,-1000,-1000));high=Part.makeBox(4000,1000,4000,A.Vector(-1000,300,-1000))
rv=root.cut(low).Volume;tv=tip.cut(high).Volume;overlap=tip.common(root).Volume
rows=[{'moving':'TIP_SKIN','fixed':'ROOT_SKIN','method':'opposite_Y300_halfspace_volume_containment_for_nonnegative_Y_translation','root_outside_Y_le300_mm3':rv,'tip_outside_Y_ge300_mm3':tv,'initial_common_mm3':overlap,'covered':max(abs(rv),abs(tv),abs(overlap))<1e-7}]
rb=bounds(root);D=A.openDocument(str(ps[1]))
for n in ['TIP_CARRIER','TIP_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_1']:
 s=D.getObject(n).Shape;gap=bounds(s)[1]-rb[4];rows.append({'moving':n,'fixed':'ROOT_SKIN','method':'optimal_Y_bounds_separated_for_nonnegative_translation','gap_lower_bound_mm':gap,'covered':gap>1e-6})
A.closeDocument(D.Name);assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'FOUR_ROOT_SKIN_PAIR_BOUNDS_MEASURED','translation_global_y_mm':[0,5],'input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'all_pairs_covered':all(t['covered'] for t in rows),'limits':['Native numeric volume/tolerance assumptions; boundary contact allowed','Only four moving tip objects versus root skin; not rest of aircraft','No adhesive process, strength, physical assembly or print acceptance; partition volume gate blocked'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows,flush=True)
