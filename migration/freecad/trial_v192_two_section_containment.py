"""Two-section numerical cavity trial with persistent stage log; no boolean or master write."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];source=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(source.read_bytes()).hexdigest();base=R/'analysis/v192_two_section_containment';log=base.with_suffix('.jsonl');out=base.with_suffix('.json');assert not log.exists() and not out.exists();start=time.time()
def stage(name,**details):
 with log.open('a',encoding='utf-8') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**details))+'\n');h.flush()
 print(name,flush=True)
r=dict(status='TWO_SECTION_CONTAINMENT_TRIAL_ONLY',source_sha256=before,stations_y_mm=[220,260],planar_inset_mm=.4,print_release=False,flight_release=False)
stage('open_source');d=App.openDocument(str(source))
try:
 wing=d.getObject('WING_R').Shape;wires=[]
 for y in r['stations_y_mm']:
  stage('slice_start',y_mm=y);ws=wing.slice(App.Vector(0,1,0),y);assert len(ws)==1
  stage('offset_start',y_mm=y,source_edges=len(ws[0].Edges));inset=ws[0].makeOffset2D(-.4,0,False,False,False);assert len(inset.Wires)==1
  wire=inset.Wires[0];stage('offset_done',y_mm=y,edges=len(wire.Edges),closed=wire.isClosed());wires.append(wire)
 stage('loft_start',edge_counts=[len(w.Edges) for w in wires]);cavity=Part.makeLoft(wires,True,True);stage('loft_returned',faces=len(cavity.Faces),solids=len(cavity.Solids))
 stage('validity_start');valid=cavity.isValid();stage('validity_done',valid=valid)
 r.update(valid=valid,solids=len(cavity.Solids),faces=len(cavity.Faces),volume_mm3=cavity.Volume)
 assert valid and len(cavity.Solids)==1
 stage('containment_cut_start');outside=cavity.cut(wing);stage('containment_cut_returned',outside_volume_mm3=outside.Volume)
 r.update(outside_volume_mm3=outside.Volume,contained_within_1e_6_mm3=outside.Volume<=1e-6)
except Exception as err:r['status']='TWO_SECTION_TRIAL_FAILED';r['error']=str(err);stage('exception',error=str(err))
finally:App.closeDocument(d.Name)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before;r['elapsed_seconds']=time.time()-start
r['limits']=['Containment boolean only; no shell subtraction or export attempted.','No full-span cavity, uniform normal wall, structural thickness or manufacturing qualification.','Master unchanged; no native geometry export produced.']
out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');stage('complete');print(json.dumps(r),flush=True)

