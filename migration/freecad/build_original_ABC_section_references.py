import FreeCAD as App,Part,json,os,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SOURCE=os.path.join(BASE,'analysis/original_front_sources/front_shared_frame_candidate.json')
EXPECTED='856b5370742863ca6981ed5baf45bdb603754326517af13774cd04151d54ae28'
raw=open(SOURCE,'rb').read()
if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Source reference changed')
data=json.loads(raw);doc=App.newDocument('ORIGINAL_ABC_SECTION_CANDIDATES');records=[]
def polygon_area(loop):
 return abs(sum(a[1]*b[2]-b[1]*a[2] for a,b in zip(loop,loop[1:]+loop[:1])))/2
for row in data['profiles']:
 loops=row['loops_xyz_candidate_mm'];faces=[]
 for loop in loops:
  pts=[App.Vector(*v) for v in loop];wire=Part.makePolygon(pts+[pts[0]]);face=Part.Face(wire)
  if not face.isValid():raise RuntimeError('Invalid source section polygon')
  faces.append(face)
 region=faces[0]
 for hole in faces[1:]:region=region.cut(hole)
 if not region.isValid() or len(region.Faces)!=1 or len(region.Wires)!=len(loops):raise RuntimeError('Native source section topology mismatch')
 expected=polygon_area(loops[0])-sum(polygon_area(v) for v in loops[1:])
 if abs(region.Area-expected)>1e-6:raise RuntimeError('Native area differs from source polygon')
 obj=doc.addObject('PartDesign::Feature','SOURCE_SECTION_'+row['section']);obj.Label='Original '+row['section']+' polygon / candidate frame / NOT RELEASED';obj.Shape=region
 records.append(dict(section=row['section'],X_candidate_mm=row['station_X_candidate_mm'],native_area_mm2=region.Area,source_polygon_area_mm2=expected,face_count=len(region.Faces),boundary_count=len(region.Wires)))
doc.recompute();doc.saveAs(os.path.join(BASE,'migration/freecad/F14_ORIGINAL_ABC_SECTION_CANDIDATES.FCStd'))
with open(os.path.join(BASE,'migration/freecad/freecad_original_ABC_section_audit.json'),'w') as f:json.dump(dict(status='NATIVE_ORIGINAL_ABC_POLYGON_REFERENCE_SECTIONS',source_sha256=EXPECTED,records=records,metric_registration_verified=False,continuous_OML_verified=False,production_geometry=False),f,indent=2)
print(json.dumps(records,indent=2))
