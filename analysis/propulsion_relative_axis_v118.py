import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
src=root/'analysis'/'propulsion_sources_v113'
v116=json.loads((root/'analysis/propulsion_common_axis_v116.json').read_text())
Ereg=json.loads((src/'upc_E_registration_v44.json').read_text()); Freg=json.loads((src/'upc_F_registration_v12.json').read_text())
# Same source image; derive scale from independently registered E-F station x difference.
xE=648.8863542888724; xF=754.962281164333
pxE=1663.3586234059521; pxF=Freg['candidate_F_station_x_pixel']
scale=(xF-xE)/(pxF-pxE)
yE=next(x for x in v116['sections'] if x['section']=='E')['optimal_abs_y_mm']; yF=next(x for x in v116['sections'] if x['section']=='F')['optimal_abs_y_mm']
zpixE=Ereg['candidate_axis_side_pixel_y']; zpixF=Freg['registered_candidate_section_axis_side_pixel_y']
dx=xF-xE; dy=yF-yE; dz=(zpixE-zpixF)*scale # image y down, so smaller pixel y is upward
length=math.sqrt(dx*dx+dy*dy+dz*dz); ux,uy,uz=dx/length,dy/length,dz/length
housing_len=73.5
end={'x_mm':xE+ux*housing_len,'abs_y_mm':yE+uy*housing_len,'relative_z_from_E_mm':uz*housing_len}
out={'status':'V118_RELATIVE_3D_EDF_AXIS_CANDIDATE','source_image_sha256_E':Ereg['source_image_sha256'],'source_image_sha256_F':Freg['source_image_sha256'],'same_side_source_image':Ereg['source_image_sha256']==Freg['source_image_sha256'],'registration_scale_from_EF_x_mm_per_pixel':scale,'E':{'x_mm':xE,'optimal_abs_y_mm':yE,'axis_side_pixel_y':zpixE,'relative_z_mm':0.0},'F':{'x_mm':xF,'optimal_abs_y_mm':yF,'axis_side_pixel_y':zpixF,'relative_z_mm':dz},'relative_axis':{'delta_x_mm':dx,'delta_y_mm':dy,'delta_z_mm':dz,'yaw_deg':math.degrees(math.atan2(dy,dx)),'pitch_deg':math.degrees(math.atan2(dz,math.hypot(dx,dy))),'unit_vector':[ux,uy,uz]},'73p5mm_housing_if_started_at_E':{'start':{'x_mm':xE,'abs_y_mm':yE,'relative_z_mm':0},'end':end},'interpretation':'Relative E-F slope is usable as a packaging candidate because E and F are registered on the same side-view image. Absolute aircraft Z/waterline remains unverified and must be anchored before CAD release.','limitations':['E/F metric registrations remain candidates, not production lofts','absolute Z datum is not verified','no source cross section exists at the 73.5 mm housing aft endpoint','continuous polygon clearance along the tilted axis is not verified'],'release':{'relative_axis_candidate':True,'absolute_axis_CAD_ready':False,'continuous_3D_clearance_verified':False,'propulsion_packaging_freeze':False,'flight_release':False}}
(root/'analysis/propulsion_relative_axis_v118.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out['relative_axis'],indent=2)); print(json.dumps(end,indent=2))