import FreeCAD as App, Part, json, os, hashlib
repo=r'C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model'
base=os.path.join(repo,'migration','freecad','F14_GESAMTSTAND_REVIEW.FCStd')
legacy=os.path.join(repo,'migration','freecad','F14_v194_FAIL_CLOSED_REVIEW.FCStd')
out=os.path.join(repo,'migration','freecad','F14_WING_PIVOT_X_CORRECTION_REVIEW.FCStd')
scale=1.1697428086486623
FS0=93.0
pivot_fs=524.16
pivot_target=(pivot_fs-FS0)*scale
pivot_legacy=613.1323905812828
dx=pivot_target-pivot_legacy
src=App.openDocument(base)
doc=App.newDocument('F14_WING_PIVOT_X_CORRECTION_REVIEW')
# Copy complete current review context
for o in src.Objects:
    sh=getattr(o,'Shape',None)
    if sh and not sh.isNull():
        n=doc.addObject('PartDesign::Feature','CTX_'+o.Name)
        n.Label='CTX | '+o.Label
        n.Shape=sh.copy()
App.closeDocument(src.Name)
leg=App.openDocument(legacy)
wing_names=['WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L','WINGBOX_REF']
for nm in wing_names:
    o=leg.getObject(nm)
    if not o: continue
    sh=o.Shape.copy()
    old=doc.addObject('PartDesign::Feature','OLD_'+nm); old.Label='ALT | '+o.Label; old.Shape=sh
    corr=doc.addObject('PartDesign::Feature','CORR_'+nm); corr.Label='KORR X | '+o.Label
    sh2=sh.copy(); sh2.translate(App.Vector(dx,0,0)); corr.Shape=sh2
# explicit target pivot axis marker
for side,y in [('R',125.20927023775283),('L',-125.20927023775283)]:
    m=doc.addObject('PartDesign::Feature','TARGET_PIVOT_'+side)
    m.Label=f'NADC FS524.16 Sollpivot {side} | X={pivot_target:.3f} mm'
    m.Shape=Part.makeLine(App.Vector(pivot_target,y,-40),App.Vector(pivot_target,y,40))
# old axis marker
for side,y in [('R',125.20927023775283),('L',-125.20927023775283)]:
    m=doc.addObject('PartDesign::Feature','OLD_PIVOT_'+side)
    m.Label=f'Legacy Pivot {side} | X={pivot_legacy:.3f} mm'
    m.Shape=Part.makeLine(App.Vector(pivot_legacy,y,-40),App.Vector(pivot_legacy,y,40))
doc.recompute(); doc.saveAs(out)
sha=hashlib.sha256(open(out,'rb').read()).hexdigest()
a={'status':'WING_PIVOT_X_CORRECTION_REVIEW_ONLY','pivot_source':'NADC FS43.68 model in x12 = FS524.16 full-scale','rc_scale_mm_per_fullscale_in':scale,'legacy_pivot_X_mm':pivot_legacy,'target_pivot_X_mm':pivot_target,'delta_X_mm':dx,'Y_preserved_mm':125.20927023775283,'Z_preserved_mm':0.0,'gates':{'X_correction_candidate_only':True,'Y_verified':False,'Z_verified':False,'glove_fit_verified':False,'master_changed':False,'production_release':False},'output_sha256':sha}
json.dump(a,open(os.path.join(repo,'migration','freecad','freecad_WING_PIVOT_X_CORRECTION_REVIEW_audit.json'),'w',encoding='utf-8'),indent=2,ensure_ascii=False)
print(json.dumps(a,indent=2))
App.closeDocument(doc.Name); App.closeDocument(leg.Name)
