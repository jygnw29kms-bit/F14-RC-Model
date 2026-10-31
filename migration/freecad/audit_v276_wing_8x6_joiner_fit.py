import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; d=App.openDocument(str(src)); seam=320.94018208216556
pos=[('FWD',569.9475331358894,-4.299519854236053),('AFT',581.1120872253817,-4.231136960437908)]
rows=[]
for side,sgn in [('R',1),('L',-1)]:
  wing=d.getObject('WING_'+side).Shape; inner=wing; outer=wing
  for tag,x,z in pos:
    if sgn>0:
      a=App.Vector(x,seam-20,z); b=App.Vector(x,seam,z)
      tin=Part.makeCylinder(4.0,20,a,App.Vector(0,1,0)); cin=Part.makeCylinder(4.15,20,a,App.Vector(0,1,0))
      tout=Part.makeCylinder(4.0,20,b,App.Vector(0,1,0)); cout=Part.makeCylinder(4.15,20,b,App.Vector(0,1,0))
    else:
      a=App.Vector(x,-seam+20,z); b=App.Vector(x,-seam,z)
      tin=Part.makeCylinder(4.0,20,a,App.Vector(0,-1,0)); cin=Part.makeCylinder(4.15,20,a,App.Vector(0,-1,0))
      tout=Part.makeCylinder(4.0,20,b,App.Vector(0,-1,0)); cout=Part.makeCylinder(4.15,20,b,App.Vector(0,-1,0))
    rec={'side':side,'joiner':tag,'x_mm':x,'z_mm':z,'inner_tube_containment':tin.common(inner).Volume/tin.Volume,'inner_cavity_containment':cin.common(inner).Volume/cin.Volume,'outer_tube_containment':tout.common(outer).Volume/tout.Volume,'outer_cavity_containment':cout.common(outer).Volume/cout.Volume}
    rows.append(rec)
a={'status':'V276_WING_8X6_JOINER_FIT','source':src.name,'tube_OD_ID_mm':[8,6],'bond_cavity_d_mm':8.3,'embed_each_side_mm':20,'rows':rows,'gates':{'all_tube_halves_contained_ge_0p995':all(min(r['inner_tube_containment'],r['outer_tube_containment'])>=0.995 for r in rows),'all_cavity_halves_contained_ge_0p995':all(min(r['inner_cavity_containment'],r['outer_cavity_containment'])>=0.995 for r in rows),'geometry_upgrade_allowed':False}}
a['gates']['geometry_upgrade_allowed']=a['gates']['all_tube_halves_contained_ge_0p995'] and a['gates']['all_cavity_halves_contained_ge_0p995']
(R/'analysis/v276_wing_8x6_joiner_fit.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))

