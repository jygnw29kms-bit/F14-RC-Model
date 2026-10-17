import adsk.core,adsk.fusion,json,os,hashlib
SOURCE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\RC_C_aperture_margin_study.json'
FRAME=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\original_front_sources\front_shared_frame_candidate.json'
EXPECTED='1088b5764b25c4c1b01526e8717366224d816f0df318bdc383531b62e3198eef'
def run_review(app,builder,mm,outdir):
 raw=open(SOURCE,'rb').read()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Study data changed')
 data=json.loads(raw);c=next(v for v in json.load(open(FRAME))['profiles'] if v['section']=='C');prior=app.activeDocument;doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_RC_C_PLANAR_APERTURE_STUDY_NOT_RELEASED';design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent
 x=c['station_X_candidate_mm'];ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);sk=root.sketches.add(plane);sk.name='C_ORIGINAL_OUTER_RC_INTERNAL_APERTURES';groups=[]
 loops=[c['loops_xyz_candidate_mm'][0]]+[v['RC_internal_candidate_loop_xyz_mm'] for v in data['records']]
 for loop in loops:
  lines=[]
  for a,b in zip(loop,loop[1:]+loop[:1]):lines.append(sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in a])),sk.modelToSketchSpace(adsk.core.Point3D.create(*[mm(v) for v in b]))))
  groups.append(lines)
 matches=[v for v in sk.profiles if v.profileLoops.count==3]
 if len(matches)!=1:raise RuntimeError('Expected one three-boundary region')
 records=[]
 for index,lines in enumerate(groups[1:]):
  gap=min(app.measureManager.measureMinimumDistance(a,b).value*10 for a in lines for b in groups[0]);expected=data['records'][index]['candidate_planar_gap_mm']
  if abs(gap-expected)>1e-6:raise RuntimeError('Independent native planar gap mismatch')
  records.append(dict(inner_loop=index+1,native_planar_gap_mm=gap,analytic_planar_gap_mm=expected))
 audit=dict(status='NATIVE_RC_C_PLANAR_APERTURE_STUDY',input_sha256=EXPECTED,profile_count=sk.profiles.count,records=records,solid_body_count=root.bRepBodies.count,metric_registration_verified=False,normal_3D_wall_verified=False,print_release=False)
 os.makedirs(outdir,exist_ok=True);design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_RC_C_PLANAR_APERTURE_STUDY.f3d')))
 with open(os.path.join(outdir,'F14_RC_C_planar_aperture_audit.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
