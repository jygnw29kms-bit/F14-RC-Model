from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_adapter_face_topology_inspection.json';a=json.loads(p.read_text());assert a['source_sha256']==hashlib.sha256((R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd').read_bytes()).hexdigest()
rows=[]
for obj in a['rows']:
 faces=obj['faces'];fan=next(f for f in faces if f['surface']=='Plane' and len(f['edge_radii_mm'])==2);radii=sorted(fan['edge_radii_mm']);groups=[]
 for radius in radii:
  seed=[f['index'] for f in faces if f['surface']!='Plane' and f['edge_radii_mm']==[radius]];assert len(seed)==1
  group=set(seed)
  while True:
   extended=group|{k for pair in obj['curved_face_pairs'] if pair['shared_edges']>0 and group.intersection(pair['faces']) for k in pair['faces']}
   if extended==group:break
   group=extended
  groups.append(group)
 assert not groups[0].intersection(groups[1]) and len(groups[0]|groups[1])==4
 pairs=[p for p in obj['curved_face_pairs'] if any(i in groups[0] for i in p['faces']) and any(i in groups[1] for i in p['faces'])];assert len(pairs)==4
 minimum=min(p['distance_mm'] for p in pairs);gap=radii[1]-radii[0]
 rows.append(dict(object=obj['object'],inner_connected_faces=sorted(groups[0]),outer_connected_faces=sorted(groups[1]),minimum_between_curved_face_groups_mm=minimum,fan_radial_gap_mm=gap,conditional_0p8mm_distance_screen=minimum>=.8 and gap>=.8))
r=dict(status='CURRENT_V192_CONNECTED_FACE_GROUP_DISTANCE_SCREEN',source_sha256=a['source_sha256'],topology_audit_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,limits=['Groups identified from fan radii and shared-edge connectivity, not merely face orientation.','Minimum face-group separation and fan radial gap only; no complete normal wall field or structural qualification.','No physical printing, flow, strength or flight test; no whole-model wall approval.'],print_release=False,flight_release=False)
(R/'analysis/v192_adapter_connected_group_distance_screen.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows))
