from pathlib import Path
import json, hashlib, statistics

ROOT=Path(__file__).resolve().parents[2]
SENS=ROOT/'analysis'/'original_front_sources'/'UPC_NASA_wing_plan_registration_sensitivity.json'
TICKS=ROOT/'analysis'/'original_front_sources'/'front_station_ticks.json'
OUT=ROOT/'analysis'/'original_front_sources'/'ABC_aircraft_FS_candidate_from_wing_registration.json'
s=json.loads(SENS.read_text(encoding='utf-8'))
t=json.loads(TICKS.read_text(encoding='utf-8'))
# Nur gut konditionierte, physikalisch sinnvolle Fits verwenden: mittlere NASA-WBL-Stationen,
# frei sowie mit unabhängigem Spannweitenmaßstab; zusätzlich lower-mid als Seitensensitivität.
keep={'mid_stations_164_to_348','lower_mid_164_to_348'}
models=[]
for c in s['cases']:
    if c['case'] not in keep: continue
    for mode in ('free_affine','span_scale_constrained'):
        f=c[mode]
        models.append({'case':c['case'],'mode':mode,'slope_px_per_in':f['slope_px_per_in'],'FS0_x_px':f['FS0_x_px'],'rms_px':f['rms_px'],'max_abs_px':f['max_abs_px'],'FS93_x_px':f['FS93_x_px']})

def fs_from_x(x,m): return (x-m['FS0_x_px'])/m['slope_px_per_in']
sections=[]
for st in t['stations']:
    if st['section'] not in ('A','B','C'): continue
    x=float(st['tick_center_x_pixel'])
    vals=[]
    for m in models:
        vals.append({'case':m['case'],'mode':m['mode'],'FS_in':fs_from_x(x,m)})
    fs=[v['FS_in'] for v in vals]
    sections.append({'section':st['section'],'tick_x_px':x,'candidates':vals,'FS_candidate_mean_in':statistics.mean(fs),'FS_candidate_min_in':min(fs),'FS_candidate_max_in':max(fs),'FS_candidate_span_in':max(fs)-min(fs)})
# independent FS93 validation of retained models
fs93=[m['FS93_x_px'] for m in models]
out={
 'status':'ABC_AIRCRAFT_FS_CANDIDATE_FROM_NASA_WING_MULTIPOINT_REGISTRATION_NOT_PRODUCTION_RELEASE',
 'inputs':{
  str(SENS.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(SENS.read_bytes()).hexdigest(),
  str(TICKS.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(TICKS.read_bytes()).hexdigest(),
 },
 'retained_models':models,
 'retention_reason':'Nur mittlere WBL164..348-Fits verwenden: dort sind LE/TE-Rasterkanten beidseitig weitgehend frei von Zeichnungsueberlagerungen und die freie X-Skalierung stimmt praktisch mit der unabhaengigen Spannweitenskalierung ueberein.',
 'independent_validation':{'Navy_FS93_UPC_candidate_band_px':[443.0,450.0],'retained_model_FS93_x_range_px':[min(fs93),max(fs93)],'all_retained_models_inside_FS93_band':all(443<=x<=450 for x in fs93)},
 'sections':sections,
 'limits':[
  'UPC Figure3.15 ist eine sekundaere Blueprint-Quelle, keine Hersteller-Stationszeichnung.',
  'NASA/Grumman Wing-FS/WBL sind primaerquellenbasiert; ihre Mehrpunktpassung liefert einen belastbaren X-Kandidaten, aber keine automatische OML- oder Z-Registrierung.',
  'A/B/C-Ticks werden nur longitudinal zugeordnet; ihre Querschnittsform und Wasserlinie bleiben getrennte Gates.',
  'Vor Master-Freigabe ist mindestens ein weiterer unabhaengiger longitudinaler Landmarkencheck ausser FS93 erforderlich.'
 ],
 'aircraft_X_registration_candidate_supported':True,
 'aircraft_X_registration_production_verified':False,
 'C_absolute_Z_registered':False,
 'master_change_allowed':False,
 'production_release':False
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out['independent_validation'],indent=2))
for r in sections: print(r['section'],round(r['FS_candidate_mean_in'],3),round(r['FS_candidate_min_in'],3),round(r['FS_candidate_max_in'],3),'span',round(r['FS_candidate_span_in'],3))
