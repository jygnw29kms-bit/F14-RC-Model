"""Studienevaluator: achsenparallele Ellipse ausEndpunkten undTangentenkontrollpunkt.
QUICK-Filletreferenz geprueft; keineallgemeineWBPPW-/Produktionsfreigabe.
"""
import math
import numpy as np
class EllipseReference:
 def __init__(self,start,end,control):
  self.start=tuple(start);self.end=tuple(end);dx,dy=np.subtract(end,start);tx0,ty0=np.subtract(control,start);tx1,ty1=np.subtract(control,end)
  if dx<=0:raise ValueError('X muss zunehmen')
  matrix=np.array([[tx0,ty0,0],[dx,dy,dx*dx],[tx1,ty1,2*dx*tx1]],float);rhs=np.array([0,-dy*dy,-2*dy*ty1]);self.A,self.B,self.C=map(float,np.linalg.solve(matrix,rhs))
  if self.C<=0:raise ValueError('Keine achsenparallele Ellipse')
  self.sign=min([-1,1],key=lambda s:abs((-self.B+s*abs(self.B))/2));self.value(start[0]);v=self.value(end[0])
  if abs(v-end[1])>1e-8:raise ValueError('Endpunkt auf anderem Zweig')
 def value(self,x):
  if not self.start[0]<=x<=self.end[0]:raise ValueError('Keine Extrapolation ausserhalb Quelldomaene')
  u=x-self.start[0];disc=self.B*self.B-4*(self.C*u*u+self.A*u)
  if disc<0:raise ValueError('Kein reeller Zweig')
  return self.start[1]+(-self.B+self.sign*math.sqrt(disc))/2
 def derivatives(self,x):
  v=self.value(x)-self.start[1];u=x-self.start[0];den=self.B+2*v
  if abs(den)<1e-14:raise ValueError('Vertikale Tangente: keine endliche X-Ableitung')
  first=-(self.A+2*self.C*u)/den;second=-(2*self.C+2*first*first)/den
  return first,second
