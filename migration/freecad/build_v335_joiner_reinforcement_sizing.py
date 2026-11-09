"""v335: precise clearance study of candidate socket reinforcement within source wing solids.
No physical stress certification is inferred from geometry containment.
"""
import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model")
b=R/"migration/freecad"
s=App.openDocument(str(b/"F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd"))
doc=App.newDocument("F14_v335_JOINER_REINFORCEMENT_SIZING")
seam=234.8834084849764
rows=[]
for side,sgn in (("R",1),("L",-1)):
 for seg in ("INNER","OUTER"):
  wing=s.getObject("V282_WING_"+side+"_"+seg).Shape
  for tag,x in (("FWD",542.0),("MID",552.0),("AFT",562.0)):
   z=-1.0
   origin=App.Vector(x,sgn*(seam-20.0 if seg=="INNER" else seam),z)
   for od in (8.6,9.0,9.5,10.0):
    raw=Part.makeCylinder(od/2.0,20.0,origin,App.Vector(0,sgn,0)).cut(Part.makeCylinder(8.3/2.0,20.0,origin,App.Vector(0,sgn,0)))
    outside=raw.cut(wing)
    frac=max(0,1-outside.Volume/max(raw.Volume,1e-9))
    rec={"side":side,"segment":seg,"position":tag,"outer_d_mm":od,"nominal_radial_reinforcement_mm":round((od-8.3)/2,3),"volume_mm3":round(raw.Volume,3),"outside_wing_mm3":round(outside.Volume,4),"inside_fraction":round(frac,6),"all_inside_wing_with_0p01mm3_tol":outside.Volume<0.01}
    rows.append(rec)
    if od==9.0:
     obj=doc.addObject("PartDesign::Feature","SLEEVE_"+side+"_"+seg+"_"+tag)
     obj.Shape=raw;obj.Label="9mm reinforcement candidate "+side+" "+seg+" "+tag
   print(side,seg,tag,[(r["outer_d_mm"],r["outside_wing_mm3"]) for r in rows[-4:]],flush=True)
doc.recompute();out=b/"F14_v335_JOINER_REINFORCEMENT_SIZING.FCStd";doc.saveAs(str(out))
report={"status":"GEOMETRY_CANDIDATES_ONLY","reference":"v282 nominal solid wing with 8.3mm holes","min_outer_d_mm":8.6,"rows":rows,"print_release":False,"flight_release":False,"sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
(b/"freecad_v335_joiner_reinforcement_sizing_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("COMPLETE",len(rows),flush=True)
