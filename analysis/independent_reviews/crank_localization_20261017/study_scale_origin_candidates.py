"""Registration sensitivity only: neither source labels nor CAD placement are promoted."""
from pathlib import Path
import json,hashlib,itertools
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
paths=['analysis/propulsion_source_silhouette_constraints_v134.json','analysis/independent_reviews/crank_localization_20261017/UPC_metric_ruler_scale_screen.json','analysis/independent_reviews/crank_localization_20261017/UPC_dimension_span_crosscheck.json']
f,ru,sp=[json.loads((R/p).read_text()) for p in paths]
scales={'historical':f['common_scale_mm_per_pixel'],'plan_span_900':sp['900mm_model_scale_from_plan_tip_span'],'ruler_midpoint':sum(ru['ruler_model_mm_per_pixel_interval'])/2}
oldzero=f['x_mapping']['E_source_px']-f['x_mapping']['E_model_mm']/scales['historical']; pivot=504.3463093769572
rows=[]
for (name,s),nose in itertools.product(scales.items(),[443.,446.5,450.]):
 rows.append(dict(scale_case=name,scale_mm_per_px=s,nose_source_px_candidate=nose,E_X_candidate_mm=(f['x_mapping']['E_source_px']-nose)*s,E_shift_vs_historical_mm=(f['x_mapping']['E_source_px']-nose)*s-f['x_mapping']['E_model_mm'],NASA_pivot_source_x_prediction_px=nose+pivot/s,NASA_pivot_not_visible_measured=True))
assert len(rows)==9
j=dict(status='NINE_SCALE_ORIGIN_SENSITIVITY_CASES_CALCULATED_NOT_REGISTERED',inputs=[dict(path=p,sha256=hashlib.sha256((R/p).read_bytes()).hexdigest()) for p in paths],historical_implied_zero_px=oldzero,rows=rows,pivot_prediction_spread_px=max(x['NASA_pivot_source_x_prediction_px'] for x in rows)-min(x['NASA_pivot_source_x_prediction_px'] for x in rows),visual_review='Original upper glove/wing root crop shows outlines and panels but no unambiguous labeled pivot center. Do not select a panel corner as the pivot merely because it matches a prediction.',limits=['443..450 nose band is a visual hypothesis, not a verified station datum.','Ruler normalization is an alternative hypothesis, not a uniform scaling correction.','No evaluated case is a measured fit or acceptable production assembly.','Pivot FS convention, independent axial landmark and WL remain gates.'],next='Find an explicitly station-indexed radome joint or wing-root landmark in a primary drawing; compare with source contour before generating a corrected assembly.',native_execution=False,geometry_changed=False,production_release=False)
(O/'scale_origin_sensitivity_cases.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'predicted_pivot_x_pixel_spread':j['pivot_prediction_spread_px'],'E_delta_range':[min(x['E_shift_vs_historical_mm'] for x in rows),max(x['E_shift_vs_historical_mm'] for x in rows)]}))
