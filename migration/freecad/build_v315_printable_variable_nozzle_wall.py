import FreeCAD as App, Part, pathlib, json, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v314_VARIABLE_ELLIPTIC_NOZZLE_CANDIDATE.FCStd'; out=R/'migration/freecad/F14_v315_PRINTABLE_VARIABLE_NOZZLE_WALL.FCStd'; audp=R/'migration/freecad/freecad_v315_printable_variable_nozzle_wall_audit.json'
v314=json.loads((R/'migration/freecad/freecad_v314_variable_elliptic_nozzle_candidate_audit.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v315_PRINTABLE_VARIABLE_NOZZLE_WALL')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull(): q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape; wall=0.8; oml_allow=0.53; FSA=1347.7432483900213
rows=[]; audits=[]
for side,sgn in [('R',1),('L',-1)]:
    wo=[]; wi=[]
    for r in v314['stations']:
        x=r['x_mm']; cy=sgn*r['axis_abs_y_mm']; cz=r['z_center_mm']; oay=r['ay_mm']-oml_allow; oaz=r['az_mm']-oml_allow; iay=oay-wall; iaz=oaz-wall
        po=[]; pi=[]
        for i in range(72):
            t=2*math.pi*i/72; po.append(App.Vector(x,cy+oay*math.cos(t),cz+oaz*math.sin(t))); pi.append(App.Vector(x,cy+iay*math.cos(t),cz+iaz*math.sin(t)))
        po.append(po[0]); pi.append(pi[0]); wo.append(Part.makePolygon(po)); wi.append(Part.makePolygon(pi))
        if side=='R': rows.append({'x_mm':x,'outer_ay_mm':oay,'outer_az_mm':oaz,'inner_ay_mm':iay,'inner_az_mm':iaz,'inner_area_mm2':math.pi*iay*iaz,'inner_area_ratio_to_FSA':math.pi*iay*iaz/FSA})
    outer=Part.makeLoft(wo,True,True); inner=Part.makeLoft(wi,True,True); duct=outer.cut(inner).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V315_NOZZLE_WALL_'+side); o.Shape=duct; o.Label='v315 printable variable nozzle wall '+side
    shell_clear=outer.distToShape(oml.Shells[0])[0] if oml.Shells else 0.0
    audits.append({'side':side,'outer_valid':outer.isValid(),'inner_valid':inner.isValid(),'wall_valid':duct.isValid(),'wall_solid_count':len(duct.Solids),'outer_OML_fraction':outer.common(oml).Volume/outer.Volume,'minimum_outer_to_OML_shell_clearance_mm':shell_clear,'wall_volume_mm3':duct.Volume})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V315_PRINTABLE_VARIABLE_NOZZLE_WALL_CANDIDATE','source_model':src.name,'architecture':{'nominal_wall_mm':wall,'OML_radial_allowance_mm':oml_allow,'material_candidate':'PPA-CF/PETG engineering screen; final material not frozen'},'stations':rows,'sides':audits,'summary':{'minimum_inner_area_ratio_to_FSA':min(r['inner_area_ratio_to_FSA'] for r in rows),'terminal_inner_area_ratio_to_FSA':rows[-1]['inner_area_ratio_to_FSA'],'minimum_measured_outer_to_OML_shell_clearance_mm':min(q['minimum_outer_to_OML_shell_clearance_mm'] for q in audits)},'gates':{'bilateral_wall_valid_single_solids':all(q['wall_valid'] and q['wall_solid_count']==1 for q in audits),'bilateral_outer_OML_containment_ge_0p999':all(q['outer_OML_fraction']>=0.999 for q in audits),'measured_outer_shell_clearance_ge_0p3mm':all(q['minimum_outer_to_OML_shell_clearance_mm']>=0.3 for q in audits),'nominal_wall_ge_0p8mm':wall>=0.8,'minimum_inner_area_ratio_ge_0p80':min(r['inner_area_ratio_to_FSA'] for r in rows)>=0.80,'minimum_inner_area_ratio_ge_0p85':min(r['inner_area_ratio_to_FSA'] for r in rows)>=0.85,'slicer_verified':False,'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))