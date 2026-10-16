import adsk.core,adsk.fusion,json,os,hashlib,math
ARCHIVE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\independent_reviews\circular_nose_sensitivity_20261016\F14_CIRCULAR_NOSE_SENSITIVITY.f3d'
EXPECTED='2d60633d4620d54d050abbf236ef51b5680e2c5aee95a244542206385968edff'
SAMPLES=[{'X_mm': 15.893897516232698, 'linear_diameter_mm': 10.4105518981092}, {'X_mm': 29.071811311307613, 'linear_diameter_mm': 20.8211037962184}, {'X_mm': 42.24972510638253, 'linear_diameter_mm': 29.584416469943235}, {'X_mm': 55.4276389014575, 'linear_diameter_mm': 36.83226905723445}, {'X_mm': 68.60555269653247, 'linear_diameter_mm': 42.894109402968915}, {'X_mm': 81.78346649160738, 'linear_diameter_mm': 47.96760621407277}]
def run_review(app,builder,mm,outdir):
 if hashlib.sha256(open(ARCHIVE,'rb').read()).hexdigest()!=EXPECTED:raise RuntimeError('Archive changed')
 prior=app.activeDocument;doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(ARCHIVE));design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent
 if root.bRepBodies.count!=1:raise RuntimeError('Expected isolated study body')
 body=root.bRepBodies.item(0);records=[]
 for row in SAMPLES:
  x=row['X_mm'];ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);sk=root.sketches.add(plane);cut=sk.projectCutEdges(body)
  if cut.count==0 or sk.profiles.count!=1:raise RuntimeError('Section extraction failed')
  area=sk.profiles.item(0).areaProperties().area*100;diam=2*math.sqrt(area/math.pi)
  points=[]
  for entity in cut:
   evaluator=entity.worldGeometry.evaluator;ok,start,end=evaluator.getParameterExtents()
   if not ok:raise RuntimeError('Curve parameter query failed')
   ok,vertices=evaluator.getStrokes(start,end,mm(.001))
   if not ok:raise RuntimeError('Curve strokes failed')
   points.extend(vertices)
  if not points:raise RuntimeError('No world section samples')
  ymin,ymax=min(p.y*10 for p in points),max(p.y*10 for p in points);zmin,zmax=min(p.z*10 for p in points),max(p.z*10 for p in points)
  records.append(dict(sampled_width_mm=ymax-ymin,sampled_height_mm=zmax-zmin,Y_range_mm=[ymin,ymax],Z_range_mm=[zmin,zmax],curve_stroke_tolerance_mm=.001,curve_sample_count=len(points),X_mm=x,native_area_mm2=area,area_equivalent_diameter_mm=diam,linear_input_diameter_mm=row['linear_diameter_mm'],diameter_difference_mm=diam-row['linear_diameter_mm']))
 audit=dict(status='NATIVE_INTERMEDIATE_STUDY_SECTION_SAMPLED_EXTENTS',archive_sha256=EXPECTED,records=records,interpretation='Area-equivalent diameter only; this does not prove circularity, source silhouette agreement or lack of local overshoot.',original_OML_verified=False,production_geometry=False)
 os.makedirs(outdir,exist_ok=True)
 with open(os.path.join(outdir,'F14_nose_intermediate_extent_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
