import FreeCAD as App, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
p=R/'migration/freecad/F14_v218_CONSOLIDATED_STRUCTURAL_MODEL.FCStd'
out=R/'migration/freecad/freecad_v218_cassette_massprops.json'
d=App.openDocument(str(p)); rows=[]
for lab in ['R','L']:
 sh=d.getObject('V217_CASSETTE_'+lab).Shape; s=sh.Solids[0]; c=s.CenterOfMass
 rows.append({'side':lab,'volume_mm3':s.Volume,'volume_cm3':s.Volume/1000.0,'center_mm':[c.x,c.y,c.z]})
tot=sum(r['volume_mm3'] for r in rows); cx=sum(r['volume_mm3']*r['center_mm'][0] for r in rows)/tot
res={'status':'V218_CASSETTE_MASSPROPS','source':str(p),'rows':rows,'pair_volume_mm3':tot,'pair_volume_cm3':tot/1000.0,'pair_center_x_mm':cx}
out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))