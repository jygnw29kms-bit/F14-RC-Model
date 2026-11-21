from pathlib import Path
import FreeCAD as App,Part,json,hashlib
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/FLANGED_WEB_BONDLINE_UNFROZEN_TRIAL_ONLY.FCStd';before=hashlib.sha256(src.read_bytes()).hexdigest();prior=json.loads((R/'analysis/v192_flanged_bond_face_contact_audit.json').read_text());assert before==prior['source_sha256'];out=R/'analysis/v192_flanged_spar_section_samples.json';assert not out.exists();basis=json.loads((R/'analysis/v192_cap_width_inner_envelope.json').read_text());d=App.openDocument(str(src));rows=[]
try:
 for y in (185,300,435):
  ref=next(r for r in basis['rows'] if r['y_mm']==y);xc=ref['x_center_mm'];zc=(ref['lower_cap_z_interval_mm'][1]+ref['upper_cap_z_interval_mm'][0])/2
  for o in d.Objects:
   if not hasattr(o,'Shape') or o.Shape.isNull():continue
   plane=Part.makePlane(2000,2000,App.Vector(-1000,y,1000),App.Vector(0,1,0),App.Vector(1,0,0));s=o.Shape.section(plane);assert len(s.Edges)>0
   rows.append({'y_mm':y,'object':o.Name,'display_origin_xz_mm':[xc,zc],'segments_xyz_mm':[[list(v) for v in e.discretize(Number=3)] for e in s.Edges]})
finally:App.closeDocument(d.Name)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before and len(rows)==15
out.write_text(json.dumps({'status':'NATIVE_SAVED_FIVE_BODY_SECTION_EDGE_SAMPLES_FOR_REVIEW','source_sha256':before,'rows':rows,'limits':['Native section edges sampled at three points per edge; display only','Section charts use local center origins; not aircraft datum verification'],'production_release':False},indent=2)+'\n');print('15 object/section samples; saved source unchanged')
