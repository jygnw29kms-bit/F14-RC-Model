import FreeCAD as App, Part, Mesh, pathlib, json, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'; omlsrc=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; out=R/'migration/freecad/F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd'; audp=R/'migration/freecad/freecad_v326_printable_transition_wall_mesh_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); tr=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))['rows']
d=App.openDocument(str(src)); od=App.openDocument(str(omlsrc)); doc=App.newDocument('F14_v326_PRINTABLE_TRANSITION_WALL_MESH'); oml=od.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape
F=next(x for x in p135['base_profiles'] if x['name']=='F'); fy=[p[0] for p in F['points']];fz=[p[1] for p in F['points']];yc=(min(fy)+max(fy))/2;hw=(max(fy)-min(fy))/2;zmin=min(fz);h=max(fz)-zmin
plan=sorted([(x['x_model_mm'],x['expected_half_width_mm']) for x in v134['plan_samples'] if x['x_model_mm']>=F['x_mm']])
def interp(arr,x,key=None):
 a=[(r['x_model_mm'],r[key]) for r in arr] if key else arr
 for (x0,y0),(x1,y1) in zip(a,a[1:]):
  if x0<=x<=x1:return y0+(y1-y0)*(x-x0)/(x1-x0)
 return a[-1][1]
def section_face(x):
 w=interp(plan,x);zt=interp(tr,x,'z_top_mm');zb=interp(tr,x,'z_bottom_mm');pts=[App.Vector(x,(y-yc)/hw*w,zb+(z-zmin)/h*(zt-zb)) for y,z in F['points']];pts.append(pts[0]);return Part.Face(Part.makePolygon(pts))
def clip_face(x,side,web=3.0):
 y0=web if side=='R' else -200;y1=200 if side=='R' else -web;pts=[App.Vector(x,y0,-100),App.Vector(x,y1,-100),App.Vector(x,y1,100),App.Vector(x,y0,100),App.Vector(x,y0,-100)];return Part.Face(Part.makePolygon(pts))
def offset_candidates(face,dist,want_larger):
 cand=[]
 for join in (2,0,1):
  for s in (-dist,dist):
   try:
    sh=face.OuterWire.makeOffset2D(s,join=join,fill=False);ws=list(sh.Wires) if sh.ShapeType!='Wire' else [sh]
    for w in ws:
     f=Part.Face(w)
     if (f.Area>face.Area)==want_larger:cand.append(f)
   except:pass
 return cand
def inward(face,dist):
 cand=[]
 for f in offset_candidates(face,dist,False):
  frac=f.common(face).Area/f.Area if f.Area else 0
  if frac>0.999:cand.append(f)
 if not cand:raise RuntimeError('no inward offset')
 return max(cand,key=lambda f:f.Area)
def outward_in_safe(face,dist,safe):
 cand=[]
 for f in offset_candidates(face,dist,True):
  frac=f.common(safe).Area/f.Area if f.Area else 0
  if frac>=0.9995:cand.append((abs(f.OuterWire.distToShape(face.OuterWire)[0]-dist),f,frac))
 if not cand:raise RuntimeError('no safe outward offset')
 return min(cand,key=lambda q:q[0])[1]
def fit_intersection(face,target,cy,cz,x):
 axis=App.Vector(1,0,0);lo,hi=1.0,60.0;best=None
 for _ in range(20):
  r=(lo+hi)/2;disk=Part.Face(Part.Wire([Part.makeCircle(r,App.Vector(x,cy,cz),axis)]));fs=list(face.common(disk).Faces)
  if not fs:lo=r;continue
  f=max(fs,key=lambda q:q.Area)
  if f.Area>=target:best=f;hi=r
  else:lo=r
 if best is None:raise RuntimeError('target unreachable')
 return best
def ring(w,n,side):
 pts=w.discretize(Number=n+1)[:-1];area=sum(pts[i].y*pts[(i+1)%n].z-pts[(i+1)%n].y*pts[i].z for i in range(n))
 if area<0:pts=list(reversed(pts))
 k=max(range(n),key=lambda i:(1 if side=='R' else -1)*pts[i].y);return pts[k:]+pts[:k]
def align(rr,prev):
 if prev is None:return rr
 best=None;n=len(rr)
 for k in range(n):
  c=rr[k:]+rr[:k];score=sum((c[i]-prev[i]).Length**2 for i in range(n))
  if best is None or score<best[0]:best=(score,c)
 return best[1]
def radial_sample(face,c,n):
 poly=face.OuterWire.discretize(Number=501); seg=list(zip(poly,poly[1:]+poly[:1])); result=[]
 for k in range(n):
  angle=2.0*math.pi*k/n;dy=math.cos(angle);dz=math.sin(angle);ts=[]
  for a,b in seg:
   ey=b.y-a.y;ez=b.z-a.z;det=dy*ez-dz*ey
   if abs(det)<1e-10:continue
   py=a.y-c.y;pz=a.z-c.z
   t=(py*ez-pz*ey)/det;u=(py*dz-pz*dy)/det
   if t>1e-8 and -1e-8<=u<=1+1e-8:ts.append(t)
  if not ts:raise RuntimeError('radial sampling failed at angle '+str(k))
  t=min(ts);result.append(App.Vector(c.x,c.y+t*dy,c.z+t*dz))
 return result
 
FSA=1347.7432483900213
for side in ('R','L'):
 free=d.getObject('V310_STRUCTURAL_BYPASS_FREEFLOW_'+side).Shape
 start=max([f for f in free.Faces if f.BoundBox.XLength<1e-5 and abs(f.CenterOfMass.x-754.962281164333)<1e-3],key=lambda f:f.Area)
 print('side',side,'start BRep',start.Area,'centroid_inside',start.isInside(start.CenterOfMass,1e-5,True),flush=True)
 for n in (96,192,384,768):
  ring=radial_sample(start,start.CenterOfMass,n)
  area=abs(sum(ring[i].y*ring[(i+1)%n].z-ring[(i+1)%n].y*ring[i].z for i in range(n)))/2
  print(side,n,round(area/start.Area,7),round(area/FSA,7),flush=True)
