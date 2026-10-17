import adsk.core,adsk.fusion,json,os,hashlib
SOURCE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\front_shared_frame_candidate.json'
EXPECTED='856b5370742863ca6981ed5baf45bdb603754326517af13774cd04151d54ae28'
def run_review(app,builder,mm,outdir):
 raw=open(SOURCE,'rb').read()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Reference data changed')
 data=json.loads(raw);prior=app.activeDocument;doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_FRONT_REFERENCE_SEMANTIC_GAPS_NOT_RELEASED'
 design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent;rows=[]
 for row in data['profiles']:
  x=row['station_X_candidate_mm'];ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);plane.name='STATION_'+row['section']+'_CANDIDATE'
  sk=root.sketches.add(plane);sk.name='ORIGINAL_'+row['section']+'_ISOTROPIC_REFERENCE_ONLY'
  for loop in row['loops_xyz_candidate_mm']:
   for a,b in zip(loop,loop[1:]+loop[:1]):
    aa=sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in a]));bb=sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in b]));sk.sketchCurves.sketchLines.addByTwoPoints(aa,bb)
  matches=[v for v in sk.profiles if v.profileLoops.count==len(row['loops_xyz_candidate_mm'])]
  if len(matches)!=1:raise RuntimeError('Reference section region missing')
  for loop in row['loops_xyz_candidate_mm']:
   for pt in loop:
    q=sk.sketchToModelSpace(sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in pt])))
    if max(abs(q.asArray()[i]*10-pt[i]) for i in range(3))>1e-6:raise RuntimeError('Coordinate roundtrip failed')
  rows.append(dict(section=row['section'],X_candidate_mm=x,profile_count=sk.profiles.count,region_boundary_count=matches[0].profileLoops.count,area_candidate_mm2=matches[0].areaProperties().area*100,coordinate_roundtrip_verified=True))
 nose_raw=open(r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\nose_to_A_stroke_center_samples.json','rb').read()
 if hashlib.sha256(nose_raw).hexdigest()!='693dda370511f332171f4fd166f5128a972028df3bb061be7ab9c8e67109e061':raise RuntimeError('Nose source data changed')
 nose=json.loads(nose_raw);guide_records=[]
 for name,plane,selector in [('SIDE_TOP',root.xZConstructionPlane,'top'),('SIDE_BOTTOM',root.xZConstructionPlane,'bottom'),('PLAN_RIGHT',root.xYConstructionPlane,'right'),('PLAN_LEFT',root.xYConstructionPlane,'left')]:
  sk=root.sketches.add(plane);sk.name='ORIGINAL_NOSE_'+name+'_PROJECTION_ONLY';points=[]
  for row in nose['samples']:
   x=row['X_candidate_mm']
   if selector in ('top','bottom'):xyz=[x,0,row['side_top_Z_candidate_mm'] if selector=='top' else row['side_bottom_Z_candidate_mm']]
   else:xyz=[x,row['width_candidate_mm']/2*(1 if selector=='right' else -1),0]
   points.append(adsk.core.Point3D.create(*[mm(v) for v in xyz]))
  for a,b in zip(points,points[1:]):sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(a),sk.modelToSketchSpace(b))
  if sk.sketchCurves.sketchLines.count!=len(points)-1:raise RuntimeError('Nose projection segments missing')
  guide_records.append(dict(name=name,point_count=len(points),segment_count=sk.sketchCurves.sketchLines.count))
 ab_raw=open(r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\AB_forebody_projection_samples.json','rb').read()
 if hashlib.sha256(ab_raw).hexdigest()!='acb895f59f215d3af069440d34415322039e8273d64a313c0b54af8a885fa523':raise RuntimeError('AB source changed')
 ab=json.loads(ab_raw);ab_records=[]
 for name,plane,which in [('CANOPY_TOP',root.xZConstructionPlane,'top'),('BODY_BOTTOM_VISIBLE',root.xZConstructionPlane,'bottom'),('PLAN_RIGHT',root.xYConstructionPlane,'right'),('PLAN_LEFT',root.xYConstructionPlane,'left')]:
  sk=root.sketches.add(plane);sk.name='ORIGINAL_AB_'+name+'_PROJECTION_ONLY';points=[]
  for row in ab['samples']:
   if which=='bottom' and row['bottom_Z_candidate_mm'] is None:continue
   x=row['X_candidate_mm']
   if which in ('top','bottom'):xyz=[x,0,row['top_Z_candidate_mm'] if which=='top' else row['bottom_Z_candidate_mm']]
   else:xyz=[x,row['width_candidate_mm']/2*(1 if which=='right' else -1),0]
   points.append(adsk.core.Point3D.create(*[mm(v) for v in xyz]))
  for a,b in zip(points,points[1:]):sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(a),sk.modelToSketchSpace(b))
  if sk.sketchCurves.sketchLines.count!=len(points)-1:raise RuntimeError('AB guide segments missing')
  ab_records.append(dict(name=name,point_count=len(points),segment_count=sk.sketchCurves.sketchLines.count))
 bc_raw=open(r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\BC_projection_samples.json','rb').read()
 if hashlib.sha256(bc_raw).hexdigest()!='d576987b9992bd30e7e698f4949e0bd0d7d507f31204419da18546665f89d374':raise RuntimeError('BC source changed')
 bc=json.loads(bc_raw);bc_records=[]
 for name,plane,which in [('TOP_VISIBLE',root.xZConstructionPlane,'top'),('BOTTOM',root.xZConstructionPlane,'bottom'),('PLAN_RIGHT_OVERALL_GLOVE',root.xYConstructionPlane,'right'),('PLAN_LEFT_OVERALL_GLOVE',root.xYConstructionPlane,'left')]:
  sk=root.sketches.add(plane);sk.name='ORIGINAL_BC_'+name+'_PROJECTION_ONLY';previous=None;previous_region=None;segments=0;gaps=0;semantic_breaks=0
  for row in bc['samples']:
   if which=='top' and row['top_Z_candidate_mm'] is None:previous=None;gaps+=1;continue
   if which in ('left','right') and previous_region is not None and previous_region!=row['plan_region']:previous=None;semantic_breaks+=1
   previous_region=row['plan_region']
   x=row['X_candidate_mm']
   if which in ('top','bottom'):xyz=[x,0,row['top_Z_candidate_mm'] if which=='top' else row['bottom_Z_candidate_mm']]
   else:xyz=[x,row['width_candidate_mm']/2*(1 if which=='right' else -1),0]
   point=sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in xyz]))
   if previous is not None:sk.sketchCurves.sketchLines.addByTwoPoints(previous,point);segments+=1
   previous=point
  if sk.sketchCurves.sketchLines.count!=segments:raise RuntimeError('BC guide count mismatch')
  bc_records.append(dict(name=name,segment_count=segments,omitted_sample_count=gaps,semantic_break_count=semantic_breaks))
 cd_raw=open(r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\CD_projection_samples.json','rb').read()
 if hashlib.sha256(cd_raw).hexdigest()!='1e7ebe6f9eeed069ceddd671f4755e6fc3e7955879a855beaf88adab98e317f3':raise RuntimeError('CD source changed')
 cd=json.loads(cd_raw);cd_records=[]
 for name,plane,which in [('TOP_VISIBLE',root.xZConstructionPlane,'top'),('BOTTOM_PROJECTION',root.xZConstructionPlane,'bottom'),('PLAN_RIGHT_VISIBLE_GLOVE',root.xYConstructionPlane,'right'),('PLAN_LEFT_VISIBLE_GLOVE',root.xYConstructionPlane,'left')]:
  sk=root.sketches.add(plane);sk.name='ORIGINAL_CD_'+name+'_PARTIAL_PROJECTION';previous=None;segments=0;gaps=0
  for row in cd['samples']:
   missing=(which=='top' and row['top_Z_candidate_mm'] is None) or (which in ('left','right') and row['width_candidate_mm'] is None)
   if missing:previous=None;gaps+=1;continue
   x=row['X_candidate_mm']
   if which in ('top','bottom'):xyz=[x,0,row['top_Z_candidate_mm'] if which=='top' else row['bottom_Z_candidate_mm']]
   else:xyz=[x,row['width_candidate_mm']/2*(1 if which=='right' else -1),0]
   point=sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in xyz]))
   if previous is not None:sk.sketchCurves.sketchLines.addByTwoPoints(previous,point);segments+=1
   previous=point
  if sk.sketchCurves.sketchLines.count!=segments:raise RuntimeError('CD guide count mismatch')
  cd_records.append(dict(name=name,segment_count=segments,omitted_sample_count=gaps))
 audit=dict(CD_projection_guides=cd_records,CD_input_sha256='1e7ebe6f9eeed069ceddd671f4755e6fc3e7955879a855beaf88adab98e317f3',BC_projection_guides=bc_records,BC_input_sha256='d576987b9992bd30e7e698f4949e0bd0d7d507f31204419da18546665f89d374',AB_projection_guides=ab_records,AB_input_sha256='acb895f59f215d3af069440d34415322039e8273d64a313c0b54af8a885fa523',nose_projection_guides=guide_records,nose_input_sha256='693dda370511f332171f4fd166f5128a972028df3bb061be7ab9c8e67109e061',nose_cross_sections_assumed=False,status='NATIVE_FRONT_REFERENCE_FRAME_CANDIDATE',input_sha256=EXPECTED,records=rows,solid_body_count=root.bRepBodies.count,metric_registration_verified=False,continuous_OML_verified=False,production_geometry=False)
 os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_FRONT_REFERENCE_SEMANTIC_GAPS.f3d')))
 with open(os.path.join(outdir,'F14_front_semantic_gap_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
