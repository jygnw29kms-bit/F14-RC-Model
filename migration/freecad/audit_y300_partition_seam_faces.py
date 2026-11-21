from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_y300_partition_seam_face_audit.json';assert not out.exists();D=A.openDocument(str(p));shapes=[o.Shape.copy() for o in D.Objects];A.closeDocument(D.Name);faces=[];rows=[]
for i,s in enumerate(shapes):
 ff=[(k,f) for k,f in enumerate(s.Faces) if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-300)<1e-6 and f.BoundBox.YLength<1e-6];assert ff;faces.append(ff);rows.append({'part_index':i,'seam_faces':[{'index':k,'area_mm2':f.Area,'wire_count':len(f.Wires)} for k,f in ff],'total_seam_area_mm2':sum(f.Area for k,f in ff)})
contacts=[]
for i,f in faces[0]:
 for j,g in faces[1]:
  c=f.common(g)
  if c.Area>1e-7:contacts.append({'part0_face':i,'part1_face':j,'common_area_mm2':c.Area})
area=sum(c['common_area_mm2'] for c in contacts);assert all(abs(r['total_seam_area_mm2']-area)<1e-5 for r in rows);assert H(p)==h;out.write_text(json.dumps({'status':'SAVED_PARTITION_SEAM_FACE_CONTACT_GEOMETRY_ONLY','input_sha256_unchanged':h,'rows':rows,'contacts':contacts,'matching_common_area_mm2':area,'limits':['Zero-gap butt seam only, no overlap joint, alignment keys or adhesive layer','Contact area is geometric shell cross-section, not allowable bond area or strength','Partition volume guard remains blocked; no print/flight release','No full seam manufacturing, skin continuity or physical proof'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows,area)
