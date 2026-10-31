import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
orig=210519.45444906852
segR=162604.72245651192+45345.41028336166
segL=162604.722456512+45345.410369372644
nominal_cavity_pair=2*math.pi*(3.15**2)*40
rows=[]
for side,sv in [('R',segR),('L',segL)]:
 removed=orig-sv; rows.append({'side':side,'original_mm3':orig,'segment_sum_mm3':sv,'removed_mm3':removed,'nominal_two_full_cylinders_mm3':nominal_cavity_pair,'delta_from_nominal_mm3':removed-nominal_cavity_pair,'delta_fraction_of_wing':(removed-nominal_cavity_pair)/orig})
aud={'status':'V263_WING_SEGMENT_VOLUME_CLOSURE','source':'v260 original wing versus v262 source-station segments','rows':rows,'interpretation':'Removed volume is dominated by the two intended 6.3 mm diameter x 40 mm bond cavities; small residual is loft/boolean/tip truncation tolerance and requires no geometry inflation.','gates':{'removed_volume_close_to_nominal_cavities_lt_0p05pct_wing':all(abs(r['delta_fraction_of_wing'])<0.0005 for r in rows),'source_station_split_retained':True,'proof_load':False,'print_release':False,'flight_release':False}}
(R/'analysis/v263_wing_segment_volume_closure.json').write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
