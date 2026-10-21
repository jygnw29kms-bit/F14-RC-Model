from pathlib import Path
import json, itertools, math, statistics, hashlib
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'analysis' / 'original_front_sources' / 'UPC_NASA_wing_plan_edge_screen.json'
OUT = ROOT / 'analysis' / 'original_front_sources' / 'UPC_NASA_wing_plan_registration_fit.json'
j = json.loads(SRC.read_text(encoding='utf-8'))
obs=[]
for row in j['rows']:
    for side in row['sides']:
        s=side['sample_rows']
        if not s: continue
        xmin=float(statistics.median(x['x_min_px'] for x in s))
        xmax=float(statistics.median(x['x_max_px'] for x in s))
        obs.append({'wbl_in':row['wbl_in'],'side':side['side'],'edge':'LE','fs_in':row['nasa_le_fs_in'],'x_px':xmin})
        obs.append({'wbl_in':row['wbl_in'],'side':side['side'],'edge':'TE','fs_in':row['nasa_te_fs_in'],'x_px':xmax})

# Robust pair-generated affine candidates x_px = intercept + slope_px_per_in * FS.
best=None
for a,b in itertools.combinations(obs,2):
    dfs=b['fs_in']-a['fs_in']
    if abs(dfs)<5: continue
    slope=(b['x_px']-a['x_px'])/dfs
    if not (1.8 <= slope <= 2.5): continue
    intercept=a['x_px']-slope*a['fs_in']
    residuals=[abs(o['x_px']-(intercept+slope*o['fs_in'])) for o in obs]
    inliers=[i for i,r in enumerate(residuals) if r<=5.0]
    if len(inliers)<2: continue
    score=(len(inliers),-sum(residuals[i]**2 for i in inliers))
    if best is None or score>best['score']:
        best={'score':score,'inliers':inliers,'seed_slope':slope,'seed_intercept':intercept}

if best is None:
    raise RuntimeError('no robust fit candidate')
xs=np.array([obs[i]['fs_in'] for i in best['inliers']],float)
ys=np.array([obs[i]['x_px'] for i in best['inliers']],float)
A=np.vstack([xs,np.ones_like(xs)]).T
slope,intercept=np.linalg.lstsq(A,ys,rcond=None)[0]
for o in obs:
    o['predicted_x_px']=float(intercept+slope*o['fs_in'])
    o['residual_px']=float(o['x_px']-o['predicted_x_px'])
    o['inlier_5px']=abs(o['residual_px'])<=5.0
inliers=[o for o in obs if o['inlier_5px']]
scale_in_per_px=1.0/slope
nose93=intercept+slope*93.0
pivot=intercept+slope*524.16
report={
 'status':'UPC_NASA_WING_MULTIPOINT_AFFINE_X_FIT_SCREEN_NOT_YET_DATUM_RELEASE',
 'input':{'path':str(SRC.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(SRC.read_bytes()).hexdigest()},
 'fit':{
  'slope_px_per_fullscale_in':float(slope),
  'scale_fullscale_in_per_px':float(scale_in_per_px),
  'FS0_x_px':float(intercept),
  'FS93_x_px_prediction':float(nose93),
  'FS524_16_pivot_x_px_prediction':float(pivot),
  'inlier_count':len(inliers),
  'observation_count':len(obs),
  'inlier_rms_px':float(math.sqrt(sum(o['residual_px']**2 for o in inliers)/len(inliers))),
  'inlier_max_abs_px':float(max(abs(o['residual_px']) for o in inliers)),
 },
 'observations':obs,
 'cross_checks':{
  'Navy_FS93_visual_UPC_candidate_band_px':[443.0,450.0],
  'FS93_prediction_inside_visual_band':bool(443.0<=nose93<=450.0),
  'historical_plan_span_fullscale_in_per_px':769.5/1701.0,
  'x_vs_span_scale_relative_difference_percent':100*(scale_in_per_px-(769.5/1701.0))/(769.5/1701.0),
 },
 'limits':[
  'Raster extrema are automated and can be contaminated by panel/detail lines or overlapping drawing elements.',
  'RANSAC-style inliers show internal planform consistency, not manufacturer-drawing accuracy of the UPC secondary blueprint.',
  'A source-registration release requires independent validation against the Navy FS93 landmark and preferably a third longitudinal landmark.',
  'No master geometry or CAD placement is changed.'
 ],
 'registration_release':False,'master_change_allowed':False,'production_release':False
}
OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report['fit'],indent=2));print(json.dumps(report['cross_checks'],indent=2))
print('inliers',[(o['side'],o['edge'],o['wbl_in'],o['x_px'],round(o['residual_px'],2)) for o in inliers])
