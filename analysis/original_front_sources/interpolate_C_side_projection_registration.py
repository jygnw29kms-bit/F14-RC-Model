import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'analysis'/'original_front_sources'
BC = SRC/'BC_projection_samples.json'
CD = SRC/'CD_projection_samples_v2.json'
FRAME = SRC/'front_shared_frame_candidate.json'
SENS = SRC/'C_axis_closure_sensitivity.json'
PIX = SRC/'front_sections_pixel_candidates.json'
OUT = SRC/'C_side_projection_registration_screen.json'

bc = json.loads(BC.read_text(encoding='utf-8'))
cd = json.loads(CD.read_text(encoding='utf-8'))
frame = json.loads(FRAME.read_text(encoding='utf-8'))
sens = json.loads(SENS.read_text(encoding='utf-8'))
pix = json.loads(PIX.read_text(encoding='utf-8'))
f = frame['profiles'][2]
station = float(f['station_X_candidate_mm'])

samples = []
for src,name in ((bc,'BC'),(cd,'CD_v2')):
    for s in src['samples']:
        if s.get('top_Z_candidate_mm') is not None and s.get('bottom_Z_candidate_mm') is not None:
            samples.append((float(s['X_candidate_mm']), float(s['top_Z_candidate_mm']), float(s['bottom_Z_candidate_mm']), name, s['source_x_pixel']))
samples.sort()
left = max(s for s in samples if s[0] < station)
right = min(s for s in samples if s[0] > station)
t = (station-left[0])/(right[0]-left[0])
interp_top = left[1] + t*(right[1]-left[1])
interp_bottom = left[2] + t*(right[2]-left[2])
interp_height = interp_top-interp_bottom
interp_center = (interp_top+interp_bottom)/2

case = next(c for c in sens['cases'] if c['threshold']==128 and c['offset_pixel']==0)
p = pix['profiles'][2]
scale = float(f['isotropic_mm_per_section_pixel'])
axis = p['source_section_axis_pixel']
zs = [float(f['axis_Z_candidate_mm']) + (axis[1]-y)*scale for x,y in case['points_pixel']]
neutral_top, neutral_bottom = max(zs), min(zs)
neutral_height = neutral_top-neutral_bottom
neutral_center = (neutral_top+neutral_bottom)/2
height_scale_needed = interp_height/neutral_height
translation_after_scale = interp_center-neutral_center

out = {
    'status':'C_SEITENPROJEKTIONS_REGISTRIERUNG_INTERPOLIERT_NUR_STUDIE',
    'inputs':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (BC,CD,FRAME,SENS,PIX)},
    'station_X_mm':station,
    'bracketing_samples':{
        'left':{'X_mm':left[0],'top_Z_mm':left[1],'bottom_Z_mm':left[2],'source':left[3],'source_x_pixel':left[4]},
        'right':{'X_mm':right[0],'top_Z_mm':right[1],'bottom_Z_mm':right[2],'source':right[3],'source_x_pixel':right[4]},
        'interpolation_fraction':t
    },
    'interpolated_side_envelope_at_C':{
        'top_Z_mm':interp_top,'bottom_Z_mm':interp_bottom,'height_mm':interp_height,'center_Z_mm':interp_center
    },
    'neutral_C_in_legacy_frame':{
        'top_Z_mm':neutral_top,'bottom_Z_mm':neutral_bottom,'height_mm':neutral_height,'center_Z_mm':neutral_center
    },
    'difference_neutral_minus_interpolated':{
        'top_Z_mm':neutral_top-interp_top,
        'bottom_Z_mm':neutral_bottom-interp_bottom,
        'height_mm':neutral_height-interp_height,
        'center_Z_mm':neutral_center-interp_center
    },
    'diagnostic_only':{
        'isotropic_vertical_scale_factor_to_match_height':height_scale_needed,
        'vertical_translation_mm_to_match_center_without_scale':translation_after_scale
    },
    'limits':[
        'Interpolation nutzt zwei Original-Seitenprojektionsproben, aber keine verifizierte C-Stationskontur.',
        'Seitensilhouette kann lokale Glove-/Inlet-/Anbauteilprojektionen enthalten.',
        'Der berechnete Skalierungsfaktor ist Diagnose und darf die C-Kontur nicht automatisch verformen.',
        'Keine gemeinsame Wasserlinie, kein Loft, keine Master-Aenderung und keine Produktionsfreigabe.'
    ],
    'next_step':'Pruefen, ob obere und untere C-Kanten semantisch zur interpolierten Seitenhülle gehoeren; erst danach Registrierungsvarianten aufbauen.',
    'master_change_allowed':False,
    'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
