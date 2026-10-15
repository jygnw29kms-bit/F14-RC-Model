import FreeCAD as App, Part, json, os, math
BASE=os.path.dirname(os.path.abspath(__file__))
EXP=os.path.join(BASE,'export')
with open(os.path.join(EXP,'exact_interface_conics.json'),encoding='utf-8') as f: conics=json.load(f)
with open(os.path.join(EXP,'F14_v187_section_inputs.json'),encoding='utf-8') as f: cfg=json.load(f)
with open(os.path.join(EXP,'F14_v187_wall_corrected_edf_adapter_audit.json'),encoding='utf-8') as f: ref=json.load(f)

def ellipse_wire(x,cy,cz,ry,rz):
    e=Part.Ellipse(App.Vector(0,0,0),ry,rz).toShape()
    e.rotate(App.Vector(0,0,0),App.Vector(1,1,1),120)
    e.translate(App.Vector(x,cy,cz))
    return Part.Wire(e)

def circle_wire(x,cy,cz,r):
    e=Part.Circle(App.Vector(0,0,0),App.Vector(0,0,1),r).toShape()
    e.rotate(App.Vector(0,0,0),App.Vector(1,1,1),120)
    e.translate(App.Vector(x,cy,cz))
    return Part.Wire(e)

def loft(sections):
    s=Part.makeLoft(sections,True,False)
    if s.isNull() or not s.isValid():
        raise RuntimeError('invalid loft')
    return s

def build_side(sign):
    outer=[ellipse_wire(r['x_mm'],sign*r['center_yz_mm'][0],r['center_yz_mm'][1],r['semi_axes_mm'][0],r['semi_axes_mm'][1]) for r in conics['outer_sections']]
    inner=[ellipse_wire(r['x_mm'],sign*r['center_yz_mm'][0],r['center_yz_mm'][1],r['semi_axes_mm'][0],r['semi_axes_mm'][1]) for r in conics['inner_flow_sections']]
    inlet=loft(outer).cut(loft(inner)).removeSplitter()
    lo=conics['outer_sections'][-1]; li=conics['inner_flow_sections'][-1]
    start_o=ellipse_wire(lo['x_mm'],sign*lo['center_yz_mm'][0],lo['center_yz_mm'][1],lo['semi_axes_mm'][0],lo['semi_axes_mm'][1])
    start_i=ellipse_wire(li['x_mm'],sign*li['center_yz_mm'][0],li['center_yz_mm'][1],li['semi_axes_mm'][0],li['semi_axes_mm'][1])
    cy=sign*cfg['fan_axis_center_y_mm']; cz=cfg['fan_axis_center_z_mm']; x=cfg['fan_face_x_mm']
    end_o=circle_wire(x,cy,cz,cfg['adapter_outer_diameter_mm']/2.0)
    end_i=circle_wire(x,cy,cz,cfg['fan_inner_diameter_mm']/2.0)
    adapter=loft([start_o,end_o]).cut(loft([start_i,end_i])).removeSplitter()
    joined=inlet.fuse(adapter).removeSplitter()
    return inlet,adapter,joined

doc=App.newDocument('F14_v187_FreeCAD_Native_Rebuild')
results=[]
for label,sign in [('R',1),('L',-1)]:
    inlet,adapter,joined=build_side(sign)
    for name,shape in [('INLET',inlet),('ADAPTER',adapter),('JOINED',joined)]:
        o=doc.addObject('PartDesign::Feature',f'{name}_{label}')
        o.Label=f'F14 v187 {name} {label}'
        o.Shape=shape
    refrow=next(r for r in ref['records'] if r['side']==label)
    results.append({
        'side':label,
        'inlet_valid':inlet.isValid(),
        'adapter_valid':adapter.isValid(),
        'joined_valid':joined.isValid(),
        'inlet_volume_mm3':inlet.Volume,
        'adapter_volume_mm3':adapter.Volume,
        'joined_volume_mm3':joined.Volume,
        'fusion_adapter_volume_mm3':refrow['adapter_volume_cm3']*1000.0,
        'fusion_joined_volume_mm3':refrow['joined_volume_cm3']*1000.0,
        'adapter_delta_mm3':adapter.Volume-refrow['adapter_volume_cm3']*1000.0,
        'joined_delta_mm3':joined.Volume-refrow['joined_volume_cm3']*1000.0,
        'joined_solids':len(joined.Solids),
        'joined_shells':len(joined.Shells),
        'joined_faces':len(joined.Faces),
        'joined_edges':len(joined.Edges),
    })

audit={'status':'FREECAD_NATIVE_V187_REBUILD','freecad_version':App.Version(),'fusion_reference_status':ref.get('status'),'results':results,'print_release':False,'flight_release':False}
with open(os.path.join(BASE,'freecad_native_v187_audit.json'),'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
doc.recompute()
doc.saveAs(os.path.join(BASE,'F14_v187_FreeCAD_Native_Rebuild.FCStd'))
Part.export([doc.getObject('JOINED_R'),doc.getObject('JOINED_L')],os.path.join(EXP,'F14_v187_FreeCAD_NATIVE_JOINED.step'))
print(json.dumps(audit,indent=2))
