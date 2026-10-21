from pathlib import Path
import json, hashlib, math
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
FIT=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_wing_plan_registration_fit.json'
OUT=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_wing_plan_registration_sensitivity.json'
j=json.loads(FIT.read_text(encoding='utf-8'))
obs=j['observations']

def fit(rows, fixed_scale_in_per_px=None):
    xs=np.array([r['fs_in'] for r in rows],float); ys=np.array([r['x_px'] for r in rows],float)
    if fixed_scale_in_per_px is None:
        A=np.vstack([xs,np.ones_like(xs)]).T
        slope,intercept=np.linalg.lstsq(A,ys,rcond=None)[0]
    else:
        slope=1.0/fixed_scale_in_per_px
        intercept=float(np.mean(ys-slope*xs))
    residual=ys-(intercept+slope*xs)
    return dict(n=len(rows),slope_px_per_in=float(slope),scale_in_per_px=float(1/slope),FS0_x_px=float(intercept),FS93_x_px=float(intercept+slope*93.0),pivot_FS524_16_x_px=float(intercept+slope*524.16),rms_px=float(math.sqrt(np.mean(residual**2))),max_abs_px=float(np.max(np.abs(residual))))

inliers=[r for r in obs if r['inlier_5px']]
span_scale=float(j['cross_checks']['historical_plan_span_fullscale_in_per_px'])
rows=[]
for name,sub in [
 ('all_5px_inliers',inliers),
 ('lower_only',[r for r in inliers if r['side']=='lower']),
 ('upper_only',[r for r in inliers if r['side']=='upper']),
 ('LE_only',[r for r in inliers if r['edge']=='LE']),
 ('TE_only',[r for r in inliers if r['edge']=='TE']),
 ('mid_stations_164_to_348',[r for r in inliers if 164<=r['wbl_in']<=348]),
 ('lower_mid_164_to_348',[r for r in inliers if r['side']=='lower' and 164<=r['wbl_in']<=348]),
]:
    if len(sub)>=2:
        rows.append({'case':name,'free_affine':fit(sub),'span_scale_constrained':fit(sub,span_scale)})

fs93=[r['free_affine']['FS93_x_px'] for r in rows]
fs93c=[r['span_scale_constrained']['FS93_x_px'] for r in rows]
out={
 'status':'UPC_NASA_WING_REGISTRATION_SENSITIVITY_SCREEN_FAIL_CLOSED',
 'input_sha256':hashlib.sha256(FIT.read_bytes()).hexdigest(),
 'span_scale_fullscale_in_per_px':span_scale,
 'cases':rows,
 'summary':{
  'free_FS93_range_px':[min(fs93),max(fs93)],
  'span_constrained_FS93_range_px':[min(fs93c),max(fs93c)],
  'navy_UPC_FS93_candidate_band_px':[443.0,450.0],
  'any_free_case_hits_band':any(443<=x<=450 for x in fs93),
  'any_span_constrained_case_hits_band':any(443<=x<=450 for x in fs93c),
 },
 'interpretation':[
  'Freie X-Skalierung testet interne NASA/UPC-Planformpassung.',
  'Spannweiten-konstante Skalierung testet isotrope Rasterhypothese aus der unabhängigen 900-mm/Grumman-Halbspannweite.',
  'Gruppenfits dienen nur der Robustheits- und Anisotropieprüfung; kein Einzelfall wird nachträglich ausgewählt, um FS93 passend zu machen.',
  'Eine Freigabe verlangt konsistente FS93-Lage über vernünftige Gruppen und eine unabhängige dritte Längsmarke.'
 ],
 'registration_release':False,'master_change_allowed':False,'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out['summary'],indent=2));
for r in rows: print(r['case'],'free',round(r['free_affine']['FS93_x_px'],3),'span',round(r['span_scale_constrained']['FS93_x_px'],3),'rms',round(r['free_affine']['rms_px'],3),round(r['span_scale_constrained']['rms_px'],3))
