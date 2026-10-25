import FreeCAD as App, Part, math, json, hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad")
src=BASE/'F14_v203_INTEGRATED_FULL_MODEL_CANDIDATE.FCStd'
out=BASE/'F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd'
d=App.openDocument(str(src))
px=504.3463093769572; py=125.20927023775282; pz=0.0
plate_t=2.0; inboard=70.0

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def cyl_y(x,y0,y1,z,r):
 c=Part.makeCylinder(r,y1-y0,App.Vector(x,y0,z),App.Vector(0,1,0)); return c

def add(name,label,shape):
 o=d.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=shape; return o
records=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 y=sign*py; pad_in=y-sign*20.0; pad_out=y+sign*12.0; strap_in=sign*inboard
 pad_y0,pad_y1=min(pad_in,pad_out),max(pad_in,pad_out); strap_y0,strap_y1=min(strap_in,pad_in),max(strap_in,pad_in)
 plates={}
 for pos,z0 in [('LOWER',-12.5),('UPPER',10.5)]:
  pad=box(px-22,px+22,pad_y0,pad_y1,z0,z0+plate_t)
  fs=box(px-22,px-10,strap_y0,strap_y1,z0,z0+plate_t)
  rs=box(px+10,px+22,strap_y0,strap_y1,z0,z0+plate_t)
  sh=pad.fuse(fs).fuse(rs)
  shaft=Part.makeCylinder(3.1,plate_t+0.2,App.Vector(px,y,z0-0.1),App.Vector(0,0,1))
  sh=sh.cut(shaft)
  plates[pos]=sh
 # v99/v103 sockets/tails on lower structure
 sockets=[]
 for fa,xc,zc in [('FRONT',px-16,-4.5),('REAR',px+16,-5.5)]:
  z0=-12.5; z1=zc+4.0; x0=xc-6; x1=xc+6
  if sign>0: ya,yb=50.0,74.0; ty0,ty1=73.9,82.0
  else: ya,yb=-74.0,-50.0; ty0,ty1=-82.0,-73.9
  raw=box(x0,x1,ya,yb,z0,z1)
  bore=cyl_y(xc,ya-0.1,yb+0.1,zc,3.2)
  ris=raw.cut(bore)
  tail=box(x0,x1,ty0,ty1,z0,z1)
  hp=ris.fuse(tail)
  sockets.append(hp)
  add(f'V204_SOCKET_{fa}_{lab}',f'v204 circular socket+tail {fa} {lab}',hp)
 lower=plates['LOWER'].fuse(sockets[0]).fuse(sockets[1])
 add(f'V204_MONO_LOWER_{lab}',f'v204 monolithic lower hardpoint {lab}',lower)
 add(f'V204_UPPER_FORK_{lab}',f'v204 upper fork plate {lab}',plates['UPPER'])
 # hardware references
 shaft=Part.makeCylinder(3.0,26.0,App.Vector(px,y,-13),App.Vector(0,0,1)); add(f'V204_SHAFT_{lab}',f'6mm pivot shaft ref {lab}',shaft)
 for pos,z0 in [('LOWER',-10.0),('UPPER',5.0)]:
  brg=Part.makeCylinder(6.5,5.0,App.Vector(px,y,z0),App.Vector(0,0,1)); add(f'V204_BEARING_{pos}_{lab}',f'6x13x5 bearing ref {pos} {lab}',brg)
 records.append({'side':lab,'pad_y':[pad_y0,pad_y1],'strap_y':[strap_y0,strap_y1]})
meta=d.addObject('App::FeaturePython','V204_META'); meta.Label='v204 structural wingbox candidate'
for n,v in [('Status','STRUCTURAL CANDIDATE / NOT RELEASED'),('Source','v31+v99+v103 ported to v203 nose-relative frame')]: meta.addProperty('App::PropertyString',n,'Gate'); setattr(meta,n,v)
for n,v in [('PivotXYSourceBacked',True),('AbsoluteZVerified',False),('MaterialVerified',False),('ProductionRelease',False)]: meta.addProperty('App::PropertyBool',n,'Gate'); setattr(meta,n,v)
d.recompute(); d.saveAs(str(out))
a={'status':'V204_STRUCTURAL_WINGBOX_CANDIDATE','pivot_mm':[px,py,pz],'records':records,'port':{'old_absolute_FS_x_shift_removed_mm':108.7860812043256,'local_pivot_z_mm':0.0},'gates':{'fork_geometry_ported':True,'circular_socket_bores_preserved':True,'monolithic_lower_union_CAD':True,'fuselage_containment_verified':False,'continuous_sweep_clearance_verified':False,'material_verified':False,'physical_proof':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(BASE/'freecad_v204_structural_wingbox_candidate_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
print(json.dumps(a,indent=2))
