from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text());caps=R/'migration/freecad/TAPERED_CAPS_UNFROZEN_FIT_TRIAL_ONLY.FCStd';void=R/'migration/freecad/WING_R_VOID_ALL17_FUSED_TRIAL_ONLY.FCStd';prev=json.loads((R/'analysis/v192_tapered_caps_reopen_audit.json').read_text());assert sha(caps)==prev['caps_sha256'] and sha(void)==prev['void_sha256']
out=R/'analysis/v192_cap_shear_web_trial.json';log=out.with_suffix('.jsonl');path=R/'migration/freecad/CAP_WEB_UNFROZEN_TRIAL_ONLY.FCStd';assert not out.exists() and not log.exists() and not path.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
wires=[]
for r in b['rows']:
 x=r['x_center_mm'];y=r['y_mm'];lo=r['lower_cap_z_interval_mm'][1];hi=r['upper_cap_z_interval_mm'][0];assert hi>lo
 pts=[App.Vector(x-.4,y,lo),App.Vector(x+.4,y,lo),App.Vector(x+.4,y,hi),App.Vector(x-.4,y,hi)];wires.append(Part.makePolygon(pts+[pts[0]]))
stage('web_loft');web=Part.makeLoft(wires,True,True);assert web.isValid() and len(web.Solids)==1
a=App.openDocument(str(caps));v=App.openDocument(str(void));d=App.newDocument('CAP_WEB_UNFROZEN');contacts=[]
try:
 c=next(o.Shape for o in v.Objects if hasattr(o,'Shape') and not o.Shape.isNull());cs=[o for o in a.Objects if hasattr(o,'Shape') and not o.Shape.isNull()];assert len(cs)==2
 stage('web_containment');outside=web.cut(c).Volume;stage('web_boundary_distance');gap=web.Shells[0].distToShape(c.Shells[0])[0]
 for o in cs:
  stage('contact',object=o.Name);common=web.common(o.Shape);dist=web.distToShape(o.Shape)[0];contacts.append({'cap':o.Name,'distance_mm':dist,'common_volume_mm3':common.Volume,'common_area_mm2':common.Area,'common_faces':len(common.Faces)})
  new=d.addObject('PartDesign::Feature',o.Name);new.Shape=o.Shape.copy()
 o=d.addObject('PartDesign::Feature','UNFROZEN_WEB_0p8');o.Shape=web
 stage('fuse_diagnostic');fused=web.fuse(cs[0].Shape).fuse(cs[1].Shape);fusion={'valid':fused.isValid(),'solids':len(fused.Solids),'volume_mm3':fused.Volume,'sum_input_volume_mm3':web.Volume+sum(o.Shape.Volume for o in cs)}
 d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(v.Name);App.closeDocument(a.Name)
assert sha(caps)==prev['caps_sha256'] and sha(void)==prev['void_sha256']
r={'status':'SEPARATE_CAP_WEB_GEOMETRIC_CONTACT_STUDY_ONLY','basis_sha256':sha(basis),'caps_sha256':sha(caps),'void_sha256':sha(void),'output_sha256':sha(path),'web_valid':True,'web_solids':1,'web_volume_mm3':web.Volume,'web_outside_void_volume_mm3':outside,'web_minimum_void_boundary_gap_mm':gap,'contacts':contacts,'fusion_diagnostic':fusion,'limits':['0.8mm centered web is an unfrozen geometric concept, not selected material or print thickness','Zero distance and single-solid fusion do not prove face contact area or bonded shear transfer; face-level verification remains open','No adhesive film, fillets, buckling, laminate, stiffness, torsion, root connection or physical proof','Separate three-body study; diagnostic fused shape not substituted for manufactured assembly; master unchanged'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
