import json
from pathlib import Path
BASE=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad")
st=[(8.793,8.401),(38.507,19.602),(68.220,25.202),(97.934,32.670),(127.648,34.537),(157.362,38.270),(187.075,38.270),(216.789,38.270),(246.503,40.137),(276.216,83.075),(305.930,86.808),(335.644,96.143),(365.358,107.344),(395.071,120.411),(424.785,133.479),(454.499,144.680),(484.213,159.615),(513.926,159.615),(543.640,150.281),(573.354,135.346),(603.067,114.811),(632.781,109.210),(662.495,109.210),(692.209,112.944),(721.922,112.944),(751.636,112.944),(781.350,111.077),(811.064,105.477),(840.777,98.009),(870.491,19.602)]
def hw(x):
    for (x0,y0),(x1,y1) in zip(st,st[1:]):
        if x0<=x<=x1:
            t=(x-x0)/(x1-x0); return y0+(y1-y0)*t
    raise ValueError(x)
inner=148.8263775443693
old=613.1323905812828
new=504.3463093769572
rows=[]
for label,x in [('v194_absolute_FS_mixed',old),('v195_nose_relative',new)]:
    h=hw(x); gap=inner-h
    rows.append({'model':label,'pivot_x_mm':x,'fuselage_half_width_interp_mm':h,'wing_inner_y_mm':inner,'signed_lateral_gap_mm':gap,'interpretation':'positive=gap; negative=wing root lies inside fuselage/glove envelope'})
out={'status':'V195_WING_ROOT_ENVELOPE_SCREEN','source':'source-derived fuselage station half-widths from build_current_full_view.py','rows':rows,'result':'v194 shows ~35.9 mm lateral gap at pivot station; v195 places wing root ~10.8 mm inside fuselage/glove envelope','gates':{'X_frame_mismatch_supported':True,'Y_verified':False,'Z_verified':False,'glove_surface_verified':False,'master_changed':False,'production_release':False}}
(BASE/'freecad_v195_wing_root_envelope_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
