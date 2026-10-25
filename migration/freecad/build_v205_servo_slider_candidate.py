import FreeCAD as App, Part, json, os, math
from pathlib import Path
BASE=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
SRC=BASE/'migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd'
KIN=BASE/'analysis/F14_sweep_linkage_kinematics_v40.json'
OUT=BASE/'migration/freecad/F14_v205_SERVO_SLIDER_CANDIDATE.FCStd'
AUD=BASE/'migration/freecad/freecad_v205_servo_slider_candidate_audit.json'
SHIFT=108.7860812043256
IDX=23

def feat(doc,name,label,shape):
    o=doc.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=shape; return o

def box(x0,x1,y0,y1,z0,z1):
    return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))

def ivol(a,b):
    try:
        s=a.common(b); return 0.0 if s.isNull() else s.Volume
    except Exception: return 0.0

doc=App.openDocument(str(SRC))
with open(KIN,encoding='utf-8') as f: kin=json.load(f)
c=kin['top_candidates'][IDX]
px=504.3463093769572; py=125.20927023775282
xmin=c['slider_x_min_mm']-SHIFT; xmax=c['slider_x_max_mm']-SHIFT
mid=(xmin+xmax)/2.0; sy=float(c['slider_attach_y_mm'])
servo=box(mid-21,mid+21,-10.5,10.5,2,42)
service=box(mid-24,mid+24,-13.5,13.5,0,44)
g=doc.addObject('App::DocumentObjectGroup','SWEEP_V205'); g.Label='05 SWEEP SERVO / SLIDER v205 CANDIDATE'
so=feat(doc,'V205_SWEEP_SERVO','v205 sweep servo envelope 42x21x40',servo); g.addObject(so)
srv=feat(doc,'V205_SWEEP_SERVO_SERVICE','v205 conservative servo service envelope',service); g.addObject(srv)
sliders=[]
for lab,sgn in [('R',1),('L',-1)]:
    sh=box(xmin-4,xmax+4,sgn*sy-4,sgn*sy+4,4,12)
    o=feat(doc,'V205_SLIDER_'+lab,'v205 split synchronized slider '+lab,sh); g.addObject(o); sliders.append(o)
# Battery position envelopes, exact accepted pack size from v162
bats=[]
for cx in (305,340,375):
    sh=box(cx-53,cx+53,-18,18,4.407593065391325,29.407593065391325)
    o=feat(doc,'V205_BATTERY_'+str(cx),'v162 accepted battery envelope center '+str(cx),sh); g.addObject(o); bats.append(o)
# reference endpoint rods at 20 and 68 deg, using candidate kinematics transformed into nose-relative X
samples={int(r['sweep_deg']):r for r in c['samples']}
rod_objs=[]
for sw in (20,68):
    r=samples[sw]
    sx=r['slider_x_mm']-SHIFT
    for lab,sgn in [('R',1),('L',-1)]:
        crank=r['crank_pin_mm']; cp=App.Vector(crank[0]-SHIFT, sgn*abs(crank[1]), 8)
        sp=App.Vector(sx, sgn*sy, 8)
        vec=cp-sp; ln=vec.Length
        if ln>0:
            rod=Part.makeCylinder(2.0,ln,sp,vec)
            o=feat(doc,f'V205_ROD_{sw}_{lab}',f'v205 rod ref sweep {sw} {lab}',rod); g.addObject(o); rod_objs.append(o)
# audits
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
fixed=[doc.getObject(n) for n in ['V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L'] if doc.getObject(n)]
rows=[]
for b in bats:
    rows.append({'pair':b.Name+'|SERVO_SERVICE','distance_mm':b.Shape.distToShape(service)[0],'intersection_mm3':ivol(b.Shape,service)})
for o in fixed:
    rows.append({'pair':o.Name+'|SERVO_SERVICE','distance_mm':o.Shape.distToShape(service)[0],'intersection_mm3':ivol(o.Shape,service)})
for s in sliders:
    for o in fixed:
        rows.append({'pair':s.Name+'|'+o.Name,'distance_mm':s.Shape.distToShape(o.Shape)[0],'intersection_mm3':ivol(s.Shape,o.Shape)})
sv=service.Volume; service_inside=ivol(service,fuse)/sv if sv else 0.0
# slider containment
slider_inside=[]
for s in sliders:
    v=s.Shape.Volume; slider_inside.append({'name':s.Name,'inside_fraction':ivol(s.Shape,fuse)/v if v else 0.0})
# Headless build: GUI visibility/colors are applied later by the Desktop-1 show script.
doc.recompute(); doc.saveAs(str(OUT))
audit={'status':'V205_SERVO_SLIDER_REPACKAGED_CANDIDATE','source_v204':str(SRC),'v40_candidate_index':IDX,'candidate':c,'nose_relative':{'shift_mm':SHIFT,'slider_x_mm':[xmin,xmax],'servo_axis_x_mm':mid,'servo_service_x_mm':[mid-24,mid+24]},'battery_rear_edge_mm':428.0,'service_gap_to_rear_battery_mm':(mid-24)-428.0,'service_inside_fuselage_fraction':service_inside,'slider_inside':slider_inside,'pair_checks':rows,'gates':{'battery_70mm_travel_packaging_pass':all(r['intersection_mm3']<1e-6 for r in rows if r['pair'].startswith('V205_BATTERY_')),'fixed_structure_sample_pass':all(r['intersection_mm3']<1e-6 for r in rows if 'BATTERY' not in r['pair']),'service_fuselage_containment_pass':service_inside>0.995,'full_dynamic_linkage_verified':False,'servo_model_selected':False,'print_release':False,'flight_release':False}}
with open(AUD,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps({'status':audit['status'],'slider_x_mm':audit['nose_relative']['slider_x_mm'],'servo_axis_x_mm':mid,'service_gap_to_rear_battery_mm':audit['service_gap_to_rear_battery_mm'],'service_inside':service_inside,'slider_inside':slider_inside,'gates':audit['gates'],'pair_checks':rows},indent=2))