import cv2, numpy as np, os
g=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_stabilator_crop.png',0)
# work on stabilator region
x0,y0,x1,y1=65,25,285,190
roi=g[y0:y1,x0:x1]
white=(roi>200).astype(np.uint8)
# connected white components; enclosed components do not touch border
n,lab,stats,cent=cv2.connectedComponentsWithStats(white,8)
mask=np.zeros_like(white)
for i in range(1,n):
 x,y,w,h,a=stats[i]
 touch=(x==0 or y==0 or x+w>=white.shape[1] or y+h>=white.shape[0])
 if (not touch) and a>80:
  mask[lab==i]=255
  print('enclosed',i,a,(x,y,w,h))
# Merge enclosed interior separated by internal structural line, then take hull.
ys,xs=np.where(mask>0)
if len(xs):
 pts=np.column_stack([xs,ys]).astype(np.int32)
 hull=cv2.convexHull(pts)
 # Simplify; convex hull is only used to remove internal lines. Later keep source corners.
 eps=.018*cv2.arcLength(hull,True)
 ap=cv2.approxPolyDP(hull,eps,True).reshape(-1,2)
 print('hull',ap.tolist())
 # convert to NASA plan-crop global pixels then model mm
 # stabilator_crop came from plan_crop [500:800,730:1080]
 sx=(900.0*(261.9/271.4))/(1039.0-172.0)
 sy=900.0/(880.0-37.0)
 model=[]
 for px,py in ap:
  gx=730+x0+int(px); gy=500+y0+int(py)
  xm=(gx-172.0)*sx
  ym=-(gy-458.5)*sy
  model.append((round(xm,2),round(ym,2)))
 print('model',model)
 dbg=cv2.cvtColor(roi,cv2.COLOR_GRAY2BGR)
 cv2.polylines(dbg,[hull],True,(0,0,255),2)
 for p in ap: cv2.circle(dbg,tuple(p),4,(255,0,0),-1)
 cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_stabilator_hull_debug.png',dbg)
