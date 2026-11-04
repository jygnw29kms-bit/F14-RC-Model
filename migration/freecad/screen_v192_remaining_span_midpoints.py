"""Adaptive planar MIDPOINT screen over limited span; not a thickness certification."""
from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(src.read_bytes()).hexdigest();out=R/'analysis/v192_adaptive_remaining_midpoint_screen.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def emit(row):
 with log.open('a') as h:h.write(json.dumps(row)+'\n')
 print(json.dumps(row),flush=True)
d=App.openDocument(str(src));trials=[];accepted=[];unresolved=[];cache={};stopped=False
try:
 wing=d.getObject('WING_R').Shape
 def sections(shape,y):
  ws=shape.slice(App.Vector(0,1,0),y)
  if len(ws)==1 and ws[0].isClosed() and ws[0].isValid():return ws
  plane=Part.makePlane(2000,2000,App.Vector(-1000,y,1000),App.Vector(0,1,0),App.Vector(1,0,0))
  section=shape.section(plane);groups=Part.sortEdges(section.Edges)
  if len(groups)!=1:raise RuntimeError('Fallback requires exactly one edge group: '+str(len(groups)))
  w=Part.Wire(groups[0])
  if not w.isClosed() or not w.isValid():raise RuntimeError('Fallback wire not closed/valid')
  emit(dict(stage='explicit_plane_fallback',y_mm=y,edge_count=len(w.Edges)))
  return [w]
 def wire(y):
  if y not in cache:
   ws=sections(wing,y);assert len(ws)==1
   off=ws[0].makeOffset2D(-.43,0,False,False,False);assert len(off.Wires)==1;cache[y]=off.Wires[0]
  return cache[y]
 queue=[(180,220,0),(360,380,0),(380,420,0),(420,440,0)]
 while queue:
  if len(trials)>=48 or time.time()-start>180:
   unresolved.extend([dict(y_start=a,y_end=b,reason='work_budget') for a,b,_ in queue]);stopped=True;break
  a,b,depth=queue.pop(0);mid=(a+b)/2
  emit(dict(stage='interval_start',a=a,b=b))
  try:
   loft=Part.makeLoft([wire(a),wire(b)],True,True);assert loft.isValid() and len(loft.Solids)==1
   outer=sections(wing,mid);inner=sections(loft,mid);assert len(outer)==len(inner)==1
   gap=inner[0].distToShape(outer[0])[0];outside=Part.Face(inner[0]).cut(Part.Face(outer[0])).Area
   row=dict(y_start=a,y_end=b,midpoint_y=mid,depth=depth,midpoint_planar_gap_mm=gap,midpoint_outside_area_mm2=outside)
   row['midpoint_screen_pass']=gap>=.42 and outside<1e-6
   if row['midpoint_screen_pass']:accepted.append(row)
   elif depth<3 and b-a>5:queue[0:0]=[(a,mid,depth+1),(mid,b,depth+1)]
   else:unresolved.append(dict(**row,reason='refinement_limit'))
  except Exception as e:row=dict(y_start=a,y_end=b,error=str(e));unresolved.append(dict(**row,reason='native_error'))
  trials.append(row);emit(dict(stage='interval_done',**row))
finally:App.closeDocument(d.Name)
assert before==hashlib.sha256(src.read_bytes()).hexdigest()
r=dict(status='ADAPTIVE_REMAINING_PLANAR_MIDPOINT_STUDY_ONLY',source_sha256=before,span_studied_mm=[180,440],planar_inset_mm=.43,numerical_midpoint_gap_threshold_mm=.42,trials=trials,accepted_intervals=accepted,unresolved_intervals=unresolved,budget_exhausted=stopped,elapsed_seconds=time.time()-start,
 limits=['Threshold is a numerical refinement criterion, not a structural or printer requirement.','Only interval midpoints checked; no error bound between samples or minimum normal wall proof.','No 3D containment or boundary-distance screen, combined cavity, shell, export or master update.','Root/tip outside Y180..440 excluded; this is not a full-span wing shell.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n');emit(dict(stage='complete',trials=len(trials),accepted=len(accepted),unresolved=len(unresolved)))

