import FreeCAD as App, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad')
sources=['F14_v285_CONSOLIDATED_8X6_LIGHT_TAIL.FCStd','F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd','F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd','F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd']
rows={}
for name in sources:
 d=App.openDocument(str(R/name)); parts=[]
 for o in d.Objects:
  if not hasattr(o,'Shape') and not hasattr(o,'Mesh'): continue
  item={'name':o.Name,'type':o.TypeId}
  if hasattr(o,'Shape') and not o.Shape.isNull():
   b=o.Shape.BoundBox;item.update({'kind':'shape','solids':len(o.Shape.Solids),'volume_mm3':round(o.Shape.Volume,2),'bounds_mm':[round(b.XMin,2),round(b.XMax,2),round(b.YMin,2),round(b.YMax,2),round(b.ZMin,2),round(b.ZMax,2)]})
  elif hasattr(o,'Mesh') and o.Mesh.CountFacets:
   b=o.Mesh.BoundBox;item.update({'kind':'mesh','facets':o.Mesh.CountFacets,'bounds_mm':[round(b.XMin,2),round(b.XMax,2),round(b.YMin,2),round(b.YMax,2),round(b.ZMin,2),round(b.ZMax,2)]})
  else: continue
  parts.append(item)
 rows[name]=parts
 dName=d.Name;App.closeDocument(dName)
(R/'v330_assembly_source_inventory.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for name,items in rows.items(): print(name,len(items),[x['name'] for x in items if x.get('kind')=='shape'][:12],flush=True)
