import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
outdir=R/'manufacturing/fit_coupons'; out=outdir/'F14_v274_CF_SLEEVE_CLAMP_COUPON.FCStd'; auditp=outdir/'v274_cf_sleeve_clamp_coupon_audit.json'
doc=App.newDocument('F14_v274_CF_SLEEVE_CLAMP_COUPON')
rows=[]; objs=[]
# sleeve blocks: OD candidates 6/8 mm, radial clearances 0.10/0.15/0.20
x0=0
for od in (6.0,8.0):
  for clr in (0.10,0.15,0.20):
    block=Part.makeBox(22,16,12,App.Vector(x0,0,0))
    bore=Part.makeCylinder(od/2+clr,22,App.Vector(x0,8,6),App.Vector(1,0,0))
    sh=block.cut(bore)
    o=doc.addObject('PartDesign::Feature',f'SLEEVE_{int(od)}_CLR_{int(clr*100):02d}'); o.Shape=sh; o.Label=f'{od:.0f}mm tube / radial clearance {clr:.2f}mm'; objs.append(o)
    rows.append({'type':'sleeve','tube_OD_mm':od,'radial_clearance_mm':clr,'bore_d_mm':od+2*clr,'valid':sh.isValid(),'volume_cm3':sh.Volume/1000})
    x0 += 27
# two C-clamp coupons using v271 cross-section, shortened to 10 mm axial test width.
for od in (6.0,8.0):
  bore=od/2+0.15; sleeve_or=bore+1.2; ir=sleeve_or+0.10; orr=ir+1.15; x=x0
  ring=Part.makeCylinder(orr,10,App.Vector(x,8,6),App.Vector(1,0,0)).cut(Part.makeCylinder(ir,10,App.Vector(x,8,6),App.Vector(1,0,0)))
  slit=Part.makeBox(12,1.0,orr-ir+3,App.Vector(x-1,7.5,6+ir-0.5)); ring=ring.cut(slit)
  lugz=6+ir-1; lug1=Part.makeBox(6,2.4,4.4,App.Vector(x+2,4.9,lugz)); lug2=Part.makeBox(6,2.4,4.4,App.Vector(x+2,8.7,lugz)); sh=ring.fuse(lug1).fuse(lug2)
  hole=Part.makeCylinder(1.55,8,App.Vector(x+5,4,lugz+2.2),App.Vector(0,1,0)); sh=sh.cut(hole).removeSplitter()
  o=doc.addObject('PartDesign::Feature',f'CLAMP_{int(od)}'); o.Shape=sh; o.Label=f'v271 style C-clamp {od:.0f}mm tube'; objs.append(o)
  rows.append({'type':'clamp','tube_OD_mm':od,'valid':sh.isValid(),'solid_count':len(sh.Solids),'volume_cm3':sh.Volume/1000})
  x0 += 25
doc.recompute(); doc.saveAs(str(out))
# STL export individually so each fit can be printed without slicing the master coupon.
stls=[]
for o in objs:
  fp=outdir/(o.Name+'.stl'); Part.export([o],str(fp)); stls.append(fp.name)
a={'status':'V274_CF_SLEEVE_CLAMP_COUPON','files':{'FCStd':out.name,'STL':stls},'rows':rows,'print_notes':['print in intended PPA-CF process and orientation','dry filament before coupon and production parts','test actual purchased CF tube; do not infer fit from nominal OD','record hand-fit, clamp force and visible wall damage'],'gates':{'all_valid':all(r['valid'] for r in rows),'actual_tube_fit_measured':False,'clamp_force_measured':False,'production_clearance_frozen':False}}
a['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); auditp.write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
