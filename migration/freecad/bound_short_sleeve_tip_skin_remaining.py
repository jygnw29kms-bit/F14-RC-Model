from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
R=Path(__file__).resolve().parents[2]
names=['WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd','Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd']
ps=[R/'migration/freecad'/n for n in names]
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hs=[H(p) for p in ps]
out=R/'analysis/v192_short_sleeve_tip_skin_remaining_bounds.json'
assert not out.exists()
def bounds(s):
 b=Bnd_Box();brepbndlib.AddOptimal(Part.__toPythonOCC__(s),b,False,True);return b.Get()
D=A.openDocument(str(ps[0]));tip=next(o.Shape.copy() for o in D.Objects if min(v.Point.y for v in o.Shape.Vertexes)>299.999);A.closeDocument(D.Name)
D=A.openDocument(str(ps[1]));sh={o.Name:o.Shape.copy() for o in D.Objects};A.closeDocument(D.Name)
tb=bounds(tip);rows=[]
for n in ['ROOT_CARRIER','ROOT_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_0']:
 fb=bounds(sh[n]);gap=tb[1]-fb[4];rows.append({'fixed':n,'method':'optimal_bounds_disjointY_for_all_positive_translation','gap_lower_bound_mm':gap,'covered':gap>1e-6})
x,_,z=json.loads((R/'analysis/v192_y300_alignment_pin_envelope_screen.json').read_text())['axis_start_mm']
radial=Part.makeCylinder(2,1000,A.Vector(x,0,z),A.Vector(0,1,0))
volume=tip.common(radial).Volume
sleeve=sh['GENERIC_4OD_2p2ID_SLEEVE'];outside=sleeve.cut(radial).Volume
rows.append({'fixed':'GENERIC_4OD_2p2ID_SLEEVE','method':'radius2_exclusion_invariant_underYtranslation','tip_overlap_cylinder_mm3':volume,'sleeve_outside_cylinder_mm3':outside,'covered':abs(volume)<1e-7 and abs(outside)<1e-7})
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'REMAINING_FOUR_PAIR_BOUNDS_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'moving':'TIP_SKIN','translation_range_mm':[0,5],'rows':rows,'all_pairs_covered':all(r['covered'] for r in rows),'limits':['Native numeric/tolerance assumptions; zero volume allows contact','Rigid geometric placeholders only; no assembly process or strength acceptance','Source partition volume gate blocked'],'print_release':False,'flight_release':False},indent=2)+'\n')
print(rows,flush=True)
