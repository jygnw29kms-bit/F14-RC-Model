import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'analysis'/'original_front_sources'
SENS = SRC/'C_axis_closure_sensitivity.json'
FRAME = SRC/'front_shared_frame_candidate.json'
PIX = SRC/'front_sections_pixel_candidates.json'
OUT = SRC/'C_neutral_vs_legacy_frame.json'

sens = json.loads(SENS.read_text(encoding='utf-8'))
frame = json.loads(FRAME.read_text(encoding='utf-8'))
pix = json.loads(PIX.read_text(encoding='utf-8'))
case = next(c for c in sens['cases'] if c['threshold']==128 and c['offset_pixel']==0)
f = frame['profiles'][2]
p = pix['profiles'][2]
scale = float(f['isotropic_mm_per_section_pixel'])
axis_px = p['source_section_axis_pixel']
pts = case['points_pixel']
ys = [(x-axis_px[0])*scale for x,y in pts]
zs = [float(f['axis_Z_candidate_mm']) + (axis_px[1]-y)*scale for x,y in pts]
legacy = f['loops_xyz_candidate_mm'][0]
ly = [q[1] for q in legacy]
lz = [q[2] for q in legacy]

def span(v): return max(v)-min(v)
neutral = {
    'width_mm': span(ys), 'height_mm': span(zs),
    'Y_min_mm': min(ys), 'Y_max_mm': max(ys),
    'Z_min_mm': min(zs), 'Z_max_mm': max(zs),
    'center_Y_mm': (min(ys)+max(ys))/2,
    'center_Z_mm': (min(zs)+max(zs))/2,
    'vertices': len(pts)
}
old = {
    'width_mm': span(ly), 'height_mm': span(lz),
    'Y_min_mm': min(ly), 'Y_max_mm': max(ly),
    'Z_min_mm': min(lz), 'Z_max_mm': max(lz),
    'center_Y_mm': (min(ly)+max(ly))/2,
    'center_Z_mm': (min(lz)+max(lz))/2,
    'vertices': len(legacy)
}
out = {
    'status':'C_NEUTRAL_GEGEN_ALTEN_GEMEINSAMEN_RAHMEN_GEPRUEFT_KEINE_LOFTFREIGABE',
    'inputs': {x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (SENS,FRAME,PIX)},
    'station_X_mm': float(f['station_X_candidate_mm']),
    'scale_mm_per_pixel': scale,
    'neutral_candidate': neutral,
    'legacy_C_polygon': old,
    'differences_neutral_minus_legacy': {
        'width_mm': neutral['width_mm']-old['width_mm'],
        'height_mm': neutral['height_mm']-old['height_mm'],
        'center_Y_mm': neutral['center_Y_mm']-old['center_Y_mm'],
        'center_Z_mm': neutral['center_Z_mm']-old['center_Z_mm']
    },
    'legacy_side_height_residual_pixels': float(f['side_height_residual_pixels']),
    'limits':[
        'Neutraler C-Kandidat nutzt weiterhin den historischen Kandidatenmaßstab und die historische Achslage.',
        'Bessere Rastertreue allein verifiziert die metrische Registrierung nicht.',
        'Kein Loft, keine Master-Aenderung und keine Produktionsfreigabe.'
    ],
    'next_step':'C-Hoehenregistrierung unabhaengig von der alten Achslage gegen Seitenprojektion pruefen.',
    'master_change_allowed':False,
    'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
