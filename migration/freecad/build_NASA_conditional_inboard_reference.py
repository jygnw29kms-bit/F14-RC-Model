from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'analysis/original_front_sources';names=['NASA_CR172559_inboard_first_three_profiles.json','NASA_CR172559_centerline_25_35_profiles.json','NASA_CR172559_span68p5_25_35_profiles.json','NASA_CR172559_span99_25_35_profiles.json'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();data={n:json.loads((P/n).read_text()) for n in names};profiles={}
for r in data[names[0]]['rows']:profiles[(20,r['header_raw_fields'][1])]=(data[names[0]]['common_chord_grid_xc'],r)
for n in names[1:]:
 for r in data[n]['rows']:profiles[(r['nominal_sweep_deg'],r['header_raw_fields'][1])]=(r['grid_xc'],r)
master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=sha(master);path=R/'migration/freecad/NASA_CONDITIONAL_INBOARD_COMPUTATIONAL_REFERENCE_ONLY.FCStd';out=P/'NASA_conditional_inboard_native_reference_audit.json';assert not path.exists() and not out.exists();d=App.newDocument('CONDITIONAL_INBOARD_REFERENCE');rows=[]
try:
 for angle in (20,25,35):
  wires=[]
  for span in (0,68.5,99):
   grid,r=profiles[(angle,span)];h=r['header_raw_fields'];chord=h[2]-h[0]
   contour=list(zip(grid,r['ordinate_upper']))+list(reversed(list(zip(grid,r['ordinate_lower']))))[0:-1]
   pts=[App.Vector(h[0]+x*chord,h[1],h[5]+z*chord) for x,z in contour];wire=Part.makePolygon(pts+[pts[0]]);assert wire.isValid() and wire.isClosed();wires.append(wire)
  s=Part.makeLoft(wires,True,True);assert s.isValid() and len(s.Solids)==1
  o=d.addObject('PartDesign::Feature','CONDITIONAL_COMPUTATIONAL_A'+str(angle));o.Shape=s;o.addProperty('App::PropertyString','CoordinateAssumption');o.CoordinateAssumption='X=XPL+xc*chord;Y=rawspan;Z=rawfield6+ordinate*chord; one source unit=1 display mm, NOT physical model scale'
  o.addProperty('App::PropertyBool','ProductionRelease');o.ProductionRelease=False
  rows.append({'nominal_sweep_deg':angle,'valid':True,'solids':1,'faces':len(s.Faces),'volume_display_units_cubed':s.Volume,'span_raw_range':[0,99]})
 d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name)
d=App.openDocument(str(path))
try:
 assert len(d.Objects)==3
 for o in d.Objects:assert o.Shape.isValid() and len(o.Shape.Solids)==1
finally:App.closeDocument(d.Name)
assert sha(master)==before
r={'status':'CONDITIONAL_THREE_INBOARD_COMPUTATIONAL_LOFT_REFERENCES_SAVED_REOPENED','input_sha256':{n:sha(P/n) for n in names},'output_sha256':sha(path),'master_sha256_unchanged':before,'rows':rows,'coordinate_assumption':'X=XPL+xc*chord; Y=rawspan; Z=rawfield6+ordinate*chord. Cross-report numeric field6 evidence supports hypothesis; exact F14 reader remains unverified.','display_scale':'1 source unit=1 CAD display mm; not model millimeters, not physical scale','limits':['Only source span0..99, not complete glove or wing; root-break127.22/.24 excluded','Ruled interpolation between3 profiles is a reconstruction choice, not a measured surface','Centerline computational continuation is not automatically exposed skin','Three overlapping sweep cases are reference alternatives, not three physical aircraft bodies','No aircraft frame/pivotWL/body registration or original factory OML release','No structural, print, STL or flight acceptance'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows))
