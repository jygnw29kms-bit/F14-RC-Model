import json, math, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = BASE / 'nose_to_A_stroke_center_samples.json'
A_CIRC = BASE / 'A_circularity_screen.json'
OUT = BASE / 'nose_aspect_A_connection_screen.json'

raw = SRC.read_bytes()
data = json.loads(raw)
ac = json.loads(A_CIRC.read_text(encoding='utf-8'))
rows = []
for s in data['samples']:
    w = float(s['width_candidate_mm'])
    h = float(s['height_candidate_mm'])
    zc = 0.5 * (float(s['side_top_Z_candidate_mm']) + float(s['side_bottom_Z_candidate_mm']))
    rows.append({
        'X_candidate_mm': float(s['X_candidate_mm']),
        'width_mm': w,
        'height_mm': h,
        'width_over_height': w / h if h else None,
        'height_over_width': h / w if w else None,
        'width_minus_height_mm': w - h,
        'side_center_Z_candidate_mm': zc,
    })

crossings = []
for a, b in zip(rows, rows[1:]):
    ya = a['width_minus_height_mm']
    yb = b['width_minus_height_mm']
    if ya == 0:
        crossings.append(a['X_candidate_mm'])
    elif ya * yb < 0:
        t = -ya / (yb - ya)
        crossings.append(a['X_candidate_mm'] + t * (b['X_candidate_mm'] - a['X_candidate_mm']))

A = rows[-1]
endpoint = data['A_endpoint_comparison']
report = {
    'status': 'NASEN_ASPEKT_UND_A_ANSCHLUSS_QUANTIFIZIERT_KEINE_FORMFREIGABE',
    'eingaben': [
        {'path': str(SRC.relative_to(BASE.parents[1])), 'sha256': hashlib.sha256(raw).hexdigest()},
        {'path': str(A_CIRC.relative_to(BASE.parents[1])), 'sha256': hashlib.sha256(A_CIRC.read_bytes()).hexdigest()},
    ],
    'proben': rows,
    'breite_gleich_hoehe_kreuzung_X_candidate_mm': crossings,
    'A_anschluss': {
        'X_candidate_mm': A['X_candidate_mm'],
        'breitendifferenz_gegen_original_A_mm': endpoint['width_difference_mm'],
        'hoehenunterschied_gegen_original_A_mm': endpoint['height_difference_mm'],
        'absolute_breitendifferenz_mm': abs(endpoint['width_difference_mm']),
        'absolute_hoehenunterschied_mm': abs(endpoint['height_difference_mm']),
        'kreisfit_A_max_abs_relativ_radius': ac['radialfehler_pixel']['max_abs_relativ_radius'],
    },
    'schlussfolgerungen': [
        'Die vorhandenen Drauf- und Seitenansichtsproben verlangen keinen Kreisquerschnitt.',
        'Der Formtrend wechselt entlang der Nase von hoeher-als-breit zu leicht breiter-als-hoch.',
        'Die Breite trifft Sektion A im aktuellen Kandidatenrahmen deutlich besser als die Hoehe.',
        'Vor einer 3D-Loftstudie muss der Seitenansichts-/Hoehenanschluss an Sektion A geklaert werden.',
        'Keine automatische Ellipse, Superellipse oder Kreisform aus diesen Daten ableiten.'
    ],
    'naechster_schritt': 'Ursache der Hoehenabweichung an A zwischen Seitenansicht, Achslage und originaler Sektion A isolieren; erst danach Querschnittskandidaten als Studie erzeugen.',
    'geometrie_geaendert': False,
    'master_geaendert': False,
    'produktion_freigegeben': False,
}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(report, indent=2, ensure_ascii=False))
