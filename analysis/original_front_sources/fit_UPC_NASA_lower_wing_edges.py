from pathlib import Path
import json, hashlib, math, statistics
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_lower_20deg_wing_screen.json'
OUT=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_lower_20deg_wing_fit.json'
j=json.loads(SRC.read_text(encoding='utf-8'))
rows=[]
for r in j['rows']:
    smp=r['sample_rows']
    if not smp: continue
    rows.append({'wbl_in':r['wbl_in'],'LE_fs_in':r['nasa_le_fs_in'],'TE_fs_in':r['nasa_te_fs_in'],'LE_x_px':float(statistics.median(s['x_min_px'] for s in smp)),'TE_x_px':float(statistics.median(s['x_max_px'] for s in smp))})

def fit(edge, filt=lambda r: True):
    rr=[r for r in rows if filt(r)]
    fs=np.array([r[edge+'_fs_in'] for r in rr],float); px=np.array([r[edge+'_x_px'] for r in rr],float)
    A=np.vstack([fs,np.ones_like(fs)]).T
    slope,intercept=np.linalg.lstsq(A,px,rcond=None)[0]
    res=px-(slope*fs+intercept)
    return {'n':len(rr),'FS_span_in':float(fs.max()-fs.min()),'slope_px_per_in':float(slope),'scale_in_per_px':float(1/slope),'FS0_x_px':float(intercept),'FS93_x_px':float(intercept+slope*93),'pivot_FS524_16_x_px':float(intercept+slope*524.16),'rms_px':float(math.sqrt(np.mean(res**2))),'max_abs_px':float(np.max(np.abs(res))),'points':[{'wbl_in':r['wbl_in'],'fs_in':r[edge+'_fs_in'],'x_px':r[edge+'_x_px'],'residual_px':float(r[edge+'_x_px']-(slope*r[edge+'_fs_in']+intercept))} for r in rr]}
fits={
 'LE_127_to_348':fit('LE',lambda r:r['wbl_in']<=347.94),
 'LE_164_to_348':fit('LE',lambda r:164<=r['wbl_in']<=347.94),
 'TE_127_to_348':fit('TE',lambda r:r['wbl_in']<=347.94),
 'TE_164_to_348':fit('TE',lambda r:164<=r['wbl_in']<=347.94),
}
out={'status':'UPC_LOWER_20DEG_WING_EDGE_FITS_SEPARATED_FOR_CONDITIONING','input_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'rows':rows,'fits':fits,'conditioning':{'LE_longitudinal_FS_span_in':fits['LE_164_to_348']['FS_span_in'],'TE_longitudinal_FS_span_in':fits['TE_164_to_348']['FS_span_in'],'TE_to_LE_FS_span_ratio':fits['TE_164_to_348']['FS_span_in']/fits['LE_164_to_348']['FS_span_in']},'limits':['LE and TE are fitted separately because TE has a very small longitudinal FS range and is poorly conditioned for FS93 extrapolation.','Tip station WBL384.69995 is excluded from regression because LE and TE geometrically converge at the physical wingtip.','No absolute registration is released from this file alone.'],'registration_release':False,'master_change_allowed':False,'production_release':False}
OUT.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['conditioning'],indent=2))
for k,v in fits.items(): print(k,'scale',round(v['scale_in_per_px'],6),'FS93',round(v['FS93_x_px'],3),'pivot',round(v['pivot_FS524_16_x_px'],3),'rms',round(v['rms_px'],3),'max',round(v['max_abs_px'],3))
