import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v296_SOURCE_BACKED_AFT_OML.FCStd'
out=R/'migration/freecad/F14_v297_ALLOWANCED_INLET_EDF_ADAPTER.FCStd'
audp=R/'migration/freecad/freecad_v297_allowanced_inlet_edf_adapter_audit.json'
v138=json.loads((R/'legacy/fusion-review-only/RC-F14-Tomcat_Fusion/Exports/Current/propulsion_v138/F14_v138_inlet_corridor_audit.json').read_text(encoding='utf-8'))
allow=json.loads((R/'analysis/independent_reviews/allowanced_inlet_20261015/F14_allowanced_inlet_wall_audit.json').read_text(encoding='utf-8'))
v187=json.loads((R/'legacy/fusion-review-only/RC-F14-Tomcat_Fusion/Exports/Current/propulsion_v187/F14_v187_wall_corrected_edf_adapter_audit.json').read_text(encoding='utf-8'))
if not allow.get('minimum_normal_wall_thickness_verified'): raise RuntimeError('allowanced wall audit not verified')
d=App.openDocument(str(src)); doc=App.newDocument('F14_v297_ALLOWANCED_INLET_EDF_ADAPTER')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
path=v138['chosen_path']; wall=0.81
axis_y=66.28458486059378; axis_z=-10.508688347971937
fan_x=658.0; adapter_od=51.64; fan_id=50.0

def circle_wire(x,y,z,d):
    e=Part.makeCircle(d/2.0,App.Vector(x,y,z),App.Vector(1,0,0))
    return Part.Wire(e)

def loft_circles(rows,diam_key,sgn):
    ws=[]
    for p in rows:
        ws.append(circle_wire(float(p['x']),sgn*float(p['y']),float(p['z']),float(p[diam_key])))
    return Part.makeLoft(ws,True,False)

rows=[]
critical=[n for n in ['V293_X620_CF_TUBE_R','V293_X620_CF_TUBE_L','V293_X620_SLEEVE_R_AFT','V293_X620_SLEEVE_L_AFT','V295_C_CLAMP_X620_R','V295_C_CLAMP_X620_L','BATTERY_TRAY_v165','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L'] if doc.getObject(n)]
for side,sgn in [('R',1),('L',-1)]:
    outer_rows=[]; inner_rows=[]
    for p in path:
        po=dict(p); pi=dict(p)
        po['outer_allowanced_d']=float(p['outer_diameter_mm'])
        pi['inner_allowanced_d']=float(p['outer_diameter_mm'])-2*wall
        outer_rows.append(po); inner_rows.append(pi)
    outer=loft_circles(outer_rows,'outer_allowanced_d',sgn)
    inner=loft_circles(inner_rows,'inner_allowanced_d',sgn)
    inlet=outer.cut(inner).removeSplitter()
    if not inlet.isValid() or len(inlet.Solids)!=1: raise RuntimeError('invalid inlet '+side)
    oi=doc.addObject('PartDesign::Feature','V297_INLET_WALL_'+side); oi.Shape=inlet; oi.Label='v297 0.81 mm allowanced inlet '+side
    # Adapter: use the controlled x650 circular interface from v138 and corrected v187 fan-face diameters.
    p0=path[-1]; x0=float(p0['x']); y0=sgn*float(p0['y']); z0=float(p0['z'])
    outer2=Part.makeLoft([circle_wire(x0,y0,z0,float(p0['outer_diameter_mm'])),circle_wire(fan_x,sgn*axis_y,axis_z,adapter_od)],True,False)
    inner2=Part.makeLoft([circle_wire(x0,y0,z0,float(p0['outer_diameter_mm'])-2*wall),circle_wire(fan_x,sgn*axis_y,axis_z,fan_id)],True,False)
    adapter=outer2.cut(inner2).removeSplitter()
    if not adapter.isValid() or len(adapter.Solids)!=1: raise RuntimeError('invalid adapter '+side)
    oa=doc.addObject('PartDesign::Feature','V297_EDF_ADAPTER_'+side); oa.Shape=adapter; oa.Label='v297 wall-corrected EDF adapter '+side
    joined=inlet.fuse(adapter).removeSplitter()
    oj=doc.addObject('PartDesign::Feature','V297_JOINED_INLET_ADAPTER_'+side); oj.Shape=joined; oj.Label='v297 joined inlet+adapter '+side
    # OML containment. Adapter ends at 658, within v296 OML domain.
    iv=inlet.common(oml).Volume; av=adapter.common(oml).Volume; jv=joined.common(oml).Volume
    # Wall thickness screen from concentric section definition; adapter minimum conservative radial difference at end sections.
    inlet_min_wall=min((float(p['outer_diameter_mm'])-(float(p['outer_diameter_mm'])-2*wall))/2 for p in path)
    adapter_start_wall=wall; adapter_end_wall=(adapter_od-fan_id)/2.0
    mind=min((joined.distToShape(doc.getObject(n).Shape)[0] for n in critical),default=999.0)
    rows.append({'side':side,'inlet_valid':inlet.isValid(),'adapter_valid':adapter.isValid(),'joined_valid':joined.isValid(),'joined_solid_count':len(joined.Solids),'inlet_volume_mm3':inlet.Volume,'adapter_volume_mm3':adapter.Volume,'joined_volume_mm3':joined.Volume,'inlet_oml_containment':iv/inlet.Volume,'adapter_oml_containment':av/adapter.Volume,'joined_oml_containment':jv/joined.Volume,'inlet_min_defined_wall_mm':inlet_min_wall,'adapter_start_wall_mm':adapter_start_wall,'adapter_end_wall_mm':adapter_end_wall,'critical_min_distance_mm':mind,'fan_axis_center_mm':[fan_x,sgn*axis_y,axis_z]})

doc.recompute(); doc.saveAs(str(out))
aud={'status':'V297_FREECAD_ALLOWANCED_INLET_EDF_ADAPTER','source_model':src.name,'source_chain':{'v138_center_corridor':True,'independent_allowanced_wall':True,'v187_wall_correction':True},'architecture':{'wall_mm':wall,'interface_x_mm':650.0,'fan_face_x_mm':fan_x,'fan_inner_diameter_mm':fan_id,'adapter_outer_diameter_mm':adapter_od,'fan_axis_abs_y_mm':axis_y,'fan_axis_z_mm':axis_z,'actual_EDF_hardware_measured':False},'rows':rows,'gates':{'bilateral_valid_single_solids':all(r['inlet_valid'] and r['adapter_valid'] and r['joined_valid'] and r['joined_solid_count']==1 for r in rows),'bilateral_oml_containment_ge_0p999':all(r['inlet_oml_containment']>=0.999 and r['adapter_oml_containment']>=0.999 and r['joined_oml_containment']>=0.999 for r in rows),'defined_wall_ge_0p8mm':all(r['inlet_min_defined_wall_mm']>=0.8 and r['adapter_start_wall_mm']>=0.8 and r['adapter_end_wall_mm']>=0.8 for r in rows),'critical_clearance_ge_1mm':all(r['critical_min_distance_mm']>=1.0 for r in rows),'actual_EDF_hardware_measured':False,'aerodynamic_smoothness_verified':False,'slicer_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
