import FreeCAD as App, Part, json, pathlib, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v288_X440_CLAMP_TOOL_ACCESS.FCStd'; out=R/'migration/freecad/F14_v293_X620_INTERNAL_JOINER_CANDIDATE.FCStd'; audp=R/'migration/freecad/freecad_v293_x620_internal_joiner_candidate_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v293_X620_INTERNAL_JOINER_CANDIDATE')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
crit=['V229_ESC_SERVICE_R','V229_ESC_SERVICE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V221_CASSETTE_R','V221_CASSETTE_L']
rows=[]; sleeve_vol=0; tube_vol=0
for sgn,lab in [(-1,'L'),(1,'R')]:
    x=620; y=sgn*25; z=0; od=8; id_=6; hl=40
    outer=Part.makeCylinder(od/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); inner=Part.makeCylinder(id_/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); tube=outer.cut(inner).removeSplitter()
    to=doc.addObject('PartDesign::Feature',f'V293_X620_CF_TUBE_{lab}'); to.Shape=tube; to.Label=f'v293 X620 8x6 CF internal joiner {lab} / OML-independent candidate'
    tube_vol += tube.Volume
    bore_r=od/2+0.15; so_r=bore_r+1.2; sleeve_names=[]
    for side,start in [('FWD',x-20),('AFT',x)]:
        so=Part.makeCylinder(so_r,20,App.Vector(start,y,z),App.Vector(1,0,0)); bi=Part.makeCylinder(bore_r,20,App.Vector(start,y,z),App.Vector(1,0,0)); sl=so.cut(bi).removeSplitter(); sleeve_vol+=sl.Volume
        o=doc.addObject('PartDesign::Feature',f'V293_X620_SLEEVE_{lab}_{side}'); o.Shape=sl; o.Label=f'v293 X620 PPA-CF sleeve {lab} {side}'
        sleeve_names.append(o.Name)
    distances={}
    for n in crit:
        ob=doc.getObject(n)
        if ob: distances[n]=tube.distToShape(ob.Shape)[0]
    rows.append({'side':lab,'tube_valid':tube.isValid(),'tube_containment':outer.common(fus).Volume/outer.Volume,'sleeve_outer_containment':Part.makeCylinder(so_r,40,App.Vector(x-20,y,z),App.Vector(1,0,0)).common(fus).Volume/Part.makeCylinder(so_r,40,App.Vector(x-20,y,z),App.Vector(1,0,0)).Volume,'min_critical_hw_distance_mm':min(distances.values()) if distances else None,'critical_distances_mm':distances,'sleeves':sleeve_names})
doc.recompute(); doc.saveAs(str(out))
tube_cm3=tube_vol/1000; sleeve_cm3=sleeve_vol/1000
aud={'status':'V293_X620_INTERNAL_JOINER_CANDIDATE','source':src.name,'geometry':{'station_x_mm':620,'positions_abs_y_mm':25,'z_mm':0,'tube_OD_ID_mm':[8,6],'tube_length_mm':80,'embed_each_side_mm':40,'sleeve_length_each_side_mm':20,'radial_clearance_mm':0.15,'sleeve_wall_mm':1.2},'rows':rows,'mass_screen':{'CF_tube_volume_cm3':tube_cm3,'CF_tube_density_g_cm3':[1.3,1.5],'CF_tube_mass_range_g':[tube_cm3*1.3,tube_cm3*1.5],'PPA_CF_sleeve_mass_g':sleeve_cm3*1.25,'combined_mass_range_g':[tube_cm3*1.3+sleeve_cm3*1.25,tube_cm3*1.5+sleeve_cm3*1.25]},'architecture':{'internal_joiner_geometry_can_be_prepared_without_outer_OML':True,'retention_and_shell_access_remain_open':True,'outer_shell_cut_created':False},'gates':{'both_tubes_valid':all(r['tube_valid'] for r in rows),'tube_containment_ge_0p995':all(r['tube_containment']>=0.995 for r in rows),'sleeve_containment_ge_0p995':all(r['sleeve_outer_containment']>=0.995 for r in rows),'critical_hw_clearance_ge_10mm':all(r['min_critical_hw_distance_mm']>=10 for r in rows),'X620_retention_defined':False,'aft_nacelle_OML_registered':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
