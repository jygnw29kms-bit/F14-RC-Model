"""Prepared read-only v192 adapter screen. Run only after native job gate is clear."""
from pathlib import Path
import hashlib
import json
import FreeCAD as App
ROOT = Path(__file__).resolve().parents[2]
pointer = json.loads((ROOT / 'migration/freecad/CURRENT.json').read_text(encoding='utf-8-sig'))
assert pointer['current_revision'] == 'v192', 'Review script for new revision first'
source = ROOT / pointer['current_master']
before = hashlib.sha256(source.read_bytes()).hexdigest()
basis = json.loads((ROOT / 'analysis/v192_surface_volume_mass_basis_audit.json').read_text(encoding='utf-8'))
assert before == basis['source_sha256'], 'Current master differs from inspected basis'
doc = App.openDocument(str(source))
rows = []
try:
    for side in ('R', 'L'):
        obj = doc.getObject('INLET_EDF_' + side)
        assert obj is not None
        shape = obj.Shape
        curves = [f for f in shape.Faces if type(f.Surface).__name__ != 'Plane']
        planes = [f for f in shape.Faces if type(f.Surface).__name__ == 'Plane']
        assert len(curves) == 2 and len(planes) == 2, 'Unexpected topology; do not apply two-face method'
        gap = curves[0].distToShape(curves[1])[0]
        fan = max(planes, key=lambda f: f.BoundBox.XMax)
        radii = sorted([float(e.Curve.Radius) for e in fan.Edges if hasattr(e.Curve, 'Radius')], reverse=True)
        assert len(radii) == 2, 'Expected exactly two circular fan boundaries'
        rows.append(dict(object=obj.Name, valid=shape.isValid(), solids=len(shape.Solids),
                         minimum_curved_face_distance_mm=gap, fan_radii_mm=radii,
                         fan_radial_gap_mm=radii[0]-radii[1],
                         conditional_0p8mm_gap_screen=bool(gap >= 0.8 and radii[0]-radii[1] >= 0.8)))
finally:
    App.closeDocument(doc.Name)
assert before == hashlib.sha256(source.read_bytes()).hexdigest(), 'Source was changed'
result = dict(status='CURRENT_V192_ADAPTER_FACE_DISTANCE_SCREEN', source_sha256=before,
              rows=rows, limits=[
                  'Only INLET_EDF_R/L; no fuselage, wing or tail wall-thickness verification.',
                  'Distance between selected curved faces is not a complete local normal-thickness field.',
                  '0.8 mm is the historical screening threshold, not a structural or printing qualification.',
                  'No physical print, flow, strength or flight test performed.'
              ], print_release=False, flight_release=False)
output = ROOT / 'analysis/v192_current_adapter_face_distance_audit.json'
assert not output.exists(), 'Preserve existing audit; review before replacing'
output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result))
