import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v285_CONSOLIDATED_8X6_LIGHT_TAIL.FCStd'; out=R/'migration/freecad/F14_v287_CAPTIVE_M3_SEGMENT_CLAMPS.FCStd'; audp=R/'migration/freecad/freecad_v287_captive_m3_segment_clamps_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v287_CAPTIVE_M3_SEGMENT_CLAMPS')
for o in d.Objects:
    if o.Name.startswith('V271_C_CLAMP_'): continue
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
critical=[n for n in ['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L'] if doc.getObject(n)]
spec=[(220,20,-10,6),(440,60,-10,8),(840,30,0,6)]
rows=[]; total=0.0
# candidate M3 nut pocket: 5.7 mm across flats, 2.8 mm depth; actual purchased nut must be measured
AF=5.7; nut_depth=2.8; Rhex=AF/math.sqrt(3.0)
def hex_prism(cx,y0,cz,depth):
    pts=[]
    for i in range(6):
        a=math.radians(30+60*i); pts.append(App.Vector(cx+Rhex*math.cos(a),y0,cz+Rhex*math.sin(a)))
    pts.append(pts[0]); wire=Part.makePolygon(pts); face=Part.Face(wire); return face.extrude(App.Vector(0,depth,0))
for x,ay,z,od in spec:
  for sgn in (-1,1):
    y=sgn*ay; side='R' if sgn>0 else 'L'; tag=f'X{x}_{side}'
    bore=od/2+0.15; sleeve_or=bore+1.2; ir=sleeve_or+0.10; orr=ir+1.15; w=7.0
    ring=Part.makeCylinder(orr,w,App.Vector(x+2,y,z),App.Vector(1,0,0)).cut(Part.makeCylinder(ir,w,App.Vector(x+2,y,z),App.Vector(1,0,0)))
    slit=Part.makeBox(w+2,1.0,orr-ir+3.0,App.Vector(x+1,y-0.5,z+ir-0.5)); ring=ring.cut(slit)
    lugz=z+ir-2.0
    # enlarged lugs for M3 screw head and captive nut
    lug1=Part.makeBox(7.0,3.2,7.0,App.Vector(x+2,y-4.0,lugz))
    lug2=Part.makeBox(7.0,3.4,7.0,App.Vector(x+2,y+0.6,lugz))
    sh=ring.fuse(lug1).fuse(lug2)
    cx=x+5.5; cz=lugz+3.5
    hole=Part.makeCylinder(1.6,9.0,App.Vector(cx,y-4.5,cz),App.Vector(0,1,0)); sh=sh.cut(hole)
    nut=hex_prism(cx,y+1.2,cz,nut_depth); sh=sh.cut(nut).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V287_C_CLAMP_'+tag); o.Shape=sh; o.Label=f'v287 C-ring clamp captive M3 nut {tag}'
    cont=sh.common(fus).Volume/sh.Volume if sh.Volume else 0.0
    mg=sh.Volume/1000*1.25; total+=mg
    mind=min((sh.distToShape(doc.getObject(n).Shape)[0] for n in critical),default=999)
    rows.append({'cut_x_mm':x,'side':side,'valid':sh.isValid(),'solid_count':len(sh.Solids),'containment':cont,'mass_PPA_CF_g':mg,'critical_hardware_min_distance_mm':mind,'M3_clearance_d_mm':3.2,'nut_pocket_AF_mm':AF,'nut_pocket_depth_mm':nut_depth})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V287_CAPTIVE_M3_SEGMENT_CLAMPS','source':src.name,'architecture':{'CF_tube_cross_drilled':False,'captive_M3_hex_nut':True,'X620_excluded':True,'actual_nut_measurement_required':True},'rows':rows,'mass':{'PPA_CF_screen_g':total},'gates':{'all_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'containment_ge_0p98':all(r['containment']>=0.98 for r in rows),'critical_hardware_clearance_positive':all(r['critical_hardware_min_distance_mm']>0 for r in rows),'mass_lt_5g':total<5.0,'actual_M3_nut_fit_measured':False,'bench_clamp_force_test_required':True,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
