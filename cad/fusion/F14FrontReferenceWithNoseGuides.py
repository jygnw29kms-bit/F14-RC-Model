import adsk.core,adsk.fusion,json,os,hashlib
SOURCE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\front_shared_frame_candidate.json'
EXPECTED='856b5370742863ca6981ed5baf45bdb603754326517af13774cd04151d54ae28'
def run_review(app,builder,mm,outdir):
 raw=open(SOURCE,'rb').read()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Reference data changed')
 data=json.loads(raw);prior=app.activeDocument;doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_FRONT_REFERENCE_WITH_NOSE_GUIDES_NOT_RELEASED'
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
 nose_raw=open(r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\nose_projection_samples.json','rb').read()
 if hashlib.sha256(nose_raw).hexdigest()!='97c6daeebae1d85eedc6d7857c2e95233bc99de8d28e666eba35ee2a45a02250':raise RuntimeError('Nose source data changed')
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
 audit=dict(nose_projection_guides=guide_records,nose_input_sha256='97c6daeebae1d85eedc6d7857c2e95233bc99de8d28e666eba35ee2a45a02250',nose_cross_sections_assumed=False,status='NATIVE_FRONT_REFERENCE_FRAME_CANDIDATE',input_sha256=EXPECTED,records=rows,solid_body_count=root.bRepBodies.count,metric_registration_verified=False,continuous_OML_verified=False,production_geometry=False)
 os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_FRONT_REFERENCE_WITH_NOSE_GUIDES.f3d')))
 with open(os.path.join(outdir,'F14_front_reference_nose_guides_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
