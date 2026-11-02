from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[2];names=['Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_short_sleeve_auxiliary_path_bounds.json';assert not out.exists();D=A.openDocument(str(ps[0]));sh={o.Name:o.Shape.copy() for o in D.Objects};A.closeDocument(D.Name);D=A.openDocument(str(ps[1]));spars=[(o.Name,o.Shape.copy()) for o in D.Objects];A.closeDocument(D.Name);x,_,z=json.loads((R/'analysis/v192_y300_alignment_pin_envelope_screen.json').read_text())['axis_start_mm'];radial=Part.makeCylinder(2,1000,A.Vector(x,0,z),A.Vector(0,1,0));rows=[]
for n in ['TIP_CARRIER','TIP_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_1']:
 s=sh[n];b=s.BoundBox;ymin=min(v.Point.y for v in s.Vertexes);ymax=max(v.Point.y for v in s.Vertexes)+5;exclusion=s.common(radial).Volume;tests=[]
 for fn in ['ROOT_CARRIER','ROOT_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_0']:
  fb=sh[fn].BoundBox;tests.append({'fixed':fn,'method':'disjointY','gap_lower_bound_mm':ymin-fb.YMax,'covered':ymin>fb.YMax+1e-6})
 tests.append({'fixed':'SLEEVE','method':'radial_exclusion_invariant_underYtranslation','overlap_long_radius2_cylinder_mm3':exclusion,'covered':abs(exclusion)<1e-7})
 window=Part.makeBox(2000,ymax-ymin,2000,A.Vector(-1000,ymin,-1000))
 for fn,f in spars:
  c=f.common(window)
  if not c.Solids:tests.append({'fixed':fn,'method':'noSolidInSweptYSlab','covered':True});continue
  cb=c.BoundBox;gap=max(cb.XMin-b.XMax,b.XMin-cb.XMax);tests.append({'fixed':fn,'method':'disjointXWithinSweptYSlab','x_gap_lower_bound_mm':gap,'covered':gap>1e-6})
 rows.append({'moving':n,'sweptY':[ymin,ymax],'tests':tests});print(n,[t for t in tests if not t['covered']],flush=True)
assert [H(p) for p in ps]==hs;out.write_text(json.dumps({'status':'AUXILIARY_RIGID_Y_PATH_BOUNDS_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'translation_range_mm':[0,5],'rows':rows,'all_pairs_covered':all(t['covered'] for r in rows for t in r['tests']),'limits':['Bounds rely on native shape/tolerance calculations; not exact arithmetic certificate','Only three auxiliary tip objects vs nine fixed objects; tip skin scope handled separately','No adhesive process, access/tooling, tolerance or strength acceptance','Source partition volume gate blocked'],'print_release':False,'flight_release':False},indent=2)+'\n')
