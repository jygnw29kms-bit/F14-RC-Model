from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_boundary_area_balance.json';assert not out.exists();D=A.openDocument(str(ps[0]));source=D.Objects[0].Shape.copy();A.closeDocument(D.Name);D=A.openDocument(str(ps[1]));parts=[o.Shape.copy() for o in D.Objects];A.closeDocument(D.Name)
# Sum every actual face-pair common area; do not assume fixed Face indices.
seam=sum(f.common(g).Area for f in parts[0].Faces for g in parts[1].Faces if abs(f.CenterOfMass.y-300)<1e-5 and abs(g.CenterOfMass.y-300)<1e-5)
rows=[]
for label,s in [('SOURCE',source)]+[('PART'+str(i),s) for i,s in enumerate(parts)]:
 by_type={}
 for f in s.Faces:
  key=type(f.Surface).__name__;by_type[key]=by_type.get(key,0)+f.Area
 rows.append({'name':label,'native_area_mm2':s.Area,'face_count':len(s.Faces),'face_area_by_surface_type_mm2':by_type})
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'BOUNDARY_AREA_BALANCE_DIAGNOSTIC_ONLY','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'common_seam_area_mm2':seam,'part_area_sum_minus_twice_seam_minus_source_mm2':sum(s.Area for s in parts)-2*seam-source.Area,'limits':['Native area integration is numerical and not rigorous defect certification','Area balance does not replace volume gate or prove identical boundaries','No tolerance modification, new geometry or release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows,'seam',seam)
