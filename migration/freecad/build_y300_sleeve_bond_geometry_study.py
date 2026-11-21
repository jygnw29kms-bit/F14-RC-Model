from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
R=Path(__file__).resolve().parents[2];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();names=['Y300_ALIGNMENT_CARRIERS_UNFROZEN_ONLY.FCStd','Y300_ALIGNMENT_SLEEVE_UNSUPPORTED_STUDY_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];hs=[H(p) for p in ps];basis=R/'analysis/v192_y300_alignment_pin_envelope_screen.json';x,_,z=json.loads(basis.read_text())['axis_start_mm'];out=R/'migration/freecad/Y300_SLEEVE_BOND_GEOMETRY_STUDY_ONLY.FCStd';report=R/'analysis/v192_y300_sleeve_bond_geometry_audit.json';assert not out.exists() and not report.exists();copies=[]
for p in ps:
 D=A.openDocument(str(p));copies.extend([(o.Name,o.Shape.copy()) for o in D.Objects]);A.closeDocument(D.Name)
D=A.newDocument('SLEEVE_BOND_GEOMETRY_STUDY');rows=[]
for name,s in copies:o=D.addObject('PartDesign::Feature',name);o.Shape=s
for idx,(y0,y1) in enumerate([(290,299.8),(300.2,310)]):
 length=y1-y0;b=Part.makeCylinder(2.1,length,A.Vector(x,y0,z),A.Vector(0,1,0)).cut(Part.makeCylinder(2,length,A.Vector(x,y0,z),A.Vector(0,1,0)));assert b.isValid() and len(b.Solids)==1;assert abs(b.Volume-math.pi*(2.1**2-2**2)*length)<1e-7;contact=[]
 for target,s in [copies[idx],copies[2]]:
  area=sum(f.common(g).Area for f in b.Faces for g in s.Faces);overlap=b.common(s).Volume;expected=2*math.pi*(2.1 if target==copies[idx][0] else 2)*length;assert abs(area-expected)<1e-6 and overlap<1e-7;contact.append({'target':target,'common_face_area_mm2':area,'independent_cylinder_area_mm2':expected,'overlap_volume_mm3':overlap})
 o=D.addObject('PartDesign::Feature','GEOMETRIC_BOND_'+str(idx));o.Shape=b;rows.append({'name':o.Name,'volume_mm3':b.Volume,'contacts':contact})
for o in D.Objects:o.addProperty('App::PropertyString','Limits');o.Limits='Geometric0.1mm radial placeholder only, no adhesive/cure/tolerance/strength. Skin bond zero thickness, seam volume gate remains blocked.'
D.recompute();D.saveAs(str(out));A.closeDocument(D.Name);D=A.openDocument(str(out));assert len(D.Objects)==5
for o in D.Objects:assert o.Shape.isValid() and len(o.Shape.Solids)==1
A.closeDocument(D.Name);assert [H(p) for p in ps]==hs;report.write_text(json.dumps({'status':'FIVE_BODY_BOND_GEOMETRY_SAVED_REOPENED','input_sha256_unchanged':dict(zip(names,hs)),'output_sha256':H(out),'rows':rows,'limits':['Adhesive not selected; geometric layer no strength or cure qualification','Carrier-to-skin adhesive thickness still absent','No seam load transfer, pin retention, manufacturing or physical proof','Source partition volume release gate remains blocked'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
