import FreeCAD as App, Part, os, json, hashlib
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
src=App.openDocument(os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'))
g=App.openDocument(os.path.join(BASE,'migration','freecad','F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'))
out=App.newDocument('F14_v195_GLOVE_TOP_OVERLAY')
def cp(srcobj,name,label):
 o=out.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=srcobj.Shape.copy(); return o
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L','WINGBOX_REF']:
 o=src.getObject(n)
 if o: cp(o,n,n)
for o in g.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): cp(o,'GUIDE_'+o.Name,'GLOVE GUIDE '+o.Label)
# Add X gap marker between guide aft and wing forward bounds, both sides near y=140
xg=457.354009651243; xw=479.4839172711096
for y,lab in [(142,'R'),(-142,'L')]:
 sh=Part.makeLine(App.Vector(xg,y,0),App.Vector(xw,y,0)); o=out.addObject('PartDesign::Feature','GAP_'+lab); o.Label=f'Projected X gap guide->wing {xw-xg:.3f} mm'; o.Shape=sh
# pivot center markers
px=504.3463093769572; py=125.20927023775282
for y,lab in [(py,'R'),(-py,'L')]:
 sh=Part.makeCylinder(3,6,App.Vector(px,y,-3)); o=out.addObject('PartDesign::Feature','PIVOT_CENTER_'+lab); o.Label='Source-backed pivot FS/BL center'; o.Shape=sh
out.recompute(); path=os.path.join(BASE,'migration','freecad','F14_v195_GLOVE_TOP_OVERLAY.FCStd'); out.saveAs(path)
a={'status':'V195_GLOVE_TOP_OVERLAY_REVIEW','guide_aft_x_mm':xg,'wing_forward_x_mm':xw,'projected_x_gap_mm':xw-xg,'pivot_x_mm':px,'pivot_abs_y_mm':py,'gates':{'guide_projection_only':True,'Y_source_backed':True,'Z_verified':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(open(path,'rb').read()).hexdigest()}
with open(os.path.join(BASE,'migration','freecad','freecad_v195_glove_top_overlay_audit.json'),'w') as fh: json.dump(a,fh,indent=2)
print(json.dumps(a,indent=2))
