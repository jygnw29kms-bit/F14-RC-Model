"""v143: tapered overlap flange grows from local duct wall to provisional EDF sleeve."""
import adsk.core,adsk.fusion,json,os,hashlib

def mm(v):return v/10.0
def ring(temp,x0,x1,y0,z0,y1,z1,od0,od1,id0,id1):
 o=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(od0/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(od1/2));i=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(id0/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(id1/2));
 if not temp.booleanOperation(o,i,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('ring diff')
 return o
def ivol(temp,a,b):
 q=temp.copy(a);ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType);return q.volume if ok and q.isValid else 0.0
def run_review(app,builder,mm_unused,outdir):
 prior=app.activeDocument;base=os.path.dirname(__file__);cfg=json.load(open(os.path.join(base,'F14_v143_section_inputs.json'),encoding='utf-8'))
 for p,h in ((cfg['path'],cfg['sha256']),(cfg['v139_audit_path'],cfg['v139_audit_sha256'])):
  if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h:raise RuntimeError('source hash mismatch')
 a139=json.load(open(cfg['v139_audit_path'],encoding='utf-8'));inherited=min(float(r['minimum_inner_outer_face_gap_mm']) for r in a139['records'])
 if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])):raise RuntimeError('import')
 imp=app.activeDocument;od=adsk.fusion.Design.cast(app.activeProduct);temp=adsk.fusion.TemporaryBRepManager.get();bs=[od.rootComponent.bRepBodies.item(i) for i in range(od.rootComponent.bRepBodies.count)];ref=next(b for b in bs if b.name=='REFERENCE_SOURCE_SILHOUETTE_GUIDED_AFT_v135');walls={s:next(b for b in bs if b.name=='INLET_WALL_COMPLETE_ENDS_'+s+'_v139') for s in ('R','L')}
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_TAPERED_FAN_SHOULDER_v143';rd=adsk.fusion.Design.cast(app.activeProduct);rd.designType=adsk.fusion.DesignTypes.DirectDesignType;root=rd.rootComponent;source=root.bRepBodies.add(temp.copy(ref));source.name=ref.name
 xi=float(cfg['interface_x_mm']);xf=float(cfg['flange_start_x_mm']);xe=float(cfg['sleeve_end_x_mm']);yi=float(cfg['interface_abs_y_mm']);zi=float(cfg['interface_z_mm']);D={'x':595.8483908511422,'y':56.30470783882318,'z':-6.556713425255683};t=(xf-D['x'])/(xi-D['x']);yf=D['y']+(yi-D['y'])*t;zf=D['z']+(zi-D['z'])*t;records=[]
 for lab,sgn in [('R',1),('L',-1)]:
  flange=ring(temp,xf,xi,sgn*yf,zf,sgn*yi,zi,float(cfg['flange_start_outer_diameter_mm']),float(cfg['flange_end_outer_diameter_mm']),float(cfg['flange_start_inner_diameter_mm']),float(cfg['flange_end_inner_diameter_mm']));sleeve=ring(temp,xi,xe,sgn*yi,zi,sgn*yi,zi,float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']));mount=temp.copy(flange);u1=temp.booleanOperation(mount,temp.copy(sleeve),adsk.fusion.BooleanTypes.UnionBooleanType);mount_out=max(0,mount.volume-ivol(temp,mount,source));wall=temp.copy(walls[lab]);u2=temp.booleanOperation(wall,temp.copy(mount),adsk.fusion.BooleanTypes.UnionBooleanType);body=root.bRepBodies.add(wall);body.name='INLET_TAPERED_FAN_MOUNT_'+lab+'_v143';outside=max(0,body.volume-ivol(temp,body,source));xfaces=[]
  for f in body.faces:
   pl=adsk.core.Plane.cast(f.geometry)
   if pl and abs(abs(pl.normal.x)-1)<1e-7 and abs(pl.normal.y)<1e-7 and abs(pl.normal.z)<1e-7:xfaces.append({'x_mm':pl.origin.x*10,'loop_count':f.loops.count,'area_mm2':f.area*100})
  ends=[f for f in xfaces if abs(f['x_mm']-595.8483908511422)<1e-5 or abs(f['x_mm']-xe)<1e-5];flange_start_wall=(float(cfg['flange_start_outer_diameter_mm'])-float(cfg['flange_start_inner_diameter_mm']))/2;flange_end_wall=(float(cfg['flange_end_outer_diameter_mm'])-float(cfg['flange_end_inner_diameter_mm']))/2;sleeve_wall=(float(cfg['sleeve_outer_diameter_mm'])-float(cfg['sleeve_inner_diameter_mm']))/2;mingap=min(inherited,flange_start_wall,flange_end_wall,sleeve_wall);contain=mount_out<=float(cfg['containment_tolerance_cm3']) and outside<=float(cfg['containment_tolerance_cm3']);endpass=len(ends)==2 and all(f['loop_count']==2 for f in ends);wallpass=mingap>=float(cfg['minimum_wall_mm']);records.append({'side':lab,'mount_union_ok':bool(u1),'combined_union_ok':bool(u2),'mount_outside_source_cm3':mount_out,'combined_outside_source_cm3':outside,'containment_pass':contain,'governing_wall_mm':mingap,'wall_pass':wallpass,'physical_end_faces':ends,'physical_end_pass':endpass,'pass':bool(u1 and u2 and contain and wallpass and endpass)})
 passed=all(r['pass'] for r in records);audit={'status':'V143_TAPERED_OVERLAP_FAN_SHOULDER','source':cfg,'records':records,'bilateral_geometry_pass':passed,'hardware_measurement_required':True,'actual_EDF_shroud_measured':False,'hardware_revision_frozen':False,'geometry_candidate_pass':passed,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()};os.makedirs(outdir,exist_ok=True);rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_TAPERED_FAN_SHOULDER_v143.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_v143_tapered_fan_shoulder_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v143_tapered_fan_shoulder_review.png'),1600,1000)
 try:doc.close(False);imp.close(False)
 except:pass
 if prior:
  try:prior.activate()
  except:pass
 return audit