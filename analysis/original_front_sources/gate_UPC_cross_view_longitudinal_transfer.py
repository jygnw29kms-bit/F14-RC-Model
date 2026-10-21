from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
REV=ROOT/'analysis'/'independent_reviews'/'crank_localization_20261017'
SRC=ROOT/'analysis'/'original_front_sources'
NOSE=REV/'UPC_probe_radome_transition_screen.json'
LOWER=SRC/'UPC_NASA_lower_20deg_wing_fit.json'
ABC=SRC/'ABC_aircraft_FS_candidate_from_wing_registration.json'
ABCDEF=SRC/'ABCDEF_aircraft_FS_candidate.json'
OUT=SRC/'UPC_cross_view_longitudinal_transfer_gate.json'
n=json.loads(NOSE.read_text(encoding='utf-8')); w=json.loads(LOWER.read_text(encoding='utf-8'))
views={v['view']:v['hinge_sensitivity_interval_px'] for v in n['views']}
le=w['fits']['LE_164_to_348']
out={
 'status':'UPC_PLAN_SIDE_X_TRANSFER_NOT_VERIFIED_FAIL_CLOSED',
 'inputs':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (NOSE,LOWER,ABC,ABCDEF)},
 'view_specific_nose_transition_px':views,
 'plan_minus_side_transition_interval_relation_px':{'plan_min_minus_side_max':views['plan'][0]-views['side'][1],'plan_max_minus_side_min':views['plan'][1]-views['side'][0]},
 'plan_lower_20deg_wing_local_LE_fit':{'scale_in_per_px':le['scale_in_per_px'],'FS93_x_prediction_px':le['FS93_x_px'],'plan_FS93_transition_interval_px':views['plan'],'prediction_vs_plan_interval_px':[le['FS93_x_px']-views['plan'][1],le['FS93_x_px']-views['plan'][0]],'rms_px':le['rms_px']},
 'decision':{
  'plan_and_side_share_verified_x_origin':False,
  'plan_and_side_share_verified_x_scale':False,
  'transfer_plan_wing_fit_to_side_ticks_ABCDEF':False,
  'ABC_aircraft_FS_candidate_from_plan_fit_valid':False,
  'ABCDEF_aircraft_FS_candidate_from_plan_fit_valid':False,
  'plan_wing_local_fit_retained_as_local_shape_screen':True,
  'master_change_allowed':False,
  'production_release':False
 },
 'reason':[
  'Plan- und Seitenansicht zeigen getrennte Nasen-Changepoints; ein gemeinsamer Raster-X-Ursprung ist nicht verifiziert.',
  'Der lokal sehr gute untere 20-Grad-LE-Fit extrapoliert FS93 in der Planansicht deutlich vor den plan-spezifischen FS93-Kandidatenbereich und ist daher keine globale affine Planregistrierung.',
  'A-F-Stationssticks liegen in der Seitenansicht und duerfen ohne Cross-View-Transformation keine Planansichts-FS-Zuordnung erben.',
  'Die zuvor abgeleiteten ABC/ABCDEF-FS-Dateien bleiben zur Fehlernachverfolgung erhalten, sind aber durch dieses Gate fuer Geometrieentscheidungen gesperrt.'
 ],
 'next_step':'Einen absoluten FS-Anker direkt in der UPC-Seitenansicht finden oder mindestens zwei homologe Seitenansichtslandmarken zu einer Primaerquelle registrieren.'
}
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps(out,indent=2,ensure_ascii=False))
