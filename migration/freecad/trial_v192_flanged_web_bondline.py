from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text());caps=R/'migration/freecad/TAPERED_CAPS_UNFROZEN_FIT_TRIAL_ONLY.FCStd';void=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';inputs={str(p):sha(p) for p in (basis,caps,void)}
out=R/'analysis/v192_flanged_web_bondline_trial.json';log=out.with_suffix('.jsonl');path=R/'migration/freecad/FLANGED_WEB_BONDLINE_UNFROZEN_TRIAL_ONLY.FCStd';assert not out.exists() and not log.exists() and not path.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
def loft(kind):
 wires=[]
 for r in b['rows']:
  x=r['x_center_mm'];y=r['y_mm'];lo=r['lower_cap_z_interval_mm'][1];hi=r['upper_cap_z_interval_mm'][0]
  width,z0,z1={'core':(.8,lo+.4,hi-.4),'lower_flange':(4,lo+.1,lo+.4),'upper_flange':(4,hi-.4,hi-.1),'lower_bond':(4,lo,lo+.1),'upper_bond':(4,hi-.1,hi)}[kind];assert z1>z0
  pts=[App.Vector(x-width/2,y,z0),App.Vector(x+width/2,y,z0),App.Vector(x+width/2,y,z1),App.Vector(x-width/2,y,z1)];wires.append(Part.makePolygon(pts+[pts[0]]))
 s=Part.makeLoft(wires,True,True);assert s.isValid() and len(s.Solids)==1;return s
stage('make_parts');parts={k:loft(k) for k in ('core','lower_flange','upper_flange','lower_bond','upper_bond')};web=parts['core'].fuse(parts['lower_flange']).fuse(parts['upper_flange']);assert web.isValid() and len(web.Solids)==1
shapes={'UNFROZEN_FLANGED_WEB':web,'GEOMETRIC_LOWER_BOND_0p1':parts['lower_bond'],'GEOMETRIC_UPPER_BOND_0p1':parts['upper_bond']}
a=App.openDocument(str(caps));v=App.openDocument(str(void));d=App.newDocument('FLANGED_WEB_BONDLINE_TRIAL');rows=[];distances=[]
try:
 c=next(o.Shape for o in v.Objects if hasattr(o,'Shape') and not o.Shape.isNull())
 for name,s in shapes.items():
  stage('containment',object=name);outside=s.cut(c).Volume;stage('distance',object=name);gap=s.Shells[0].distToShape(c.Shells[0])[0]
  o=d.addObject('PartDesign::Feature',name);o.Shape=s;rows.append({'object':name,'valid':True,'solids':1,'volume_mm3':s.Volume,'outside_void_volume_mm3':outside,'minimum_void_boundary_gap_mm':gap})
 for o in a.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull():continue
  new=d.addObject('PartDesign::Feature',o.Name);new.Shape=o.Shape.copy();distances.append({'cap':o.Name,'flanged_web_distance_mm':web.distToShape(o.Shape)[0]})
 d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(v.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items())
r={'status':'FLANGED_WEB_AND_EXPLICIT_GEOMETRIC_BOND_LAYERS_TRIAL_ONLY','input_sha256':inputs,'output_sha256':sha(path),'dimensions_mm':{'web_width':.8,'flange_width':4,'flange_vertical_thickness':.3,'bond_vertical_thickness':.1},'rows':rows,'cap_web_distances':distances,'limits':['0.1mm is vertical geometric separation, not constant normal bond thickness','4mm flange and0.3mm thickness are unfrozen packaging concepts; no selected material or printable-detail acceptance','Geometric bond solids are placeholders, not adhesive properties, chemistry or qualified bond','Face-level bond contacts, native reopen, shear transfer, peel, flange bending, buckling and root transfer remain open','Five-body separate study; master unchanged'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(rows));print(json.dumps(distances))
