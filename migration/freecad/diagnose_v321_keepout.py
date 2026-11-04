import FreeCAD as App, Part, pathlib, json, collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
wd=App.openDocument(str(R/'migration/freecad/F14_v321_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
kd=App.openDocument(str(R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'))
rows=[]
for side in ('R','L'):
 m=wd.getObject('V321_TRANSITION_WALL_'+side).Mesh
 keep=kd.getObject('V310_HYBRID_KEEPOUT_'+side).Shape
 bins=collections.Counter(); distbins=collections.Counter(); viol=[]
 for f in m.Facets[::12]:
  p=sum((App.Vector(*q) for q in f.Points),App.Vector())/3.0
  if 754.9<=p.x<=810.6 and keep.isInside(p,0.05,True):
   bins[round(p.x/2)*2]+=1
   if len(viol)<10:viol.append([round(p.x,3),round(p.y,3),round(p.z,3)])
 rows.append({'side':side,'facets':m.CountFacets,'points':m.CountPoints,'solid':m.isSolid(),'nonmanifold':m.hasNonManifolds(),'violations_sampled_facets':sum(bins.values()),'bins':dict(bins),'samples':viol})
print(json.dumps(rows,indent=2),flush=True)
(R/'migration/freecad/freecad_v321_keepout_location_diagnostic.json').write_text(json.dumps({'source':'v321 WIP mesh','method':'every twelfth facet centroid vs v310 keepout, includes internal faces; exploratory only','sides':rows},indent=2))
