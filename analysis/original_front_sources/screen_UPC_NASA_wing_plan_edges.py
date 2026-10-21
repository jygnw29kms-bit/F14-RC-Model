from pathlib import Path
import json, hashlib
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'references' / 'UPC_Figure3_15_source_exact.png'
WING = ROOT / 'cad' / 'fusion' / 'F14TomcatRC' / 'NASA_F14_basic_wing_v08.json'
OUT = ROOT / 'analysis' / 'original_front_sources' / 'UPC_NASA_wing_plan_edge_screen.json'

img = np.array(Image.open(SRC).convert('L'))
wing = json.loads(WING.read_text(encoding='utf-8'))
sections = wing['sections']
# UPC span screen: dark tip extrema y=445 and 2146 -> center 1295.5, half span 850.5 px.
y_tip_upper, y_tip_lower = 445.0, 2146.0
y_center = (y_tip_upper + y_tip_lower) / 2.0
half_span_px = (y_tip_lower - y_tip_upper) / 2.0
wbl_tip = float(sections[-1]['wbl_in'])
y_scale_in_per_px = wbl_tip / half_span_px
threshold = 128
x_roi = [1050, 1900]
rows = []
for s in sections:
    wbl = float(s['wbl_in'])
    rec = {
        'wbl_in': wbl,
        'nasa_le_fs_in': float(s['leading_edge_fs_in']),
        'nasa_te_fs_in': float(s['trailing_edge_fs_in']),
        'sides': []
    }
    for side, sign in [('upper', -1), ('lower', 1)]:
        yf = y_center + sign * wbl / y_scale_in_per_px
        yc = int(round(yf))
        candidates = []
        for y in range(yc-2, yc+3):
            xs = np.where(img[y, x_roi[0]:x_roi[1]+1] < threshold)[0] + x_roi[0]
            if len(xs):
                candidates.append({'y_px': y, 'x_min_px': int(xs.min()), 'x_max_px': int(xs.max()), 'dark_count': int(len(xs))})
        rec['sides'].append({'side': side, 'predicted_y_px': yf, 'sample_rows': candidates})
    rows.append(rec)
report = {
    'status': 'UPC_NASA_WING_PLAN_EDGE_RASTER_SCREEN_NOT_REGISTERED',
    'inputs': {
        str(SRC.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(SRC.read_bytes()).hexdigest(),
        str(WING.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(WING.read_bytes()).hexdigest(),
    },
    'threshold': threshold,
    'x_roi_px': x_roi,
    'y_center_from_tip_extrema_px': y_center,
    'half_span_px': half_span_px,
    'nasa_tip_wbl_in': wbl_tip,
    'y_scale_in_per_px_from_nasa_tip': y_scale_in_per_px,
    'rows': rows,
    'limits': [
        'Raster extrema can include panel lines, labels or overlapping drawing elements.',
        'No edge is promoted until upper/lower symmetry and NASA planform consistency are checked.',
        'The NASA basic wing is source-backed but the UPC drawing is a secondary blueprint source.',
        'No geometry or master datum is changed.'
    ],
    'production_release': False,
}
OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')
print('y_center', y_center, 'scale_in_per_px', y_scale_in_per_px)
for r in rows:
    vals=[]
    for sd in r['sides']:
        mids=sd['sample_rows']
        vals.append((sd['side'], round(sd['predicted_y_px'],2), [(x['x_min_px'],x['x_max_px']) for x in mids]))
    print(r['wbl_in'], vals)
