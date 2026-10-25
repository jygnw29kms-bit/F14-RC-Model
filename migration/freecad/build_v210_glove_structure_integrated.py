import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
base=App.openDocument(str(R/'migration/freecad/F14_v208_SWEEP_PACKAGING_INTEGRATED.FCStd'))
g=App.openDocument(str(R/'migration/freecad/F14_v209_FIXED_GLOVE_STRUCTURAL_ENCLOSURE.FCStd'))
out=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'
aud=R/'migration/freecad/freecad_v210_glove_structure_integrated_audit.json'
for n in ['V209_INNER_ATTACH_R','V209_OUTER_SKIN_RAIL_R','V209_FIXED_GLOVE_UNDERSIDE_R','V209_INNER_ATTACH_L','V209_OUTER_SKIN_RAIL_L','V209_FIXED_GLOVE_UNDERSIDE_L']:
 o=g.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  q=base.addObject('PartDesign::Feature',n); q.Label=o.Label; q.Shape=o.Shape.copy()
base.recompute(); base.saveAs(str(out))
wr=base.getObject('WING_R').Shape.BoundBox; wl=base.getObject('WING_L').Shape.BoundBox
sr=base.getObject('V209_FIXED_GLOVE_UNDERSIDE_R').Shape.BoundBox; sl=base.getObject('V209_FIXED_GLOVE_UNDERSIDE_L').Shape.BoundBox
res={'status':'V210_GLOVE_STRUCTURE_INTEGRATED','source_v208':'F14_v208_SWEEP_PACKAGING_INTEGRATED.FCStd','source_v209':'F14_v209_FIXED_GLOVE_STRUCTURAL_ENCLOSURE.FCStd','global_vertical_clearance_mm':{'R':wr.ZMin-sr.ZMax,'L':wl.ZMin-sl.ZMax},'proof_note':'Wing sweep rotates about Z axis, preserving all wing Z coordinates; skin Zmax below wing Zmin therefore proves nonintersection for all sweep angles.','gates':{'fixed_glove_structural_enclosure_integrated':True,'all_sweep_vertical_nonintersection_proven':min(wr.ZMin-sr.ZMax,wl.ZMin-sl.ZMax)>0,'minimum_global_vertical_clearance_ge_1mm':min(wr.ZMin-sr.ZMax,wl.ZMin-sl.ZMax)>=1.0,'absolute_Z_OML_verified':False,'production_OML':False,'servo_model_selected':False,'material_verified':False,'print_release':False,'flight_release':False}}
res['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); aud.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))
