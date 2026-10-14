import cv2, numpy as np, os
base=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references'
img=cv2.imread(os.path.join(base,'NASA_F14_side_crop.png'),0)
m=img.copy()
# remove dimension lines/text around aircraft
m[0:170,0:1430]=255
m[:,1180:1430]=255
m[430:570,0:1430]=255
bw=cv2.threshold(m,180,255,cv2.THRESH_BINARY_INV)[1]
bw=cv2.morphologyEx(bw,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8),iterations=1)
contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sorted(contours,key=cv2.contourArea,reverse=True)
for i,c in enumerate(contours[:10]):
 x,y,w,h=cv2.boundingRect(c); print(i,cv2.contourArea(c),(x,y,w,h))
cand=[c for c in contours if cv2.boundingRect(c)[2]>700 and cv2.boundingRect(c)[3]>100]
c=max(cand,key=cv2.contourArea)
x,y,w,h=cv2.boundingRect(c)
print('chosen',x,y,w,h,cv2.contourArea(c))
eps=0.0025*cv2.arcLength(c,True)
a=cv2.approxPolyDP(c,eps,True).reshape(-1,2)
print('pts',len(a)); print(a.tolist())
out=cv2.cvtColor(m,cv2.COLOR_GRAY2BGR)
cv2.drawContours(out,[c],-1,(0,0,255),2)
for pt in a: cv2.circle(out,tuple(pt),4,(255,0,0),-1)
cv2.imwrite(os.path.join(base,'NASA_F14_side_contour_debug.png'),out)
