import cv2, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_F14_plan_crop.png')
crop=img[500:800,730:1080]
cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\NASA_stabilator_crop.png',crop)
print(crop.shape)
