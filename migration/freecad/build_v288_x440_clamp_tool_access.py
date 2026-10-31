import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v287_CAPTIVE_M3_SEGMENT_CLAMPS.FCStd'; out=R/'migration/freecad/F14_v288_X440_CLAMP_TOOL_ACCESS.FCStd'; audp=R/'migration/freecad/freecad_v288_x440_clamp_tool_access_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v288_X440_CLAMP_TOOL_ACCESS')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
critical_names=['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L']
rows=[]
x=440; ay=60; z=-3.05
for sgn in (-1,1):
    side='R' if sgn>0 else 'L'; y=sgn*ay; start=App.Vector(x+5.5,y,z); vec=App.Vector(0,sgn*140,0)
    ko=Part.makeCylinder(4.0,vec.Length,start,vec); tag=f'X440_{side}'
    o=doc.addObject('PartDesign::Feature','V288_TOOL_ACCESS_'+tag); o.Shape=ko; o.Label=f'v288 8mm captive-M3 tool access keepout {tag}'
    hits={}
    for n in critical_names:
        ob=doc.getObject(n)
        if ob: hits[n]=ko.common(ob.Shape).Volume
    clamp=doc.getObject('V287_C_CLAMP_'+tag).Shape
    rows.append({'side':side,'valid':ko.isValid(),'clamp_intersection_mm3':ko.common(clamp).Volume,'clamp_distance_mm':ko.distToShape(clamp)[0],'critical_intersections_mm3':hits,'max_critical_intersection_mm3':max(hits.values()) if hits else 0.0})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V288_X440_CLAMP_TOOL_ACCESS','source':src.name,'rows':rows,'gates':{'both_corridors_valid':all(r['valid'] for r in rows),'both_reach_clamps':all(r['clamp_intersection_mm3']>0 and r['clamp_distance_mm']==0 for r in rows),'no_critical_hardware_intersection':all(r['max_critical_intersection_mm3']<1e-6 for r in rows),'final_shell_access_hole_frozen':False,'tool_fit_bench_required':True,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
