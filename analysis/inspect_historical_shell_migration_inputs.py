"""Inspect shell migration inputs without fetching LFS or opening CAD."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
selected=list(R.glob('**/F14_HOLLOW_WING_SEGMENTS_CHECKPOINT_v57.f3d'))
selected+=list(R.glob('**/F14_SOURCE_WING_SHELL_FEASIBILITY_v53.f3d'))
rows=[]
for p in sorted(selected):
 raw=p.read_bytes(); pointer=raw.startswith(b'version https://git-lfs.github.com/spec/v1')
 row={'path':p.relative_to(R).as_posix(),'local_bytes':len(raw),'local_sha256':hashlib.sha256(raw).hexdigest(),'is_lfs_pointer':pointer,'native_geometry_opened':False}
 if pointer:
  txt=raw.decode('ascii');row['expected_lfs_oid_sha256']=re.search(r'oid sha256:([0-9a-f]{64})',txt).group(1);row['expected_payload_bytes']=int(re.search(r'size (\d+)',txt).group(1))
 rows.append(row)
assert rows
result={'status':'LEGACY_SHELL_MIGRATION_INPUT_AVAILABILITY_ONLY','files':rows,
 'all_selected_geometry_payloads_locally_present':all(not r['is_lfs_pointer'] for r in rows),
 'next_steps':['Fetch only the exact historical payload if a legacy read-only comparison is necessary; never install historical cores.',
 'Prefer FreeCAD reconstruction from verified source sections. A Fusion archive is not a neutral BREP import.',
 'Do not interpret matching historical bounding boxes as current shell geometry or valid joints.'],
 'native_execution_performed':False,'print_release':False,'flight_release':False}
(R/'analysis/historical_shell_migration_input_availability.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'selected':len(rows),'pointers':sum(r['is_lfs_pointer'] for r in rows)}))
