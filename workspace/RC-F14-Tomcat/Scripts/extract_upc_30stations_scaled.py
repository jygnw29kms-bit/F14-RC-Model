import cv2, numpy as np, os, json, math
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_pages\\UPC_page_041.png')
b,g,r=cv2.split(img)
mask=((b>130)&(b>g*1.10)&(b>r*1.25)&(r<210)).astype(np.uint8)*255
n,labels,stats,cent=cv2.connectedComponentsWithStats(mask,8)
comps=sorted([(stats[i,cv2.CC_STAT_AREA],i) for i in range(1,n)], reverse=True)
top=(labels==comps[0][1]).astype(np.uint8)
side=(labels==comps[1][1]).astype(np.uint8)

def bbox(m):
 ys,xs=np.where(m>0); return xs.min(),ys.min(),xs.max(),ys.max()
tx0,ty0,tx1,ty1=bbox(top); sx0,sy0,sx1,sy1=bbox(side)
L=900.0*(1591.67/1629.17)  # UPC scale ratio applied to our 900 mm span
top_mm_per_px=L/(tx1-tx0)
side_mm_per_px=L/(sx1-sx0)
top_cy=(ty0+ty1)/2.0

# nose vertical datum from first few side-contour columns
nose_ys=[]
for x in range(sx0,min(sx0+10,sx1+1)):
 nose_ys += np.where(side[:,x]>0)[0].tolist()
side_datum=float(np.mean(nose_ys)) if nose_ys else (sy0+sy1)/2.0

def sample(m,x0,x1,f):
 x=int(round(x0+f*(x1-x0))); ys=[]
 for xx in range(max(0,x-2),min(m.shape[1],x+3)):
  ys += np.where(m[:,xx]>0)[0].tolist()
 if not ys:return None
 return min(ys),max(ys)

stations=[]
for i,f in enumerate(np.linspace(0.01,0.99,30)):
 te=sample(top,tx0,tx1,float(f)); se=sample(side,sx0,sx1,float(f))
 if te:
  tmin,tmax=te
  half=max(abs(tmin-top_cy),abs(tmax-top_cy))*top_mm_per_px
 else: half=0.5
 if se:
  smin,smax=se
  ztop=(side_datum-smin)*side_mm_per_px
  zbot=(side_datum-smax)*side_mm_per_px
 else: ztop=zbot=0
 stations.append({'index':i+1,'f':round(float(f),6),'x_mm':round(float(f*L),3),
                  'half_width_mm':round(float(half),3),'z_top_mm':round(float(ztop),3),'z_bottom_mm':round(float(zbot),3)})
out=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\analysis\\upc_fuselage_30stations_scaled.json'
with open(out,'w',encoding='utf-8') as fp: json.dump({'L_mm':L,'top_mm_per_px':top_mm_per_px,'side_mm_per_px':side_mm_per_px,'side_datum_px':side_datum,'stations':stations},fp,indent=2)
print('L',L,'top_scale',top_mm_per_px,'side_scale',side_mm_per_px,'datum',side_datum)
for s in stations: print(s)
