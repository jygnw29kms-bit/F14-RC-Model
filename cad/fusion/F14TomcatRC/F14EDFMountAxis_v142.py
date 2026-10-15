"""v142: micro-optimize provisional EDF sleeve end axis for bilateral source containment."""
import adsk.core,adsk.fusion,json,os,hashlib

def mm(v):return v/10.0
def frange(a,b,s):
 n=int(round((b-a)/s));return [a+i*s for i in range(n+1)]
def ring(temp,x0,x1,y0,z0,y1,z1,od,id_):
 o=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(od/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(od/2));i=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x0),mm(y0),mm(z0)),mm(id_/2),adsk.core.Point3D.create(mm(x1),mm(y1),mm(z1)),mm(id_/2));
 if not temp.booleanOperation(o,i,adsk.fusion.BooleanTypes.DifferenceBooleanType):raise RuntimeError('ring diff')
 return o
def ivol(temp,a,b):
 q=temp.copy(a);ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType);return q.volume if ok and q.isValid else 0.0
def run_review(app,builder,mm_unused,outdir):
 prior=app.activeDocument;base=os.path.dirname(__file__);cfg=json.load(open(os.path.join(base,'F14_v142_section_inputs.json'),encoding='utf-8'))
 if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('source hash')
 if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])):raise RuntimeError('import')
 imp=app.activeDocument;d=adsk.fusion.Design.cast(app.activeProduct);temp=adsk.fusion.TemporaryBRepManager.get();bs=[d.rootComponent.bRepBodies.item(i) for i in range(d.rootComponent.bRepBodies.count)];ref=next(b for b in bs if b.name=='REFERENCE_SOURCE_SILHOUETTE_GUIDED_AFT_v135');walls={s:next(b for b in bs if b.name=='INLET_WALL_COMPLETE_ENDS_'+s+'_v139') for s in ('R','L')}
 x0=float(cfg['flange_start_x_mm']);xi=float(cfg['interface_x_mm']);xe=float(cfg['sleeve_end_x_mm']);yi=float(cfg['interface_abs_y_mm']);zi=float(cfg['interface_z_mm']);D={'x':595.8483908511422,'y':56.30470783882318,'z':-6.556713425255683};t=(x0-D['x'])/(xi-D['x']);yf=D['y']+(yi-D['y'])*t;zf=D['z']+(zi-D['z'])*t
 candidates=[]
 for ye in frange(*[float(x) for x in cfg['end_abs_y_range_mm']]):
  for ze in frange(*[float(x) for x in cfg['end_z_range_mm']]):
   sides=[]
   for lab,sgn in [('R',1),('L',-1)]:
    flange=ring(temp,x0,xi,sgn*yf,zf,sgn*yi,zi,float(cfg['flange_outer_diameter_mm']),float(cfg['flange_inner_diameter_mm']));sleeve=ring(temp,xi,xe,sgn*yi,zi,sgn*ye,ze,float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']));m=temp.copy(flange);temp.booleanOperation(m,sleeve,adsk.fusion.BooleanTypes.UnionBooleanType);out=max(0.0,m.volume-ivol(temp,m,ref));sides.append({'side':lab,'outside_cm3':out})
   mx=max(s['outside_cm3'] for s in sides);sm=sum(s['outside_cm3'] for s in sides);move=(ye-yi)**2+(ze-zi)**2;candidates.append({'end_abs_y_mm':ye,'end_z_mm':ze,'max_outside_cm3':mx,'sum_outside_cm3':sm,'movement_cost_mm2':move,'sides':sides})
 candidates.sort(key=lambda c:(c['max_outside_cm3']>float(cfg['containment_tolerance_cm3']),c['max_outside_cm3'],c['sum_outside_cm3'],c['movement_cost_mm2']));best=candidates[0]
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_EDF_MOUNT_AXIS_REFINED_v142';rd=adsk.fusion.Design.cast(app.activeProduct);rd.designType=adsk.fusion.DesignTypes.DirectDesignType;root=rd.rootComponent;source=root.bRepBodies.add(temp.copy(ref));source.name=ref.name;records=[]
 for lab,sgn in [('R',1),('L',-1)]:
  flange=ring(temp,x0,xi,sgn*yf,zf,sgn*yi,zi,float(cfg['flange_outer_diameter_mm']),float(cfg['flange_inner_diameter_mm']));sleeve=ring(temp,xi,xe,sgn*yi,zi,sgn*best['end_abs_y_mm'],best['end_z_mm'],float(cfg['sleeve_outer_diameter_mm']),float(cfg['sleeve_inner_diameter_mm']));mount=temp.copy(flange);ok=temp.booleanOperation(mount,sleeve,adsk.fusion.BooleanTypes.UnionBooleanType);wall=temp.copy(walls[lab]);ok2=temp.booleanOperation(wall,temp.copy(mount),adsk.fusion.BooleanTypes.UnionBooleanType);body=root.bRepBodies.add(wall);body.name='INLET_FAN_MOUNT_REFINED_'+lab+'_v142';outside=max(0.0,body.volume-ivol(temp,body,source));xfaces=[]
  for f in body.faces:
   pl=adsk.core.Plane.cast(f.geometry)
   if pl and abs(abs(pl.normal.x)-1)<1e-7 and abs(pl.normal.y)<1e-7 and abs(pl.normal.z)<1e-7:xfaces.append({'x_mm':pl.origin.x*10,'loop_count':f.loops.count,'area_mm2':f.area*100})
  ends=[f for f in xfaces if abs(f['x_mm']-595.8483908511422)<1e-5 or abs(f['x_mm']-xe)<1e-5];records.append({'side':lab,'mount_union_ok':bool(ok),'combined_union_ok':bool(ok2),'outside_source_cm3':outside,'physical_ends':ends,'physical_ends_pass':len(ends)==2 and all(f['loop_count']==2 for f in ends),'pass':bool(ok and ok2 and outside<=float(cfg['containment_tolerance_cm3']) and len(ends)==2 and all(f['loop_count']==2 for f in ends))})
 passed=all(r['pass'] for r in records);audit={'status':'V142_EDF_MOUNT_AXIS_MICRO_OPTIMIZATION','source':cfg,'candidate_count':len(candidates),'best':best,'top20':candidates[:20],'axis_change':{'delta_y_mm':best['end_abs_y_mm']-yi,'delta_z_mm':best['end_z_mm']-zi,'sleeve_yaw_deg':__import__('math').degrees(__import__('math').atan2(best['end_abs_y_mm']-yi,xe-xi)),'sleeve_pitch_deg':__import__('math').degrees(__import__('math').atan2(best['end_z_mm']-zi,xe-xi))},'records':records,'bilateral_geometry_pass':passed,'hardware_measurement_required':True,'hardware_revision_frozen':False,'geometry_candidate_pass':passed,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()};os.makedirs(outdir,exist_ok=True);rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_EDF_MOUNT_AXIS_REFINED_v142.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_v142_edf_mount_axis_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v142_edf_mount_axis_review.png'),1600,1000)
 try:doc.close(False);imp.close(False)
 except:pass
 if prior:
  try:prior.activate()
  except:pass
 return audit