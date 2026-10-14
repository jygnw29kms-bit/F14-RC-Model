import cv2, numpy as np, math
g=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\general_09.png',0)
e=cv2.Canny(g,50,150)
lines=cv2.HoughLinesP(e,1,np.pi/180,threshold=180,minLineLength=500,maxLineGap=20)
arr=[]
if lines is not None:
 for L in lines.reshape(-1,4):
  x1,y1,x2,y2=[int(v) for v in L]
  ln=math.hypot(x2-x1,y2-y1); ang=math.degrees(math.atan2(y2-y1,x2-x1))
  if abs(ang)<4: arr.append((ln,ang,(x1,y1,x2,y2)))
for x in sorted(arr,reverse=True)[:30]: print(x)
