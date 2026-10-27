from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();void=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';before=sha(void);assert before in b['input_sha256'].values()
out=R/'analysis/v192_tapered_cap_loft_trial.json';log=out.with_suffix('.jsonl');path=R/'migration/freecad/TAPERED_CAPS_UNFROZEN_FIT_TRIAL_ONLY.FCStd';assert not out.exists() and not log.exists() and not path.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(void));d=App.newDocument('CAPS_UNFROZEN_TRIAL');rows=[]
try:
 objs=[o for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(objs)==1;c=objs[0].Shape
 for side in ('lower','upper'):
  wires=[]
  for r in b['rows']:
   x=r['x_center_mm'];y=r['y_mm'];half=r['cap_width_mm']/2;lo,hi=r[side+'_cap_z_interval_mm'];pts=[App.Vector(x-half,y,lo),App.Vector(x+half,y,lo),App.Vector(x+half,y,hi),App.Vector(x-half,y,hi)];wires.append(Part.makePolygon(pts+[pts[0]]))
  stage('loft_start',side=side);s=Part.makeLoft(wires,True,True);assert s.isValid() and len(s.Solids)==1;stage('outside_cut_start',side=side);outside=s.cut(c).Volume;stage('outside_cut_done',side=side,outside_volume_mm3=outside)
  stage('distance_start',side=side);gap,pts,info=s.Shells[0].distToShape(c.Shells[0]);stage('distance_done',side=side,distance_mm=gap)
  o=d.addObject('PartDesign::Feature','UNFROZEN_'+side.upper()+'_CAP');o.Shape=s;o.addProperty('App::PropertyBool','ProductionRelease');o.ProductionRelease=False
  rows.append({'side':side,'valid':True,'solids':1,'volume_mm3':s.Volume,'outside_void_volume_mm3':outside,'contained_within_1e_6_mm3':outside<=1e-6,'minimum_void_boundary_gap_mm':gap,'closest_point_pairs_mm':[[list(p),list(q)] for p,q in pts]})
 stage('save');d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(a.Name)
assert sha(void)==before
r={'status':'TWO_SEPARATE_TAPERED_CAP_SOLID_FIT_TRIALS_ONLY','basis_sha256':sha(basis),'void_sha256':before,'output_sha256':sha(path),'rows':rows,'limits':['Five-section ruled lofts from sampled inner bounds; no geometric repair or clipping','16-to-8mm width and 1mm vertical thickness are unfrozen concepts, not selected carbon products','No web, bond, root load transfer, composite layup, buckling, stiffness, mass or physical proof','Containment result only; requested .2mm vertical reserve is not a continuous normal-clearance guarantee','Not integrated into wing; master unchanged'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(rows))
