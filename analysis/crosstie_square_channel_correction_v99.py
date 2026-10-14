import math,json,pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
r=3.0; a=3.2
for g in [0.25,0.3,0.5,1.0]:
    t=a/(r+g)
    if t>=1: frac=0
    elif t<=1/math.sqrt(2): frac=1
    else:
        half=math.acos(t)
        frac=8*half/(2*math.pi)
    print(g,frac, math.pi*6*22*frac)
res={'status':'V99_SQUARE_CHANNEL_AREA_CORRECTION','tube_radius_mm':r,'square_channel_half_width_mm':a,'corner_radial_gap_mm':a*math.sqrt(2)-r,'side_radial_gap_mm':a-r,'coverage_sensitivity':[]}
for g in [0.25,0.3,0.5,1.0]:
    t=a/(r+g)
    if t>=1: frac=0.0
    elif t<=1/math.sqrt(2): frac=1.0
    else: frac=8*math.acos(t)/(2*math.pi)
    res['coverage_sensitivity'].append({'max_radial_gap_mm':g,'circumference_fraction':frac,'effective_area_mm2_at_22mm':math.pi*6*22*frac})
res['decision']='Do not credit square channel. Replace with true circular 6.4 mm bore in v99.'
(R/'analysis/crosstie_square_channel_correction_v99.json').write_text(json.dumps(res,indent=2),encoding='utf-8')