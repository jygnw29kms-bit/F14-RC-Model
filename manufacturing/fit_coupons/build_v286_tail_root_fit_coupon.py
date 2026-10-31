import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
D=R/'manufacturing/fit_coupons'; D.mkdir(parents=True,exist_ok=True)
out=D/'F14_v286_TAIL_ROOT_FIT_COUPON.FCStd'; audp=D/'v286_tail_root_fit_coupon_audit.json'
doc=App.newDocument('F14_v286_TAIL_ROOT_FIT_COUPON'); rows=[]
# D-bore gauge hubs. Flat removes 0.50 mm from the nominal 3.0 mm radius on +X side; clearances applied radially and at flat.
for i,clr in enumerate([0.00,0.05,0.10]):
    r=3.0+clr; hub=Part.makeCylinder(7.0,8,App.Vector(i*18,0,0),App.Vector(0,0,1))
    bore=Part.makeCylinder(r,10,App.Vector(i*18,0,-1),App.Vector(0,0,1))
    # D-flat at x >= center + (2.50 + clr)
    cutter=Part.makeBox(10,10,10,App.Vector(i*18+2.50+clr,-5,-1))
    dbore=bore.cut(cutter); sh=hub.cut(dbore).removeSplitter()
    o=doc.addObject('PartDesign::Feature',f'D_BORE_CLR_{int(clr*100):02d}'); o.Shape=sh; o.Label=f'v286 D-bore gauge +{clr:.2f} mm'
    stl=D/f'D_BORE_CLR_{int(clr*100):02d}.stl'; Part.export([o],str(stl)); rows.append({'type':'D_bore','clearance_mm':clr,'valid':sh.isValid(),'stl':stl.name})
# Root-fitting tongue envelope socket gauges: 36 x 31 x 3.5 mm outer envelope with per-face fit clearance.
for i,clr in enumerate([0.10,0.15,0.20]):
    x0=i*50; block=Part.makeBox(44,39,7,App.Vector(x0,20,0))
    slot=Part.makeBox(36+2*clr,31+2*clr,3.5+2*clr,App.Vector(x0+4-clr,24-clr,1.75-clr))
    sh=block.cut(slot).removeSplitter(); o=doc.addObject('PartDesign::Feature',f'ROOT_SOCKET_CLR_{int(clr*100):02d}'); o.Shape=sh; o.Label=f'v286 root-fitting envelope socket +{clr:.2f} mm/face'
    stl=D/f'ROOT_SOCKET_CLR_{int(clr*100):02d}.stl'; Part.export([o],str(stl)); rows.append({'type':'root_socket','per_face_clearance_mm':clr,'valid':sh.isValid(),'stl':stl.name})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V286_TAIL_ROOT_FIT_COUPON','files':{'FCStd':out.name,'STL':[r['stl'] for r in rows]},'rows':rows,'test_notes':['print in intended PPA-CF process/orientation and dry filament identically to production','measure actual 6 mm D-shaft fit in three D-bore gauges','use actual v284 root-fitting print or matching envelope gauge to select socket/bond gap','record insertion force, backlash, adhesive wet-out and cured pull/torsion result','do not promote v284 root fitting from geometry alone'],'gates':{'all_valid':all(r['valid'] for r in rows),'actual_D_shaft_fit_measured':False,'actual_root_socket_fit_measured':False,'adhesive_cure_coupon_tested':False,'torsion_proof_tested':False,'production_clearance_frozen':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
