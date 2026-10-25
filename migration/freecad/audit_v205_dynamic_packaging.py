import FreeCAD as App, Part, math, json
from pathlib import Path
P=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v205_SYNCHRONIZED_SWEEP_CANDIDATE.FCStd")
d=App.openDocument(str(P)); fus=d.getObject('FUSELAGE_CURRENT').Shape
DX=108.7860812043256; px=504.3463093769572; py=125.20927023775282; sy=65.; xmid=457.3099792190261; horn_r=17.; yoke_w=16.; z0=5.;z1=11.
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text())
fixed=[]
for lab in ['R','L']:
 for n in [f'V204_MONO_LOWER_{lab}',f'V204_UPPER_FORK_{lab}']:
  fixed.append((n,d.getObject(n).Shape))
servo_body=d.getObject('V205_SWEEP_SERVO_BODY_REF').Shape; servo_service=d.getObject('V205_SWEEP_SERVO_SERVICE').Shape
# battery boxes proven envelope positions
bats=[]
for center in [305,340,375]: bats.append((center,Part.makeBox(106,36,25,App.Vector(center-53,-18,4.407593065391325))))

def capsule(p0,p1,w,za,zb):
 x0,y0=p0;x1,y1=p1;dx=x1-x0;dy=y1-y0;L=math.hypot(dx,dy);a=math.degrees(math.atan2(dy,dx));r=w/2
 sh=Part.makeBox(L,w,zb-za,App.Vector(0,-r,za));sh.rotate(App.Vector(),App.Vector(0,0,1),a);sh.translate(App.Vector(x0,y0,0));return sh.fuse(Part.makeCylinder(r,zb-za,App.Vector(x0,y0,za))).fuse(Part.makeCylinder(r,zb-za,App.Vector(x1,y1,za)))
def rod(a,b,r=2):
 va=App.Vector(*a);v=App.Vector(*b)-va;L=v.Length;return Part.makeCylinder(r,L,va,v.normalize())
def yoke(x):
 sh=Part.makeBox(yoke_w,136,z1-z0,App.Vector(x-yoke_w/2,-68,z0));sl=Part.makeBox(5,13,(z1-z0)+.4,App.Vector(x-2.5,7,z0-.2));sh=sh.cut(sl)
 for yy in [65,-65]:sh=sh.cut(Part.makeCylinder(1.65,6.4,App.Vector(x,yy,z0-.2)))
 return sh
# static containment
static=[]
for n in ['V205_SWEEP_SERVO_BODY_REF','V205_SWEEP_SERVO_SERVICE','V205_YOKE_MOTION_ENVELOPE']:
 sh=d.getObject(n).Shape; inter=sh.common(fus); frac=(inter.Volume/sh.Volume if sh.Volume else 0); static.append({'name':n,'inside_fraction':frac})
# battery distances to complete envelopes
battery=[]
for center,b in bats:
 for n,sh in [('servo_body',servo_body),('servo_service',servo_service),('yoke_motion',d.getObject('V205_YOKE_MOTION_ENVELOPE').Shape)]: battery.append({'battery_center':center,'target':n,'distance_mm':b.distToShape(sh)[0]})
rows=[]
for s in c['samples']:
 deg=s['sweep_deg']; x=s['slider_x_mm']-DX; yk=yoke(x)
 off=x-xmid; yp=math.sqrt(max(0,horn_r**2-off**2))
 horn=capsule((xmid,0),(x,yp),5,11.4,13.4).fuse(Part.makeCylinder(2,6.5,App.Vector(x,yp,7)))
 for sign,lab in [(1,'R'),(-1,'L')]:
  cp=(s['crank_pin_mm'][0]-DX,sign*abs(s['crank_pin_mm'][1]))
  piv=(px,sign*py); sl=(x,sign*sy)
  cr=capsule(piv,cp,14,4,9).cut(Part.makeCylinder(1.65,5.4,App.Vector(cp[0],cp[1],3.8)))
  rd=rod((cp[0],cp[1],7.5),(sl[0],sl[1],7.5))
  # rotated moving hub from 20deg base
  hub=d.getObject('V205_MOVING_HUB_'+lab).Shape.copy();hub.rotate(App.Vector(px,sign*py,0),App.Vector(0,0,1),-sign*(deg-20))
  for pname,sh in [('yoke',yk),('horn',horn),('crank',cr),('rod',rd),('hub',hub)]:
   for fn,fx in fixed:
    # hub vs forks should maintain designed axial gap; crank/rod/yoke should not hit any fixed structure
    dist=sh.distToShape(fx)[0]; rows.append({'sweep_deg':deg,'side':lab,'part':pname,'target':fn,'distance_mm':dist})
   if pname in ['yoke','horn','rod']:
    for bc,b in bats: rows.append({'sweep_deg':deg,'side':lab,'part':pname,'target':f'battery_{bc}','distance_mm':sh.distToShape(b)[0]})
   if pname in ['yoke','horn','rod','crank']:
    rows.append({'sweep_deg':deg,'side':lab,'part':pname,'target':'servo_body','distance_mm':sh.distToShape(servo_body)[0]})
# collapse duplicate yoke/horn checks per sides okay
crit=min(rows,key=lambda r:r['distance_mm']); bad=[r for r in rows if r['distance_mm']<0.05]
res={'status':'V205_DYNAMIC_PACKAGING_SCREEN_2DEG','static_containment':static,'battery_static':battery,'minimum_dynamic_distance':crit,'zero_or_near_hits':bad[:100],'near_hit_count':len(bad),'gates':{'servo_body_contained':next(x for x in static if x['name']=='V205_SWEEP_SERVO_BODY_REF')['inside_fraction']>0.999,'servo_service_contained':next(x for x in static if x['name']=='V205_SWEEP_SERVO_SERVICE')['inside_fraction']>0.999,'battery_all_positions_clear':all(x['distance_mm']>1 for x in battery),'dynamic_non_joint_clearance_positive':len(bad)==0,'continuous_2deg_sampled':True,'servo_model_selected':False,'material_verified':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v205_dynamic_packaging_audit.json").write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
