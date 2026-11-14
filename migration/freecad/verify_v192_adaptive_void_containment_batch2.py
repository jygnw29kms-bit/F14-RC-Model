"""Budgeted read-only containment of saved adaptive void tools."""
from pathlib import Path
import FreeCAD as App,json,hashlib,time
R=Path(__file__).resolve().parents[2];src=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';tools=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();build=json.loads((R/'analysis/v192_adaptive_void_segments_build.json').read_text());assert sha(src)==build['source_sha256'] and sha(tools)==build['output_sha256']
out=R/'analysis/v192_adaptive_void_containment_batch2.json';log=out.with_suffix('.jsonl');assert not out.exists() and not log.exists();start=time.time()
def stage(name,**kw):
 with log.open('a') as h:h.write(json.dumps(dict(stage=name,elapsed_seconds=time.time()-start,**kw))+'\n')
 print(name,flush=True)
a=App.openDocument(str(src));b=App.openDocument(str(tools));rows=[];remaining=[]
try:
 wing=a.getObject('WING_R').Shape
 for item in [row for row in build['rows'] if row['index'] in (15,16)]:
  index=item['index']
  if time.time()-start>150:remaining.append(index);continue
  stage('segment_start',index=index);obj=b.getObject('VOID_TOOL_'+str(index));assert obj is not None;s=obj.Shape
  valid=s.isValid();assert valid and len(s.Solids)==1
  stage('containment_start',index=index);outside=s.cut(wing);volume=outside.Volume
  row=dict(index=index,object=obj.Name,valid=valid,solids=len(s.Solids),outside_volume_mm3=volume,contained_within_1e_6_mm3=volume<=1e-6);rows.append(row);stage('segment_done',**row)
finally:App.closeDocument(b.Name);App.closeDocument(a.Name)
assert sha(src)==build['source_sha256'] and sha(tools)==build['output_sha256']
r=dict(status='SAVED_ADAPTIVE_VOID_CONTAINMENT_BATCH_ONLY',source_sha256=sha(src),tools_sha256=sha(tools),rows=rows,remaining_indices=remaining,elapsed_seconds=time.time()-start,limits=['Containment of individual saved tools only; no fusion, subtraction or boundary clearance verification.','No full-span wing shell or structural/printing qualification.'],print_release=False,flight_release=False)
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete',checked=len(rows),remaining=remaining);print(json.dumps({'checked':len(rows),'remaining':remaining,'all_checked_contained':all(x['contained_within_1e_6_mm3'] for x in rows)}))

