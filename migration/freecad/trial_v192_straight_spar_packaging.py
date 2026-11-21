from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';basis=R/'analysis/v192_spar_depth_envelope.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(src);b=json.loads(basis.read_text());assert b['source_sha256']==before
out=R/'analysis/v192_straight_spar_packaging_trial.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
def point(y):
 r=next(r for r in b['rows'] if r['y_mm']==y and r['fraction_of_section_X_bounds']==.35)
 return App.Vector(r['x_mm'],y,(r['z_bottom_mm']+r['z_top_mm'])/2)
a=point(155);z=point(440);v=z-a;tool=Part.makeCylinder(2,v.Length,a,v);assert tool.isValid() and len(tool.Solids)==1
stage('open');d=App.openDocument(str(src))
try:
 w=d.getObject('WING_R').Shape;stage('outside_cut_start');outside=tool.cut(w).Volume;stage('outside_cut_done',outside_volume_mm3=outside)
 stage('boundary_distance_start');dist,pts,info=tool.Shells[0].distToShape(w.Shells[0]);stage('boundary_distance_done',distance_mm=dist)
finally:App.closeDocument(d.Name)
assert sha(src)==before
r={'status':'STRAIGHT_4MM_SOLID_CYLINDER_PACKAGING_STUDY_ONLY','source_sha256':before,'depth_basis_sha256':sha(basis),'axis_start_mm':list(a),'axis_end_mm':list(z),'axis_length_mm':v.Length,'diameter_mm':4,'candidate_volume_mm3':tool.Volume,'outside_wing_volume_mm3':outside,'native_boundary_distance_mm':dist,'closest_point_pairs_mm':[[list(p),list(q)] for p,q in pts],'inside_outer_reference':outside<1e-7,'limits':['Solid cylinder is a packaging envelope, not selected carbon tube/rod or manufactured spar','Endpoints from 35-percent section X bounds and midheight; straight axis between them','Distance only to outer wing; skin, adhesive, tolerance, ribs and other hardware consume clearance','No root bridge, bearing attachment, buckling, stress, stiffness, mass, proof test or structural release','No master change or production part generated'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
