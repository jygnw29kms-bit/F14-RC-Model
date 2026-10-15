"""Visual-only UPC stabilator contour diagnostic. NASA/full-scale geometry remains authoritative."""
import cv2, numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'references/UPC_general/general_09.png'
OUT=ROOT/'references/UPC_general/stabilator_contour_debug.png'
img=cv2.imread(str(SRC),0)
if img is None: raise RuntimeError(f"missing source {SRC}")
x0,x1=1700,2180; y0,y1=420,900
c=img[y0:y1,x0:x1]
bw=cv2.threshold(c,180,255,cv2.THRESH_BINARY_INV)[1]; bw[:,430:]=0
contours,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cand=[]
for q in contours:
    x,y,w,h=cv2.boundingRect(q); a=cv2.contourArea(q)
    if w>150 and h>100: cand.append((a,x,y,w,h,q))
if not cand: raise RuntimeError("no candidate contour")
a,x,y,w,h,q=sorted(cand,reverse=True)[0]
eps=.008*cv2.arcLength(q,True); ap=cv2.approxPolyDP(q,eps,True).reshape(-1,2)
print("VISUAL_DIAGNOSTIC_ONLY",{"area_px2":a,"bbox":(x,y,w,h),"poly_local":ap.tolist()})
dbg=cv2.cvtColor(c,cv2.COLOR_GRAY2BGR); cv2.drawContours(dbg,[q],-1,(0,0,255),3)
for p in ap: cv2.circle(dbg,tuple(p),5,(255,0,0),-1)
cv2.imwrite(str(OUT),dbg)
print("wrote",OUT)
