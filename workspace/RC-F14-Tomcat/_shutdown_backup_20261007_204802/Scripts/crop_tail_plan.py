import cv2, os
img=cv2.imread(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\general_09.png')
# crop right/aft region containing upper stabilator + vertical-tail footprint
crop=img[360:980,1650:2500]
cv2.imwrite(r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\\references\\UPC_general\\tail_plan_crop.png',crop)
print(crop.shape)
