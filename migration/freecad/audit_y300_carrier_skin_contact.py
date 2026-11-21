from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['Y300_ALIGNMENT_CARRIERS_UNFROZEN_ONLY.FCStd','Y300_ALIGNMENT_SLEEVE_UNSUPPORTED_STUDY_ONLY.FCStd','WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_y300_carrier_skin_contact_audit.json';assert not out.exists();sh=[]
for p in ps:
 D=A.openDocument(str(p));sh.append([(o.Name,o.Shape.copy()) for o in D.Objects]);A.closeDocument(D.Name)
wing=sh[2][0][1];sleeve=sh[1][0][1];wf=[(i,f,f.BoundBox) for i,f in enumerate(wing.Faces)];rows=[]
def overlap(a,b):return all(getattr(a,n+'Min')<=getattr(b,n+'Max')+1e-6 and getattr(b,n+'Min')<=getattr(a,n+'Max')+1e-6 for n in ('X','Y','Z'))
for name,s in sh[0]:
 contacts=[]
 for i,f in enumerate(s.Faces):
  b=f.BoundBox
  for j,g,bb in wf:
   if overlap(b,bb):
    area=f.common(g).Area
    if area>1e-7:contacts.append({'carrier_face':i,'wing_face':j,'area_mm2':area})
 rows.append({'carrier':name,'skin_contact_faces':contacts,'total_geometric_contact_area_mm2':sum(c['area_mm2'] for c in contacts),'sleeve_distance_mm':s.distToShape(sleeve)[0],'sleeve_overlap_mm3':s.common(sleeve).Volume});print(rows[-1],flush=True)
assert all(r['total_geometric_contact_area_mm2']>0 for r in rows);assert [H(p) for p in ps]==hs;out.write_text(json.dumps({'status':'CARRIER_SKIN_GEOMETRIC_CONTACT_AND_SLEEVE_GAP_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'limits':['Skin contact has zero adhesive thickness; no bond strength, peel or manufacturing tolerance accepted','Positive sleeve gap means no direct sleeve-carrier contact; adhesive layer or retention still missing','No seam structural or print acceptance; source partition volume gate remains blocked'],'print_release':False,'flight_release':False},indent=2)+'\n')
