import adsk.core,adsk.fusion,json,os,hashlib
SOURCE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\circular_nose_sensitivity_input.json'
EXPECTED='d8a8656bfdf5dd5a144f490444143ac0145877e648b5e47e0bfbb00638010fb3'
def run_review(app,builder,mm,outdir):
 raw=open(SOURCE,'rb').read()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Study inputs changed')
 data=json.loads(raw);prior=app.activeDocument;doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_CIRCULAR_NOSE_SENSITIVITY_NOT_ORIGINAL_OML';design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent;profiles=[]
 for row in data['sections']:
  x=row['X_candidate_mm'];ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);sk=root.sketches.add(plane)
  center=sk.modelToSketchSpace(adsk.core.Point3D.create(mm(x),0,mm(row['center_Z_candidate_mm'])));sk.sketchCurves.sketchCircles.addByCenterRadius(center,mm(row['study_diameter_mm']/2))
  if sk.profiles.count!=1:raise RuntimeError('Study profile missing')
  profiles.append(sk.profiles.item(0))
 li=root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
 for profile in profiles:li.loftSections.add(profile)
 feature=root.features.loftFeatures.add(li)
 if not feature or feature.bodies.count!=1:raise RuntimeError('Study loft failed')
 body=feature.bodies.item(0);body.name='SENSITIVITY_ONLY_NOT_ORIGINAL_OML_NOT_PRINTABLE'
 if not body.isValid or not body.isSolid:raise RuntimeError('Study body invalid')
 audit=dict(status='NATIVE_CIRCULAR_NOSE_SENSITIVITY_ONLY',input_sha256=EXPECTED,section_count=len(profiles),body_valid=body.isValid,body_solid=body.isSolid,volume_cm3=body.volume,original_shape_verified=False,production_geometry=False,print_release=False)
 os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_CIRCULAR_NOSE_SENSITIVITY.f3d')))
 with open(os.path.join(outdir,'F14_circular_nose_sensitivity_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
