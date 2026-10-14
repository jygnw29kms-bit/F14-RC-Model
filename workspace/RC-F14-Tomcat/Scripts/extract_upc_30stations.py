import cv2, numpy as np, os, json, math
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_pages\\UPC_page_041.png')
b,g,r=cv2.split(img)
mask=((b>130)&(b>g*1.10)&(b>r*1.25)&(r<210)).astype(np.uint8)*255
n,labels,stats,cent=cv2.connectedComponentsWithStats(mask,8)
# known largest components from page: top contour, side contour
comps=sorted([(stats[i,cv2.CC_STAT_AREA],i) for i in range(1,n)], reverse=True)
top_label=comps[0][1]
side_label=comps[1][1]
top=(labels==top_label).astype(np.uint8)
side=(labels==side_label).astype(np.uint8)

def bbox(binmask):
    ys,xs=np.where(binmask>0)
    return xs.min(),ys.min(),xs.max(),ys.max()
tx0,ty0,tx1,ty1=bbox(top)
sx0,sy0,sx1,sy1=bbox(side)
print('top bbox',tx0,ty0,tx1,ty1)
print('side bbox',sx0,sy0,sx1,sy1)

# Scale to our model using UPC's own 1:12 nominal dimensions, then to 900 mm span baseline.
# UPC table: L=1591.67, H=406.67, span=1629.17 mm.
scale_to_ours=900.0/1629.17
L=1591.67*scale_to_ours
H=406.67*scale_to_ours

def sample_component(binmask,x0,x1,f):
    x=int(round(x0+f*(x1-x0)))
    # search a few cols around x and collect component pixels
    ys=[]
    for xx in range(max(0,x-2),min(binmask.shape[1],x+3)):
        yy=np.where(binmask[:,xx]>0)[0]
        ys.extend(yy.tolist())
    if not ys: return None
    return min(ys),max(ys)

stations=[]
for i,f in enumerate(np.linspace(0.015,0.985,30)):
    te=sample_component(top,tx0,tx1,float(f))
    se=sample_component(side,sx0,sx1,float(f))
    if te:
        tmin,tmax=te
        cy=(ty0+ty1)/2.0
        # use distance from centerline to larger outer edge
        half=max(abs(tmin-cy),abs(tmax-cy))/((ty1-ty0)/2.0) * (H*0.52)  # provisional lateral scale tied to observed envelope
    else: half=0
    if se:
        smin,smax=se
        # vertical normalize to full UPC height bbox
        ztop=(sy1-smin)/(sy1-sy0)*H
        zbot=(sy1-smax)/(sy1-sy0)*H
        # recenter around local mid; store lower as negative around waterline proxy
        mid=(ztop+zbot)/2
        thick=ztop-zbot
        ztop2=mid
        zbot2=mid-thick
    else:
        ztop2=zbot2=0
    stations.append({
      'index':i+1,'f':round(float(f),6),'x_mm':round(float(f*L),3),
      'half_width_mm':round(float(half),3),
      'z_top_raw_mm':round(float(ztop2),3),
      'z_bottom_raw_mm':round(float(zbot2),3)
    })
out=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\analysis\\upc_fuselage_30stations.json'
with open(out,'w',encoding='utf-8') as fp: json.dump({'L_mm':L,'H_mm':H,'stations':stations},fp,indent=2)
for s in stations: print(s)
print('wrote',out)
