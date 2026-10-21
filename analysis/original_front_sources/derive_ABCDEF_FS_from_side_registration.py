from pathlib import Path
import json,hashlib,itertools,statistics
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/'analysis'/'original_front_sources'/'Navy_F14_station_ruler_calibration.json'
REG=ROOT/'analysis'/'original_front_sources'/'Navy_UPC_side_longitudinal_landmark_fit.json'
ABC=ROOT/'analysis'/'original_front_sources'/'front_station_ticks.json'
DEF=ROOT/'analysis'/'original_front_sources'/'DEF_station_ticks.json'
FRAME=ROOT/'analysis'/'original_front_sources'/'ABCDEF_shared_frame_candidate.json'
WING=ROOT/'cad'/'fusion'/'F14TomcatRC'/'NASA_F14_basic_wing_v08.json'
OUT=ROOT/'analysis'/'original_front_sources'/'ABCDEF_FS_from_Navy_UPC_side_registration.json'
cal=json.loads(CAL.read_text(encoding='utf-8')); reg=json.loads(REG.read_text(encoding='utf-8')); abc=json.loads(ABC.read_text(encoding='utf-8')); de=json.loads(DEF.read_text(encoding='utf-8')); frame=json.loads(FRAME.read_text(encoding='utf-8')); wing=json.loads(WING.read_text(encoding='utf-8'))
navy_px_per_in=float(cal['fit']['px_per_FS_in']); navy_fs0=float(cal['fit']['FS0_x_px'])
def navy_fs(x): return (x-navy_fs0)/navy_px_per_in
models=[]
for bow_navy_x,bow_upc_x,nose_upc_x in itertools.product([252.0,254.0],[909.0,910.0],[440.75,441.25]):
 fs=np.array([93.0,navy_fs(bow_navy_x),navy_fs(569.0)],float); px=np.array([nose_upc_x,bow_upc_x,2087.0],float)
 A=np.vstack([fs,np.ones_like(fs)]).T; slope,intercept=np.linalg.lstsq(A,px,rcond=None)[0]
 models.append({'slope_px_per_in':float(slope),'FS0_x_px':float(intercept)})
nom=reg['nominal_fit'];nom_model={'slope_px_per_in':float(nom['slope_px_per_FS_in']),'FS0_x_px':float(nom['FS0_x_px'])}
ticks={r['section']:float(r['tick_center_x_pixel']) for r in abc['stations']};ticks.update({r['section']:float(r['tick_center_x_pixel']) for r in de['stations']})
old={p['section']:float(p['station_X_candidate_mm']) for p in frame['profiles'] if p['section'] in ticks}
rc_scale=900.0/(2.0*float(wing['sections'][-1]['wbl_in']))
sections=[]
for sec in 'ABCDEF':
 x=ticks[sec]
 def fs_of(xv,m): return (xv-m['FS0_x_px'])/m['slope_px_per_in']
 fs_nom=fs_of(x,nom_model);vals=[fs_of(x+dx,m) for m in models for dx in (-0.5,0.5)];lo,hi=min(vals),max(vals)
 xn=(fs_nom-93.0)*rc_scale; xnlo=(lo-93.0)*rc_scale; xnhi=(hi-93.0)*rc_scale
 sections.append({'section':sec,'side_tick_x_px':x,'tick_halfwidth_screen_px':0.5,'FS_nominal_in':fs_nom,'FS_sensitivity_range_in':[lo,hi],'FS_sensitivity_span_in':hi-lo,'nose_relative_X_nominal_mm':xn,'nose_relative_X_sensitivity_range_mm':[xnlo,xnhi],'historical_X_candidate_mm':old[sec],'new_minus_historical_mm':xn-old[sec]})
deltas=[r['new_minus_historical_mm'] for r in sections]
out={'status':'ABCDEF_SIDE_VIEW_AIRCRAFT_FS_ENGINEERING_CANDIDATE_NAVY_THREE_LANDMARK_REGISTRATION','inputs':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (CAL,REG,ABC,DEF,FRAME,WING)},'registration_nominal':nom,'registration_model_count_for_sensitivity':len(models),'tick_screen_halfwidth_px':0.5,'rc_scale_mm_per_fullscale_in':rc_scale,'nose_reference_FS_in':93.0,'sections':sections,'historical_delta_summary_mm':{'min':min(deltas),'max':max(deltas),'mean':statistics.mean(deltas),'span':max(deltas)-min(deltas)},'gates':{'side_aircraft_X_engineering_candidate_supported':True,'side_aircraft_X_production_verified':False,'section_Z_registered':False,'master_change_allowed':False,'production_release':False},'limits':['FS ranges include landmark-line interval corners and +/-0.5px tick localization screen only; they are not statistical confidence intervals.','Navy Figure4-7 is a training schematic and UPC Figure3.15 a secondary blueprint; agreement supports engineering registration but not manufacturing metrology.','Only longitudinal station positions are registered; section shapes and Z/Waterline remain separate gates.']}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for r in sections: print(r['section'],'FS',round(r['FS_nominal_in'],3),'range',tuple(round(v,3) for v in r['FS_sensitivity_range_in']),'Xmm',round(r['nose_relative_X_nominal_mm'],3),'deltaOld',round(r['new_minus_historical_mm'],3))
print('old delta summary',out['historical_delta_summary_mm'])
