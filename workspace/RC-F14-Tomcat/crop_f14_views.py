import cv2, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\NASA_F14_Fig4_3view.png')
# plan view crop
plan=img[680:1590,180:1570]
side=img[1590:2160,120:1550]
front=img[230:680,240:1500]
base=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references'
cv2.imwrite(os.path.join(base,'NASA_F14_plan_crop.png'),plan)
cv2.imwrite(os.path.join(base,'NASA_F14_side_crop.png'),side)
cv2.imwrite(os.path.join(base,'NASA_F14_front_crop.png'),front)
print(plan.shape,side.shape,front.shape)
