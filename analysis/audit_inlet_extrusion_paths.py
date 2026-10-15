"""Audit commanded endpoint closure; no physical seam-strength claim."""
from pathlib import Path
import zipfile,re,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1]
archive=ROOT/'manufacturing/candidates/inlet_slice_trial_20261015/F14_INLETS_SLICED_TRIAL_NOT_RELEASED.3mf'
with zipfile.ZipFile(archive) as z: lines=z.read('Metadata/plate_1.gcode').decode().splitlines()
x=y=None;layer=0;obj=None;relative_e=False;absolute_xy=True;active=None;paths=[]
def finish():
 global active
 if active:
  active['endpoint_gap_mm']=math.dist(active.pop('start'),active.pop('end'));paths.append(active);active=None
for line in lines:
 m=re.match(r'; layer num/total_layer_count: (\d+)/(\d+)',line)
 if m:finish();layer=int(m.group(1))
 m=re.match(r'; start printing object, unique label id: (\d+)',line)
 if m:finish();obj=m.group(1)
 if line.startswith('; stop printing object'):finish();obj=None
 command=line.split(';')[0].strip(); op=command.split(' ')[0] if command else ''
 if op=='M83':relative_e=True
 if op=='M82':relative_e=False
 if op=='G90':absolute_xy=True
 if op=='G91':absolute_xy=False
 if op not in ('G0','G1','G2','G3'):continue
 fields={k:float(v) for k,v in re.findall(r'([XYZE])([-+]?\d*\.?\d+)',command)}
 old=(x,y)
 if 'X' in fields:x=fields['X'] if absolute_xy else (x or 0)+fields['X']
 if 'Y' in fields:y=fields['Y'] if absolute_xy else (y or 0)+fields['Y']
 moving='X' in fields or 'Y' in fields
 printing=layer and obj and relative_e and fields.get('E',0)>0 and moving
 if printing:
  if None in old or x is None or y is None:raise ValueError('Unknown XY')
  if active is None:active=dict(layer=layer,object_id=obj,start=old,end=(x,y),moves=0)
  active['end']=(x,y);active['moves']+=1
 elif moving or fields.get('E',0)<0:finish()
finish()
gaps=[p['endpoint_gap_mm'] for p in paths]
result=dict(status='GCODE_CONTIGUOUS_EXTRUSION_ENDPOINT_CLOSURE_AUDIT',archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),path_count=len(paths),maximum_endpoint_gap_mm=max(gaps),paths_above_0p05mm=sum(g>.05 for g in gaps),paths_above_0p2mm=sum(g>.2 for g in gaps),paths_above_0p5mm=sum(g>.5 for g in gaps),paths=paths,arc_geometry_self_intersections_verified=False,bead_overlap_or_seam_strength_verified=False,physical_print_verified=False,print_release=False)
out=ROOT/'manufacturing/candidates/inlet_slice_trial_20261015/path_audit';out.mkdir(exist_ok=True);(out/'extrusion_path_audit.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='paths'})
