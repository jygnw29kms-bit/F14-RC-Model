import FreeCAD as App, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v323_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
rows=[]
for side in ('R','L'):
 m=d.getObject('V323_TRANSITION_WALL_'+side).Mesh
 ints=m.getSelfIntersections()
 row={'side':side,'solid':m.isSolid(),'nonmanifold':m.hasNonManifolds(),'self_intersections':len(ints),'facets':m.CountFacets,'first_intersections':str(ints[:15])}
 rows.append(row)
 print(json.dumps(row),flush=True)
(R/'migration/freecad/freecad_v323_candidate_self_intersections.json').write_text(json.dumps({'sides':rows},indent=2))
