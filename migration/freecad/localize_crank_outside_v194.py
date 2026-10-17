import FreeCAD as App,Part,json,os,math,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SOURCE=os.path.join(BASE,'migration/freecad/F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd')
KIN=os.path.join(BASE,'analysis/F14_sweep_linkage_kinematics_v40.json')
OUT=os.path.join(BASE,'migration/freecad/freecad_v194_crank_outside_localization.json')
REVIEW=os.path.join(BASE,'migration/freecad/F14_v194_CRANK_OUTSIDE_REVIEW.FCStd')
def bounds(shape):
 b=shape.BoundBox;return dict(x=[b.XMin,b.XMax],y=[b.YMin,b.YMax],z=[b.ZMin,b.ZMax])
def feature(doc,name,shape):
 o=doc.addObject('PartDesign::Feature',name);o.Shape=shape;return o
source_hash=hashlib.sha256(open(SOURCE,'rb').read()).hexdigest();doc=App.openDocument(SOURCE);fuse=doc.getObject('FUSELAGE_CURRENT').Shape;wings={s:doc.getObject('WING_'+s).Shape for s in ['R','L']};c=json.load(open(KIN))['top_candidates'][1];review=App.newDocument('CRANK_OUTSIDE_DIAGNOSTIC');records=[];px=613.1323905812828;py0=125.20927023775282;z=8.407593065391325
for sample in c['samples']:
 sweep=float(sample['sweep_deg'])
 if sweep not in [20.0,44.0,68.0]:continue
 cp=sample['crank_pin_mm']
 for side,sign in [('R',1),('L',-1)]:
  start=App.Vector(px,sign*py0,z);end=App.Vector(float(cp[0]),sign*abs(float(cp[1])),z);direction=end-start;crank=Part.makeCylinder(4,direction.Length,start,direction)
  wing=wings[side].copy();wing.rotate(App.Vector(px,sign*py0,0),App.Vector(0,0,1),-sign*(sweep-20));envelope=fuse.fuse(wing)
  if envelope.isNull() or not envelope.isValid():raise RuntimeError('Invalid envelope union')
  outside=crank.cut(envelope)
  if not outside.isNull() and not outside.isValid():raise RuntimeError('Invalid outside query result')
  vol=outside.Volume if not outside.isNull() else 0.0;fraction=vol/crank.Volume
  records.append(dict(side=side,sweep_deg=sweep,crank_volume_mm3=crank.Volume,outside_volume_mm3=vol,outside_fraction=fraction,crank_bbox_mm=bounds(crank),outside_bbox_mm=bounds(outside) if vol else None,wing_bbox_mm=bounds(wing),pivot_mm=[px,sign*py0,z],pin_mm=[end.x,end.y,end.z]))
  feature(review,'CRANK_'+side+'_'+str(int(sweep)),crank)
  if vol:feature(review,'OUTSIDE_'+side+'_'+str(int(sweep)),outside)
review.recompute();review.saveAs(REVIEW)
assert hashlib.sha256(open(SOURCE,'rb').read()).hexdigest()==source_hash
report=dict(status='NATIVE_CRANK_OUTSIDE_CANDIDATE_AIRFRAME_LOCALIZATION',source_sha256=source_hash,records=records,scope='Three representative angles only; outside of provisional fuselage-plus-rotated-wing union. No hardware or original-aircraft envelope verification.',current_master_modified=False,mechanical_release=False,print_release=False)
with open(OUT,'w') as f:json.dump(report,f,indent=2)
print(json.dumps(records,indent=2))
