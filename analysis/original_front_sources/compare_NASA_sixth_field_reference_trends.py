from pathlib import Path
import json,hashlib,math
P=Path(__file__).resolve().parent;R=P.parents[1]
paths=[P/'NASA_CR172559_inboard_first_three_profiles.json',P/'NASA_CR172559_inboard_sweep_grid_comparison.json',R/'analysis/airframe_pivot_wl_regression_v127.json']
a,b,known=[json.loads(p.read_text()) for p in paths]
records=[]
for angle,headers in [(20,[r['header_raw_fields'] for r in a['rows']])]+[(r['nominal_sweep_deg'],[h['raw_header'] for h in r['first_three_headers']]) for r in b['records']]:
 y0,y1=headers[0][1],headers[-1][1];z0,z1=headers[0][5],headers[-1][5];slope=(z1-z0)/(y1-y0)
 records.append({'nominal_sweep_deg':angle,'raw_span_sixth_pairs':[[h[1],h[5]] for h in headers],'endpoint_secant_slope':slope,'secant_angle_deg_if_same_length_units':math.degrees(math.atan(slope)),'middle_field_residual_from_endpoint_secant':headers[1][5]-(z0+slope*(headers[1][1]-y0))})
near=a['nearby_station_break_raw_headers'];print('nearby headers:',near)
# Keep close stations separate; comparison of a mean is numerical hypothesis only.
if isinstance(near,list) and len(near)>=2:
 headers=near[:2]
else:raise AssertionError('Unexpected nearby header schema')
if isinstance(headers[0],dict):raise AssertionError('Inspect schema before mapping')
mean=sum(h[5] for h in headers)/2;ref=known['source_sections'][0]
r={'status':'NUMERIC_REFERENCE_FIELD_HYPOTHESIS_ONLY_NOT_READER_VALIDATION','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'records':records,'near_break':{'separate_raw_headers':headers,'mean_span':sum(h[1] for h in headers)/2,'mean_sixth_field':mean,'CR3992_root_reference_WL':ref['reference_vertical_wl_in'],'difference_mean_sixth_minus_reference_WL':mean-ref['reference_vertical_wl_in']},'interpretation':'Numerical similarity can motivate a section-reference-WL hypothesis; it cannot identify the F14 reader field, coordinate transform or pivot waterline.','limits':['Do not merge127.22 and127.24 into one section','Do not infer pivot WL by extrapolating inboard/outboard trends','Earlier v127 extrapolated pivot value remains historical regression, not source datum','No physical registration or geometry generated'],'production_release':False}
(P/'NASA_sixth_field_reference_trend_hypothesis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(records));print(r['near_break'])
