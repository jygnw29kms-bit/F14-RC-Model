import FreeCAD as App, Part, Mesh, pathlib, json, hashlib, collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; out=R/'migration/freecad/F14_v318_SOURCE_CONFORMAL_NOZZLE_MESH.FCStd'; audp=R/'migration/freecad/freecad_v318_source_conformal_nozzle_mesh_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); trace=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v318_SOURCE_CONFORMAL_NOZZLE_MESH'); oml=d.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape
F=next(x for x in p135['base_profiles'] if x['name']=='F'); fy=[p[0] for p in F['points']]; fz=[p[1] for p in F['points']]; yc=(min(fy)+max(fy))/2; hw=(max(fy)-min(fy))/2; zmin=min(fz); h=max(fz)-zmin
plan=sorted([(x['x_model_mm'],x['expected_half_width_mm']) for x in v134['plan_samples'] if x['x_model_mm']>=F['x_mm']]); tr=trace['rows']
def interp(arr,x,key=None):
 a=[(r['x_model_mm'],r[key]) for r in arr] if key else arr
 for (x0,y0),(x1,y1) in zip(a,a[1:]):
  if x0<=x<=x1:return y0+(y1-y0)*(x-x0)/(x1-x0)
 return a[-1][1]
def section_face(x):
 w=interp(plan,x);zt=interp(tr,x,'z_top_mm');zb=interp(tr,x,'z_bottom_mm');pts=[App.Vector(x,(y-yc)/hw*w,zb+(z-zmin)/h*(zt-zb)) for y,z in F['points']];pts.append(pts[0]);return Part.Face(Part.makePolygon(pts))
def clip_face(x,side,web):
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
   except Exception:pass
 if not cand:raise RuntimeError('no inward offset')
 return max(cand,key=lambda f:f.Area)
def ring_points(wire,n,side):
 pts=wire.discretize(Number=n+1)[:-1]
 area=sum(pts[i].y*pts[(i+1)%n].z-pts[(i+1)%n].y*pts[i].z for i in range(n))
 if area<0:pts=list(reversed(pts))
 k=max(range(n),key=lambda i:(1 if side=='R' else -1)*pts[i].y)
 return pts[k:]+pts[:k]
def add_tri(m,pts,tri,outer_centroids=None):
 a,b,c=[pts[i] for i in tri];m.addFacet(a,b,c)
 if outer_centroids is not None:outer_centroids.append((a+b+c)/3.0)
FSA=1347.7432483900213;web=3.0;outer_clear=1.0;wall=0.8;inner_clear=1.8;stations=[810.5+4*i for i in range(7)];N=96;rows=[];stls=[]
for side in ('R','L'):
 outer_r=[];inner_r=[];side_rows=[]
 for x in stations:
  rf=max(section_face(x).common(clip_face(x,side,web)).Faces,key=lambda f:f.Area); of=inward(rf,outer_clear); inf=inward(rf,inner_clear); op=ring_points(of.OuterWire,N,side);ip=ring_points(inf.OuterWire,N,side)
  outer_r.append(op);inner_r.append(ip);side_rows.append({'x_mm':x,'outer_area_mm2':of.Area,'inner_flow_area_mm2':inf.Area,'inner_area_ratio_to_FSA':inf.Area/FSA,'section_wall_gap_mm':inf.OuterWire.distToShape(of.OuterWire)[0]})
 pts=[];oidx=[];iidx=[]
 for j in range(len(stations)):
  o=[];ii=[]
  for p in outer_r[j]:o.append(len(pts));pts.append(p)
  for p in inner_r[j]:ii.append(len(pts));pts.append(p)
  oidx.append(o);iidx.append(ii)
 tris=[];outer_tris=[]
 for j in range(len(stations)-1):
  for i in range(N):
   q=(i+1)%N;tris += [(oidx[j][i],oidx[j+1][i],oidx[j+1][q]),(oidx[j][i],oidx[j+1][q],oidx[j][q])];outer_tris += tris[-2:]
   tris += [(iidx[j][i],iidx[j+1][q],iidx[j+1][i]),(iidx[j][i],iidx[j][q],iidx[j+1][q])]
 for end,j in [('front',0),('rear',len(stations)-1)]:
  for i in range(N):
   q=(i+1)%N
   if j==0:tris += [(oidx[j][i],iidx[j][q],iidx[j][i]),(oidx[j][i],oidx[j][q],iidx[j][q])]
   else:tris += [(oidx[j][i],iidx[j][i],iidx[j][q]),(oidx[j][i],iidx[j][q],oidx[j][q])]
 edgecount=collections.Counter()
 for a,b,c in tris:
  for u,v in ((a,b),(b,c),(c,a)):edgecount[tuple(sorted((u,v)))]+=1
 m=Mesh.Mesh();cent=[]
 outer_set=set(outer_tris)
 for t in tris:add_tri(m,pts,t,cent if t in outer_set else None)
 try:m.harmonizeNormals()
 except Exception:pass
 obj=doc.addObject('Mesh::Feature','V318_SOURCE_CONFORMAL_WALL_'+side);obj.Mesh=m;obj.Label='v318 source-conformal manifold nozzle mesh '+side
 stl=R/f'manufacturing/candidates/nozzle_mesh_v318_{side}_NOT_RELEASED.stl';Mesh.export([obj],str(stl));stls.append({'side':side,'path':str(stl.relative_to(R)),'sha256':hashlib.sha256(stl.read_bytes()).hexdigest(),'bytes':stl.stat().st_size})
 shell=oml.Shells[0];clearances=[shell.distToShape(Part.Vertex(p))[0] for ring in outer_r for p in ring];inside_centroids=sum(1 for p in cent if oml.isInside(p,0.05,True))
 rows.append({'side':side,'stations':side_rows,'mesh_facets':m.CountFacets,'mesh_points':m.CountPoints,'mesh_is_solid':m.isSolid(),'edge_count_min':min(edgecount.values()),'edge_count_max':max(edgecount.values()),'nonmanifold_edge_count':sum(1 for v in edgecount.values() if v!=2),'minimum_outer_vertex_OML_clearance_mm':min(clearances),'outer_triangle_centroids_inside_fraction':inside_centroids/len(cent)})
doc.recompute();doc.saveAs(str(out));rat=[s['inner_area_ratio_to_FSA'] for r in rows for s in r['stations']];gaps=[s['section_wall_gap_mm'] for r in rows for s in r['stations']]
aud={'status':'V318_SOURCE_CONFORMAL_NOZZLE_MANIFOLD_MESH','source_model':src.name,'architecture':{'station_count':len(stations),'ring_points':N,'center_web_half_width_mm':web,'OML_clearance_mm':outer_clear,'nominal_wall_mm':wall,'inner_total_offset_mm':inner_clear},'sides':rows,'stl_exports':stls,'summary':{'minimum_inner_area_ratio_to_FSA':min(rat),'minimum_section_wall_gap_mm':min(gaps),'minimum_outer_vertex_OML_clearance_mm':min(r['minimum_outer_vertex_OML_clearance_mm'] for r in rows)},'gates':{'bilateral_mesh_is_solid':all(r['mesh_is_solid'] for r in rows),'all_edges_exactly_two_facets':all(r['nonmanifold_edge_count']==0 and r['edge_count_min']==2 and r['edge_count_max']==2 for r in rows),'outer_triangle_centroids_inside_OML_ge_0p999':all(r['outer_triangle_centroids_inside_fraction']>=0.999 for r in rows),'minimum_outer_vertex_OML_clearance_ge_0p3mm':all(r['minimum_outer_vertex_OML_clearance_mm']>=0.3 for r in rows),'minimum_section_wall_gap_ge_0p75mm':min(gaps)>=0.75,'minimum_inner_area_ratio_ge_1p00':min(rat)>=1.0,'slicer_verified':False,'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();audp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))