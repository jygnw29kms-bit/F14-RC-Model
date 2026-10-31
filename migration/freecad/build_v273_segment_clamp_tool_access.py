import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v272_RETAINED_SERVICEABLE_ENDMODEL.FCStd'; out=R/'migration/freecad/F14_v273_SEGMENT_CLAMP_TOOL_ACCESS.FCStd'; audp=R/'migration/freecad/freecad_v273_segment_clamp_tool_access_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v273_SEGMENT_CLAMP_TOOL_ACCESS')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
# x, abs y, z screw-axis, dedicated access? X440 is already inside sweep service keepout.
spec=[(220,20,-4.35),(840,30,5.65)]
critical_names=['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L']
rows=[]
for x,ay,z in spec:
  for sgn in (-1,1):
    y=sgn*ay; start=App.Vector(x+5.5,y,z); vec=App.Vector(0,sgn*140,0)
    ko=Part.makeCylinder(4.0,vec.Length,start,vec)
    tag=f'X{x}_{"R" if sgn>0 else "L"}'; o=doc.addObject('PartDesign::Feature','V273_TOOL_ACCESS_'+tag); o.Shape=ko; o.Label=f'v273 8mm clamp tool access keepout {tag}'
    hits={}
    for n in critical_names:
      ob=doc.getObject(n)
      if ob: hits[n]=ko.common(ob.Shape).Volume
    rows.append({'cut_x_mm':x,'side':'R' if sgn>0 else 'L','valid':ko.isValid(),'tool_corridor_d_mm':8.0,'length_mm':140.0,'critical_intersections_mm3':hits,'max_critical_intersection_mm3':max(hits.values()) if hits else 0.0})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V273_SEGMENT_CLAMP_TOOL_ACCESS','source':src.name,'architecture':{'X440_uses_existing_sweep_hatch':True,'X220_and_X840_dedicated_tool_corridors':True,'corridor_is_keepout_not_shell_cut':True},'rows':rows,'gates':{'all_valid':all(r['valid'] for r in rows),'no_critical_hardware_intersection':all(r['max_critical_intersection_mm3']<1e-6 for r in rows),'final_shell_access_hole_diameter_frozen':False,'tool_fit_bench_required':True,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
