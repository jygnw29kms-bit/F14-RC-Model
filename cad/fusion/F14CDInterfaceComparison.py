import adsk.core,adsk.fusion,json,os,hashlib
ARCHIVE=r'C:\Users\dezen\Desktop\F14-RC-Model\analysis\independent_reviews\C_D_internal_flow_20261017\F14_C_TO_D_INTERNAL_FLOW_STUDY.f3d'
EXPECTED='bb8b3a2d63e1f68586e8431ac711550b72d660080cce98a04cc3937d83dbc588'
def run_review(app,builder,mm,outdir):
 if hashlib.sha256(open(ARCHIVE,'rb').read()).hexdigest()!=EXPECTED:raise RuntimeError('Archive changed')
 prior=app.activeDocument;doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(ARCHIVE));design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent;flows=[b for b in root.bRepBodies if b.name.startswith('C_TO_D_FLOW_VOLUME_STUDY_')];walls=[b for b in root.bRepBodies if b not in flows];records=[]
 if len(flows)!=2 or len(walls)!=2:raise RuntimeError('Expected isolated two flow studies and two reference walls')
 for flow in flows:
  wall=next(b for b in walls if (b.boundingBox.minPoint.y+b.boundingBox.maxPoint.y)*(flow.boundingBox.minPoint.y+flow.boundingBox.maxPoint.y)>0)
  ff=[f for f in flow.faces if adsk.core.Plane.cast(f.geometry) and abs(adsk.core.Plane.cast(f.geometry).normal.x)>.999];wf=[f for f in wall.faces if adsk.core.Plane.cast(f.geometry) and abs(adsk.core.Plane.cast(f.geometry).normal.x)>.999]
  end=max(ff,key=lambda f:f.pointOnFace.x);start=min(wf,key=lambda f:f.pointOnFace.x);loops=[v for v in start.loops if not v.isOuter]
  if len(loops)!=1:raise RuntimeError('Reference inlet inner boundary ambiguous')
  x=start.pointOnFace.x*10;ci=root.constructionPlanes.createInput();ci.setByOffset(root.yZConstructionPlane,adsk.core.ValueInput.createByReal(mm(x if root.yZConstructionPlane.geometry.normal.x>0 else -x)));plane=root.constructionPlanes.add(ci);sk=root.sketches.add(plane)
  for edge in loops[0].edges:sk.project(edge)
  if sk.profiles.count!=1:raise RuntimeError('Reference flow profile ambiguous')
  area=sk.profiles.item(0).areaProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy).area*100
  flow_area=end.area*100;flow_length=sum(e.length for e in end.edges)*10;reference_length=sum(e.length for e in loops[0].edges)*10
  records.append(dict(flow_body=flow.name,axial_gap_mm=(end.pointOnFace.x-start.pointOnFace.x)*10,flow_end_area_mm2=flow_area,native_inlet_inner_profile_area_mm2=area,area_difference_mm2=flow_area-area,flow_end_perimeter_mm=flow_length,native_inlet_inner_perimeter_mm=reference_length,perimeter_difference_mm=flow_length-reference_length))
 audit=dict(status='NATIVE_C_D_INTERFACE_AREA_PERIMETER_COMPARISON',archive_sha256=EXPECTED,records=records,interpretation='Axial location, area and perimeter comparison only; these do not prove full boundary coincidence or tangent continuity.',full_boundary_coincidence_verified=False,wall_thickness_verified=False,print_release=False)
 os.makedirs(outdir,exist_ok=True)
 with open(os.path.join(outdir,'F14_C_D_interface_comparison.json'),'w') as f:json.dump(audit,f,indent=2)
 doc.close(False)
 if prior:prior.activate()
 return audit
