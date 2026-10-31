import FreeCAD as App, Part, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; d=App.openDocument(str(src))
seam=234.8834084849764; pos=[('FWD',552.0,-1.0),('AFT',562.0,-1.0)]; rows=[]
for side,sgn in [('R',1),('L',-1)]:
  wing=d.getObject('WING_'+side).Shape
  for tag,x,z in pos:
    start=App.Vector(x,sgn*(seam-20),z); axis=App.Vector(0,sgn,0)
    tube=Part.makeCylinder(4.0,40,start,axis); cav=Part.makeCylinder(4.15,40,start,axis)
    rows.append({'side':side,'joiner':tag,'tube_containment':tube.common(wing).Volume/tube.Volume,'cavity_containment':cav.common(wing).Volume/cav.Volume,'tube_to_surface_mm':tube.distToShape(wing)[0]})
a={'status':'V279_WING_8X6_3D_VERIFY','source':src.name,'seam':{'WBL_in':200.79919,'model_y_mm':seam},'tube_OD_ID_mm':[8,6],'cavity_d_mm':8.3,'positions_mm':pos,'rows':rows,'gates':{'all_tubes_contained_ge_0p995':all(r['tube_containment']>=0.995 for r in rows),'all_cavities_contained_ge_0p995':all(r['cavity_containment']>=0.995 for r in rows),'3d_geometry_upgrade_allowed':False}}
a['gates']['3d_geometry_upgrade_allowed']=a['gates']['all_tubes_contained_ge_0p995'] and a['gates']['all_cavities_contained_ge_0p995']
(R/'analysis/v279_wing_8x6_3d_verify.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
