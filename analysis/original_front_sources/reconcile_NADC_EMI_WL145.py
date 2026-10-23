import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'analysis' / 'original_front_sources'
NADC = SRC / 'NADC_WL12_1_vertical_datum_candidate.json'
EMI_IMG = SRC / 'NASA_F14_EMI' / 'page_182_rotated270.png'
OUT = SRC / 'NADC_EMI_WL145_source_convergence.json'

nadc = json.loads(NADC.read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

nadc_wl = float(nadc['WL12_1_candidate_fullscale']['nominal_in'])
nadc_lo, nadc_hi = map(float, nadc['WL12_1_candidate_fullscale']['rounding_only_interval_in'])
emi_centroid_wl = 145.0
emi_bottom_wl = 120.0
emi_radius = 34.0
rc_mm_per_in = 1.1697428086486623

delta = nadc_wl - emi_centroid_wl
result = {
  'status': 'NADC_EMI_GLOBAL_WL145_ENGINEERING_CONVERGENCE_C_NOT_REGISTERED',
  'inputs': {
    str(NADC.relative_to(ROOT)).replace('\\','/'): sha(NADC),
    str(EMI_IMG.relative_to(ROOT)).replace('\\','/'): sha(EMI_IMG),
  },
  'NADC': {
    'source': 'NADC-81293-60 / AD-A124468 Figure 3, 1:12 model',
    'model_WL_in': 12.1,
    'fullscale_candidate_WL_in': nadc_wl,
    'rounding_only_interval_in': [nadc_lo, nadc_hi],
  },
  'NASA_EMI': {
    'source': 'NASA F-14 EM analysis Aircraft Data, Figure 16',
    'fuselage_centroid_WL_in': emi_centroid_wl,
    'bottom_WL_in': emi_bottom_wl,
    'fuselage_radius_in': emi_radius,
    'consistency_check_bottom_plus_radius_in': emi_bottom_wl + emi_radius,
    'note': 'EMI model is a simplified electromagnetic-analysis geometry; its centroid WL is a datum clue, not OML metrology.'
  },
  'comparison': {
    'NADC_minus_EMI_centroid_WL_in': delta,
    'absolute_difference_in': abs(delta),
    'absolute_difference_RC_mm': abs(delta) * rc_mm_per_in,
    'EMI_centroid_inside_NADC_rounding_interval': nadc_lo <= emi_centroid_wl <= nadc_hi,
  },
  'gate': {
    'global_WL_near_145_supported_for_cross_source_engineering_study': nadc_lo <= emi_centroid_wl <= nadc_hi,
    'global_WL145_production_verified': False,
    'UPC_C_local_axis_tied_to_global_WL145': False,
    'C_absolute_Z_registered': False,
    'ABCDEF_absolute_Z_loft_allowed': False,
    'master_change_allowed': False,
    'production_release': False,
  },
  'next_step': 'Find a homologous vertical landmark that ties the detached UPC C-section local axis to the global aircraft WL~145 reference. Do not translate C merely because two global-datum sources agree.'
}
OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(OUT)
print(json.dumps(result['comparison'], indent=2))