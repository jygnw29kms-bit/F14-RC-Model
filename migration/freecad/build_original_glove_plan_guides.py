import FreeCAD as App,Part,json,os,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SOURCE=os.path.join(BASE,'analysis/original_front_sources/glove_projection_guides_v2.json')
EXPECTED='69599bd066dbd08693b906af792c3dd3ac93187b0fe45a67b7cdab7e34a78ca8'
raw=open(SOURCE,'rb').read()
if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Guide inputs changed')
data=json.loads(raw);doc=App.newDocument('ORIGINAL_GLOVE_PLAN_GUIDES');records=[]
for row in data['paths']:
 points=[App.Vector(*v) for v in row['points_xyz_candidate_mm']];wire=Part.makePolygon(points)
 if not wire.isValid() or len(wire.Edges)!=len(points)-1:raise RuntimeError('Invalid guide transfer')
 obj=doc.addObject('PartDesign::Feature',row['name']);obj.Label=row['name']+' / Z0 projection only / NOT SURFACE RAIL';obj.Shape=wire
 records.append(dict(name=row['name'],point_count=len(points),edge_count=len(wire.Edges),length_mm=wire.Length))
doc.recompute();doc.saveAs(os.path.join(BASE,'migration/freecad/F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'))
with open(os.path.join(BASE,'migration/freecad/freecad_original_glove_plan_guides_audit.json'),'w') as f:json.dump(dict(status='NATIVE_ORIGINAL_GLOVE_PLAN_PROJECTION_GUIDES',input_sha256=EXPECTED,records=records,true_surface_elevation_verified=False,loft_rail_attachment_verified=False,production_geometry=False),f,indent=2)
print(json.dumps(records,indent=2))
