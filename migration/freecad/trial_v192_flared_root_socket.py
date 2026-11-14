from pathlib import Path
import FreeCAD as App,Part,json,hashlib,time
R=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();master=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';sparfile=R/'migration/freecad/FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd';basis=R/'analysis/v192_cap_width_inner_envelope.json';b=json.loads(basis.read_text())['rows'][0];inputs={str(p):sha(p) for p in (master,sparfile,basis)}
out=R/'analysis/v192_flared_root_socket_trial.json';log=out.with_suffix('.jsonl');path=R/'migration/freecad/FLARED_ROOT_SOCKET_UNFROZEN_CONCEPT_ONLY.FCStd';assert not out.exists() and not log.exists() and not path.exists()
def stage(name,**kw):
 with log.open('a') as f:f.write(json.dumps(dict(stage=name,**kw))+'\n')
 print(name,flush=True)
def rect(x,y,width,lo,hi):
 pts=[App.Vector(x-width/2,y,lo),App.Vector(x+width/2,y,lo),App.Vector(x+width/2,y,hi),App.Vector(x-width/2,y,hi)];return Part.makePolygon(pts+[pts[0]])
a=App.openDocument(str(master));sp=App.openDocument(str(sparfile));d=App.newDocument('FLARED_ROOT_SOCKET_CONCEPT');rows=[]
try:
 lower=sp.getObject('CONTINUOUS_LOWER_CAP_REFERENCE').Shape;f=next(f for f in lower.Faces if abs(f.BoundBox.YMin-149)<1e-7 and f.BoundBox.YLength<1e-7);xroot=(f.BoundBox.XMin+f.BoundBox.XMax)/2
 px,py=613.1323905812828,125.20927023775282
 xpos=lambda y:xroot+(b['x_center_mm']-xroot)*(y-149)/36
 lo=b['lower_cap_z_interval_mm'][0]-.8;hi=b['upper_cap_z_interval_mm'][1]+.8
 stage('build_flared_body');s=Part.makeLoft([rect(px,py,24,-8,8),rect(xroot,149,20,lo,hi),rect(xpos(175),175,20,lo,hi)],True,True)
 boss=Part.makeCylinder(12,16,App.Vector(px,py,-8));s=s.fuse(boss).cut(Part.makeCylinder(3,24,App.Vector(px,py,-12)))
 stage('cut_unfrozen_slots')
 slots=[]
 for side in ('lower','upper'):
  z0,z1=b[side+'_cap_z_interval_mm'];slots.append(Part.makeLoft([rect(xpos(y),y,16.3,z0-.15,z1+.15) for y in (149,176)],True,True))
 slots.append(Part.makeLoft([rect(xpos(y),y,4.3,b['lower_cap_z_interval_mm'][1]-.15,b['upper_cap_z_interval_mm'][0]+.15) for y in (149,176)],True,True))
 for tool in slots:s=s.cut(tool)
 assert s.isValid() and len(s.Solids)==1
 for o in sp.Objects:
  if not hasattr(o,'Shape') or o.Shape.isNull():continue
  stage('spar_interface',object=o.Name);overlap=s.common(o.Shape).Volume;dist=s.distToShape(o.Shape)[0];rows.append({'object':o.Name,'overlap_volume_mm3':overlap,'distance_mm':dist})
 stage('outer_packaging_baseline');wing=a.getObject('WING_R').Shape;body=a.getObject('FUSELAGE_CURRENT').Shape;outside=s.cut(body).cut(wing).Volume
 o=d.addObject('PartDesign::Feature','FLARED_SOCKET_UNFROZEN_NO_HARDWARE_RELEASE');o.Shape=s;d.recompute();d.saveAs(str(path))
finally:App.closeDocument(d.Name);App.closeDocument(sp.Name);App.closeDocument(a.Name)
assert all(sha(Path(p))==h for p,h in inputs.items())
r={'status':'FLARED_ROOT_SOCKET_CLEARANCE_CONCEPT_ONLY','input_sha256':inputs,'output_sha256':sha(path),'packaging_accepted_against_current_reference':outside<=1e-6,'valid':True,'solids':1,'volume_mm3':s.Volume,'interface_rows':rows,'baseline20_outside_current_body_or_wing_volume_mm3':outside,'assumptions':{'pivot_xyz_mm':[px,py,0],'boss_od_mm':24,'nominal_bore_mm':6,'socket_y_interval_mm':[149,175],'cap_slot_width_mm':16.3,'cap_slot_vertical_extra_each_side_mm':.15,'web_flange_slot_width_mm':4.3,'hardware_selected':False},'limits':['Socket clearances are coordinate offsets, not normal-distance manufacturing tolerances','Slots start atY149 and open pastY175; hard stop/assembly insertion/adhesive retention not qualified','Provisional pivotZ0 and vertical bore, not calibrated canted bearing axis','Baseline outside-volume is against incomplete body/glove; no exterior enlargement or integration','No sweep envelope, load-transfer contact/bond, bearing selection, stress or physical proof','Native reopen remains open; master unchanged'],'print_release':False,'flight_release':False}
out.write_text(json.dumps(r,indent=2)+'\n');stage('complete');print(json.dumps(r))
