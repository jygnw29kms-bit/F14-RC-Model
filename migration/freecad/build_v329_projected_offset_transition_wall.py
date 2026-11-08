import FreeCAD as App, Part, Mesh, pathlib, json, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'; omlsrc=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; out=R/'migration/freecad/F14_v329_PRINTABLE_TRANSITION_WALL_MESH.FCStd'; audp=R/'migration/freecad/freecad_v329_printable_transition_wall_mesh_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); tr=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))['rows']
d=App.openDocument(str(src)); od=App.openDocument(str(omlsrc)); doc=App.newDocument('F14_v329_PRINTABLE_TRANSITION_WALL_MESH'); oml=od.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape
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
def project_outer(inner_ring,outer):
 op=outer.OuterWire.discretize(Number=193);segments=[]
 for a,b in zip(op,op[1:]):
  vy=b.y-a.y;vz=b.z-a.z;ll=vy*vy+vz*vz
  if ll>1e-14:segments.append((a,vy,vz,ll))
 result=[]
 for p in inner_ring:
  best=None
  for a,vy,vz,ll in segments:
   t=max(0.0,min(1.0,((p.y-a.y)*vy+(p.z-a.z)*vz)/ll))
   yy=a.y+t*vy;zz=a.z+t*vz
   ds=(p.y-yy)**2+(p.z-zz)**2
   if best is None or ds<best[0]:best=(ds,App.Vector(p.x,yy,zz))
  result.append(best[1])
 return result

FSA=1347.7432483900213;x0=754.962281164333;x1=810.5;xs=[x0]+[x0+10.0*i for i in range(1,6)]+[810.5];oml_clear=.53;keepout_margin=1.5;wall=.8;slab=.2;N=192;rows=[]
for side in ('R','L'):
 keep=d.getObject('V310_HYBRID_KEEPOUT_'+side).Shape;free=d.getObject('V310_STRUCTURAL_BYPASS_FREEFLOW_'+side).Shape;start=max([f for f in free.Faces if f.BoundBox.XLength<1e-5 and abs(f.CenterOfMass.x-x0)<1e-3],key=lambda f:f.Area);c0=start.CenterOfMass;end_y=(49.821144898732506 if side=='R' else -50.242574947575726);end_z=(-5.665327686040352 if side=='R' else -5.874838829350968);inners=[];outers=[];sr=[]
 for i,x in enumerate(xs):
  target=start.Area+(FSA-start.Area)*(x-x0)/(x1-x0);raw=max(section_face(x).common(clip_face(x,side)).Faces,key=lambda f:f.Area);outer_safe=inward(raw,oml_clear);prism=outer_safe.extrude(App.Vector(slab,0,0));cut=prism.cut(keep);solid=max(cut.Solids,key=lambda s:s.Volume);planar=[f for f in solid.Faces if f.BoundBox.XLength<1e-4 and abs(f.CenterOfMass.x-x)<0.02];safe0=max(planar,key=lambda f:f.Area);safe=inward(safe0,keepout_margin);inner_safe=inward(safe,wall)
  if i==0 and start.common(inner_safe).Area/start.Area>=0.9995:inner=start
  else:
   t=(x-x0)/(x1-x0);cy=c0.y+(end_y-c0.y)*t;cz=c0.z+(end_z-c0.z)*t;inner=fit_intersection(inner_safe,target,cy,cz,x)
  outer=outward_in_safe(inner,wall,safe);inners.append(inner);outers.append(outer);c=inner.CenterOfMass;sr.append({'x_mm':x,'inner_area_mm2':inner.Area,'inner_FSA_ratio':inner.Area/FSA,'wall_gap_mm':inner.OuterWire.distToShape(outer.OuterWire)[0],'outer_safe_fraction':outer.common(safe).Area/outer.Area,'center_y_mm':c.y,'center_z_mm':c.z})
 ori=[];iri=[];prev_i=None
 for outer,inner in zip(outers,inners):
  ri=align(ring(inner.OuterWire,N,side),prev_i);ro=project_outer(ri,outer);prev_i=ri;ori.append(ro);iri.append(ri)
 pts=[];oidx=[];iidx=[]
 for ro,ri in zip(ori,iri):
  a=[];b=[]
  for p in ro:a.append(len(pts));pts.append(p)
  for p in ri:b.append(len(pts));pts.append(p)
  oidx.append(a);iidx.append(b)
 tris=[];outer_tris=[]
 for j in range(len(xs)-1):
  for i in range(N):
   q=(i+1)%N;tt=[(oidx[j][i],oidx[j+1][i],oidx[j+1][q]),(oidx[j][i],oidx[j+1][q],oidx[j][q])];tris+=tt;outer_tris+=tt;tris += [(iidx[j][i],iidx[j+1][q],iidx[j+1][i]),(iidx[j][i],iidx[j][q],iidx[j+1][q])]
 for j in (0,len(xs)-1):
  for i in range(N):
   q=(i+1)%N
   if j==0:tris += [(oidx[j][i],iidx[j][q],iidx[j][i]),(oidx[j][i],oidx[j][q],iidx[j][q])]
   else:tris += [(oidx[j][i],iidx[j][i],iidx[j][q]),(oidx[j][i],iidx[j][q],oidx[j][q])]
 m=Mesh.Mesh([[(pts[k].x,pts[k].y,pts[k].z) for k in t] for t in tris])
 outer_cent=[(pts[a]+pts[b]+pts[c])/3.0 for a,b,c in outer_tris]
 try:m.removeDuplicatedPoints();m.removeDuplicatedFacets();m.harmonizeNormals()
 except:pass
 self_count=-1;keepviol=sum(1 for p in outer_cent if keep.isInside(p,0.05,True));omlviol=sum(1 for p in outer_cent if not oml.isInside(p,0.05,True));o=doc.addObject('Mesh::Feature','V329_TRANSITION_WALL_'+side);o.Mesh=m;o.Label='v329 printable transition wall mesh '+side
 shifts=[math.hypot(sr[i]['center_y_mm']-sr[i-1]['center_y_mm'],sr[i]['center_z_mm']-sr[i-1]['center_z_mm']) for i in range(1,len(sr))];rows.append({'side':side,'stations':sr,'mesh_is_solid':None,'mesh_has_nonmanifolds':None,'self_intersection_count':self_count,'outer_centroid_keepout_violations':keepviol,'outer_centroid_OML_violations':omlviol,'minimum_inner_FSA_ratio':min(q['inner_FSA_ratio'] for q in sr),'minimum_wall_gap_mm':min(q['wall_gap_mm'] for q in sr),'maximum_center_shift_per_station_mm':max(shifts)})
doc.recompute();doc.saveAs(str(out));aud={'status':'V329_PRINTABLE_TRANSITION_WALL_MESH','source_model':src.name,'architecture':{'x_range_mm':[x0,x1],'station_count':len(xs),'ring_points':N,'OML_clearance_mm':oml_clear,'keepout_margin_mm':keepout_margin,'nominal_wall_mm':wall,'target_inner_area_policy':'linear exact v310 outlet to 1.00 FSA'},'sides':rows,'summary':{'minimum_inner_FSA_ratio':min(r['minimum_inner_FSA_ratio'] for r in rows),'minimum_wall_gap_mm':min(r['minimum_wall_gap_mm'] for r in rows),'maximum_center_shift_per_station_mm':max(r['maximum_center_shift_per_station_mm'] for r in rows),'total_self_intersections':sum(r['self_intersection_count'] for r in rows)},'gates':{'bilateral_mesh_solid':False,'bilateral_no_nonmanifolds':False,'zero_self_intersections':False,'zero_sampled_keepout_violations':all(r['outer_centroid_keepout_violations']==0 for r in rows),'zero_sampled_OML_violations':all(r['outer_centroid_OML_violations']==0 for r in rows),'minimum_inner_flow_no_less_than_v310_outlet':min(r['minimum_inner_FSA_ratio'] for r in rows)>=0.928,'terminal_inner_area_reaches_1p00_FSA':all(r['stations'][-1]['inner_FSA_ratio']>=0.999 for r in rows),'minimum_wall_gap_ge_0p75mm':min(r['minimum_wall_gap_mm'] for r in rows)>=0.75,'center_shift_per_station_le_6mm':all(r['maximum_center_shift_per_station_mm']<=6 for r in rows),'slicer_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps({'summary':aud['summary'],'gates':aud['gates']},indent=2))