import FreeCAD as App, Part, json, hashlib
from pathlib import Path
BASE=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad")
src=App.openDocument(str(BASE/'F14_GESAMTSTAND_REVIEW.FCStd'))
out=App.newDocument('F14_WING_PIVOT_FOCUSED_REVIEW')
keep=[
('LEGACY_FULL_FUSELAGE_CURRENT','FUSELAGE'),
('LEGACY_FULL_STABILATOR_L','STAB_L'),('LEGACY_FULL_STABILATOR_R','STAB_R'),
('LEGACY_FULL_VTAIL_L','VTAIL_L'),('LEGACY_FULL_VTAIL_R','VTAIL_R'),
('LEGACY_FULL_WING_R','WING_R_OLD'),('LEGACY_FULL_WING_L','WING_L_OLD')]
for name,newname in keep:
    o=src.getObject(name)
    if not o or not hasattr(o,'Shape') or o.Shape.isNull(): raise RuntimeError(name)
    n=out.addObject('PartDesign::Feature',newname); n.Label=newname; n.Shape=o.Shape.copy()
old_pivot=613.1323905812828
target=504.3463093769572
dx=target-old_pivot
for srcname,newname in [('LEGACY_FULL_WING_R','WING_R_CORR_X'),('LEGACY_FULL_WING_L','WING_L_CORR_X')]:
    o=src.getObject(srcname); sh=o.Shape.copy(); sh.translate(App.Vector(dx,0,0))
    n=out.addObject('PartDesign::Feature',newname); n.Label=newname; n.Shape=sh
for x,label in [(old_pivot,'PIVOT_OLD'),(target,'PIVOT_NADC_FS524_16')]:
    for y,side in [(125.20927023775283,'R'),(-125.20927023775283,'L')]:
        n=out.addObject('PartDesign::Feature',f'{label}_{side}'); n.Label=f'{label}_{side}'; n.Shape=Part.makeCylinder(5,28,App.Vector(x,y,-14),App.Vector(0,0,1))
ax=out.addObject('PartDesign::Feature','CENTER_AXIS'); ax.Label='CENTER_AXIS'; ax.Shape=Part.makeLine(App.Vector(0,0,0),App.Vector(900,0,0))
out.recompute(); path=BASE/'F14_WING_PIVOT_FOCUSED_REVIEW.FCStd'; out.saveAs(str(path)); App.closeDocument(out.Name); App.closeDocument(src.Name)
a={'status':'FOCUSED_WING_PIVOT_REVIEW','delta_X_mm':dx,'old_pivot_X_mm':old_pivot,'target_pivot_X_mm':target,'object_count':14,'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'gates':{'review_only':True,'Y_verified':False,'Z_verified':False,'master_changed':False}}
(BASE/'freecad_WING_PIVOT_FOCUSED_REVIEW_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
