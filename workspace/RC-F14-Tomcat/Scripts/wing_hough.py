import cv2, numpy as np, math
g=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\wing_forward_debug.png',0)
edges=cv2.Canny(g,50,150,apertureSize=3)
lines=cv2.HoughLinesP(edges,1,np.pi/180,threshold=80,minLineLength=140,maxLineGap=12)
arr=[]
if lines is not None:
 for L in lines.reshape(-1,4):
  x1,y1,x2,y2=[int(v) for v in L]
  ln=math.hypot(x2-x1,y2-y1)
  ang=math.degrees(math.atan2(y2-y1,x2-x1))
  arr.append((ln,ang,(x1,y1,x2,y2)))
for a in sorted(arr,reverse=True)[:30]: print(a)
