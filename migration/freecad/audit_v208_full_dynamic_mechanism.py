import FreeCAD as App,Part,json,math
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v208_YOKE_CLEARANCE_FINAL_CANDIDATE.FCStd")
d=App.openDocument(str(p));c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());DX=108.7860812043256
px=504.3463093769572;py=125.20927023775282;sy=65.;mid=457.3099792190261;horn_r=17.
# helpers
def capsule(p0,p1,w,za,zb):
 x0,y0=p0;x1,y1=p1;dx=x1-x0;dy=y1-y0;L=math.hypot(dx,dy);a=math.degrees(math.atan2(dy,dx));r=w/2
 sh=Part.makeBox(L,w,zb-za,App.Vector(0,-r,za));sh.rotate(App.Vector(),App.Vector(0,0,1),a);sh.translate(App.Vector(x0,y0,0));return sh.fuse(Part.makeCylinder(r,zb-za,App.Vector(x0,y0,za))).fuse(Part.makeCylinder(r,zb-za,App.Vector(x1,y1,za)))
def rod(a,b,r=2):
 va=App.Vector(*a);v=App.Vector(*b)-va;return Part.makeCylinder(r,v.Length,va,v.normalize())
profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
def yoke(x):
 pts=[App.Vector(x+w,y,2.5) for y,w in profile]+[App.Vector(x-w,y,2.5) for y,w in reversed(profile)];sh=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(App.Vector(0,0,8));sh=sh.cut(Part.makeBox(5,13,8.4,App.Vector(x-2.5,7,2.3)))
 for yy in [65,-65]:sh=sh.cut(Part.makeCylinder(1.65,8.4,App.Vector(x,yy,2.3)))
 return sh
fixed={}
for n in ['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','BATTERY_TRAY_v207','V205_SWEEP_SERVO_BODY_REF','V205_SWEEP_SERVO_SERVICE','INLET_EDF_R','INLET_EDF_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():fixed[n]=o.Shape
bats={c0:Part.makeBox(106,36,25,App.Vector(c0-53,-18,4.407593065391325)) for c0 in [305,340,375]}
rows=[]
for s in c['samples']:
 deg=s['sweep_deg'];x=s['slider_x_mm']-DX;yk=yoke(x);off=x-mid;pin_y=math.sqrt(max(0,horn_r*horn_r-off*off));horn=capsule((mid,0),(x,pin_y),5,11.4,13.4).fuse(Part.makeCylinder(2,6.5,App.Vector(x,pin_y,7)))
 for sign,lab in [(1,'R'),(-1,'L')]:
  cp=(s['crank_pin_mm'][0]-DX,sign*abs(s['crank_pin_mm'][1]));piv=(px,sign*py);sl=(x,sign*sy)
  cr=capsule(piv,cp,14,4,9).cut(Part.makeCylinder(1.65,5.4,App.Vector(cp[0],cp[1],3.8)));rd=rod((cp[0],cp[1],7.5),(sl[0],sl[1],7.5));hub=d.getObject('V205_MOVING_HUB_'+lab).Shape.copy();hub.rotate(App.Vector(px,sign*py,0),App.Vector(0,0,1),-sign*(deg-20))
  parts={'yoke':yk,'horn':horn,'crank':cr,'rod':rd,'hub':hub}
  for pn,sh in parts.items():
   for tn,t in fixed.items():
    # intentional mechanical interfaces skipped: hub to its own upper/lower fork, horn to servo body/service
    if pn=='hub' and tn in [f'V204_MONO_LOWER_{lab}',f'V204_UPPER_FORK_{lab}']:continue
    if pn=='horn' and tn in ['V205_SWEEP_SERVO_BODY_REF','V205_SWEEP_SERVO_SERVICE']:continue
    rows.append({'sweep_deg':deg,'side':lab,'part':pn,'target':tn,'distance_mm':sh.distToShape(t)[0]})
   if pn in ['yoke','horn','rod']:
    for bc,b in bats.items():rows.append({'sweep_deg':deg,'side':lab,'part':pn,'target':f'BATTERY_{bc}','distance_mm':sh.distToShape(b)[0]})
# sort and flag
rows2=sorted(rows,key=lambda q:q['distance_mm']);crit=rows2[0];near=[q for q in rows2 if q['distance_mm']<=1.0]
res={'status':'V208_FULL_DYNAMIC_MECHANISM_SCREEN','sample_count':len(c['samples']),'minimum_nonintentional':crit,'minimum_by_part':{p:min(q['distance_mm'] for q in rows if q['part']==p) for p in sorted(set(q['part'] for q in rows))},'near_or_below_1mm_count':len(near),'near_or_below_1mm':near[:80],'gates':{'all_nonintentional_clear_gt_1mm':len(near)==0,'sampled_every_2deg':True,'continuous_between_samples_analytic_verified':False,'servo_model_selected':False,'materials_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v208_full_dynamic_mechanism_audit.json").write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='near_or_below_1mm'},indent=2))
