"""v153: direct battery-adjustment-envelope search in registered v105 fuselage/wingbox."""
import adsk.core,adsk.fusion,json,os,hashlib

def mm(v):return v/10.0
def frange(a,b,s):
 n=int(round((b-a)/s));return [a+i*s for i in range(n+1)]
def box(temp,cx,cy,cz,l,w,h):
 c=adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz));obb=adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h));return temp.createBox(obb)
def ivol(temp,a,b):
 q=temp.copy(a);ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType);return q.volume if ok and q.isValid else 0.0
def evaluate(temp,fus,blockers,cx,cy,cz,l,w,h):
 b=box(temp,cx,cy,cz,l,w,h);total=b.volume;inside=ivol(temp,b,fus);outside=max(0,total-inside);coll=[];ct=0
 for s in blockers:
  v=ivol(temp,b,s);ct+=v
  if v>0:coll.append({'body':s.name,'intersection_cm3':v})
 return {'center_mm':[cx,cy,cz],'x_range_mm':[cx-l/2,cx+l/2],'y_range_mm':[cy-w/2,cy+w/2],'z_range_mm':[cz-h/2,cz+h/2],'total_cm3':total,'inside_fuselage_cm3':inside,'outside_fuselage_cm3':outside,'containment_fraction':inside/total if total else 0,'fixed_structure_intersection_cm3':ct,'collisions':coll}
def run_review(app,builder,mm_unused,outdir):
 prior=app.activeDocument;base=os.path.dirname(__file__);cfg=json.load(open(os.path.join(base,'F14_v153_section_inputs.json'),encoding='utf-8'))
 if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('v153 source hash')
 if not app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path'])):raise RuntimeError('v105 import')
 imp=app.activeDocument;d=adsk.fusion.Design.cast(app.activeProduct);root=d.rootComponent;temp=adsk.fusion.TemporaryBRepManager.get();bodies=[root.bRepBodies.item(i) for i in range(root.bRepBodies.count)]
 fus=next((b for b in bodies if b.name=='UPC_FUSELAGE_ROBUST_CLEARANCE_CUT_v29'),None)
 if fus is None:raise RuntimeError('fuselage body missing')
 blockers=[b for b in bodies if b is not fus and (b.name.startswith('MONOLITHIC_') or b.name.startswith('ENG_') or b.name.startswith('REF_CF') or 'WINGBOX' in b.name or 'HARDPOINT' in b.name)]
 l,w,h=[float(x) for x in cfg['tray_envelope_mm']];xr=[float(x) for x in cfg['x_center_range_mm']];yr=[float(x) for x in cfg['y_center_range_mm']];zr=[float(x) for x in cfg['z_center_range_mm']]
 rec=[]
 for x in frange(*xr):
  for y in frange(*yr):
   for z in frange(*zr):rec.append(evaluate(temp,fus,blockers,x,y,z,l,w,h))
 rec.sort(key=lambda q:(q['outside_fuselage_cm3']+q['fixed_structure_intersection_cm3'],-q['containment_fraction'],abs(q['center_mm'][1])))
 seed=rec[0];hw=float(cfg['refine_half_window_mm']);st=float(cfg['refine_step_mm']);fine=[]
 for x in frange(seed['center_mm'][0]-hw,seed['center_mm'][0]+hw,st):
  for y in frange(seed['center_mm'][1]-min(hw,8),seed['center_mm'][1]+min(hw,8),st):
   for z in frange(seed['center_mm'][2]-hw,seed['center_mm'][2]+hw,st):fine.append(evaluate(temp,fus,blockers,x,y,z,l,w,h))
 fine.sort(key=lambda q:(q['outside_fuselage_cm3']+q['fixed_structure_intersection_cm3'],-q['containment_fraction'],abs(q['center_mm'][1])));best=fine[0];best['pass']=best['outside_fuselage_cm3']<=float(cfg['containment_tolerance_cm3']) and best['fixed_structure_intersection_cm3']<=float(cfg['collision_tolerance_cm3'])
 doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name='F14_BATTERY_TRAY_ENVELOPE_v153';rd=adsk.fusion.Design.cast(app.activeProduct);rd.designType=adsk.fusion.DesignTypes.DirectDesignType;rr=rd.rootComponent;rf=rr.bRepBodies.add(temp.copy(fus));rf.name=fus.name
 for s in blockers:
  try:b=rr.bRepBodies.add(temp.copy(s));b.name=s.name
  except:pass
 env=rr.bRepBodies.add(box(temp,*best['center_mm'],l,w,h));env.name='BATTERY_ADJUSTMENT_ENVELOPE_v153'
 audit={'status':'V153_BATTERY_ADJUSTMENT_ENVELOPE_PACKAGING','source':cfg,'inventory':[b.name for b in bodies],'blocker_names':[b.name for b in blockers],'coarse_count':len(rec),'refined_count':len(fine),'best':best,'top20':fine[:20],'geometry_candidate_pass':best['pass'],'battery_hardware_frozen':False,'CG_range_mass_rollup_verified':False,'retention_structure_designed':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
 os.makedirs(outdir,exist_ok=True);rd.exportManager.execute(rd.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_BATTERY_TRAY_ENVELOPE_v153.f3d')));json.dump(audit,open(os.path.join(outdir,'F14_v153_battery_tray_audit.json'),'w'),indent=2);app.activeViewport.fit();app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v153_battery_tray_review.png'),1600,1000)
 try:doc.close(False);imp.close(False)
 except:pass
 if prior:
  try:prior.activate()
  except:pass
 return audit