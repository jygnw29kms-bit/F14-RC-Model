from pathlib import Path
import FreeCAD as A,Part,json,math,hashlib
R=Path(__file__).resolve().parents[2];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rings=R/'migration/freecad/CANTED_BEARING_ENVELOPES_UNSELECTED_ONLY.FCStd';rh=H(rings);out=R/'migration/freecad/CANTED_HOUSING_SHOULDER_CONCEPT_ONLY.FCStd';report=R/'analysis/v192_canted_housing_shoulder_concept.json';assert not out.exists() and not report.exists();axis=A.Vector(0,math.sin(math.radians(1.5)),math.cos(math.radians(1.5)));p=A.Vector(613.1323905812828,125.20927023775282,0);s=Part.makeCylinder(9,21,p-axis*10.5,axis).cut(Part.makeCylinder(4,21,p-axis*10.5,axis))
for t in (-10.5,5.5):s=s.cut(Part.makeCylinder(6.5,5,p+axis*t,axis))
expected=math.pi*((9**2-4**2)*21-2*(6.5**2-4**2)*5);assert s.isValid() and len(s.Solids)==1 and abs(s.Volume-expected)<1e-6
D=A.openDocument(str(rings));copies=[(o.Name,o.Shape.copy()) for o in D.Objects];A.closeDocument(D.Name);checks=[]
for name,ring in copies:
 overlap=ring.common(s).Volume;assert overlap<1e-7;checks.append({'ring':name,'overlap_housing_mm3':overlap,'distance_mm':ring.distToShape(s)[0]})
D=A.newDocument('CANTED_HOUSING_CONCEPT');o=D.addObject('PartDesign::Feature','HOUSING');o.Shape=s;o.addProperty('App::PropertyString','Limits');o.Limits='Unselected18OD/21length,13seat/5depth,8centralbore; zero nominal seat clearance. No retention, tolerances, material, shaft, root attachment or aircraft fit.'
for name,ring in copies:o=D.addObject('PartDesign::Feature',name);o.Shape=ring
D.recompute();D.saveAs(str(out));A.closeDocument(D.Name);D=A.openDocument(str(out));assert len(D.Objects)==3
for o in D.Objects:assert o.Shape.isValid() and len(o.Shape.Solids)==1
A.closeDocument(D.Name);assert H(rings)==rh;report.write_text(json.dumps({'status':'SEPARATE_HOUSING_SHOULDER_CONCEPT_SAVED_REOPENED','ring_input_sha256_unchanged':rh,'output_sha256':H(out),'housing_volume_mm3':s.Volume,'independent_analytic_volume_mm3':expected,'interface_checks':checks,'nominal_shoulder_annulus_area_mm2':math.pi*(6.5**2-4**2),'limits':['Zero nominal radial seat clearance is a geometric placeholder, not tolerance specification','Shoulder annulus is geometric, not effective race contact or thrust rating','No outer-race retention on open ends, shaft retention, fasteners, structure or materials','Not attached to root socket; no aircraft envelope fit or physical pivot WL verified'],'hardware_selected':False,'print_release':False,'flight_release':False},indent=2)+'\n');print(s.Volume,checks)
