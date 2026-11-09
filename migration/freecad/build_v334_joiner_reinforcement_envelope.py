"""v334: calculate structural sleeve envelope for wing 8x6 joiners.
Native separate sleeve candidates, no unvalidated modification to source wing solids.
"""
import FreeCAD as App, Part, pathlib, json, math, hashlib
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model")
base=R/"migration/freecad"
src=App.openDocument(str(base/"F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd"))
doc=App.newDocument("F14_v334_JOINER_REINFORCEMENT_ENVELOPE")
seam=234.8834084849764
centres=[("FWD",542.0,-1.0),("MID",552.0,-1.0),("AFT",562.0,-1.0)]
row=[]
for side,sgn in (("R",1),("L",-1)):
 for seg in ("INNER","OUTER"):
  wing=src.getObject("V282_WING_"+side+"_"+seg).Shape
  for tag,x,z in centres:
   # 20 mm embed per segment, locally interrupted at the wing seam
   ystart=(seam-20.0 if seg=="INNER" else seam)
   origin=App.Vector(x,sgn*ystart,z)
   for outer_d in (10.0,11.0,12.0):
    outer=Part.makeCylinder(outer_d/2,20.0,origin,App.Vector(0,sgn,0))
    bore=Part.makeCylinder(8.3/2,20.0,origin,App.Vector(0,sgn,0))
    sleeve=outer.cut(bore)
    contained=sleeve.common(wing)
    coverage=contained.Volume/sleeve.Volume if sleeve.Volume>0 else 0
    entry={"side":side,"segment":seg,"position":tag,"outer_d_mm":outer_d,"bore_d_mm":8.3,"length_mm":20.0,"sleeve_vol_mm3":round(sleeve.Volume,3),"contained_vol_mm3":round(contained.Volume,3),"within_wing_fraction":round(coverage,5),"outside_wing_mm3":round(sleeve.Volume-contained.Volume,4)}
    row.append(entry)
    if outer_d==10.0:
     # separate diagnostic sleeve: no fusion or production release
     o=doc.addObject("PartDesign::Feature",f"SLEEVE_{side}_{seg}_{tag}")
     o.Label=f"DEV {side} {seg} {tag} 10mm OD / 8.3mm bore"
     o.Shape=sleeve
     entry["cad_object"]=o.Name
   print(side,seg,tag,[(r["outer_d_mm"],r["within_wing_fraction"]) for r in row[-3:]],flush=True)
doc.recompute()
out=base/"F14_v334_JOINER_REINFORCEMENT_ENVELOPE.FCStd"
doc.saveAs(str(out))
report={"status":"DEVELOPMENT_ENVELOPE","source":"F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd","candidate":"separate 10/11/12 mm OD sleeve, 8.3 mm bore, 20 mm embed, independent per half","measurement":"fraction of candidate sleeve volume lying within original solid wing","note":"Solid wing includes socket cavities, so containment is diagnostic. A final hollow shell, bonds, tolerances and fatigue are not yet engineered.","rows":row,"print_release":False,"flight_release":False,"cad_sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
(base/"freecad_v334_joiner_reinforcement_envelope_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("FINAL",len(row),flush=True)
