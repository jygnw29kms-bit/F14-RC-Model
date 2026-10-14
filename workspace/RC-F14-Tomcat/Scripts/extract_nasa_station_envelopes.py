import cv2, json, os, numpy as np, math

base=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references'
plan=cv2.imread(os.path.join(base,'NASA_F14_plan_crop.png'),0)
side=cv2.imread(os.path.join(base,'NASA_F14_side_crop.png'),0)

# Calibration derived from NASA Figure 4 dimensions already used in CAD.
# Plan: aircraft nose/tail approx x=172..1039 px, total airframe length 868.50 mm.
plan_x0, plan_x1 = 172.0, 1039.0
L = 900.0*(261.9/271.4)
# Lateral centerline from digitized plan extremes.
plan_cy=(37.0+880.0)/2.0
plan_sy=900.0/(880.0-37.0)

# Side: aircraft x=196..1179 px, waterline y=329; tail-top calibrates vertical.
side_x0, side_x1 = 196.0,1179.0
side_sx=L/(side_x1-side_x0)
waterline_y=329.0
side_sz=(900.0*(40.9/271.4))/(329.0-207.0)

def nearest_dark_extent(img, x, ymid, ylo, yhi, thresh=175):
    xi=int(round(x))
    ys=np.where(img[int(ylo):int(yhi)+1, xi] < thresh)[0]
    if len(ys)==0: return None
    ys=ys+int(ylo)
    # use closest dark marks above/below mid while avoiding isolated text by taking outer aircraft vicinity
    above=ys[ys<=ymid]
    below=ys[ys>=ymid]
    if len(above)==0 or len(below)==0: return None
    return int(above.min()), int(below.max())

stations=[]
for f in np.linspace(0.02,0.98,31):
    xp=plan_x0+f*(plan_x1-plan_x0)
    xs=side_x0+f*(side_x1-side_x0)

    # plan: get dark-pixel envelope near aircraft centerline, ignore dimension areas by restricting band
    col=plan[:,int(round(xp))]
    ys=np.where(col<175)[0]
    ys=ys[(ys>120)&(ys<885)]
    # robust choose nearest connected aircraft envelope around centerline
    if len(ys):
        # take percentiles to reject isolated annotations
        lo=np.percentile(ys,5)
        hi=np.percentile(ys,95)
        halfw=max(abs(lo-plan_cy),abs(hi-plan_cy))*plan_sy
    else:
        halfw=0

    col2=side[:,int(round(xs))]
    ys2=np.where(col2<175)[0]
    ys2=ys2[(ys2>170)&(ys2<430)]
    if len(ys2):
        top=np.percentile(ys2,5)
        bot=np.percentile(ys2,95)
        ztop=-(top-waterline_y)*side_sz
        zbot=-(bot-waterline_y)*side_sz
    else:
        ztop=zbot=0
    stations.append({
      'f':round(float(f),5),
      'x_mm':round(float(f*L),3),
      'half_width_mm':round(float(halfw),3),
      'z_top_mm':round(float(ztop),3),
      'z_bottom_mm':round(float(zbot),3)
    })

out=os.path.join(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC','analysis','nasa_station_envelopes.json')
with open(out,'w',encoding='utf-8') as fp: json.dump(stations,fp,indent=2)
for s in stations: print(s)
print('wrote',out)
