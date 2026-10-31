import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v250_PRINT_SEGMENTATION_REVIEW.FCStd'))
fus=d.getObject('FUSELAGE_CURRENT').Shape
hardware=[]
for n in ['BATTERY_TRAY_v165','V221_CASSETTE_R','V221_CASSETTE_L','V225_SERVO_SERVICE','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull(): hardware.append((n,o.Shape))
# two symmetric 12x8x6 mm alignment tongues per longitudinal cut
spec=[(220,20,0),(440,40,0),(620,15,30),(840,40,0)]
rows=[]
for x,ay,z in spec:
 for y in (-ay,ay):
  sh=Part.makeBox(12,8,6,App.Vector(x-6,y-4,z-3))
  frac=sh.common(fus).Volume/sh.Volume if sh.Volume else 0
  ds=sorted((sh.distToShape(s)[0],n) for n,s in hardware)
  rows.append({'cut_x_mm':x,'y_mm':y,'z_mm':z,'containment_fraction':frac,'nearest_hardware':ds[0][1] if ds else None,'min_hardware_distance_mm':ds[0][0] if ds else 999})
out={'status':'V251_SEGMENT_CONNECTOR_SEARCH','connector_box_mm':[12,8,6],'rows':rows,'gates':{'eight_candidates':len(rows)==8,'containment_ge_0p995':all(r['containment_fraction']>=0.995 for r in rows),'hardware_clearance_ge_4mm':all(r['min_hardware_distance_mm']>=4 for r in rows)}}
(R/'analysis/v251_segment_connector_search.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))