import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v269_SERVICEABLE_SEGMENTED_ENDMODEL.FCStd'; out=R/'migration/freecad/F14_v271_C_RING_SEGMENT_RETENTION.FCStd'; audp=R/'migration/freecad/freecad_v271_c_ring_segment_retention_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v271_C_RING_SEGMENT_RETENTION')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
spec=[(220,20,-10,6),(440,60,-10,8),(840,30,0,6)]
rows=[]; mass=0.0
for x,ay,z,od in spec:
  for sgn in (-1,1):
    y=sgn*ay; tag=f'X{x}_{"R" if sgn>0 else "L"}'
    bore=od/2+0.15; sleeve_or=bore+1.2; ir=sleeve_or+0.10; orr=ir+1.15; w=7.0
    ring=Part.makeCylinder(orr,w,App.Vector(x+2,y,z),App.Vector(1,0,0)).cut(Part.makeCylinder(ir,w,App.Vector(x+2,y,z),App.Vector(1,0,0)))
    slit=Part.makeBox(w+2,1.0,orr-ir+3.0,App.Vector(x+1,y-0.5,z+ir-0.5))
    ring=ring.cut(slit)
    lugz=z+ir-1.0
    lug1=Part.makeBox(5.0,2.4,4.4,App.Vector(x+3,y-3.1,lugz))
    lug2=Part.makeBox(5.0,2.4,4.4,App.Vector(x+3,y+0.7,lugz))
    sh=ring.fuse(lug1).fuse(lug2)
    hole=Part.makeCylinder(1.55,8.0,App.Vector(x+5.5,y-4.0,lugz+2.2),App.Vector(0,1,0))
    sh=sh.cut(hole).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V271_C_CLAMP_'+tag); o.Shape=sh; o.Label=f'v271 C-ring M3 segment clamp {tag}'
    cont=sh.common(fus).Volume/sh.Volume if sh.Volume else 0
    mg=sh.Volume/1000*1.25; mass+=mg
    rows.append({'cut_x_mm':x,'side':'R' if sgn>0 else 'L','valid':sh.isValid(),'solid_count':len(sh.Solids),'containment':cont,'mass_PPA_CF_g':mg,'outer_radius_mm':orr,'axial_width_mm':w,'slit_mm':1.0,'M3_clearance_mm':3.1})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V271_C_RING_SEGMENT_RETENTION','source':src.name,'architecture':{'receiving_sleeve_C_clamp':True,'CF_tube_cross_drilled':False,'X620_excluded':True,'M3_clamp_screw':True},'rows':rows,'mass':{'PPA_CF_screen_g':mass},'gates':{'all_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'containment_ge_0p98':all(r['containment']>=0.98 for r in rows),'mass_lt_3p5g':mass<3.5,'bench_clamp_force_test_required':True,'thread_insert_or_nut_detail_open':True,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
