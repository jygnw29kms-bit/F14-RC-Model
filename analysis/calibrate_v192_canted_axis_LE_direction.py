"""Direction-only LE chord-line calibration; no physical axis placement or CAD change."""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];source=R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json';j=json.loads(source.read_text());first,last=j['sections'][0],j['sections'][-1]
def le(section):
 q=section['ordinates_xc_upper_lower'][0];assert q[0]==0
 return [section['leading_edge_fs_in'],section['wbl_in'],section['reference_vertical_wl_in']+q[1]*(section['trailing_edge_fs_in']-section['leading_edge_fs_in'])]
a,b=le(first),le(last);v=[y-x for x,y in zip(a,b)];baseline=math.degrees(math.atan2(v[0],v[1]));k=[0,math.sin(math.radians(1.5)),math.cos(math.radians(1.5))]
def projected_angle(rotation_deg):
 t=math.radians(rotation_deg);c,s=math.cos(t),math.sin(t);dot=sum(x*y for x,y in zip(v,k));cross=[k[1]*v[2]-k[2]*v[1],k[2]*v[0]-k[0]*v[2],k[0]*v[1]-k[1]*v[0]]
 w=[v[i]*c+cross[i]*s+k[i]*dot*(1-c) for i in range(3)]
 return math.degrees(math.atan2(w[0],w[1]))
rows=[]
for nominal in (20,30,40,50,54,60,68):
 target=baseline+(nominal-20);uncalibrated=-(nominal-20);lo,hi=-60.,1.
 assert projected_angle(lo)>=target>=projected_angle(hi)
 for _ in range(70):
  mid=(lo+hi)/2
  if projected_angle(mid)>target:lo=mid
  else:hi=mid
 solved=(lo+hi)/2
 rows.append(dict(nominal_label_deg=nominal,target_projected_root_tip_LE_angle_deg=target,uncalibrated_rotation_deg=uncalibrated,uncalibrated_projected_angle_deg=projected_angle(uncalibrated),calibrated_rotation_deg=solved,rotation_correction_deg=solved-uncalibrated,residual_deg=projected_angle(solved)-target))
assert max(abs(x['residual_deg']) for x in rows)<1e-10
r=dict(status='SOURCE_LE_ENDPOINT_DIRECTION_CALIBRATION_ONLY',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_LE_points_FS_BL_WL_in=[a,b],source_projected_root_tip_LE_angle_deg=baseline,assumed_right_axis_unit_direction=k,rows=rows,
 limits=['Uses root-to-tip leading-edge endpoint line; not a certified local whole-edge sweep definition.','Targets preserve source baseline angle plus nominal increment; source baseline is reported, not forced to exactly20deg.','Axis direction only: translation cancels; pivot waterline and actual axis-line placement remain unverified.','No native CAD, body/glove collision, hardware, or manufacturing result produced.'],master_change_allowed=False,production_release=False)
(R/'analysis/v192_canted_axis_LE_direction_calibration.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'baseline_deg':baseline,'case68':rows[-1]}))
