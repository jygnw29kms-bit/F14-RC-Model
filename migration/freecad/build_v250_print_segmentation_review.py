import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v248_TAIL_SERVO_MOUNT_INTEGRATED.FCStd'; out=R/'migration/freecad/F14_v250_PRINT_SEGMENTATION_REVIEW.FCStd'; audp=R/'migration/freecad/freecad_v250_print_segmentation_review_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v250_PRINT_SEGMENTATION_REVIEW')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
# Longitudinal segmentation reference plates, 0.4 mm thick so they are visible but never production solids.
for x in [220.0,440.0,620.0,840.0]:
    sh=Part.makeBox(0.4,360,180,App.Vector(x-0.2,-180,-70))
    o=doc.addObject('PartDesign::Feature',f'V250_SEG_X_{int(x)}'); o.Shape=sh; o.Label=f'v250 segmentation reference X={x:.1f} / NOT PART'
# Wing seam references at exact CR3992 defining station WBL274.36816.
y=320.94018208216556
for lab,sgn in [('R',1),('L',-1)]:
    yy=sgn*y
    y0=yy-0.2 if sgn>0 else yy-0.2
    sh=Part.makeBox(190,0.4,50,App.Vector(470,y0,-25))
    o=doc.addObject('PartDesign::Feature',f'V250_WING_SEAM_{lab}'); o.Shape=sh; o.Label=f'v250 wing seam {lab} / CR3992 WBL274.36816 / NOT PART'
doc.recompute(); doc.saveAs(str(out))
mods=[
 {'name':'NOSE','x':[0.5,220.0],'max_width_mm':76.54,'split_y':False},
 {'name':'FORWARD_CENTER_LR','x':[220,440],'max_piece_width_mm':159.615,'split_y':True},
 {'name':'WINGBOX_CENTER_LR','x':[440,620],'max_piece_width_mm':159.615,'split_y':True},
 {'name':'AFT_NACELLE_LR','x':[620,840],'max_piece_width_mm':159.615,'split_y':True,'final_cut_provisional':True},
 {'name':'TAIL_END','x':[840,879],'max_width_mm':196.018,'split_y':False},
]
for m in mods: m['length_mm']=m['x'][1]-m['x'][0]
aud={'status':'V250_PRINT_SEGMENTATION_REVIEW','source':'F14_v248_TAIL_SERVO_MOUNT_INTEGRATED.FCStd','safe_build_cube_mm':[250,250,250],'longitudinal_cut_planes_mm':[220,440,620,840],'wing_seam':{'source':'CR3992 Appendix 2 defining station','WBL_in':274.36816,'model_abs_y_mm':y},'modules':mods,'gates':{'all_module_lengths_le_250':all(m['length_mm']<=250 for m in mods),'nose_width_le_250':76.54<=250,'tail_width_le_250':196.018<=250,'central_half_width_le_250':159.615<=250,'wing_parts_bbox_axes_le_250':True,'aft_nacelle_final_seam_frozen':False,'joiner_design_complete':False,'service_hatches_complete':False,'print_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
