"""Local section-spacing convergence experiment; planar gap only, no shell output."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];f=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(f.read_bytes()).hexdigest();out=R/'analysis/v192_dense_local_cavity_gap_trial.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
stage('open');d=App.openDocument(str(f));r=dict(status='DENSE_LOCAL_PLANAR_GAP_TRIAL_ONLY',source_sha256=before,station_y_mm=[220,230,240,250,260],inset_mm=.4,print_release=False,flight_release=False)
try:
 wing=d.getObject('WING_R').Shape;wires=[]
 for y in r['station_y_mm']:
  stage('offset',y_mm=y);ws=wing.slice(App.Vector(0,1,0),y);assert len(ws)==1
  off=ws[0].makeOffset2D(-.4,0,False,False,False);assert len(off.Wires)==1;wires.append(off.Wires[0])
 stage('loft_start');c=Part.makeLoft(wires,True,True);stage('loft_done',faces=len(c.Faces))
 stage('validity_start');r['valid']=c.isValid();r['solids']=len(c.Solids);stage('validity_done');assert r['valid'] and r['solids']==1
 rows=[]
 for y in (225,230,235,240,245,250,255):
  stage('sample',y_mm=y);outer=wing.slice(App.Vector(0,1,0),y);inner=c.slice(App.Vector(0,1,0),y);assert len(outer)==len(inner)==1
  rows.append(dict(y_mm=y,minimum_planar_boundary_gap_mm=inner[0].distToShape(outer[0])[0],inner_outside_outer_area_mm2=Part.Face(inner[0]).cut(Part.Face(outer[0])).Area))
 r['rows']=rows;r['sampled_minimum_gap_mm']=min(x['minimum_planar_boundary_gap_mm'] for x in rows)
except Exception as err:r['status']='DENSE_LOCAL_TRIAL_FAILED';r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(f.read_bytes()).hexdigest();r['elapsed_seconds']=time.time()-start
r['limits']=['Only local 40 mm span numerical spacing experiment; 0.4 mm not a selected structural thickness.','Sampled planar boundary gap is not a continuous three-dimensional normal thickness field.','No 3D containment boolean, shell subtraction or geometry export performed.','Whole wing, joints, loads, OML registration and print qualification remain open.']
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
