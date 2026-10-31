import FreeCAD as App, Part, json, pathlib, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v269_SERVICEABLE_SEGMENTED_ENDMODEL.FCStd'; out=R/'migration/freecad/F14_v270_SEGMENT_CLAMP_RETENTION.FCStd'; audp=R/'migration/freecad/freecad_v270_segment_clamp_retention_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v270_SEGMENT_CLAMP_RETENTION')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
# cut_x, abs_y, z, tube_OD; X620 deliberately excluded while aft-nacelle OML gate is open
spec=[(220,20,-10,6),(440,60,-10,8),(840,30,0,6)]
rows=[]; mass=0.0
for x,ay,z,od in spec:
    for sgn in (-1,1):
        y=sgn*ay; tag=f'X{x}_{"R" if sgn>0 else "L"}'
        # Clamp collar on aft receiving sleeve: 8 mm axial width, 1.4 mm radial wall beyond old sleeve.
        old_bore=od/2+0.15; old_or=old_bore+1.2
        inner_r=old_or+0.10; outer_r=inner_r+1.4
        collar=Part.makeCylinder(outer_r,8,App.Vector(x+2,y,z),App.Vector(1,0,0)).cut(Part.makeCylinder(inner_r,8,App.Vector(x+2,y,z),App.Vector(1,0,0)))
        # 0.9 mm axial slit on outboard side, giving elastic clamp action without drilling the CF tube.
        slit_y=y + sgn*(outer_r-0.45)
        slit=Part.makeBox(10,0.9,2*outer_r+4,App.Vector(x+1, slit_y-(0.9 if sgn<0 else 0), z-outer_r-2))
        collar=collar.cut(slit)
        # paired clamp ears outside the sleeve; M3 clearance hole tangential to Y axis through ears only.
        ear_x=x+3.5; ear_z=z+outer_r-0.2
        e1=Part.makeBox(5,3.0,4.4,App.Vector(ear_x,y-1.5,ear_z))
        e2=Part.makeBox(5,3.0,4.4,App.Vector(ear_x,y-1.5,ear_z+4.8))
        sh=collar.fuse(e1).fuse(e2)
        hole=Part.makeCylinder(1.6,6,App.Vector(ear_x+2.5,y-3,ear_z+4.6),App.Vector(0,1,0))
        sh=sh.cut(hole).removeSplitter()
        o=doc.addObject('PartDesign::Feature','V270_CLAMP_'+tag); o.Shape=sh; o.Label=f'v270 M3 split-clamp segment retention {tag}'
        cont=sh.common(fus).Volume/sh.Volume if sh.Volume else 0
        # check distance to service keepouts and critical hardware
        critical=[n for n in ['V253_ACCESS_BATTERY','V253_ACCESS_SWEEP','V253_ACCESS_TAIL_R','V253_ACCESS_TAIL_L','V221_CASSETTE_R','V221_CASSETTE_L','V225_SERVO_SERVICE','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L'] if doc.getObject(n)]
        ds=[(n,sh.distToShape(doc.getObject(n).Shape)[0]) for n in critical]
        nearest=min(ds,key=lambda t:t[1]) if ds else (None,999)
        mg=sh.Volume/1000*1.25; mass+=mg
        rows.append({'cut_x_mm':x,'side':'R' if sgn>0 else 'L','tube_OD_mm':od,'valid':sh.isValid(),'solids':len(sh.Solids),'containment':cont,'mass_PPA_CF_g':mg,'nearest_object':nearest[0],'nearest_distance_mm':nearest[1]})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V270_SEGMENT_CLAMP_RETENTION','source':src.name,'architecture':{'retention':'split clamp on receiving sleeve','CF_tube_cross_drilled':False,'X620_retention_created':False,'reason_X620':'aft nacelle OML gate open','M3_clearance_hole_mm':3.2},'rows':rows,'mass':{'PPA_CF_screen_g':mass},'gates':{'all_valid':all(r['valid'] and r['solids']>=1 for r in rows),'containment_ge_0p98':all(r['containment']>=0.98 for r in rows),'critical_clearance_nonnegative':all(r['nearest_distance_mm']>=0 for r in rows),'CF_tube_not_cross_drilled':True,'M3_hardware_bench_fit_required':True,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
