from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;old=O/'NASA_CR172559_inboard_first_two_profiles.json';a=json.loads(old.read_text());xc=a['common_chord_grid_xc']
u=[.00179,.00824,.01202,.01620,.02198,.02985,.03556,.04009,.04385,.04706,.04982,.05221,.05427,.05605,.05756,.05883,.05986,.06067,.06128,.06168,.06189,.06192,.06177,.06144,.06095,.06030,.05948,.05852,.05741,.05616,.05326,.04987,.04602,.04179,.03954,.03722,.03482,.03236,.02985,.02728,.02467,.02200,.01930,.01656,.01378,.01096,.00811,.00522,.00232,-.00059]
l=[.00179,-.00370,-.00669,-.00984,-.01396,-.01917,-.02269,-.02531,-.02736,-.02899,-.03029,-.03134,-.03217,-.03283,-.03333,-.03369,-.03394,-.03409,-.03415,-.03412,-.03401,-.03384,-.03358,-.03326,-.03287,-.03241,-.03187,-.03127,-.03058,-.02983,-.02810,-.02609,-.02385,-.02142,-.02015,-.01886,-.01755,-.01625,-.01496,-.01369,-.01246,-.01126,-.01012,-.00902,-.00798,-.00696,-.00597,-.00498,-.00399,-.00299]
assert len(u)==len(l)==len(xc)==50 and u[0]==l[0] and all(x>=y for x,y in zip(u,l))
t=[x-y for x,y in zip(u,l)]
row=dict(header_raw_fields=[432.93372,99,628.11401,0,1,160.54604],ordinate_upper=u,ordinate_lower=l,max_dimensionless_thickness=max(t),normalized_piecewise_linear_area=sum((xc[i+1]-xc[i])*(t[i]+t[i+1])/2 for i in range(49)),leading_edge_upper_lower_equal=True,trailing_edge_gap=u[-1]-l[-1],source_pdf_pages=[20,21],page_join_note='Final upper value -0.00059 is first number on sheet2, followed by first lower value +0.00179.')
a['rows'].append(row);a['status']='THREE_COMPLETE_INBOARD_INPUT_PROFILES_VISUALLY_TRANSCRIBED_NO_CAD';a['previous_two_profile_dataset_sha256']=hashlib.sha256(old.read_bytes()).hexdigest();a['source_pdf_pages']=[20,21];a['visual_digit_checks'].append('Sheet2 initial -0.00059 is upper99 endpoint, not lower99 leading ordinate; lower starts +0.00179.')
a['nearby_station_break_raw_headers']=[[502.78067,127.22,629.36968,0,1,159.93040],[502.80906,127.24,629.37056,0,1,159.92996]]
a['limits']=['First three complete input profiles only; remaining stations and25/35degree comparison not recovered here.','Nearby127.22/127.24 headers retained separately; do not average or assume continuous fixed-to-moving-wing join.','Raw field convention and physical registration remain unverified; no native glove or production geometry.']
assert len(a['rows'])==3
(O/'NASA_CR172559_inboard_first_three_profiles.json').write_text(json.dumps(a,indent=2)+'\n');print('3 complete profiles, each50 upper/lower; page join preserved; nearby break not merged')
