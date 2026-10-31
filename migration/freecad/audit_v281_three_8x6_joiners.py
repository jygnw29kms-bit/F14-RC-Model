import FreeCAD as App, Part, pathlib, json, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; d=App.openDocument(str(src)); seam=234.8834084849764
pos=[('FWD',542.0,-1.0),('MID',552.0,-1.0),('AFT',562.0,-1.0)]; rows=[]
for side,sgn in [('R',1),('L',-1)]:
  wing=d.getObject('WING_'+side).Shape
  for tag,x,z in pos:
    start=App.Vector(x,sgn*(seam-20),z); axis=App.Vector(0,sgn,0)
    tube=Part.makeCylinder(4.0,40,start,axis); cav=Part.makeCylinder(4.15,40,start,axis)
    rows.append({'side':side,'joiner':tag,'tube_containment':tube.common(wing).Volume/tube.Volume,'cavity_containment':cav.common(wing).Volume/cav.Volume})
root=19.221033999999996; pivot_tip=324.79072976224717; seam_tip=215.11659151502354; M=root*(seam_tip/pivot_tip)**2; per=M/3; I=math.pi/64*(8**4-6**4); stress=(per*1000)*4/I; fos=250/stress
a={'status':'V281_THREE_8X6_JOINERS','source':src.name,'seam_WBL_in':200.79919,'model_y_mm':seam,'positions':pos,'rows':rows,'load_screen':{'seam_moment_Nm':M,'moment_per_tube_Nm':per,'stress_MPa':stress,'FOS_250MPa_typical_lower':fos},'gates':{'all_tubes_contained_ge_0p995':all(r['tube_containment']>=0.995 for r in rows),'all_cavities_contained_ge_0p995':all(r['cavity_containment']>=0.995 for r in rows),'FOS_ge_3':fos>=3,'upgrade_allowed':False}}
a['gates']['upgrade_allowed']=a['gates']['all_tubes_contained_ge_0p995'] and a['gates']['all_cavities_contained_ge_0p995'] and a['gates']['FOS_ge_3']
(R/'analysis/v281_three_8x6_joiners.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
