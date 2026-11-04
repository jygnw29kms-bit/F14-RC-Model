from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['Y300_SLEEVE_BOND_GEOMETRY_STUDY_ONLY.FCStd','WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd','WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_y300_five_body_containment_audit.json';assert not out.exists();sh=[]
for p in ps:
 D=A.openDocument(str(p));sh.append([(o.Name,o.Shape.copy()) for o in D.Objects]);A.closeDocument(D.Name)
void=sh[1][0][1];wing=sh[3][0][1];rows=[]
for name,s in sh[0]:
 rows.append({'object':name,'valid':s.isValid(),'outside_saved_void_mm3':s.cut(void).Volume,'overlap_wing_skin_mm3':s.common(wing).Volume,'spar_overlaps':[{'object':n,'volume_mm3':s.common(t).Volume} for n,t in sh[2]]});print(name,flush=True)
assert [H(p) for p in ps]==hs;out.write_text(json.dumps({'status':'SAVED_FIVE_BODY_STUDY_CONTAINMENT_SCREEN_COMPLETE','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'limits':['Zero overlap is geometric only, not manufacturing clearance or strength','Carrier skin contact is zero-gap, no adhesive-thickness model yet','No structural seam/assembly/physical proof; source partition volume gate blocked'],'print_release':False,'flight_release':False},indent=2)+'\n');print([(r['object'],r['outside_saved_void_mm3'],r['overlap_wing_skin_mm3']) for r in rows])
