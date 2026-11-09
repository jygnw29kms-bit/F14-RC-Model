"""v332: Abstände und Einschubgeometrie der 8x6-Flügelverbinder aus der v330-Montage."""
import FreeCAD as App, pathlib, json
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad")
d=App.openDocument(str(R/"F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd"))
rows=[]
for side in ("R","L"):
 inner=d.getObject("REVIEW_V282_WING_"+side+"_INNER").Shape
 outer=d.getObject("REVIEW_V282_WING_"+side+"_OUTER").Shape
 for pos in ("FWD","MID","AFT"):
  nm="V282_WING_JOINER_"+side+"_"+pos
  j=d.getObject("REVIEW_"+nm).Shape
  row={"side":side,"position":pos}
  for target,body in (("inner",inner),("outer",outer)):
   try:
    dist,_,_=j.distToShape(body)
    row[target+"_minimum_surface_distance_mm"]=round(float(dist),5)
    row[target+"_volume_overlap_mm3"]=round(float(j.common(body).Volume),5)
   except Exception as e:row[target+"_error"]=str(e)
  rows.append(row)
  print(json.dumps(row),flush=True)
report={"source":"F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd","status":"v332_joiner_clearance_diagnostic","notes":"Solid-to-solid minimum distance does not establish nominal slot wall clearance or manufacturing tolerance. Physical fit test remains required.","connectors":rows,"fit_release":False,"print_release":False,"flight_release":False}
(R/"freecad_v332_joiner_clearances_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
