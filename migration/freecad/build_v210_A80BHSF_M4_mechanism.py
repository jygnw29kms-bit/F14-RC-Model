import FreeCAD as App,Part,json,hashlib,math
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v209_LOWERED_SWEEP_RODS_CANDIDATE.FCStd';out=BASE/'F14_v210_A80BHSF_M4_MECHANISM.FCStd'
d=App.openDocument(str(src));DX=108.7860812043256;px=504.3463093769572;py=125.20927023775282;mid=457.3099792190261
for n in ['V205_SWEEP_SERVO_BODY_REF','V208_SYNC_YOKE_20','V205_CRANK_R_20','V205_CRANK_L_20']:
 if d.getObject(n): d.removeObject(n)
# real servo body reference 40x20x37.5, inverted output at lower face
servo=Part.makeBox(40,20,37.5,App.Vector(mid-20,-10,14));o=d.addObject('PartDesign::Feature','V210_SERVO_A80BHSF_V2');o.Label='AGFRC A80BHSF V2 40x20x37.5mm / 36kgcm@8.4V';o.Shape=servo
# v208 yoke external geometry with M4.2 rod holes
x20=471.21391879567443;z0=2.5;z1=10.5;profile=[(-68,8),(-31,8),(-27,5),(-19,5),(-15,8),(15,8),(19,5),(27,5),(31,8),(68,8)]
pts=[App.Vector(x20+w,y,z0) for y,w in profile]+[App.Vector(x20-w,y,z0) for y,w in reversed(profile)];yoke=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(App.Vector(0,0,8));yoke=yoke.cut(Part.makeBox(5,13,8.4,App.Vector(x20-2.5,7,z0-.2)))
for yy in [65,-65]:yoke=yoke.cut(Part.makeCylinder(2.1,8.4,App.Vector(x20,yy,z0-.2)))
yo=d.addObject('PartDesign::Feature','V210_SYNC_YOKE_M4_20');yo.Label='v210 7075-T6 candidate sync yoke / M4.2 joints @20deg';yo.Shape=yoke
# candidate23 cranks with M4.2 pin bores, external unchanged
c=json.loads(Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/v40_candidate23.json").read_text());s=c['samples'][0]
def capsule(p0,p1,w,za,zb):
 x0,y0=p0;x1,y1=p1;dx=x1-x0;dy=y1-y0;L=math.hypot(dx,dy);a=math.degrees(math.atan2(dy,dx));r=w/2
 sh=Part.makeBox(L,w,zb-za,App.Vector(0,-r,za));sh.rotate(App.Vector(),App.Vector(0,0,1),a);sh.translate(App.Vector(x0,y0,0));return sh.fuse(Part.makeCylinder(r,zb-za,App.Vector(x0,y0,za))).fuse(Part.makeCylinder(r,zb-za,App.Vector(x1,y1,za)))
for sign,lab in [(1,'R'),(-1,'L')]:
 cp=(s['crank_pin_mm'][0]-DX,sign*abs(s['crank_pin_mm'][1]));piv=(px,sign*py);cr=capsule(piv,cp,14,4,9).cut(Part.makeCylinder(2.1,5.4,App.Vector(cp[0],cp[1],3.8)));co=d.addObject('PartDesign::Feature',f'V210_CRANK_M4_{lab}_20');co.Label=f'v210 crank M4.2 {lab} @20deg';co.Shape=cr
m=d.addObject('App::FeaturePython','V210_META');m.Label='v210 A80BHSF + M4 mechanism hardware freeze candidate'
for n,v in [('ServoModel','AGFRC A80BHSF V2'),('YokeMaterialCandidate','EN AW-7075-T6/T651'),('LoadedJointPins','4mm steel shoulder pins / 4.2mm clearance')]:m.addProperty('App::PropertyString',n,'Hardware');setattr(m,n,v)
for n,v in [('ServoDimensionsVerified',True),('ServoCurrentVerified',True),('YokeMaterialStockVerified',False),('FastenerGradeVerified',False),('ProductionRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out));a={'status':'V210_A80BHSF_M4_MECHANISM','servo':{'model':'AGFRC A80BHSF V2','dims_mm':[40,20,37.5],'weight_g':79,'voltage_V':[4.8,8.4],'stall_kgcm_8p4V':36,'loading_current_A_8p4V':5.0,'travel_deg':180},'joint_upgrade':{'pin_nominal_mm':4.0,'clearance_hole_mm':4.2,'rod_mm':4.0},'yoke_material_candidate':'EN AW-7075-T6/T651','gates':{'CAD_updated':True,'dynamic_external_clearance_inherited_v209':True,'material_certificate_verified':False,'fastener_grade_verified':False,'physical_proof':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v210_A80BHSF_M4_mechanism_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
