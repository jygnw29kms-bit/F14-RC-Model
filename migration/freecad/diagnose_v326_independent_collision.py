import FreeCAD as App, Part, pathlib, json, collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
md=App.openDocument(str(R/'migration/freecad/F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
kd=App.openDocument(str(R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'))
od=App.openDocument(str(R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'))
oml=od.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape
result={'method':'facet midpoints (every 6th) and 3 vertices on every 96th facet; exploratory independent v326_candidate check', 'sides':[]}
for side in ('R','L'):
 m=md.getObject('V326_TRANSITION_WALL_'+side).Mesh
 keep=kd.getObject('V310_HYBRID_KEEPOUT_'+side).Shape
 bins=collections.Counter(); points=[]; omlbins=collections.Counter()
 for i,f in enumerate(m.Facets):
  if i%6: continue
  v=[App.Vector(*p) for p in f.Points]
  samples=[sum(v,App.Vector())/3.0]
  if i%96==0:samples+=v
  for p in samples:
   if keep.isInside(p,0.0001,True):
    bins[int(p.x//2)*2]+=1
    if len(points)<20: points.append([round(p.x,3),round(p.y,3),round(p.z,3)])
   if i%48==0 and not oml.isInside(p,0.05,True):omlbins[int(p.x//2)*2]+=1
 row={'side':side,'mesh_solid':m.isSolid(),'nonmanifold':m.hasNonManifolds(),'mesh_facets':m.CountFacets,'keepout_hits_sampled':sum(bins.values()),'keepout_hits_by_x_bin':dict(sorted(bins.items())),'oml_hits_sampled':sum(omlbins.values()),'oml_hits_by_x_bin':dict(sorted(omlbins.items())),'keepout_example_xyz':points}
 result['sides'].append(row)
print(json.dumps(result,indent=2),flush=True)
(R/'migration/freecad/freecad_v326_candidate_independent_wall_collision_screen.json').write_text(json.dumps(result,indent=2))
