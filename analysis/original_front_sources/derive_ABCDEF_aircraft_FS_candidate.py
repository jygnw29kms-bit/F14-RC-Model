from pathlib import Path
import json, hashlib, statistics

ROOT=Path(__file__).resolve().parents[2]
SENS=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_wing_plan_registration_sensitivity.json'
ABC=ROOT/'analysis'/'original_front_sources'/'front_station_ticks.json'
DEF=ROOT/'analysis'/'original_front_sources'/'DEF_station_ticks.json'
FRAME=ROOT/'analysis'/'original_front_sources'/'ABCDEF_shared_frame_candidate.json'
WING=ROOT/'cad'/'fusion'/'F14TomcatRC'/'NASA_F14_basic_wing_v08.json'
OUT=ROOT/'analysis'/'original_front_sources'/'ABCDEF_aircraft_FS_candidate.json'
s=json.loads(SENS.read_text(encoding='utf-8')); abc=json.loads(ABC.read_text(encoding='utf-8')); de=json.loads(DEF.read_text(encoding='utf-8')); fr=json.loads(FRAME.read_text(encoding='utf-8')); w=json.loads(WING.read_text(encoding='utf-8'))
models=[]
for c in s['cases']:
    if c['case'] not in {'mid_stations_164_to_348','lower_mid_164_to_348'}: continue
    for mode in ('free_affine','span_scale_constrained'):
        f=c[mode]; models.append({'case':c['case'],'mode':mode,'slope_px_per_in':f['slope_px_per_in'],'FS0_x_px':f['FS0_x_px'],'FS93_x_px':f['FS93_x_px'],'rms_px':f['rms_px']})
ticks={r['section']:float(r['tick_center_x_pixel']) for r in abc['stations']}
ticks.update({r['section']:float(r['tick_center_x_pixel']) for r in de['stations']})
old={p['section']:float(p['station_X_candidate_mm']) for p in fr['profiles'] if p['section'] in ticks}
scale=900.0/(2.0*float(w['sections'][-1]['wbl_in']))
rows=[]
for sec in 'ABCDEF':
    x=ticks[sec]
    vals=[(x-m['FS0_x_px'])/m['slope_px_per_in'] for m in models]
    fs_mean=statistics.mean(vals); fs_lo=min(vals); fs_hi=max(vals)
    nx=(fs_mean-93.0)*scale
    rows.append({'section':sec,'tick_x_px':x,'FS_candidate_mean_in':fs_mean,'FS_candidate_range_in':[fs_lo,fs_hi],'FS_candidate_span_in':fs_hi-fs_lo,'nose_relative_X_mm':nx,'nose_relative_X_range_mm':[(fs_lo-93.0)*scale,(fs_hi-93.0)*scale],'historical_X_candidate_mm':old[sec],'new_minus_historical_mm':nx-old[sec]})
deltas=[r['new_minus_historical_mm'] for r in rows]
out={
 'status':'ABCDEF_LONGITUDINAL_REGISTRATION_CANDIDATE_NASA_WING_MULTIPOINT_PLUS_NAVY_FS93',
 'inputs':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SENS,ABC,DEF,FRAME,WING)},
 'retained_model_count':len(models),
 'retained_models':models,
 'independent_FS93_validation':{'candidate_band_px':[443.0,450.0],'retained_model_range_px':[min(m['FS93_x_px'] for m in models),max(m['FS93_x_px'] for m in models)],'all_inside':all(443<=m['FS93_x_px']<=450 for m in models)},
 'scale_mm_per_fullscale_in':scale,'nose_reference_FS_in':93.0,'sections':rows,
 'historical_frame_delta_summary_mm':{'min':min(deltas),'max':max(deltas),'mean':statistics.mean(deltas),'span':max(deltas)-min(deltas)},
 'interpretation':[
  'A-F-Ticks werden direkt im UPC-Originalraster lokalisiert; A-C aus bestehender Tick-Pruefung, D-F aus neuem visuell kontrolliertem Tick-Screen.',
  'X-Registrierung stammt aus NASA/Grumman-Mehrpunktpassung der 20-Grad-Fluegel-LE/TE-Kanten und wird unabhaengig am Navy-FS93-Nasenlandmark geprueft.',
  'Historische UPC-X-Kandidaten bleiben nur Vergleich; sie werden nicht ueberschrieben.',
  'Z-/Waterline-Registrierung und Querschnittssemantik bleiben getrennt offen.'
 ],
 'aircraft_X_registration_candidate_supported':True,
 'aircraft_X_registration_production_verified':False,
 'C_absolute_Z_registered':False,'master_change_allowed':False,'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for r in rows: print(r['section'],'FS',round(r['FS_candidate_mean_in'],3),'X',round(r['nose_relative_X_mm'],3),'old',round(r['historical_X_candidate_mm'],3),'delta',round(r['new_minus_historical_mm'],3),'spanFS',round(r['FS_candidate_span_in'],3))
print('delta summary',out['historical_frame_delta_summary_mm'])
