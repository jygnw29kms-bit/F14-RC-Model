from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];names=['WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd','Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_short_sleeve_seam_probe_access_screen.json';assert not out.exists()
objects=[]
D=A.openDocument(str(ps[0]))
for o in D.Objects:
 s=o.Shape.copy();tip=min(v.Point.y for v in s.Vertexes)>299.999
 if tip:s.translate(A.Vector(0,5,0))
 objects.append(('TIP_SKIN' if tip else 'ROOT_SKIN',s))
A.closeDocument(D.Name)
D=A.openDocument(str(ps[1]))
for o in D.Objects:
 s=o.Shape.copy()
 if o.Name in ['TIP_CARRIER','TIP_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_1']:s.translate(A.Vector(0,5,0))
 objects.append((o.Name,s))
A.closeDocument(D.Name)
D=A.openDocument(str(ps[2]));objects.extend((o.Name,o.Shape.copy()) for o in D.Objects);A.closeDocument(D.Name)
x,_,z=json.loads((R/'analysis/v192_y300_alignment_pin_envelope_screen.json').read_text())['axis_start_mm'];rows=[]
for name,axis in [('plusX',A.Vector(1,0,0)),('minusX',A.Vector(-1,0,0)),('plusZ',A.Vector(0,0,1)),('minusZ',A.Vector(0,0,-1))]:
 start=A.Vector(x,302.5,z)+axis*2.5;probe=Part.makeCylinder(.25,40,start,axis);checks=[]
 for n,s in objects:checks.append({'object':n,'overlap_mm3':probe.common(s).Volume})
 rows.append({'direction':name,'checks':checks,'all_local_overlaps_below_1e_minus7_mm3':all(abs(c['overlap_mm3'])<1e-7 for c in checks)})
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'IDEAL_SEAM_PROBE_ENVELOPES_SCREENED_NOT_REAL_TOOL_ACCESS','input_sha256_unchanged':dict(zip(names,hs)),'tip_translation_y_mm':5,'probe_y_mm':302.5,'probe_radius_mm':.25,'probe_axial_length_mm':40,'probe_inner_radial_offset_mm':2.5,'rows':rows,'limits':['Hypothetical straight cylindrical inspection probe only, not selected adhesive applicator','Four finite radial corridors only; external approach, handle and aircraft objects omitted','No adhesive application, film displacement, fixture or cure acceptance','Positive overlap rejects only this corridor; zero overlap is not actual tool accessibility','No source partition volume or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)

