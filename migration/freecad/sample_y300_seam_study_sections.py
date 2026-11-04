from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];names=['Y300_SLEEVE_BOND_GEOMETRY_STUDY_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd','WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_y300_seam_study_section_samples.json';assert not out.exists();sh=[]
for n,p in zip(names,ps):
 D=A.openDocument(str(p));sh.extend([(n,o.Name,o.Shape.copy()) for o in D.Objects]);A.closeDocument(D.Name)
rows=[]
for y in (295,305):
 pts=[A.Vector(500,y,-100),A.Vector(800,y,-100),A.Vector(800,y,100),A.Vector(500,y,100)];plane=Part.Face(Part.makePolygon(pts+[pts[0]]));objects=[]
 for source,name,s in sh:
  sec=s.section(plane);objects.append({'source':source,'object':name,'edges':[[[p.x,p.z] for p in e.discretize(Number=7)] for e in sec.Edges]})
 rows.append({'y_mm':y,'objects':objects})
assert [H(p) for p in ps]==hs;out.write_text(json.dumps({'status':'NATIVE_SECTION_EDGE_SAMPLES_NOT_CAD_SCREENSHOT','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'limits':['Sampled edges only, no full surface or strength acceptance','Skin bond zero thickness; source partition volume gate blocked']},indent=2)+'\n');print([(r['y_mm'],sum(len(o['edges']) for o in r['objects'])) for r in rows])
