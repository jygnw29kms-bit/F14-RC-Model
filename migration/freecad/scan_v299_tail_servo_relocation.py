import FreeCAD as App, Part, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v298_EDF_PACKAGING_ENVELOPE.FCStd'))
oml=d.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
crank=d.getObject('V241_LIGHT_D_CRANK_R').Shape
root=d.getObject('V284_LIGHT_D_ROOT_FITTING_R').Shape
edf=d.getObject('V298_HOUSING_SKIN_SERVICE_R').Shape
rows=[]
for cx in [690,700,710]:
 for cy in [18,20,22]:
  for cz in [-4,0,4]:
   body=Part.makeBox(23,27.5,12,App.Vector(cx-11.5,cy-13.75,cz-6))
   env=Part.makeBox(27,31.5,16,App.Vector(cx-13.5,cy-15.75,cz-8))
   omfrac=env.common(oml).Volume/env.Volume
   ed=env.distToShape(edf)[0]
   cr=env.distToShape(crank)[0]
   rt=env.distToShape(root)[0]
   rows.append({'center_R_mm':[cx,cy,cz],'center_L_mm':[cx,-cy,cz],'service_oml_fraction':omfrac,'edf_service_clearance_mm':ed,'crank_service_clearance_mm':cr,'root_service_clearance_mm':rt,'pass':omfrac>=0.999 and ed>=2.0})
rows.sort(key=lambda q:(not q['pass'],abs(q['center_R_mm'][0]-700)+abs(q['center_R_mm'][1]-20)+abs(q['center_R_mm'][2]),-q['edf_service_clearance_mm']))
result={'status':'V299_TARGETED_TAIL_SERVO_RELOCATION','constraints':{'service_OML_fraction_min':0.999,'EDF_service_clearance_min_mm':2.0},'rows':rows,'best':next((q for q in rows if q['pass']),None)}
out=R/'migration/freecad/freecad_v299_tail_servo_relocation_scan.json'; out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
