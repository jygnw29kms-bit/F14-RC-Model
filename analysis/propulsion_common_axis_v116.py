import json, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v113=json.loads((root/'analysis/propulsion_local_packaging_v113.json').read_text())
srcdir=root/'analysis'/'propulsion_sources_v113'
base=json.loads((srcdir/'upc_source_section_candidates_v07.json').read_text())
common_scale=868.496683861459/(1048*2113/1344)
req_radius=52.5/2+0.8+0.75
rows=[]
for rec in v113['sections']:
    name=rec['section']; source=next(s for s in base['profiles'] if s['name']==('F_R' if name=='F' else name))
    axis=float(source['source_section_axis_pixel'][0]); left,right=rec['optimal_centers_pixels']; off_px=(right[0]-left[0])/2
    scale=common_scale*rec['isotropic_factor']; y=off_px*scale
    available_r=rec['available_disk_diameter_mm']/2
    margin=available_r-req_radius
    rows.append({'section':name,'x_mm':rec['x_mm'],'optimal_abs_y_mm':y,'source_offset_px':off_px,'section_mm_per_px':scale,'available_radius_mm':available_r,'required_radius_mm':req_radius,'radial_center_tolerance_mm':margin,'feasible_abs_y_interval_mm':[y-margin,y+margin] if margin>=0 else None})
E=next(x for x in rows if x['section']=='E'); F=next(x for x in rows if x['section']=='F')
lo=max(E['feasible_abs_y_interval_mm'][0],F['feasible_abs_y_interval_mm'][0]); hi=min(E['feasible_abs_y_interval_mm'][1],F['feasible_abs_y_interval_mm'][1]); overlap=max(0,hi-lo)
out={'status':'V116_E_F_COMMON_LATERAL_AXIS_SCREEN','source_v113':'analysis/propulsion_local_packaging_v113.json','candidate':{'shroud_od_mm':52.5,'skin_mm':0.8,'radial_service_mm':0.75,'required_radius_to_source_contour_mm':req_radius},'sections':rows,'E_F':{'optimal_center_shift_mm':F['optimal_abs_y_mm']-E['optimal_abs_y_mm'],'axial_distance_mm':F['x_mm']-E['x_mm'],'optimal_centerline_slope_deg_approx':__import__('math').degrees(__import__('math').atan2(F['optimal_abs_y_mm']-E['optimal_abs_y_mm'],F['x_mm']-E['x_mm'])),'common_lateral_axis_interval_mm':[lo,hi] if overlap>0 else None,'common_axis_interval_width_mm':overlap,'nominal_common_abs_y_mm':(lo+hi)/2 if overlap>0 else None,'lateral_common_axis_pass':overlap>0},'limitations':['only lateral coordinate is cross-source comparable in this screen','vertical center registration remains unverified','interval assumes each sampled disk is locally valid around its optimum by radial-margin translation; exact polygon must be retested at chosen common center','continuous sections between E and F remain unmeasured'],'release':{'lateral_axis_candidate':overlap>0,'vertical_axis_candidate':False,'continuous_3D_axis_verified':False,'propulsion_packaging_freeze':False,'flight_release':False}}
(root/'analysis/propulsion_common_axis_v116.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['E_F'],indent=2))