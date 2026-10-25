import json
p=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/F14_sweep_linkage_kinematics_v40.json"
d=json.load(open(p,encoding='utf-8'))
print('keys',list(d.keys()))
print('candidate_count_field',d.get('candidate_count'))
print('candidates type',type(d.get('candidates')).__name__, len(d.get('candidates',[])) if isinstance(d.get('candidates'),list) else None)
DX=108.7860812043256
rows=[]
for i,c in enumerate(d.get('top_candidates',[])):
    mid=(c['slider_x_min_mm']+c['slider_x_max_mm'])/2-DX
    service_start=mid-24.0
    gap=service_start-428.0
    rows.append({'index':i,'battery_service_gap_mm':gap,'score':c['score'],'slider_mid_current_mm':mid,'travel_mm':c['slider_travel_mm'],'min_arm_mm':c['min_linkage_moment_arm_mm'],'slider_y_mm':c['slider_attach_y_mm'],'slider_x20_old_mm':c['slider_x_at_20_mm'],'candidate':c})
rows.sort(key=lambda r:(r['battery_service_gap_mm'],r['score']),reverse=True)
for r in rows[:20]:
    print({k:r[k] for k in ['index','battery_service_gap_mm','score','slider_mid_current_mm','travel_mm','min_arm_mm','slider_y_mm','slider_x20_old_mm']})
open(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_battery_clearance_rank.json",'w',encoding='utf-8').write(json.dumps({'status':'V40_BATTERY_CLEARANCE_RANK','rows':rows},indent=2))
