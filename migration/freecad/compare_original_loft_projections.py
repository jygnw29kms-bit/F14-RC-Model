import FreeCAD as App,json,os,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
ARCHIVE=os.path.join(BASE,'migration/freecad/F14_ORIGINAL_OUTER_RULED_LOFT_STUDY.FCStd')
if hashlib.sha256(open(ARCHIVE,'rb').read()).hexdigest()!='a1cb207d14ac861484bcd90b3148915f8f826066cc203ee6b51205004f47fdd9':raise RuntimeError('Loft study changed')
frame=json.load(open(os.path.join(BASE,'analysis/original_front_sources/ABCDEF_shared_frame_candidate.json')));profiles=frame['profiles'];doc=App.openDocument(ARCHIVE);records=[]
for region,filename in [('AB','AB_forebody_projection_samples.json'),('BC','BC_projection_samples.json'),('CD','CD_projection_samples.json')]:
 samples=json.load(open(os.path.join(BASE,'analysis/original_front_sources',filename)))['samples']
 for row in samples:
  x=row['X_candidate_mm'];index=next(i for i in range(5) if profiles[i]['station_X_candidate_mm']<x<profiles[i+1]['station_X_candidate_mm']);name=profiles[index]['section']+'_TO_'+profiles[index+1]['section'];shape=doc.getObject(name).Shape;wires=shape.slice(App.Vector(1,0,0),x)
  if len(wires)!=1:raise RuntimeError('Expected one native outer section')
  points=[]
  for edge in wires[0].Edges:points.extend(edge.discretize(Deflection=.001))
  if not points or max(abs(p.x-x) for p in points)>1e-6:raise RuntimeError('Invalid native cut sample coordinates')
  width=max(p.y for p in points)-min(p.y for p in points);top=max(p.z for p in points);bottom=min(p.z for p in points)
  sw=row['width_candidate_mm'];st=row['top_Z_candidate_mm'];sb=row['bottom_Z_candidate_mm']
  records.append(dict(region=region,source_x_pixel=row['source_x_pixel'],X_mm=x,segment=name,native_sampled_width_mm=width,source_width_candidate_mm=sw,width_residual_mm=width-sw if sw is not None else None,native_sampled_top_Z_mm=top,source_top_Z_candidate_mm=st,top_residual_mm=top-st if st is not None else None,native_sampled_bottom_Z_mm=bottom,source_bottom_Z_candidate_mm=sb,bottom_residual_mm=bottom-sb if sb is not None else None,plan_boundary_scope=row.get('plan_region',row.get('plan_status','forebody only'))))
report=dict(status='NATIVE_ORIGINAL_SECTION_LOFT_SOURCE_PROJECTION_COMPARISON',records=records,curve_requested_deflection_mm=.001,acceptance_tolerance_assigned=False,metric_frame_verified=False,continuous_original_OML_verified=False,production_geometry=False)
with open(os.path.join(BASE,'migration/freecad/freecad_original_loft_projection_comparison.json'),'w') as f:json.dump(report,f,indent=2)
print(json.dumps(dict(sample_count=len(records),max_abs_width_residual_mm=max(abs(v['width_residual_mm']) for v in records if v['width_residual_mm'] is not None)),indent=2))
