import json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
shift=187.59240693460868
xshift=-108.78608120432557
res={
 'status':'V246_CR3992_WING_WL_TRANSFORM_GATE',
 'source':'NASA CR-3992 Appendix 2 / Grumman basic F-14 wing',
 'source_mapping':'WL = reference_vertical_wl_in + y/c * chord; scale 1.1697428086486623 mm/in',
 'direct_root_LE_check':{'WBL_in':127.23,'reference_vertical_wl_in':159.93018,'LE_yc':0.00756,'chord_in':126.46470,'absolute_LE_WL_in':160.886253132,'absolute_LE_Z_model_mm':188.19553761158534,'current_local_LE_Z_mm':0.603130676976662,'derived_sourceWL_to_localZ_shift_mm':shift},
 'cad_transform_verification':{'v190_wing_z_bounds_mm':[175.16714742841788,196.6867869631904],'v244_wing_z_bounds_mm':[-12.425259506190798,9.094380028581725],'z_delta_min_mm':shift,'z_delta_max_mm':shift,'constant_z_translation_verified':True,'v244_minus_v190_x_translation_mm':xshift,'shape_not_rescaled_or_relofted_by_v191_v195':True},
 'v245_note':'Nearest-vertex checks at intermediate loft stations are invalid because Part.makeLoft does not expose defining intermediate wires as exterior topology vertices. v245 is diagnostic only and superseded by this transform proof.',
 'gates':{'CR3992_absolute_wing_WL_traceable':True,'wing_local_to_source_WL_constant_transform_verified':True,'pivot_axis_absolute_WL_verified':False,'fuselage_absolute_WL_registered':False,'common_fuselage_wing_absolute_Z_verified':False,'production_OML':False,'flight_release':False}
}
(R/'analysis/v246_cr3992_wing_wl_transform_gate.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))