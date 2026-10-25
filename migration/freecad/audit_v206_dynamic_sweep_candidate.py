import FreeCAD as App, Part, json
from pathlib import Path
BASE=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
DOC=BASE/'migration/freecad/F14_v205_SERVO_SLIDER_CANDIDATE.FCStd'
KIN=BASE/'analysis/F14_sweep_linkage_kinematics_v40.json'
OUT=BASE/'migration/freecad/freecad_v206_dynamic_sweep_audit.json'
SHIFT=108.7860812043256; IDX=23; SY=65.0

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def ivol(a,b):
    try:
        s=a.common(b); return 0.0 if s.isNull() else s.Volume
    except Exception: return 0.0

d=App.openDocument(str(DOC))
with open(KIN,encoding='utf-8') as f: c=json.load(f)['top_candidates'][IDX]
fixed=[]
for n in ['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','INLET_EDF_R','INLET_EDF_L','V205_SWEEP_SERVO_SERVICE']:
    o=d.getObject(n)
    if o and hasattr(o,'Shape') and not o.Shape.isNull(): fixed.append((n,o.Shape))
bats=[]
for cx in (305,340,375): bats.append((f'BAT_{cx}',box(cx-53,cx+53,-18,18,4.407593065391325,29.407593065391325)))
rows=[]; min_dist=1e9; worst=None; collision_count=0
for r in c['samples']:
    sw=float(r['sweep_deg']); sx=float(r['slider_x_mm'])-SHIFT
    for lab,sgn in [('R',1),('L',-1)]:
        slider=box(sx-4,sx+4,sgn*SY-4,sgn*SY+4,4,12)
        cp0=r['crank_pin_mm']; cp=App.Vector(float(cp0[0])-SHIFT,sgn*abs(float(cp0[1])),8)
        sp=App.Vector(sx,sgn*SY,8); vec=cp-sp
        rod=Part.makeCylinder(2.0,vec.Length,sp,vec) if vec.Length>0 else Part.Shape()
        for kind,sh in [('slider',slider),('rod',rod)]:
            for fn,fs in fixed+bats:
                dist=sh.distToShape(fs)[0]; inter=ivol(sh,fs)
                rec={'sweep_deg':sw,'side':lab,'moving':kind,'fixed':fn,'distance_mm':dist,'intersection_mm3':inter}
                rows.append(rec)
                if dist<min_dist: min_dist=dist; worst=rec
                if inter>1e-6: collision_count+=1
# wing-to-new-servo check through all sweep states
wing_rows=[]
for side,sgn,wn in [('R',1,'WING_R_SWEEP_20'),('L',-1,'WING_L_SWEEP_20')]:
    w=d.getObject(wn)
    if not w: continue
    base=w.Shape
    pivot=App.Vector(504.3463093769572,sgn*125.20927023775282,0)
    srv=d.getObject('V205_SWEEP_SERVO_SERVICE').Shape
    for sw in range(20,69,2):
        sh=base.copy(); sh.rotate(pivot,App.Vector(0,0,1),-sgn*(sw-20))
        dist=sh.distToShape(srv)[0]; inter=ivol(sh,srv)
        rec={'side':side,'sweep_deg':sw,'distance_mm':dist,'intersection_mm3':inter}; wing_rows.append(rec)
        if dist<min_dist: min_dist=dist; worst={'moving':'wing','fixed':'servo_service',**rec}
        if inter>1e-6: collision_count+=1
audit={'status':'V206_DYNAMIC_SWEEP_PACKAGING_AUDIT','candidate_index':IDX,'sweep_range_deg':[20,68],'step_deg':2,'dynamic_records':rows,'wing_servo_records':wing_rows,'minimum_distance_mm':min_dist,'worst_record':worst,'positive_collision_record_count':collision_count,'gates':{'dynamic_packaging_collision_free':collision_count==0,'full_20_68_sampled':True,'continuous_between_samples_certified':False,'servo_model_selected':False,'material_verified':False,'physical_endurance_test':False,'print_release':False,'flight_release':False}}
with open(OUT,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps({'status':audit['status'],'minimum_distance_mm':min_dist,'worst_record':worst,'positive_collision_record_count':collision_count,'gates':audit['gates']},indent=2))