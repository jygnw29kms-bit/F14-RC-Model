from pathlib import Path
import json, hashlib, statistics

ROOT=Path(__file__).resolve().parents[2]
ABC=ROOT/'analysis'/'original_front_sources'/'ABC_aircraft_FS_candidate_from_wing_registration.json'
FRAME=ROOT/'analysis'/'original_front_sources'/'front_shared_frame_candidate.json'
WING=ROOT/'cad'/'fusion'/'F14TomcatRC'/'NASA_F14_basic_wing_v08.json'
OUT=ROOT/'analysis'/'original_front_sources'/'ABC_FS_vs_historical_frame.json'
a=json.loads(ABC.read_text(encoding='utf-8')); f=json.loads(FRAME.read_text(encoding='utf-8')); w=json.loads(WING.read_text(encoding='utf-8'))
scale=900.0/(2.0*float(w['sections'][-1]['wbl_in']))
old={p['section']:float(p['station_X_candidate_mm']) for p in f['profiles'] if p['section'] in ('A','B','C')}
rows=[]
for s in a['sections']:
    sec=s['section']; fs=float(s['FS_candidate_mean_in'])
    x_abs=fs*scale; x_nose=(fs-93.0)*scale
    lo=(float(s['FS_candidate_min_in'])-93.0)*scale; hi=(float(s['FS_candidate_max_in'])-93.0)*scale
    rows.append({'section':sec,'FS_candidate_mean_in':fs,'model_scale_mm_per_fullscale_in':scale,'X_absolute_FS_scaled_mm':x_abs,'X_nose_relative_FS93_mm':x_nose,'X_nose_relative_range_mm':[lo,hi],'historical_candidate_X_mm':old[sec],'new_minus_historical_mm':x_nose-old[sec]})
deltas=[r['new_minus_historical_mm'] for r in rows]
out={
 'status':'ABC_NEW_FS_REGISTRATION_VS_HISTORICAL_CANDIDATE_FRAME_SCREEN',
 'inputs':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ABC,FRAME,WING)},
 'scale_mm_per_fullscale_in':scale,
 'nose_reference_FS_in':93.0,
 'rows':rows,
 'delta_summary_mm':{'min':min(deltas),'max':max(deltas),'mean':statistics.mean(deltas),'span':max(deltas)-min(deltas)},
 'interpretation':[
  'Neue X-Werte sind aus NASA/Grumman-Wing-Mehrpunktfit plus unabhängigem Navy-FS93-Nasencheck abgeleitet.',
  'Historische ABC-X-Werte stammen aus dem früheren UPC-Kandidatenrahmen mit nicht verifiziertem Maßstab/Ursprung.',
  'Ein nahezu gemeinsamer negativer Versatz bei kleiner Restdrift ist konsistent mit der bereits bekannten Kombination aus Ursprung- und Skalierungsfehler.',
  'Diese Prüfung ändert weder Querschnittsformen noch Z-Lage.'
 ],
 'historical_frame_superseded_for_longitudinal_study':True,
 'master_change_allowed':False,'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for r in rows: print(r['section'],'FS',round(r['FS_candidate_mean_in'],3),'noseX',round(r['X_nose_relative_FS93_mm'],3),'old',round(r['historical_candidate_X_mm'],3),'delta',round(r['new_minus_historical_mm'],3))
print('delta span',round(out['delta_summary_mm']['span'],3),'mean',round(out['delta_summary_mm']['mean'],3))
