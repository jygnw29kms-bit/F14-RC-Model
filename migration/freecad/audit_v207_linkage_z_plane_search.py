import FreeCAD as App, Part, json
from pathlib import Path
BASE=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
D=App.openDocument(str(BASE/'migration/freecad/F14_v205_SERVO_SLIDER_CANDIDATE.FCStd'))
with open(BASE/'analysis/F14_sweep_linkage_kinematics_v40.json',encoding='utf-8') as f: C=json.load(f)['top_candidates'][23]
SHIFT=108.7860812043256; SY=65.0

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def iv(a,b):
    try:
        s=a.common(b); return 0 if s.isNull() else s.Volume
    except: return 0
fixed=[]
for n in ['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','INLET_EDF_R','INLET_EDF_L','V205_SWEEP_SERVO_SERVICE']:
    o=D.getObject(n)
    if o and hasattr(o,'Shape') and not o.Shape.isNull(): fixed.append((n,o.Shape))
bats=[(f'BAT_{cx}',box(cx-53,cx+53,-18,18,4.407593065391325,29.407593065391325)) for cx in (305,340,375)]
results=[]
for zc in (5.0,6.0,7.0,8.0,9.0):
    mind=1e9; worst=None; hits=0
    for r in C['samples']:
        sw=float(r['sweep_deg']); sx=float(r['slider_x_mm'])-SHIFT
        for lab,sgn in [('R',1),('L',-1)]:
            slider=box(sx-4,sx+4,sgn*SY-4,sgn*SY+4,zc-4,zc+4)
            p0=r['crank_pin_mm']; cp=App.Vector(float(p0[0])-SHIFT,sgn*abs(float(p0[1])),zc); sp=App.Vector(sx,sgn*SY,zc); v=cp-sp
            rod=Part.makeCylinder(2.0,v.Length,sp,v)
            for kind,sh in [('slider',slider),('rod',rod)]:
                for fn,fs in fixed+bats:
                    dist=sh.distToShape(fs)[0]; inter=iv(sh,fs)
                    if dist<mind: mind=dist; worst={'z_center_mm':zc,'sweep_deg':sw,'side':lab,'moving':kind,'fixed':fn,'distance_mm':dist,'intersection_mm3':inter}
                    if inter>1e-6: hits+=1
    results.append({'z_center_mm':zc,'minimum_distance_mm':mind,'worst':worst,'collision_records':hits})
valid=[r for r in results if r['collision_records']==0]
best=max(valid,key=lambda x:x['minimum_distance_mm']) if valid else None
out={'status':'V207_LINKAGE_Z_PLANE_SEARCH','results':results,'best':best,'gates':{'zero_collision_plane_found':best is not None,'target_min_clearance_1p5mm_pass':bool(best and best['minimum_distance_mm']>=1.5),'print_release':False,'flight_release':False}}
with open(BASE/'migration/freecad/freecad_v207_linkage_z_plane_search.json','w',encoding='utf-8') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))