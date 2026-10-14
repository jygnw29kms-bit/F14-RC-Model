import cv2, numpy as np, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\general_09.png',0)
bw=cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)[1]
# suppress page borders/title block/dimension labels roughly
m=bw.copy()
m[:70,:]=0; m[-180:,:]=0; m[:,:180]=0; m[:,2500:]=0
n,lab,stats,cent=cv2.connectedComponentsWithStats(m,8)
arr=[]
for i in range(1,n):
 x,y,w,h,area=stats[i]
 if area>100: arr.append((area,x,y,w,h,i))
for a in sorted(arr,reverse=True)[:25]: print(a)
