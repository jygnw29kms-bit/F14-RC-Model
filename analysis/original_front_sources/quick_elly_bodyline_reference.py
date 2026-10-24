"""Getrennte EL LY-Bodyline-Studie nach historischem CURVES-Zweig400.
Kein ELLI-Querschnittsevaluator; keine Produktionsfreigabe.
"""
import math
import numpy as np
class QuickEllyBodylineReference:
 def __init__(self,start,end,control):
  self.start=tuple(start);self.end=tuple(end)
  dx,dy=np.subtract(end,start);tx0,ty0=np.subtract(control,start);tx1,ty1=np.subtract(control,end)
  if dx<=0:raise ValueError('X muss zunehmen')
  matrix=[[tx0,ty0,0],[dx,dy,dy*dy],[tx1,ty1,2*dy*ty1]]
  self.A,self.B,self.C=map(float,np.linalg.solve(matrix,[0,-dx*dx,-2*dx*tx1]))
  if abs(self.C)<1e-5:raise ValueError('Historischer Parabelfallback hier nicht implementiert')
  self.sign=math.copysign(1,self.B) if self.B!=0 else math.copysign(1,dy)
  if max(abs(self.value(start[0])-start[1]),abs(self.value(end[0])-end[1]))>1e-8:raise ValueError('Endpunktzweig passt nicht')
 def value(self,x):
  if not self.start[0]<=x<=self.end[0]:raise ValueError('Keine Extrapolation')
  u=x-self.start[0];disc=self.B*self.B-4*self.C*u*(u+self.A)
  if disc<0:raise ValueError('Kein reeller Zweig')
  return self.start[1]+(self.sign*math.sqrt(disc)-self.B)/(2*self.C)
 def derivatives(self,x):
  u=x-self.start[0];v=self.value(x)-self.start[1];den=2*self.C*v+self.B
  if abs(den)<1e-14:raise ValueError('Singulaere Ableitung, kein historisches Clamping uebernommen')
  first=-(2*u+self.A)/den
  return first,-2*(1+self.C*first*first)/den
