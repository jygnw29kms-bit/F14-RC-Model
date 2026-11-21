"""Revisionsgebundene Rechenstudie; keine native CAD-Ausfuehrung."""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pointer_path = ROOT / 'migration/freecad/CURRENT.json'
pointer = json.loads(pointer_path.read_text(encoding='utf-8-sig'))
master = ROOT / pointer['current_master']
basis_path = ROOT / 'analysis/v192_surface_volume_mass_basis_audit.json'
basis = json.loads(basis_path.read_text(encoding='utf-8'))
assert pointer['current_revision'] == 'v192', 'Neue Revision erfordert neue native Flaechenbasis'
assert sha(master) == basis['source_sha256'], 'CAD-Datei passt nicht zur Flaechenbasis'
names = ['FUSELAGE_CURRENT', 'WING_R', 'WING_L', 'STABILATOR_L', 'STABILATOR_R',
         'VTAIL_L', 'VTAIL_R', 'VENTRAL_L', 'VENTRAL_R']
by_name = {row['name']: row for row in basis['rows']}
assert len(by_name) == len(basis['rows'])
areas = {name: by_name[name]['surface_area_mm2'] for name in names}
assert all(by_name[name]['valid'] and math.isfinite(area) and area > 0
           for name, area in areas.items())
total = math.fsum(areas.values())
rows = []
for name, area in areas.items():
    rows.append({'object': name, 'reference_area_mm2': area,
                 'fraction_of_selected_reference_area': area / total,
                 'conditional_layer_mass_g_at_0_4mm': {
                     str(density): area * 0.4 * density / 1000 for density in (1.07, 1.27)}})
result = {
    'status': 'REVISIONSGEBUNDENE_REFERENZFLAECHEN_ANTEILE_KEINE_DRUCKMASSE',
    'current_revision': pointer['current_revision'], 'master_sha256': sha(master),
    'native_basis_sha256': sha(basis_path), 'pointer_sha256': sha(pointer_path),
    'total_selected_reference_area_mm2': total, 'rows': rows,
    'limits': [
        '0.4 mm und Dichten 1.07/1.27 g/cm3 sind Rechenannahmen, keine Konstruktions- oder Materialfreigabe.',
        'Objektflaechen enthalten End- und Anschlussflaechen; keine exklusive physische Druckhaut.',
        'Flaechenanteil ist kein Anteil am Abfluggewicht. Rippen, Verbindungen und Hardware fehlen.',
        'Keine strukturelle Mindestdicke, kein Slicergebnis, kein gemessenes Gewicht.',
        'Originalhautregistrierung und physischer Schalenaufbau bleiben offen.'
    ], 'production_release': False, 'flight_release': False}
out = ROOT / 'analysis/v192_reference_area_component_shares.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'area_mm2': total, 'fuselage_fraction': rows[0]['fraction_of_selected_reference_area'],
                  'output': str(out)}))
