import FreeCAD as App, pathlib,json,collections
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
rows=[]
for side in ('R','L'):
 m=d.getObject('V326_TRANSITION_WALL_'+side).Mesh
 ints=m.getSelfIntersections()
 pairs=set((min(a,b),max(a,b)) for a,b,*rest in ints)
 classes=collections.Counter()
 examples=[]
 for a,b in sorted(pairs):
  fa=m.Facets[a].Points;fb=m.Facets[b].Points
  shared=sum(any((App.Vector(*p)-App.Vector(*q)).Length<1e-4 for q in fb) for p in fa)
  classes['shared_'+str(shared)]+=1
  if shared==0 and len(examples)<15:examples.append([a,b])
 row={'side':side,'raw_intersections':len(ints),'unique_pairs':len(pairs),'classes':dict(classes),'no_common_vertex_examples':examples}
 rows.append(row)
 print(json.dumps(row),flush=True)
(R/'migration/freecad/freecad_v326_self_intersection_classification.json').write_text(json.dumps({'sides':rows},indent=2))
