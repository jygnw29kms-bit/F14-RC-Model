import json, math
inv=json.load(open(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/sketchfab_f14d_wing_origins.json',encoding='utf-8'))
scale=inv['scale_mm_per_fbx_unit_for_900_span']
mn=inv['model_bounds_min'];mx=inv['model_bounds_max']
# FBX axes: X lateral, Y longitudinal, nose is min Y, Z vertical
pivot_model_x_mm=125.20927023775282
pivot_nose_rel_mm=504.3463093769572
pivot_fbx_x=pivot_model_x_mm/scale
pivot_fbx_y=mn[1]+pivot_nose_rel_mm/scale
pivot_fbx_z=None
wingL=inv['wings'][0];wingR=inv['wings'][1]
res={'status':'SKETCHFAB_SOURCE_PIVOT_XY_PLAUSIBILITY','scale_mm_per_fbx_unit':scale,'fbx_nose_y':mn[1],'source_pivot_model_mm':{'nose_relative_longitudinal':pivot_nose_rel_mm,'abs_lateral':pivot_model_x_mm},'mapped_pivot_fbx':{'x_abs':pivot_fbx_x,'y':pivot_fbx_y,'z_unregistered':None},'wing_bounds':{'L':{'x': [wingL['bounds_min'][0],wingL['bounds_max'][0]],'y':[wingL['bounds_min'][1],wingL['bounds_max'][1]]},'R':{'x':[wingR['bounds_min'][0],wingR['bounds_max'][0]],'y':[wingR['bounds_min'][1],wingR['bounds_max'][1]]}},'checks':{'mapped_lateral_inside_wing_bbox': wingL['bounds_min'][0] <= pivot_fbx_x <= wingL['bounds_max'][0], 'mapped_longitudinal_inside_wing_bbox': wingL['bounds_min'][1] <= pivot_fbx_y <= wingL['bounds_max'][1]},'limits':['Sketchfab model is visual secondary reference, not dimensional master.','Longitudinal mapping uses FBX nose minimum and span-normalized scale; no production release.','Z intentionally not registered.']}
open(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/sketchfab_f14d_source_pivot_xy_plausibility.json','w',encoding='utf-8').write(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
