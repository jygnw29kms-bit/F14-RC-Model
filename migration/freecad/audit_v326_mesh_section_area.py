import FreeCAD as App, pathlib, json, math, collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
model=App.openDocument(str(R/'migration/freecad/F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
audit=json.loads((R/'migration/freecad/freecad_v326_printable_transition_wall_mesh_audit.json').read_text())
FSA=1347.7432483900213;N=96;rows=[]
def polygon_area(points):
 return abs(sum(points[i].y*points[(i+1)%len(points)].z-points[(i+1)%len(points)].y*points[i].z for i in range(len(points)))/2)
for side in ('R','L'):
 m=model.getObject('V326_TRANSITION_WALL_'+side).Mesh
 meta=next(q for q in audit['sides'] if q['side']==side)
 grouped=collections.defaultdict(dict)
 for facet in m.Facets:
  for a in facet.Points:
   v=App.Vector(*a); grouped[round(v.x,3)][(round(v.y,4),round(v.z,4))]=v
 sections=[]
 for station in meta['stations']:
  x=station['x_mm'];c=App.Vector(x,station['center_y_mm'],station['center_z_mm'])
  group=grouped.get(round(x,3),{})
  bins=collections.defaultdict(list)
  for v in group.values():
   th=math.atan2(v.z-c.z,v.y-c.y)%(2*math.pi)
   k=int(round(th*N/(2*math.pi)))%N
   bins[k].append((math.hypot(v.y-c.y,v.z-c.z),v))
  ok=len(bins)==N and all(len(bins[k])==2 for k in range(N))
  if not ok:
   sections.append({'x':x,'valid_grouping':False,'bin_count':len(bins),'bin_sizes':dict(collections.Counter(len(q) for q in bins.values()))})
   continue
  inn=[sorted(bins[k],key=lambda q:q[0])[0][1] for k in range(N)]
  out=[sorted(bins[k],key=lambda q:q[0])[1][1] for k in range(N)]
  gaps=[sorted(bins[k],key=lambda q:q[0])[1][0]-sorted(bins[k],key=lambda q:q[0])[0][0] for k in range(N)]
  actual=polygon_area(inn)
  sections.append({'x':round(x,3),'valid_grouping':True,'actual_inner_polygon_FSA':actual/FSA,'actual_inner_area_mm2':actual,'original_BRep_target_area_mm2':station['inner_area_mm2'],'area_loss_pct':100*(1-actual/station['inner_area_mm2']),'minimum_radial_gap_mm':min(gaps),'outer_polygon_area_mm2':polygon_area(out)})
 row={'side':side,'mesh_is_solid':m.isSolid(),'mesh_has_nonmanifolds':m.hasNonManifolds(),'facets':m.CountFacets,'sections':sections,'mesh_min_FSA':min(z['actual_inner_polygon_FSA'] for z in sections if z['valid_grouping']),'mesh_terminal_FSA':sections[-1].get('actual_inner_polygon_FSA'),'max_area_loss_pct':max(z['area_loss_pct'] for z in sections if z['valid_grouping']),'min_radial_gap':min(z['minimum_radial_gap_mm'] for z in sections if z['valid_grouping']),'all_sections_reconstructed':all(z['valid_grouping'] for z in sections)}
 rows.append(row)
 print(json.dumps({k:v for k,v in row.items() if k!='sections'},indent=2),flush=True)
p=R/'migration/freecad/freecad_v326_mesh_section_area_audit.json'
p.write_text(json.dumps({'scope':'independent reconstruction of 96-point polar rings from saved mesh facets; radial gap is not minimum Euclidean wall thickness','sides':rows},indent=2))
