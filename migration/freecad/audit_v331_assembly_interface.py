"""v331: gezielte Schnittmengenprüfung der in v330 zusammengeführten Baugruppen.
Die Rumpfvollreferenz ist NICHT als hohler Produktionsrumpf anzusehen.
Überschneidungen mit der Rumpfreferenz sind deshalb diagnostisch, nicht automatisch Fehler.
"""
import FreeCAD as App, pathlib, json, math
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad")
d=App.openDocument(str(R/"F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd"))
names=[
("V282_WING_R_INNER","V282_WING_R_OUTER"),
("V282_WING_L_INNER","V282_WING_L_OUTER"),
("V282_WING_JOINER_R_FWD","V282_WING_R_INNER"),
("V282_WING_JOINER_R_FWD","V282_WING_R_OUTER"),
("V282_WING_JOINER_R_MID","V282_WING_R_INNER"),
("V282_WING_JOINER_R_MID","V282_WING_R_OUTER"),
("V282_WING_JOINER_R_AFT","V282_WING_R_INNER"),
("V282_WING_JOINER_R_AFT","V282_WING_R_OUTER"),
("V282_WING_JOINER_L_FWD","V282_WING_L_INNER"),
("V282_WING_JOINER_L_FWD","V282_WING_L_OUTER"),
("V282_WING_JOINER_L_MID","V282_WING_L_INNER"),
("V282_WING_JOINER_L_MID","V282_WING_L_OUTER"),
("V282_WING_JOINER_L_AFT","V282_WING_L_INNER"),
("V282_WING_JOINER_L_AFT","V282_WING_L_OUTER"),
("STABILATOR_R","V312_POST_F_SOURCE_CONSTRAINED_OML"),
("STABILATOR_L","V312_POST_F_SOURCE_CONSTRAINED_OML"),
("V297_JOINED_INLET_ADAPTER_R","FUSELAGE_CURRENT"),
("V297_JOINED_INLET_ADAPTER_L","FUSELAGE_CURRENT")
]
rows=[]
for a,b in names:
 oa=d.getObject("REVIEW_"+a);ob=d.getObject("REVIEW_"+b)
 row={"a":a,"b":b,"status":"not_tested"}
 if not oa or not ob:row["status"]="missing_object"
 elif oa.Shape.isNull() or ob.Shape.isNull():row["status"]="null_shape"
 elif not oa.Shape.BoundBox.intersect(ob.Shape.BoundBox):row["status"]="no_bounding_overlap";row["intersection_mm3"]=0
 else:
  try:
   common=oa.Shape.common(ob.Shape)
   row["status"]="exact_boolean_ok"
   row["intersection_mm3"]=round(float(common.Volume),4)
   row["shared_volume_fraction_smaller"]=round(float(common.Volume)/max(min(oa.Shape.Volume,ob.Shape.Volume),1e-9),5)
  except Exception as e:row["status"]="boolean_error";row["error"]=str(e)
 rows.append(row)
 print(a,b,row["status"],row.get("intersection_mm3"),flush=True)
report={"status":"v331_assembly_interface_audit","source":"F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd","scope":"diagnostic selected interfaces; not full assembly validation","pairs":rows,"tested_count":len(rows),"boolean_errors":sum(x["status"]=="boolean_error" for x in rows),"print_release":False,"flight_release":False}
(R/"freecad_v331_assembly_interface_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
