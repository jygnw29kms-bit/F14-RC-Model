from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[2]
O=Path(__file__).parent
rels=[
 'analysis/original_front_sources/Navy_UPC_side_longitudinal_landmark_fit.json',
 'analysis/original_front_sources/ABCDEF_FS_from_Navy_UPC_side_registration.json',
 'analysis/original_front_sources/NADC_WL12_1_vertical_datum_candidate.json',
 'analysis/original_front_sources/C_vertical_datum_source_gate.json',
 'analysis/original_front_sources/UPC_cross_view_longitudinal_transfer_gate.json']
data={p:json.loads((R/p).read_text()) for p in rels}
fs=data[rels[1]]['sections'][2]
wl=data[rels[2]]['WL12_1_candidate_fullscale']
scale=12.0
cfs=fs['FS_nominal_in']; cr=fs['FS_sensitivity_range_in']
out={
 'status':'SIDE_X_ENGINEERING_CANDIDATE_SUPPORTED_C_Z_REMAINS_FAIL_CLOSED',
 'inputs':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in rels},
 'side_X_gate':{
  'supported_for_engineering_study':bool(data[rels[0]]['side_X_registration_candidate_supported']),
  'production_verified':False,
  'C_FS_nominal_in':cfs,
  'C_FS_sensitivity_range_in':cr,
  'C_nose_relative_X_nominal_mm':fs['nose_relative_X_nominal_mm'],
  'basis':'Navy/UPC side-view three-landmark affine registration; no plan-to-side transfer.'},
 'NADC_C_longitudinal_correspondence_study':{
  'C_equivalent_model_station_in_if_1_12_correspondence_assumed':cfs/scale,
  'range_model_in':[cr[0]/scale,cr[1]/scale],
  'NADC_nose_station_model_in':7.7,
  'C_distance_aft_of_NADC_nose_model_in':cfs/scale-7.7,
  'NADC_WL12_1_fullscale_candidate_in':wl['nominal_in'],
  'usable_as_longitudinal_study_location':True,
  'usable_as_C_vertical_translation':False},
 'C_Z_gate':{
  'absolute_Z_registered':False,
  'common_aircraft_waterline_verified':False,
  'reason':'The new side-X registration locates C longitudinally but supplies no homologous vertical landmark tying the detached UPC C-section axis to NADC WL12.1 or another aircraft waterline.',
  'diagnostic_translation_3_5656mm_allowed_as_geometry_correction':False,
  'NADC_WL12_1_direct_transfer_allowed':False,
  'A_B_C_loft_allowed':False,
  'master_change_allowed':False,
  'production_release':False},
 'supersession_note':'The old NADC_UPC longitudinal gate is superseded only for engineering side-X location by the later three-landmark Navy/UPC side registration. Its caution against treating NADC WL12.1 as a C-Z datum remains valid.',
 'next_step':'Find one source-traceable vertical aircraft datum visible in the UPC side view and semantically tied to the detached C section, or an independent primary-source C-section waterline. Until then keep C in local section coordinates.'}
(O/'side_X_C_Z_gate_reconciliation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))