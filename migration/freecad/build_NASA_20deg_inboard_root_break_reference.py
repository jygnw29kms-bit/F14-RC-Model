from pathlib import Path
import FreeCAD as A, Part, json, hashlib
R=Path(__file__).resolve().parents[2]; P=R/'analysis/original_front_sources'; H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['NASA_CR172559_inboard_first_three_profiles.json','NASA_CR172559_20deg_root_break_profiles.json']; data=[json.loads((P/n).read_text()) for n in names]
path=R/'migration/freecad/NASA_20DEG_INBOARD_ROOT_BREAK_REFERENCE_ONLY.FCStd'; out=P/'NASA_20deg_inboard_root_break_native_audit.json'; assert not path.exists() and not out.exists()
master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd'; before=H(master); sections=[]; wires=[]
for dataset, rows in [(data[0],data[0]['rows']),(data[1],data[1]['rows'])]:
 for r in rows:
  h=r['header_raw_fields']; c=h[2]-h[0]; g=dataset['common_chord_grid_xc']; pairs=list(zip(g,r['ordinate_upper']))+list(reversed(list(zip(g,r['ordinate_lower']))))[:-1]
  points=[(h[0]+x*c,h[5]+z*c) for x,z in pairs]; v=[A.Vector(x,h[1],z) for x,z in points]; w=Part.makePolygon(v+[v[0]]); assert w.isValid() and w.isClosed(); wires.append(w); sections.append((h[1],points))
def area(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2)
expected=0
for (y,p),(yy,q) in zip(sections[:3],sections[1:4]):
 mid=[((x+xx)/2,(z+zz)/2) for (x,z),(xx,zz) in zip(p,q)]; expected+=(yy-y)*(area(p)+4*area(mid)+area(q))/6
s=Part.makeLoft(wires[:4],True,True); assert s.isValid() and len(s.Solids)==1; assert abs(s.Volume-expected)<1e-5
D=A.newDocument('NASA_20_ROOT_BREAK_REFERENCE'); o=D.addObject('PartDesign::Feature','INBOARD_0_TO_127p22');o.Shape=s; o=D.addObject('PartDesign::Feature','SEPARATE_SECTION_127p24');o.Shape=wires[4]
for o in D.Objects:
 o.addProperty('App::PropertyString','Limits');o.Limits='Conditional source frame: X=XPL+xc*chord,Y=rawspan,Z=field6+ordinate*chord. Source unit=display mm only. No physical scale, factory OML or pivot registration. No bridge across 127.22/127.24.'
D.recompute();D.saveAs(str(path));A.closeDocument(D.Name);D=A.openDocument(str(path)); assert len(D.Objects)==2
assert D.Objects[0].Shape.isValid() and len(D.Objects[0].Shape.Solids)==1
assert D.Objects[1].Shape.isValid() and len(D.Objects[1].Shape.Solids)==0 and D.Objects[1].Shape.isClosed()
volume=D.Objects[0].Shape.Volume;A.closeDocument(D.Name);assert H(master)==before
out.write_text(json.dumps({'status':'SAVED_REOPENED_CONDITIONAL_REFERENCE','input_sha256':{n:H(P/n) for n in names},'output_sha256':H(path),'master_sha256_unchanged':before,'inboard_span_raw':[0,127.22],'separate_wire_span_raw':127.24,'bridge_across_break':False,'native_volume_display_units_cubed':volume,'independent_prismoidal_volume':expected,'absolute_volume_difference':abs(volume-expected),'limits':['Ruled interpolation is a reconstruction assumption','Source unit equals display mm only, not physical model scale','Conditional Z=field6+ordinate*chord; exact reader not verified','No factory skin, body or pivot WL registration','Separate 127.24 wire is not a solid outboard wing'],'print_release':False,'flight_release':False},indent=2)+'\n');print('VERIFIED',volume,expected)
