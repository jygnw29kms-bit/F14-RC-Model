import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v256_CONSOLIDATED_JOINER_STATE.FCStd'))
scale=1.1697428086486623; shift_z=187.59240693460868; fs0=93.0
wbl=274.36816; seam_y=wbl*scale; fs=580.24175; wl=156.6950322115
x=(fs-fs0)*scale; z=wl*scale-shift_z
rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 wing=d.getObject('WING_'+lab).Shape
 y0=sgn*(seam_y-30) if sgn>0 else sgn*(seam_y+30)
 # build consistently from inboard to outboard along sign direction
 start=App.Vector(x,sgn*(seam_y-30),z); axis=App.Vector(0,sgn,0)
 outer=Part.makeCylinder(3.0,60,start,axis); bore=Part.makeCylinder(2.0,60,start,axis); tube=outer.cut(bore)
 frac=outer.common(wing).Volume/outer.Volume
 cavity=Part.makeCylinder(3.15,60,start,axis); cfrac=cavity.common(wing).Volume/cavity.Volume
 rows.append({'side':lab,'x_mm':x,'seam_abs_y_mm':seam_y,'z_mm':z,'tube_length_mm':60,'OD_ID_mm':[6,4],'outer_containment_fraction':frac,'6p3mm_bond_cavity_containment_fraction':cfrac,'tube_volume_cm3':tube.Volume/1000.0})
out={'status':'V257_WING_SEGMENT_CF_JOINER_SCREEN','source_station':{'WBL_in':wbl,'model_abs_y_mm':seam_y,'local_circle_center_fs_in':fs,'local_circle_center_wl_in':wl,'current_local_x_mm':x,'current_local_z_mm':z,'v10_local_max_tube_od_mm':6.782904640047178},'rows':rows,'architecture':{'tube':'6x4 CF','embed_each_side_mm':30,'bond_cavity_diameter_mm':6.3,'printed_external_sleeve_not_used_due_local_thickness_limit':True},'gates':{'6mm_tube_full_length_containment_ge_0p995':all(r['outer_containment_fraction']>=0.995 for r in rows),'6p3mm_bond_cavity_full_length_containment_ge_0p995':all(r['6p3mm_bond_cavity_containment_fraction']>=0.995 for r in rows),'adhesive_system_selected':False,'continuous_spar_load_transfer_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
(R/'analysis/v257_wing_segment_cf_joiner_screen.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))