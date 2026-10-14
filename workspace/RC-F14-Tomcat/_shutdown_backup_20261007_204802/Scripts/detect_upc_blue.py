import cv2, numpy as np, os, json, math
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_pages\\UPC_page_041.png')
# blue contour extraction in BGR
b,g,r=cv2.split(img)
mask=((b>130)&(b>g*1.10)&(b>r*1.25)&(r<210)).astype(np.uint8)*255
n,labels,stats,cent=cv2.connectedComponentsWithStats(mask,8)
comps=[]
for i in range(1,n):
    x,y,w,h,area=stats[i]
    if area>20: comps.append((area,x,y,w,h,i))
print(sorted(comps, reverse=True)[:30])
# save debug
dbg=img.copy()
for area,x,y,w,h,i in sorted(comps,reverse=True)[:12]:
    cv2.rectangle(dbg,(x,y),(x+w,y+h),(0,0,255),2)
cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_pages\\UPC_page_041_blue_debug.png',dbg)
