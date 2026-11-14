from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'analysis/original_front_sources';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();names=['NASA_20DEG_INBOARD_ROOT_BREAK_REFERENCE_ONLY.FCStd','NASA_20DEG_EIGHT_SECTION_OUTBOARD_R2_REFERENCE_ONLY.FCStd'];paths=[R/'migration/freecad'/n for n in names];before=[H(p) for p in paths];m=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';mh=H(m);out=R/'migration/freecad/NASA_20DEG_SEPARATE_INBOARD_OUTBOARD_R2_REFERENCE_ONLY.FCStd';audit=P/'NASA_20deg_separate_reference_assembly_audit.json';assert not out.exists() and not audit.exists();shapes=[]
for p in paths:
 d=A.openDocument(str(p));shapes.append(next(o.Shape.copy() for o in d.Objects if len(o.Shape.Solids)==1));A.closeDocument(d.Name)
assert shapes[1].BoundBox.YMin>shapes[0].BoundBox.YMax;gap=shapes[1].BoundBox.YMin-shapes[0].BoundBox.YMax
D=A.newDocument('SEPARATE_SOURCE_REFERENCES');rows=[]
for name,s in zip(['INBOARD_COMPUTATIONAL','OUTBOARD_COMPUTATIONAL_R2'],shapes):
 o=D.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyString','ReferenceLimits');o.ReferenceLimits='Conditional source XYZ/display units only; no aircraft registration. Two separate solids, no bridge/union across source break. Not exposed factory glove skin or production model.';rows.append({'name':name,'volume_display_units_cubed':s.Volume,'y_range_raw':[s.BoundBox.YMin,s.BoundBox.YMax]})
D.recompute();D.saveAs(str(out));A.closeDocument(D.Name);D=A.openDocument(str(out));assert len(D.Objects)==2
for o,row in zip(D.Objects,rows):assert o.Shape.isValid() and len(o.Shape.Solids)==1 and abs(o.Shape.Volume-row['volume_display_units_cubed'])<1e-7
A.closeDocument(D.Name);assert [H(p) for p in paths]==before and H(m)==mh
audit.write_text(json.dumps({'status':'TWO_SEPARATE_SOURCE_SOLIDS_SAVED_REOPENED','input_sha256':dict(zip(names,before)),'output_sha256':H(out),'master_sha256_unchanged':mh,'rows':rows,'separating_y_slab_width_raw':gap,'positive_volume_overlap_impossible_by_disjoint_y_bounds':True,'union_or_bridge_created':False,'limits':['Shared conditional source frame only, not aircraft/model registration','Slab width is not minimum Euclidean surface clearance','Inboard centerline continuation not necessarily exposed skin','Different contours across break remain unconnected','No factory OML structural print or flight acceptance'],'production_release':False},indent=2)+'\n');print(rows,gap)
