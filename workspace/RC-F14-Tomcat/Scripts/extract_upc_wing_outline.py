import cv2, numpy as np, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\general_09.png')
g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
crop=g[70:920,1280:1820]
bw=cv2.threshold(crop,180,255,cv2.THRESH_BINARY_INV)[1]
bw=cv2.morphologyEx(bw,cv2.MORPH_CLOSE,np.ones((2,2),np.uint8),iterations=1)
contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sorted(contours,key=cv2.contourArea,reverse=True)
for i,c in enumerate(contours[:20]):
 x,y,w,h=cv2.boundingRect(c); print(i,cv2.contourArea(c),(x,y,w,h))
dbg=cv2.cvtColor(crop,cv2.COLOR_GRAY2BGR)
for i,c in enumerate(contours[:8]):
 cv2.drawContours(dbg,[c],-1,(0,0,255),2)
cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\wing_forward_debug.png',dbg)
