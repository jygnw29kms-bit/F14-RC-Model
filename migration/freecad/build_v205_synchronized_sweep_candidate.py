import FreeCAD as App, Part, math, json, hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad")
src=BASE/'F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd'; out=BASE/'F14_v205_SYNCHRONIZED_SWEEP_CANDIDATE.FCStd'
d=App.openDocument(str(src))
# remove obsolete v193/v194 review mechanism from candidate copy
for o in list(d.Objects):
    if o.Name in ['SWEEP_SLIDER_R','SWEEP_SLIDER_L','SWEEP_SERVO_SERVICE_REF'] or o.Name.startswith('V194_'):
        try:d.removeObject(o.Name)
        except:pass
DX=108.7860812043256; px=504.3463093769572; py=125.20927023775282; root_y=148.8263775443693
root_le=479.4839172711096; root_te=627.4150906440201
# v40 candidate 23, transformed to nose-relative X
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text())
xmin=c['slider_x_min_mm']-DX; xmax=c['slider_x_max_mm']-DX; xmid=(xmin+xmax)/2; sy=c['slider_attach_y_mm']; horn_r=17.0
z_yoke0=5.0; z_yoke1=11.0; yoke_wx=16.0

def feat(name,label,shape):
 o=d.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape;return o

def capsule_xy(p0,p1,width,z0,z1):
 x0,y0=p0;x1,y1=p1;dx=x1-x0;dy=y1-y0;L=math.hypot(dx,dy);ang=math.degrees(math.atan2(dy,dx));r=width/2
 rect=Part.makeBox(L,width,z1-z0,App.Vector(0,-r,z0));rect.rotate(App.Vector(0,0,0),App.Vector(0,0,1),ang);rect.translate(App.Vector(x0,y0,0))
 c0=Part.makeCylinder(r,z1-z0,App.Vector(x0,y0,z0),App.Vector(0,0,1));c1=Part.makeCylinder(r,z1-z0,App.Vector(x1,y1,z0),App.Vector(0,0,1));return rect.fuse(c0).fuse(c1)
def cyl_between(a,b,r):
 va=App.Vector(*a);vb=App.Vector(*b);v=vb-va;L=v.Length;return Part.makeCylinder(r,L,va,v.normalize())
# moving root hub + lug each side
for sign,lab in [(1,'R'),(-1,'L')]:
 yp=sign*py; yr=sign*root_y
 boss=Part.makeCylinder(12.0,20.0,App.Vector(px,yp,-10),App.Vector(0,0,1))
 boss=boss.cut(Part.makeCylinder(3.1,20.4,App.Vector(px,yp,-10.2),App.Vector(0,0,1)))
 boss=boss.cut(Part.makeCylinder(6.55,5.2,App.Vector(px,yp,-10.1),App.Vector(0,0,1)))
 boss=boss.cut(Part.makeCylinder(6.55,5.2,App.Vector(px,yp,4.9),App.Vector(0,0,1)))
 ymin=min(yp,yr+sign*8);ymax=max(yp,yr+sign*8);x0=max(root_le,px-20);x1=min(root_te,px+20)
 lug=Part.makeBox(x1-x0,ymax-ymin,16,App.Vector(x0,ymin,-8));hub=boss.fuse(lug)
 feat(f'V205_MOVING_HUB_{lab}',f'v205 moving pivot hub + root lug {lab}',hub)
# yoke at 20deg assembly state
x20=xmax
yoke=Part.makeBox(yoke_wx,136,z_yoke1-z_yoke0,App.Vector(x20-yoke_wx/2,-68,z_yoke0))
# pin slot centered on moving X, positive-Y scotch path; cut with service margins
slot=Part.makeBox(5.0,13.0,(z_yoke1-z_yoke0)+0.4,App.Vector(x20-2.5,7.0,z_yoke0-0.2)); yoke=yoke.cut(slot)
# rod-end M3.3 holes at y +/-65
for yy in [65,-65]: yoke=yoke.cut(Part.makeCylinder(1.65,6.4,App.Vector(x20,yy,z_yoke0-0.2),App.Vector(0,0,1)))
feat('V205_SYNC_YOKE_20','v205 synchronized scotch-yoke @20deg',yoke)
# guide envelope of the moving yoke (reference physical corridor)
yoke_env=Part.makeBox((xmax-xmin)+yoke_wx,136,z_yoke1-z_yoke0,App.Vector(xmin-yoke_wx/2,-68,z_yoke0));feat('V205_YOKE_MOTION_ENVELOPE','v205 yoke motion envelope reference',yoke_env)
# servo body and service envelope, upside down, output below
servo_body=Part.makeBox(42,21,40,App.Vector(xmid-21,-10.5,14));servo_service=Part.makeBox(48,27,44,App.Vector(xmid-24,-13.5,12));feat('V205_SWEEP_SERVO_BODY_REF','v205 42x21x40 sweep servo reference',servo_body);feat('V205_SWEEP_SERVO_SERVICE','v205 sweep servo service envelope',servo_service)
# horn at 20deg / pin engages yoke slot
half=(xmax-xmin)/2; beta=math.acos(half/horn_r); pinx=xmid+horn_r*math.cos(beta);piny=horn_r*math.sin(beta)
horn=capsule_xy((xmid,0),(pinx,piny),5.0,11.4,13.4);pin=Part.makeCylinder(2.0,6.5,App.Vector(pinx,piny,7.0),App.Vector(0,0,1));shaft=Part.makeCylinder(3.0,1.0,App.Vector(xmid,0,13.4),App.Vector(0,0,1));feat('V205_SERVO_HORN_20','v205 servo horn @20deg',horn.fuse(pin).fuse(shaft))
# physical linkage at 20deg: crank + rods, mirrored
for sign,lab in [(1,'R'),(-1,'L')]:
 yp=sign*py; crank_pin=(px+25,yp-sign*15); slider=(x20,sign*sy)
 crank=capsule_xy((px,yp),crank_pin,14.0,4.0,9.0)
 # M3.3 rod pin bore at moving crank end
 crank=crank.cut(Part.makeCylinder(1.65,5.4,App.Vector(crank_pin[0],crank_pin[1],3.8),App.Vector(0,0,1)))
 feat(f'V205_CRANK_{lab}_20',f'v205 candidate23 crank {lab} @20deg',crank)
 rod=cyl_between((crank_pin[0],crank_pin[1],7.5),(slider[0],slider[1],7.5),2.0);feat(f'V205_ROD_{lab}_20',f'v205 4mm linkage rod {lab} @20deg',rod)
# metadata
m=d.addObject('App::FeaturePython','V205_META');m.Label='v205 synchronized sweep candidate'
for n,v in [('Status','CANDIDATE23 SCOTCH-YOKE / NOT RELEASED'),('KinematicsSource','v40 top_candidate[23]'),('Architecture','single central servo + mechanically synchronized yoke')]:m.addProperty('App::PropertyString',n,'Gate');setattr(m,n,v)
for n,v in [('Battery70mmTravelPreserved',True),('AbsolutePivotZVerified',False),('ServoModelSelected',False),('ProductionRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out))
a={'status':'V205_SYNCHRONIZED_SWEEP_CANDIDATE','candidate_index':23,'pivot_mm':[px,py,0],'slider_current_mm':{'min':xmin,'max':xmax,'mid':xmid,'travel':xmax-xmin,'y_abs':sy},'battery_rear_end_mm':428,'service_envelope':{'x':[xmid-24,xmid+24],'y':[-13.5,13.5],'z':[12,56],'battery_x_gap_mm':xmid-24-428},'servo_body':{'x':[xmid-21,xmid+21],'y':[-10.5,10.5],'z':[14,54]},'yoke':{'width_x_mm':16,'span_y_mm':136,'thickness_z_mm':6,'motion_x_bounds':[xmin-8,xmax+8],'z':[5,11]},'horn':{'radius_mm':17,'beta20_deg':math.degrees(beta),'pin20_xy':[pinx,piny]},'v40':{'min_moment_arm_mm':c['min_linkage_moment_arm_mm'],'max_moment_arm_mm':c['max_linkage_moment_arm_mm'],'rod_length_mm':c['rod_length_mm']},'gates':{'kinematics_candidate_valid':True,'mechanical_sync_modeled':True,'root_hub_modeled':True,'battery_packaging_verified':False,'fixed_structure_clearance_verified':False,'servo_containment_verified':False,'servo_model_selected':False,'material_verified':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(BASE/'freecad_v205_synchronized_sweep_candidate_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print(json.dumps(a,indent=2))
