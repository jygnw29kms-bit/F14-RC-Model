import adsk.core,adsk.fusion,json,os,hashlib
ARCHIVE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\independent_reviews\joined_inlets_20261015\F14_JOINED_INLET_ADAPTER_CANDIDATES.f3d'
INPUT=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\RC_C_aperture_margin_study.json'
def run_review(app,builder,mm,outdir):
 if hashlib.sha256(open(ARCHIVE,'rb').read()).hexdigest()!='c2f0d24853aeccd6182120752f8500db062d11536d334d44054d0383751a1240':raise RuntimeError('Inlet archive changed')
 raw=open(INPUT,'rb').read()
 if hashlib.sha256(raw).hexdigest()!='1088b5764b25c4c1b01526e8717366224d816f0df318bdc383531b62e3198eef':raise RuntimeError('C aperture changed')
 data=json.loads(raw);prior=app.activeDocument;doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(ARCHIVE));doc.name='F14_C_TO_D_INTERNAL_FLOW_STUDY_NOT_RELEASED';design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent;walls=[b for b in root.bRepBodies];records=[]
 if len(walls)!=2:raise RuntimeError('Expected two existing inlet walls')
 for row in data['records']:
  coords=row['RC_internal_candidate_loop_xyz_mm'];mean_y=sum(v[1] for v in coords)/len(coords);wall=next(b for b in walls if (b.boundingBox.minPoint.y+b.boundingBox.maxPoint.y)*mean_y>0)
  faces=[f for f in wall.faces if adsk.core.Plane.cast(f.geometry) and abs(adsk.core.Plane.cast(f.geometry).normal.x)>.999]
  face=min(faces,key=lambda f:f.pointOnFace.x);xd=face.pointOnFace.x*10;inner=[v for v in face.loops if not v.isOuter]
  if len(inner)!=1:raise RuntimeError('Expected existing D inner flow boundary')
  profiles=[]
  for x in [coords[0][0],xd]:
   ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);sk=root.sketches.add(plane)
   if len(profiles)==0:
    for a,b in zip(coords,coords[1:]+coords[:1]):sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in a])),sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in b])))
   else:
    for edge in inner[0].edges:sk.project(edge)
   if sk.profiles.count!=1:raise RuntimeError('Transition profile missing/ambiguous')
   profiles.append(sk.profiles.item(0))
  li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
  for profile in profiles:li.loftSections.add(profile)
  feature=root.features.loftFeatures.add(li)
  if not feature or feature.bodies.count!=1:raise RuntimeError('Internal flow study loft failed')
  body=feature.bodies.item(0);body.name='C_TO_D_FLOW_VOLUME_STUDY_'+str(row['inner_loop'])+'_NOT_WALL_NOT_PRINTABLE'
  if not body.isSolid or not body.isValid:raise RuntimeError('Invalid study flow volume')
  wall.isVisible=False;records.append(dict(inner_loop=row['inner_loop'],C_X_mm=coords[0][0],D_X_mm=xd,valid=body.isValid,volume_cm3=body.volume,D_profile_from_existing_native_inner_edges=True))
 audit=dict(status='NATIVE_C_TO_D_INTERNAL_FLOW_STUDY',records=records,wall_thickness_verified=False,source_outer_containment_verified=False,metric_registration_verified=False,print_release=False)
 os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_C_TO_D_INTERNAL_FLOW_STUDY.f3d')))
 with open(os.path.join(outdir,'F14_C_to_D_flow_study_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
