import FreeCAD as App, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p)); fus=d.getObject('FUSELAGE_CURRENT'); px=504.3463093769572; py=125.20927023775282
contain=[]
for n in ['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L']:
 o=d.getObject(n); v=o.Shape.Volume; c=o.Shape.common(fus.Shape); iv=c.Volume if not c.isNull() else 0
 contain.append({'name':n,'volume_mm3':v,'inside_mm3':iv,'inside_fraction':iv/v if v else 0})
sweep=[]
angles=[20,28,36,44,52,60,68]
for lab,sgn in [('R',1),('L',-1)]:
 base=d.getObject('WING_'+lab).Shape
 fixed=[('LOWER',d.getObject('V204_MONO_LOWER_'+lab).Shape),('UPPER',d.getObject('V204_UPPER_FORK_'+lab).Shape)]
 for deg in angles:
  sh=base.copy(); sh.rotate(App.Vector(px,sgn*py,0),App.Vector(0,0,1),-sgn*(deg-20))
  for name,fx in fixed:
   dist=sh.distToShape(fx)[0]
   sweep.append({'side':lab,'sweep_deg':deg,'part':name,'distance_mm':dist})
res={'status':'V204_FAST_CONTAINMENT_SWEEP_DISTANCE_SCREEN','containment':contain,'min_inside_fraction':min(x['inside_fraction'] for x in contain),'sweep':sweep,'minimum_sampled_distance_mm':min(x['distance_mm'] for x in sweep),'minimum_record':min(sweep,key=lambda x:x['distance_mm']),'gates':{'containment_verified':min(x['inside_fraction'] for x in contain)>0.999,'sampled_sweep_clearance_positive':all(x['distance_mm']>0.05 for x in sweep),'continuous_sweep_verified':False,'physical_proof':False,'print_release':False,'flight_release':False}}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v204_containment_sweep_fast_audit.json").write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
