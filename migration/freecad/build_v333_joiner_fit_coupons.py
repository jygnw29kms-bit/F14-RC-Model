"""v333 8-mm CFRP tube / FDM socket tolerance coupons for Bambu P2S.
Three separate FreeCAD solid coupons (8.2/8.3/8.4 mm), separately exported as developmental STL.
This is a manufacturing fit trial only; not an approved load-bearing wing.
"""
import FreeCAD as App, Part, MeshPart, pathlib, json, math, hashlib
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model")
OUT=R/"manufacturing/fit_coupons/v333_8mm_joiner"
OUT.mkdir(parents=True,exist_ok=True)
doc=App.newDocument("F14_v333_JOINER_FIT_COUPONS")
rows=[]
for i,d in enumerate([8.2,8.3,8.4]):
 x=i*30
 # 22 x 22 x 14 mm body, through-hole along Y axis, as in original wing joiners
 blank=Part.makeBox(22,14,12,App.Vector(x,0,0))
 bore=Part.makeCylinder(d/2,14,App.Vector(x+11,0,6),App.Vector(0,1,0))
 sh=blank.cut(bore).removeSplitter()
 if not sh.isValid() or len(sh.Solids)!=1: raise RuntimeError("invalid coupon for d="+str(d))
 obj=doc.addObject("PartDesign::Feature","FIT_D"+str(d).replace(".","_"))
 obj.Label="Carbon tube OD 8.00 / hole D %.1f mm"%d
 obj.Shape=sh
 mesh=MeshPart.meshFromShape(Shape=sh,LinearDeflection=0.08,AngularDeflection=0.25,Relative=False)
 path=OUT/("F14_v333_fit_socket_D"+str(d).replace(".","p")+"_DEV_ONLY.stl")
 mesh.write(str(path))
 rows.append({"bore_d_mm":d,"tube_od_nominal_mm":8.0,"diametral_clearance_nominal_mm":round(d-8.0,3),"radial_clearance_nominal_mm":round((d-8.0)/2,3),"solid":sh.isValid() and len(sh.Solids)==1,"mesh_solid":bool(mesh.isSolid()),"mesh_nonmanifolds":bool(mesh.hasNonManifolds()),"stl":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
doc.recompute()
cad=R/"migration/freecad/F14_v333_JOINER_FIT_COUPONS.FCStd"
doc.saveAs(str(cad))
report={"status":"DEV_ONLY","model":"F14_v333_JOINER_FIT_COUPONS.FCStd","source_design":"v282 8x6 CF joiner and 8.3 mm cavity","slicer_verified":False,"fit_verified":False,"load_verified":False,"flight_release":False,"samples":rows,"cad_sha256":hashlib.sha256(cad.read_bytes()).hexdigest()}
(OUT/"FIT_COUPON_AUDIT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2),flush=True)
