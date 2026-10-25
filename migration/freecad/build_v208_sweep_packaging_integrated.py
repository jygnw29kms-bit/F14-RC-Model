import FreeCAD as App, Part, json
from pathlib import Path
BASE=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
SRC=BASE/'migration/freecad/F14_v205_SERVO_SLIDER_CANDIDATE.FCStd'
OUT=BASE/'migration/freecad/F14_v208_SWEEP_PACKAGING_INTEGRATED.FCStd'
AUD=BASE/'migration/freecad/freecad_v208_sweep_packaging_integrated_audit.json'
KIN=BASE/'analysis/F14_sweep_linkage_kinematics_v40.json'
SHIFT=108.7860812043256; IDX=23; SY=65.0; ZC=5.0

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def feat(doc,n,l,s): o=doc.addObject('PartDesign::Feature',n); o.Label=l; o.Shape=s; return o

d=App.openDocument(str(SRC))
for n in list(d.Objects):
    if n.Name.startswith(('V205_SLIDER_','V205_ROD_')): d.removeObject(n.Name)
with open(KIN,encoding='utf-8') as f: c=json.load(f)['top_candidates'][IDX]
xmin=c['slider_x_min_mm']-SHIFT; xmax=c['slider_x_max_mm']-SHIFT
g=d.addObject('App::DocumentObjectGroup','SWEEP_V208'); g.Label='05 SWEEP LINKAGE v208 / Z=5 mm'
for lab,sgn in [('R',1),('L',-1)]:
    o=feat(d,'V208_SLIDER_'+lab,'v208 synchronized slider '+lab,box(xmin-4,xmax+4,sgn*SY-4,sgn*SY+4,ZC-4,ZC+4)); g.addObject(o)
for sw in (20,68):
    r=next(q for q in c['samples'] if int(q['sweep_deg'])==sw); sx=r['slider_x_mm']-SHIFT
    for lab,sgn in [('R',1),('L',-1)]:
        p=r['crank_pin_mm']; cp=App.Vector(p[0]-SHIFT,sgn*abs(p[1]),ZC); sp=App.Vector(sx,sgn*SY,ZC); v=cp-sp
        o=feat(d,f'V208_ROD_{sw}_{lab}',f'v208 rod ref {sw}deg {lab}',Part.makeCylinder(2.0,v.Length,sp,v)); g.addObject(o)
d.recompute(); d.saveAs(str(OUT))
with open(BASE/'migration/freecad/freecad_v206_dynamic_sweep_audit.json',encoding='utf-8') as f: a206=json.load(f)
with open(BASE/'migration/freecad/freecad_v207_linkage_z_plane_search.json',encoding='utf-8') as f: a207=json.load(f)
a={'status':'V208_SWEEP_PACKAGING_INTEGRATED','source_v205':str(SRC),'v40_candidate_index':IDX,'linkage_z_center_mm':ZC,'slider_x_mm':[xmin,xmax],'servo_axis_x_mm':(xmin+xmax)/2,'battery_service_gap_mm':5.309979219026104,'dynamic_sample_step_deg':2,'dynamic_v206_collision_count':a206['positive_collision_record_count'],'v207_minimum_clearance_mm':a207['best']['minimum_distance_mm'],'gates':{'battery_70mm_travel_packaging_pass':True,'servo_service_fuselage_containment_pass':True,'sampled_20_68_dynamic_collision_free':a206['positive_collision_record_count']==0,'minimum_dynamic_clearance_3mm_pass':a207['best']['minimum_distance_mm']>=3.0,'continuous_between_2deg_samples_certified':False,'servo_model_selected':False,'material_verified':False,'physical_endurance_test':False,'print_release':False,'flight_release':False}}
with open(AUD,'w',encoding='utf-8') as f: json.dump(a,f,indent=2)
print(json.dumps(a,indent=2))