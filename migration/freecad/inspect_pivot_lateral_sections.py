import FreeCAD as App,Part,json,os,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SOURCE=os.path.join(BASE,'migration/freecad/F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd')
OUT=os.path.join(BASE,'migration/freecad/freecad_pivot_lateral_sections_20261018.json')
raw_hash=hashlib.sha256(open(SOURCE,'rb').read()).hexdigest();doc=App.openDocument(SOURCE);fuse=doc.getObject('FUSELAGE_CURRENT').Shape
if fuse.isNull() or not fuse.isValid():raise RuntimeError('Invalid candidate fuselage')
rows=[]
for x in [610.0,625.0,640.0]:
 for z in [4.407593065391325,8.407593065391325,12.407593065391325]:
  line=Part.makeLine(App.Vector(x,-250,z),App.Vector(x,250,z))
  try: cut=fuse.common(line)
  except Exception as exc:raise RuntimeError('Native lateral section failed') from exc
  if not cut.isNull() and not cut.isValid():raise RuntimeError('Invalid lateral section')
  intervals=[]
  for edge in cut.Edges:
   points=[v.Point for v in edge.Vertexes]
   if not points:raise RuntimeError('Section edge has no endpoints')
   intervals.append([min(p.y for p in points),max(p.y for p in points)])
  rows.append(dict(X_mm=x,Z_mm=z,candidate_fuselage_lateral_intervals_mm=sorted(intervals),section_edge_count=len(cut.Edges)))
assert hashlib.sha256(open(SOURCE,'rb').read()).hexdigest()==raw_hash
report=dict(status='NATIVE_CANDIDATE_FUSELAGE_LATERAL_SECTIONS_AT_CRANK_HEIGHT',source_sha256=raw_hash,records=rows,scope='Nine straight-line intersections with provisional candidate fuselage only. Excludes missing glove/wingbox envelope; no original-aircraft dimensional verification.',current_master_modified=False,production_geometry=False)
with open(OUT,'w') as f:json.dump(report,f,indent=2)
print(json.dumps(rows,indent=2))
