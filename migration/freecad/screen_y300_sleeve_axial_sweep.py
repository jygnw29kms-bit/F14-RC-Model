from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/Y300_SKIN_BOND_VERTICAL_RECESS_STUDY_ONLY.FCStd';h=hashlib.sha256(p.read_bytes()).hexdigest();out=R/'analysis/v192_y300_sleeve_axial_sweep_screen.json';assert not out.exists();basis=json.loads((R/'analysis/v192_y300_alignment_pin_envelope_screen.json').read_text());x,_,z=basis['axis_start_mm'];sweep=Part.makeCylinder(2,40,A.Vector(x,270,z),A.Vector(0,1,0));D=A.openDocument(str(p));rows=[]
try:
 for o in D.Objects:
  if 'SLEEVE' in o.Name:continue
  rows.append({'object':o.Name,'swept_outer_cylinder_overlap_mm3':sweep.common(o.Shape).Volume})
finally:A.closeDocument(D.Name)
assert hashlib.sha256(p.read_bytes()).hexdigest()==h;out.write_text(json.dumps({'status':'EXACT_IDEAL_AXIAL_OUTER_ENVELOPE_SWEEP_SCREEN_ONLY','input_sha256_unchanged':h,'sleeve_final_y_interval_mm':[290,310],'assumed_translation_range_mm':[-20,0],'swept_outer_cylinder_y_interval_mm':[270,310],'swept_outer_radius_mm':2,'rows':rows,'limits':['Fixed carriers and geometric adhesive placeholders; only sleeve moves along globalY','Outer solid cylinder contains entire moving hollow sleeve for continuous translations; conservative collision envelope','Zero volume intersection allows contact and does not prove positive clearance','No wing/skin/spar access path or full-part assembly sequence tested','No wet adhesive scraping, cure, insertion force, tolerance or physical proof','Partition volume gate remains blocked; no printing or flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
