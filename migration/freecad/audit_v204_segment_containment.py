import FreeCAD as App, Part, json
from pathlib import Path
p=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/F14_v204_STRUCTURAL_WINGBOX_CANDIDATE.FCStd")
d=App.openDocument(str(p)); fus=d.getObject('FUSELAGE_CURRENT').Shape; px=504.3463093769572; py=125.20927023775282

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def cyl_y(x,y0,y1,z,r): return Part.makeCylinder(r,y1-y0,App.Vector(x,y0,z),App.Vector(0,1,0))
def frac(sh):
 c=sh.common(fus); iv=c.Volume if not c.isNull() else 0; return iv/sh.Volume if sh.Volume else 0,iv,sh.Volume
rows=[]
for sign,lab in [(1,'R'),(-1,'L')]:
 y=sign*py; pad_in=y-sign*20; pad_out=y+sign*12; strap_in=sign*70
 py0,py1=min(pad_in,pad_out),max(pad_in,pad_out); sy0,sy1=min(strap_in,pad_in),max(strap_in,pad_in)
 segs=[('PAD',box(px-22,px+22,py0,py1,-12.5,-10.5)),('FRONT_STRAP',box(px-22,px-10,sy0,sy1,-12.5,-10.5)),('REAR_STRAP',box(px+10,px+22,sy0,sy1,-12.5,-10.5))]
 for name,sh in segs:
  f,iv,v=frac(sh); rows.append({'side':lab,'part':name,'inside_fraction':f,'inside_mm3':iv,'volume_mm3':v})
 for fa,xc,zc in [('FRONT',px-16,-4.5),('REAR',px+16,-5.5)]:
  z0=-12.5;z1=zc+4;x0=xc-6;x1=xc+6
  if sign>0: ya,yb=50,74;ty0,ty1=73.9,82
  else: ya,yb=-74,-50;ty0,ty1=-82,-73.9
  ris=box(x0,x1,ya,yb,z0,z1).cut(cyl_y(xc,ya-0.1,yb+0.1,zc,3.2)); tail=box(x0,x1,ty0,ty1,z0,z1); hp=ris.fuse(tail)
  for n,sh in [('SOCKET_'+fa,hp)]:
   f,iv,v=frac(sh);rows.append({'side':lab,'part':n,'inside_fraction':f,'inside_mm3':iv,'volume_mm3':v})
res={'status':'V204_SEGMENT_CONTAINMENT','rows':rows,'worst':min(rows,key=lambda r:r['inside_fraction'])}
Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad/freecad_v204_segment_containment_audit.json").write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
