import cv2, numpy as np, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_stabilator_crop.png',0)
roi=img[20:210,60:310]
bw=cv2.threshold(roi,180,255,cv2.THRESH_BINARY_INV)[1]
# remove dimension line on far right / neighboring upper structure
bw[:,220:]=0
bw[:25,:]=0
contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
arr=[]
for c in contours:
 x,y,w,h=cv2.boundingRect(c); a=cv2.contourArea(c)
 if a>100: arr.append((a,x,y,w,h,c))
for a,x,y,w,h,c in sorted(arr,reverse=True):
 print('contour',a,(x,y,w,h))
 eps=.012*cv2.arcLength(c,True)
 ap=cv2.approxPolyDP(c,eps,True).reshape(-1,2)
 print(ap.tolist())
 dbg=cv2.cvtColor(roi,cv2.COLOR_GRAY2BGR); cv2.drawContours(dbg,[c],-1,(0,0,255),2)
 for p in ap: cv2.circle(dbg,tuple(p),3,(255,0,0),-1)
 cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_stabilator_contour_debug.png',dbg)
 break
