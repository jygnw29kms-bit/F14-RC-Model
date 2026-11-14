from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'analysis/original_front_sources'; path=R/'migration/freecad/NASA_20DEG_INBOARD_ROOT_BREAK_REFERENCE_ONLY.FCStd';out=P/'NASA_20deg_root_break_saved_vertex_audit.json';assert not out.exists();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=H(path);m=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';mh=H(m)
a=json.loads((P/'NASA_CR172559_inboard_first_three_profiles.json').read_text());b=json.loads((P/'NASA_CR172559_20deg_root_break_profiles.json').read_text());D=A.openDocument(str(path));rows=[]
try:
 for dataset in (a,b):
  for r in dataset['rows']:
   h=r['header_raw_fields'];c=h[2]-h[0];shape=D.getObject('SEPARATE_SECTION_127p24' if h[1]==127.24 else 'INBOARD_0_TO_127p22').Shape;distances=[]
   for side in ('upper','lower'):
    for x,z in zip(dataset['common_chord_grid_xc'],r['ordinate_'+side]):
     v=A.Vector(h[0]+x*c,h[1],h[5]+z*c);distances.append(Part.Vertex(v).distToShape(shape)[0])
   assert len(distances)==100 and max(distances)<1e-7
   rows.append({'span_raw':h[1],'source_points':100,'maximum_point_to_saved_shape_distance':max(distances)})
 assert D.getObject('INBOARD_0_TO_127p22').Shape.BoundBox.YMax<127.23
 assert abs(D.getObject('SEPARATE_SECTION_127p24').Shape.BoundBox.YMin-127.24)<1e-7
finally:A.closeDocument(D.Name)
assert H(path)==before and H(m)==mh
out.write_text(json.dumps({'status':'500_SOURCE_POINTS_CHECKED_AGAINST_SAVED_NATIVE_SHAPES','reference_sha256_unchanged':before,'master_sha256_unchanged':mh,'rows':rows,'limits':['Point distances verify sampled source boundary positions only, not all loft surfaces','No bridge across root break','Conditional coordinate hypothesis and display units remain unchanged','No factory OML, print or flight acceptance'],'production_release':False},indent=2)+'\n');print(rows)
