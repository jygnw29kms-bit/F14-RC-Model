from pathlib import Path
import json,hashlib,itertools,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/'analysis'/'original_front_sources'/'Navy_F14_station_ruler_calibration.json'
NOSE=ROOT/'analysis'/'independent_reviews'/'crank_localization_20261017'/'UPC_probe_radome_transition_screen.json'
OUT=ROOT/'analysis'/'original_front_sources'/'Navy_UPC_side_longitudinal_landmark_fit.json'
cal=json.loads(CAL.read_text(encoding='utf-8')); nose=json.loads(NOSE.read_text(encoding='utf-8'))
f=cal['fit']; navy_px_per_in=float(f['px_per_FS_in']); navy_fs0=float(f['FS0_x_px'])
def navy_fs(x): return (x-navy_fs0)/navy_px_per_in
landmarks=[
 {'name':'FS93_radome_flare','FS_in_interval':[93.0,93.0],'navy_x_interval_px':[f['FS93_x_px'],f['FS93_x_px']],'upc_x_interval_px':[440.75,441.25]},
 {'name':'canopy_center_bow','FS_in_interval':[navy_fs(252.0),navy_fs(254.0)],'navy_x_interval_px':[252.0,254.0],'upc_x_interval_px':[909.0,910.0]},
 {'name':'aft_nozzle_endpoint','FS_in_interval':[navy_fs(569.0),navy_fs(569.0)],'navy_x_interval_px':[569.0,569.0],'upc_x_interval_px':[2087.0,2087.0]},
]
fs=np.array([sum(r['FS_in_interval'])/2 for r in landmarks],float); x=np.array([sum(r['upc_x_interval_px'])/2 for r in landmarks],float)
A=np.vstack([fs,np.ones_like(fs)]).T
a,b=np.linalg.lstsq(A,x,rcond=None)[0]; pred=a*fs+b;res=x-pred
pairs=[]
for i,j in itertools.combinations(range(3),2):
    aa=(x[j]-x[i])/(fs[j]-fs[i]);bb=x[i]-aa*fs[i]
    k=({0,1,2}-{i,j}).pop(); rr=x[k]-(aa*fs[k]+bb)
    pairs.append({'anchors':[landmarks[i]['name'],landmarks[j]['name']],'held_out':landmarks[k]['name'],'slope_px_per_in':float(aa),'scale_in_per_px':float(1/aa),'held_out_residual_px':float(rr)})
cases=[]
for bow_fs,bow_x,nose_x in itertools.product(landmarks[1]['FS_in_interval'],landmarks[1]['upc_x_interval_px'],landmarks[0]['upc_x_interval_px']):
    fsi=np.array([93.0,bow_fs,landmarks[2]['FS_in_interval'][0]],float); xi=np.array([nose_x,bow_x,2087.0],float)
    AA=np.vstack([fsi,np.ones_like(fsi)]).T;aa,bb=np.linalg.lstsq(AA,xi,rcond=None)[0];rr=xi-(aa*fsi+bb)
    cases.append({'scale_in_per_px':float(1/aa),'FS0_x_px':float(bb),'rms_px':float(math.sqrt(np.mean(rr**2))),'max_abs_px':float(np.max(np.abs(rr)))})
out={'status':'NAVY_UPC_SIDE_THREE_LANDMARK_AFFINE_REGISTRATION_SCREEN','inputs':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (CAL,NOSE)},'landmarks':landmarks,'nominal_fit':{'slope_px_per_FS_in':float(a),'scale_FS_in_per_px':float(1/a),'FS0_x_px':float(b),'rms_px':float(math.sqrt(np.mean(res**2))),'max_abs_px':float(np.max(np.abs(res))),'residuals_px':{landmarks[i]['name']:float(res[i]) for i in range(3)}},'pair_holdout_tests':pairs,'interval_sensitivity':{'case_count':len(cases),'scale_in_per_px_range':[min(c['scale_in_per_px'] for c in cases),max(c['scale_in_per_px'] for c in cases)],'FS0_x_px_range':[min(c['FS0_x_px'] for c in cases),max(c['FS0_x_px'] for c in cases)],'rms_px_range':[min(c['rms_px'] for c in cases),max(c['rms_px'] for c in cases)],'max_abs_px_range':[min(c['max_abs_px'] for c in cases),max(c['max_abs_px'] for c in cases)]},'limits':['Navy Figure4-7 is a low-resolution training schematic; its ruler gives source-traceable FS but landmark pixels are schematic, not manufacturing dimensions.','UPC Figure3.15 is a secondary blueprint source.','Three-landmark agreement can support an engineering registration candidate, not production OML release.'],'side_X_registration_candidate_supported':True,'support_basis':'Drei homologe Seitenansichtslandmarken; nominal RMS <0.2px, paarweise Holdout-Residuen <=1.5px und Linienbreiten-Sensitivitaet bleibt im wenigen-Pixel-Bereich.','master_change_allowed':False,'production_release':False}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('landmarks',[(r['name'],r['FS_in_interval'],r['upc_x_interval_px']) for r in landmarks]);print(json.dumps(out['nominal_fit'],indent=2));print('pairs',pairs);print('sens',out['interval_sensitivity'])
