"""Compare historical hollow-wing envelopes to current datums; not a BREP equivalence test."""
from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[1]
paths={
 'old_shell':R/'legacy/fusion-review-only/RC-F14-Tomcat_Fusion/Exports/Current/source_shell_v53/F14_v57_hollow_segment_audit.json',
 'datum':R/'migration/freecad/freecad_v191_datum_audit.json',
 'current':R/'migration/freecad/CURRENT.json'}
data={k:json.loads(p.read_text(encoding='utf-8-sig')) for k,p in paths.items()}
assert data['current']['current_revision']=='v192'
shift=data['datum']['source_wl_to_local_z_shift_mm']
rows=[]
for side in ('R','L'):
 parts=[p for p in data['old_shell']['segments'] if '_WING_'+side+'_' in p['name']]
 assert len(parts)==2
 current=next(x for x in data['datum']['records'] if x['name']=='WING_'+side)
 transformed={axis:[min(p['bounds_mm'][axis][0] for p in parts)+(shift if axis=='z' else 0),
                    max(p['bounds_mm'][axis][1] for p in parts)+(shift if axis=='z' else 0)] for axis in ('x','y','z')}
 delta={axis:[transformed[axis][i]-current['bounds_mm'][axis][i] for i in (0,1)] for axis in ('x','y','z')}
 rows.append(dict(side=side,historical_parts=[p['name'] for p in parts],
                  translated_historical_union_bounds_mm=transformed,current_v191_wing_bounds_mm=current['bounds_mm'],
                  bound_deltas_mm=delta,max_abs_bound_delta_mm=max(abs(v) for pair in delta.values() for v in pair)))
result=dict(status='HISTORICAL_SHELL_ENVELOPE_TRANSFER_SCREEN_ONLY',
 input_sha256={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},
 applied_z_translation_mm=shift,rows=rows,
 limits=['Bounding boxes alone cannot establish matching outer surfaces, wall thickness or solid validity.',
 'v191 datum report is historical evidence; current v192 BREP equivalence has not been executed.',
 'No historical shell imported, no old core installed, no current geometry changed.',
 'Historical NO_JOINTS candidates lack validated joining and continuous load paths.',
 'Reuse requires native surface comparison, wall checks, joint design and current slicer checks.'],
 reuse_authorized_by_this_screen=False,print_release=False,flight_release=False)
out=R/'analysis/historical_wing_shell_datum_transfer_screen.json'
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
