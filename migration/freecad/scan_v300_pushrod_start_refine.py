import FreeCAD as App, Part, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v299_TAIL_SERVO_RELOCATION_CANDIDATE.FCStd')); oml=d.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
endx=751.0078983334656
def rod(a,b,r):
 v=b.sub(a); return Part.makeCylinder(r,v.Length,a,v.normalize())
rows=[]
for sx in [722.0,722.5,723.0,723.5]:
 for sz in [10.0,11.0,12.0]:
  sides=[]
  for side,sgn in [('R',1),('L',-1)]:
   a=App.Vector(sx,sgn*20,sz); b=App.Vector(endx,sgn*76,0); sh=rod(a,b,2.0); edf=d.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape; fit=d.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
   sides.append({'side':side,'oml_containment':sh.common(oml).Volume/sh.Volume,'edf_clearance_mm':sh.distToShape(edf)[0],'edf_intersection_mm3':sh.common(edf).Volume,'root_clearance_mm':sh.distToShape(fit)[0]})
  rows.append({'start_abs_mm':[sx,20.0,sz],'dynamic_corridor_diameter_mm':4.0,'sides':sides,'pass':all(s['oml_containment']>=0.995 and s['edf_intersection_mm3']<1e-6 and s['edf_clearance_mm']>=1.0 and s['root_clearance_mm']>=1.0 for s in sides)})
rows.sort(key=lambda q:(not q['pass'],-min(s['edf_clearance_mm'] for s in q['sides'])))
res={'status':'V300_PUSHROD_START_REFINEMENT','best':rows[0],'passing_count':sum(r['pass'] for r in rows),'rows':rows};(R/'migration/freecad/freecad_v300_pushrod_start_refine.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
