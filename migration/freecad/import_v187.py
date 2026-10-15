import FreeCAD as App
import Part, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(BASE, 'export', 'F14_v187_WALL_CORRECTED_EDF_ADAPTER.step')
AUDIT = os.path.join(BASE, 'export', 'F14_v187_wall_corrected_edf_adapter_audit.json')
OUT = os.path.join(BASE, 'freecad_import_audit.json')

if not os.path.exists(STEP):
    raise RuntimeError('STEP export missing: ' + STEP)

with open(AUDIT, encoding='utf-8') as f:
    fusion = json.load(f)

doc = App.newDocument('F14_v187_FreeCAD_Import')
shape = Part.read(STEP)
obj = doc.addObject('PartDesign::Feature', 'F14_v187_IMPORTED_STEP')
obj.Label = 'F14 v187 imported from Fusion STEP'
obj.Shape = shape

def bb(s):
    b=s.BoundBox
    return {'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}

result = {
    'status':'FREECAD_STEP_IMPORT_AUDIT',
    'step_path':STEP,
    'shape_valid':shape.isValid(),
    'shape_null':shape.isNull(),
    'solids':len(shape.Solids),
    'shells':len(shape.Shells),
    'faces':len(shape.Faces),
    'edges':len(shape.Edges),
    'volume_mm3':shape.Volume,
    'bounds_mm':bb(shape),
    'fusion_reference_status':fusion.get('status'),
    'print_release':False
}
with open(OUT,'w',encoding='utf-8') as f:
    json.dump(result,f,indent=2)
doc.recompute()
doc.saveAs(os.path.join(BASE,'F14_v187_FreeCAD_Import.FCStd'))
print(json.dumps(result,indent=2))
