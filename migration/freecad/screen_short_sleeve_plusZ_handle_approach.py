from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];names=['WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd','Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_short_sleeve_plusZ_probe_handle_approach.json';assert not out.exists()
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
# Conservative enclosing bounds suffice to place the hypothetical handle above all local objects.
zmax=max(s.BoundBox.ZMax for n,s in objects);inner_z=z+2.5;length=zmax+50-inner_z
probe=Part.makeCylinder(.25,length,A.Vector(x,302.5,inner_z),A.Vector(0,0,1))
handle=Part.makeCylinder(3,45,A.Vector(x,302.5,zmax+5),A.Vector(0,0,1))
envelope=Part.makeCompound([probe,handle]);checks=[]
for n,s in objects:checks.append({'object':n,'overlap_mm3':envelope.common(s).Volume})
rows=[{'direction':'plusZ','checks':checks,'all_local_overlaps_below_1e_minus7_mm3':all(abs(c['overlap_mm3'])<1e-7 for c in checks)}]
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'IDEAL_SEAM_PROBE_ENVELOPES_SCREENED_NOT_REAL_TOOL_ACCESS','input_sha256_unchanged':dict(zip(names,hs)),'tip_translation_y_mm':5,'probe_y_mm':302.5,'probe_radius_mm':.25,'probe_axial_length_mm':length,'local_enclosing_zmax_mm':zmax,'handle_radius_mm':3,'handle_length_mm':45,'handle_zmin_mm':zmax+5,'approach_translation':'positiveZ from above all listed objects; probe swept cylinder spans inner stop to above local zmax; handle remains above local enclosing zmax','probe_inner_radial_offset_mm':2.5,'rows':rows,'limits':['Hypothetical straight cylindrical inspection probe only, not selected adhesive applicator','Single hypothetical plusZ probe/handle approach screened against listed local bodies only; rest of aircraft omitted','No adhesive application, film displacement, fixture or cure acceptance','Positive overlap rejects only this corridor; zero overlap is not actual tool accessibility','No source partition volume or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)


