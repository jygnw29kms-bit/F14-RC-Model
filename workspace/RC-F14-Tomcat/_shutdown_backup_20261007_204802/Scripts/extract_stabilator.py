import cv2, numpy as np, os, math
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\general_09.png',0)
# upper stabilator region, avoiding dimensions and lower thin vertical-tail projection
x0,x1=1700,2180; y0,y1=420,900
c=img[y0:y1,x0:x1]
bw=cv2.threshold(c,180,255,cv2.THRESH_BINARY_INV)[1]
# erase dimension line on far right and anything below surface region
bw[:,430:]=0
contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cand=[]
for q in contours:
 x,y,w,h=cv2.boundingRect(q); a=cv2.contourArea(q)
 if w>150 and h>100: cand.append((a,x,y,w,h,q))
for a,x,y,w,h,q in sorted(cand,reverse=True)[:10]:
 print(a,(x,y,w,h))
 if a==sorted(cand,reverse=True)[0][0]:
  eps=.008*cv2.arcLength(q,True)
  ap=cv2.approxPolyDP(q,eps,True).reshape(-1,2)
  print('poly local',ap.tolist())
  # global -> model x/y
  scale=879.283929853852/1768.0
  pts=[]
  for px,py in ap:
   gx=x0+int(px); gy=y0+int(py)
   xm=(gx-408)*scale
   ym=(1028-gy)*scale
   pts.append((round(xm,2),round(ym,2)))
  print('model',pts)
  dbg=cv2.cvtColor(c,cv2.COLOR_GRAY2BGR); cv2.drawContours(dbg,[q],-1,(0,0,255),3)
  for p in ap: cv2.circle(dbg,tuple(p),5,(255,0,0),-1)
  cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\stabilator_contour_debug.png',dbg)
