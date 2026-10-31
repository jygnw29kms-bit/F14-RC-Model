import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd'; out=R/'migration/freecad/F14_v283_LIGHT_STABILATOR_ROOT_FITTING.FCStd'; audp=R/'migration/freecad/freecad_v283_light_stabilator_root_fitting_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v283_LIGHT_STABILATOR_ROOT_FITTING')
for o in d.Objects:
    if o.Name.startswith('V235_D_ROOT_FITTING_'): continue
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=736.0078983334656; rows=[]; total=0.0
def d_bore(y0,y1,sgn,r,flat_x):
    cyl=Part.makeCylinder(r,abs(y1-y0),App.Vector(px,sgn*y0,0),App.Vector(0,sgn,0)); lo=px-r-1; hi=px+flat_x; ya=min(sgn*y0,sgn*y1)-1; yb=max(sgn*y0,sgn*y1)+1; clip=Part.makeBox(hi-lo,yb-ya,2*r+2,App.Vector(lo,ya,-r-1)); return cyl.common(clip)
for lab,sgn in [('R',1),('L',-1)]:
    # 24 mm long annular hub around 6 mm D-shaft, outer radius 6.5 mm.
    hub=Part.makeCylinder(6.5,24,App.Vector(px,sgn*82,0),App.Vector(0,sgn,0))
    bore=d_bore(82,106,sgn,3.05,2.45); hub=hub.cut(bore)
    # 36 x 31 x 3.5 mm tongue envelope retained, center opened leaving 4 mm perimeter bond frame.
    y0=104 if sgn>0 else -135
    outer=Part.makeBox(36,31,3.5,App.Vector(px-18,y0,-1.75))
    iy0=108 if sgn>0 else -131
    inner=Part.makeBox(28,23,5.5,App.Vector(px-14,iy0,-2.75))
    frame=outer.cut(inner)
    fit=hub.fuse(frame).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V283_LIGHT_D_ROOT_FITTING_'+lab); o.Shape=fit; o.Label='v283 light D-bore stabilator root fitting '+lab
    shaft=doc.getObject('V237_D_SHAFT_'+lab).Shape; stab=doc.getObject('STABILATOR_'+lab).Shape; servo=doc.getObject('V233_TORQ_SERVICE_'+lab).Shape; crank=doc.getObject('V241_LIGHT_D_CRANK_'+lab).Shape
    frame_cont=frame.common(stab).Volume/frame.Volume if frame.Volume else 0
    mg=fit.Volume/1000*1.25; total+=mg
    rows.append({'side':lab,'valid':fit.isValid(),'solid_count':len(fit.Solids),'volume_cm3':fit.Volume/1000,'PPA_CF_mass_g':mg,'shaft_intersection_mm3':fit.common(shaft).Volume,'frame_stabilator_containment':frame_cont,'to_servo_service_mm':fit.distToShape(servo)[0],'to_light_crank_mm':fit.distToShape(crank)[0]})
doc.recompute(); doc.saveAs(str(out))
old_pair=22.0805902347973; aud={'status':'V283_LIGHT_STABILATOR_ROOT_FITTING','source':src.name,'geometry':{'hub_outer_radius_mm':6.5,'hub_length_mm':24,'D_bore_radius_mm':3.05,'tongue_outer_mm':[36,31,3.5],'tongue_window_mm':[28,23],'frame_border_mm':4},'rows':rows,'mass':{'pair_PPA_CF_g':total,'v235_pair_PPA_CF_g':old_pair,'saving_g':old_pair-total},'gates':{'both_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'no_shaft_intersection':all(r['shaft_intersection_mm3']<1e-6 for r in rows),'frame_contained_in_stabilator_ge_0p999':all(r['frame_stabilator_containment']>0.999 for r in rows),'servo_clearance_positive':all(r['to_servo_service_mm']>0 for r in rows),'crank_clearance_nonnegative':all(r['to_light_crank_mm']>=0 for r in rows),'bond_area_reduction_requires_coupon':True,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
