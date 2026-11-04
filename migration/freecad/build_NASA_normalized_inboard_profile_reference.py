from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'analysis/original_front_sources'
files=['NASA_CR172559_inboard_first_three_profiles.json','NASA_CR172559_centerline_25_35_profiles.json','NASA_CR172559_span68p5_25_35_profiles.json','NASA_CR172559_span99_25_35_profiles.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=sha(master)
rows=[];b=json.loads((P/files[0]).read_text())
for r in b['rows']:rows.append((20,b['common_chord_grid_xc'],r))
for name in files[1:]:
 for r in json.loads((P/name).read_text())['rows']:rows.append((r['nominal_sweep_deg'],r['grid_xc'],r))
path=R/'migration/freecad/NASA_NORMALIZED_INBOARD_PROFILES_REFERENCE_ONLY.FCStd';report=P/'NASA_normalized_inboard_profile_native_audit.json'
assert not path.exists() and not report.exists()
d=App.newDocument('NORMALIZED_PROFILE_CHART_ONLY');audit=[]
try:
 for angle,g,r in rows:
  span=r['header_raw_fields'][1];col=(20,25,35).index(angle);row=(0,68.5,99).index(span)
  # Chart coordinates only: one normalized chord=1000 display mm.
  ox=col*1200;oy=row*250
  pts=[App.Vector(ox+x*1000,oy+y*1000,0) for x,y in zip(g,r['ordinate_upper'])]
  pts += [App.Vector(ox+x*1000,oy+y*1000,0) for x,y in reversed(list(zip(g,r['ordinate_lower'])))][:-1]
  pts.append(pts[0]);wire=Part.makePolygon(pts)
  assert wire.isValid() and wire.isClosed() and len(wire.Faces)==len(wire.Solids)==0
  o=d.addObject('PartDesign::Feature',f'CHART_A{angle}_SPAN{str(span).replace(".","p")}');o.Shape=wire
  o.addProperty('App::PropertyString','CoordinateMeaning');o.CoordinateMeaning='NORMALIZED_PROFILE_CHART_NOT_AIRCRAFT_POSITION; one chord=1000 display mm; row/column offsets arbitrary'
  o.addProperty('App::PropertyBool','ProductionRelease');o.ProductionRelease=False
  audit.append({'object':o.Name,'sweep_deg':angle,'raw_span':span,'edges':len(wire.Edges),'closed':True,'valid':True,'faces':0,'solids':0})
 d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name)
d=App.openDocument(str(path))
try:
 assert len(d.Objects)==9
 for o in d.Objects:assert o.Shape.isValid() and o.Shape.isClosed() and len(o.Shape.Solids)==len(o.Shape.Faces)==0
finally:App.closeDocument(d.Name)
assert sha(master)==before
report.write_text(json.dumps({'status':'SAVED_AND_REOPENED_NINE_NORMALIZED_CHART_WIRES_ONLY','input_sha256':{n:sha(P/n) for n in files},'output_sha256':sha(path),'rows':audit,'master_sha256_unchanged':before,'limits':['Arbitrary chart layout, not aircraft coordinates or physical dimensions','Straight segments between original normalized samples, not spline reconstruction','No surfaces, solids, glove loft, registration, STL or print release'],'production_release':False},indent=2)+'\n')
print('Nine normalized chart wires saved and reopened; no faces or solids')
