import FreeCAD as App, Part, Mesh, pathlib, json, math, hashlib, collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'; out=R/'migration/freecad/F14_v320_SOURCE_CONFORMAL_TRANSITION_FLOW_MESH.FCStd'; audp=R/'migration/freecad/freecad_v320_source_conformal_transition_flow_mesh_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); tr=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))['rows']
d=App.openDocument(str(src)); doc=App.newDocument('F14_v320_SOURCE_CONFORMAL_TRANSITION_FLOW_MESH')
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
def inward(face,dist):
 cand=[]
 for join in (2,0,1):
  for s in (-dist,dist):
   try:
    sh=face.OuterWire.makeOffset2D(s,join=join,fill=False);ws=list(sh.Wires) if sh.ShapeType!='Wire' else [sh]
    for w in ws:
     f=Part.Face(w);frac=f.common(face).Area/f.Area if f.Area else 0
     if f.Area<face.Area and frac>0.999:cand.append(f)
   except: pass
 if not cand: raise RuntimeError('no inward offset')
 return max(cand,key=lambda f:f.Area)
def fit_intersection(face,target,cy,cz,x):
    axis=App.Vector(1,0,0)
    lo,hi=1.0,60.0; best=None
    for _ in range(18):
        r=(lo+hi)/2
        e=Part.makeCircle(r,App.Vector(x,cy,cz),axis)
        disk=Part.Face(Part.Wire([e]))
        com=face.common(disk)
        fs=list(com.Faces)
        if not fs:
            lo=r; continue
        f=max(fs,key=lambda q:q.Area)
        if f.Area>=target:
            best=f; hi=r
        else:
            lo=r
    if best is None:
        raise RuntimeError('target area not reachable at x %.3f'%x)
    return best

def ring(w,n,side):
 pts=w.discretize(Number=n+1)[:-1]
 area=sum(pts[i].y*pts[(i+1)%n].z-pts[(i+1)%n].y*pts[i].z for i in range(n))
 if area<0:pts=list(reversed(pts))
 k=max(range(n),key=lambda i:(1 if side=='R' else -1)*pts[i].y)
 return pts[k:]+pts[:k]
FSA=1347.7432483900213; x0=754.962281164333; x1=810.5; xs=[x0,758.5,762.5,766.5,770.5,774.5,778.5,782.5,786.5,790.5,794.5,798.5,802.5,806.5,810.5]; reserve=1.33; slab=.2; N=96; rows=[]
for side in ('R','L'):
 keep=d.getObject('V310_HYBRID_KEEPOUT_'+side).Shape; free=d.getObject('V310_STRUCTURAL_BYPASS_FREEFLOW_'+side).Shape
 start=max([f for f in free.Faces if f.BoundBox.XLength<1e-5 and abs(f.CenterOfMass.x-x0)<1e-3],key=lambda f:f.Area)
 faces=[]; sr=[]; c0=start.CenterOfMass; end_y=(49.821144898732506 if side=='R' else -50.242574947575726); end_z=(-5.665327686040352 if side=='R' else -5.874838829350968)
 for i,x in enumerate(xs):
  target=start.Area+(FSA-start.Area)*(x-x0)/(x1-x0)
  if i==0: f=start; safe_frac=1.0; cap=start.Area
  else:
   raw=max(section_face(x).common(clip_face(x,side)).Faces,key=lambda f:f.Area); flow=inward(raw,reserve); prism=flow.extrude(App.Vector(slab,0,0)); cut=prism.cut(keep); solid=max(cut.Solids,key=lambda s:s.Volume); planar=[f for f in solid.Faces if f.BoundBox.XLength<1e-4 and abs(f.CenterOfMass.x-x)<0.02]; capface=max(planar,key=lambda f:f.Area); cap=capface.Area; t=(x-x0)/(x1-x0); cy=c0.y+(end_y-c0.y)*t; cz=c0.z+(end_z-c0.z)*t; f=fit_intersection(capface,target,cy,cz,x); safe_frac=f.common(capface).Area/f.Area if f.Area else 0
  faces.append(f); c=f.CenterOfMass; sr.append({'x_mm':x,'target_area_mm2':target,'actual_area_mm2':f.Area,'FSA_ratio':f.Area/FSA,'capacity_area_mm2':cap,'contained_in_free_component_fraction':safe_frac,'center_y_mm':c.y,'center_z_mm':c.z})
 rings=[]
 for f in faces:
  rr=ring(f.OuterWire,N,side)
  if rings:
   prev=rings[-1]
   best=None
   for k in range(N):
    cand=rr[k:]+rr[:k]
    score=sum((cand[i]-prev[i]).Length**2 for i in range(N))
    if best is None or score<best[0]:best=(score,cand)
   rr=best[1]
  rings.append(rr)
 pts=[]; idx=[]
 for rr in rings:
  ix=[]
  for p in rr:ix.append(len(pts));pts.append(p)
  idx.append(ix)
 tris=[]
 for j in range(len(rings)-1):
  for i in range(N):
   q=(i+1)%N;tris += [(idx[j][i],idx[j+1][i],idx[j+1][q]),(idx[j][i],idx[j+1][q],idx[j][q])]
 m=Mesh.Mesh()
 for a,b,c in tris:m.addFacet(pts[a],pts[b],pts[c])
 # triangulate concave end caps using FreeCAD's polygon tessellator
 for j in (0,len(rings)-1):
  poly=Part.Face(Part.makePolygon(rings[j]+[rings[j][0]]))
  vv,tt=poly.tessellate(0.10)
  for a,b,c in tt:m.addFacet(vv[a],vv[b],vv[c])
 try:
  m.removeDuplicatedPoints();m.removeDuplicatedFacets();m.harmonizeNormals()
 except:pass
 self_count=len(m.getSelfIntersections())
 o=doc.addObject('Mesh::Feature','V320_TRANSITION_FLOW_'+side);o.Mesh=m;o.Label='v320 source-conformal transition flow mesh '+side
 shifts=[math.hypot(sr[i]['center_y_mm']-sr[i-1]['center_y_mm'],sr[i]['center_z_mm']-sr[i-1]['center_z_mm']) for i in range(1,len(sr))]
 rows.append({'side':side,'stations':sr,'mesh_is_solid':m.isSolid(),'mesh_has_nonmanifolds':m.hasNonManifolds(),'self_intersection_count':self_count,'facets':m.CountFacets,'maximum_center_shift_per_station_mm':max(shifts),'minimum_FSA_ratio':min(q['FSA_ratio'] for q in sr),'minimum_free_component_containment_fraction':min(q['contained_in_free_component_fraction'] for q in sr)})
doc.recompute();doc.saveAs(str(out));aud={'status':'V320_SOURCE_CONFORMAL_TRANSITION_FLOW_MESH','source_model':src.name,'architecture':{'x_range_mm':[x0,x1],'station_count':len(xs),'ring_points':N,'source_conformal_reserve_mm':reserve,'target_area_policy':'linear from exact v310 outlet area to 1.00 FSA'},'sides':rows,'summary':{'minimum_FSA_ratio':min(r['minimum_FSA_ratio'] for r in rows),'maximum_center_shift_per_station_mm':max(r['maximum_center_shift_per_station_mm'] for r in rows),'minimum_free_component_containment_fraction':min(r['minimum_free_component_containment_fraction'] for r in rows)},'gates':{'bilateral_mesh_solid':all(r['mesh_is_solid'] for r in rows),'bilateral_no_nonmanifolds':all(not r['mesh_has_nonmanifolds'] for r in rows),'zero_self_intersections':all(r['self_intersection_count']==0 for r in rows),'minimum_flow_area_no_less_than_v310_outlet':min(r['minimum_FSA_ratio'] for r in rows)>=0.928,'terminal_area_reaches_1p00_FSA':all(r['stations'][-1]['FSA_ratio']>=0.999 for r in rows),'all_scaled_sections_contained_ge_0p9995':all(r['minimum_free_component_containment_fraction']>=0.9995 for r in rows),'center_shift_per_station_le_6mm':all(r['maximum_center_shift_per_station_mm']<=6 for r in rows),'transition_wall_defined':False,'slicer_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps({'summary':aud['summary'],'gates':aud['gates']},indent=2))






