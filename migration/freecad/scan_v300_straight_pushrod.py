import FreeCAD as App, Part, pathlib, json, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v299_TAIL_SERVO_RELOCATION_CANDIDATE.FCStd'))
oml=d.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
crank_x=751.0078983334656

def rod(a,b,r):
 v=b.sub(a); L=v.Length; return Part.makeCylinder(r,L,a,v.normalize())
rows=[]
for sx in [718.0,720.0,722.0]:
 for sz in [6.0,8.0,10.0]:
  for radius in [1.0,1.25,1.5,1.75,2.0]:
   sides=[]
   for side,sgn in [('R',1),('L',-1)]:
    a=App.Vector(sx,sgn*20.0,sz); b=App.Vector(crank_x,sgn*76.0,0.0)
    sh=rod(a,b,radius); edf=d.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape; fit=d.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape; crank=d.getObject('V241_LIGHT_D_CRANK_'+side).Shape
    om=sh.common(oml).Volume/sh.Volume; ed=sh.distToShape(edf)[0]; edi=sh.common(edf).Volume; fd=sh.distToShape(fit)[0]; ci=sh.common(crank).Volume
    sides.append({'side':side,'start_mm':[a.x,a.y,a.z],'end_mm':[b.x,b.y,b.z],'radius_mm':radius,'length_mm':a.distanceToPoint(b),'oml_containment':om,'edf_clearance_mm':ed,'edf_intersection_mm3':edi,'root_fitting_clearance_mm':fd,'crank_joint_intersection_mm3':ci})
   passed=all(s['oml_containment']>=0.995 and s['edf_intersection_mm3']<1e-6 and s['edf_clearance_mm']>=1.0 and s['root_fitting_clearance_mm']>=1.0 for s in sides)
   rows.append({'start_abs_mm':[sx,20.0,sz],'radius_mm':radius,'diameter_mm':2*radius,'pass':passed,'sides':sides})
rows.sort(key=lambda q:(not q['pass'],-q['radius_mm'],-min(s['oml_containment'] for s in q['sides']),-min(s['edf_clearance_mm'] for s in q['sides'])))
res={'status':'V300_STRAIGHT_PUSHROD_SCAN','criteria':{'oml_containment_min':0.995,'edf_clearance_min_mm':1.0,'root_fitting_clearance_min_mm':1.0},'passing_count':sum(r['pass'] for r in rows),'best':next((r for r in rows if r['pass']),None),'top':rows[:12]}
out=R/'migration/freecad/freecad_v300_straight_pushrod_scan.json';out.write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
