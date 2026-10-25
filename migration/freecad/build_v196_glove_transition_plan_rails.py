import FreeCAD as App, Part, math, json, os, hashlib
BASE=r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad"
OUT=os.path.join(BASE,'F14_v196_GLOVE_TRANSITION_PLAN_RAILS.FCStd')
AUD=os.path.join(BASE,'freecad_v196_glove_transition_plan_rails_audit.json')
# Source points from verified extraction
sides={
 'R': {'guide_prev':(444.1760958561681,131.9109170887001),'guide_end':(457.354009651243,137.1820826067301),'wing_fwd':(479.4839172711096,148.8263775443693)},
 'L': {'guide_prev':(444.1760958561681,-132.17447536460162),'guide_end':(457.354009651243,-137.44564088263158),'wing_fwd':(479.4839172711096,-148.8263775443693)}
}
d=App.newDocument('F14_v196_GLOVE_TRANSITION_PLAN_RAILS')
grp=d.addObject('App::DocumentObjectGroup','PLAN_TRANSITION_REFERENCE'); grp.Label='PLAN-ÜBERGANGSRAILS / NUR XY-REFERENZ / Z NICHT REGISTRIERT'
records=[]
for side,data in sides.items():
 p0,p1,p2=data['guide_prev'],data['guide_end'],data['wing_fwd']
 v1=(p1[0]-p0[0],p1[1]-p0[1]); v2=(p2[0]-p1[0],p2[1]-p1[1])
 def ang(v): return math.degrees(math.atan2(v[1],v[0]))
 a1,a2=ang(v1),ang(v2); kink=abs((a2-a1+180)%360-180)
 # smooth 2D spline using last guide tangent and target; midpoint follows Hermite-like tangent continuation
 L=math.hypot(v2[0],v2[1]); tlen=max(1e-9,math.hypot(v1[0],v1[1])); tu=(v1[0]/tlen,v1[1]/tlen)
 mid=(p1[0]+0.48*(p2[0]-p1[0]), p1[1]+0.48*(p2[1]-p1[1]))
 ctrl=(p1[0]+0.30*L*tu[0], p1[1]+0.30*L*tu[1])
 curve=Part.BSplineCurve(); curve.interpolate([App.Vector(p1[0],p1[1],0),App.Vector(ctrl[0],ctrl[1],0),App.Vector(mid[0],mid[1],0),App.Vector(p2[0],p2[1],0)])
 o=d.addObject('PartDesign::Feature','TRANSITION_RAIL_'+side); o.Label=f'Glove→WingRoot Plan-Rail {side} / REFERENZ'; o.Shape=curve.toShape(); grp.addObject(o)
 line=d.addObject('PartDesign::Feature','DIRECT_CHORD_'+side); line.Label=f'Direktverbindung {side} / Diagnose'; line.Shape=Part.makeLine(App.Vector(p1[0],p1[1],0),App.Vector(p2[0],p2[1],0)); grp.addObject(line)
 m=d.addObject('PartDesign::Feature','WING_ROOT_TARGET_'+side); m.Label=f'Wing-root Zielpunkt {side} / XY'; m.Shape=Part.makeCircle(3,App.Vector(p2[0],p2[1],0)); grp.addObject(m)
 records.append({'side':side,'guide_tangent_deg':a1,'direct_connector_deg':a2,'tangent_kink_deg':kink,'gap_mm':L,'guide_end_xy':p1,'wing_forward_root_xy':p2})
meta=d.addObject('App::FeaturePython','GATE_META'); meta.Label='FAIL-CLOSED: PLAN ONLY – KEIN Z / KEINE OML-FREIGABE'
d.recompute(); d.saveAs(OUT)
audit={'status':'V196_GLOVE_TRANSITION_PLAN_RAILS_REFERENCE_ONLY','records':records,'method':'BSpline through guide-end tangent continuation, midpoint, and v195 forward inner wing-root point; XY projection only','gates':{'X_v195_supported':True,'pivot_Y_source_backed':True,'plan_transition_reference_only':True,'Z_registered':False,'3D_glove_surface_created':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(open(OUT,'rb').read()).hexdigest()}
open(AUD,'w',encoding='utf-8').write(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2))
