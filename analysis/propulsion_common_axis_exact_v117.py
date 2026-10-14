import json, math, pathlib, importlib.util
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v113=json.loads((root/'analysis/propulsion_local_packaging_v113.json').read_text()); v116=json.loads((root/'analysis/propulsion_common_axis_v116.json').read_text())
srcdir=root/'analysis'/'propulsion_sources_v113'; base=json.loads((srcdir/'upc_source_section_candidates_v07.json').read_text())
spec=importlib.util.spec_from_file_location('vc',srcdir/'validate_source_contours.py'); vc=importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
def dist(p,a,b):
 px,py=p; ax,ay=a; bx,by=b; vx=bx-ax; vy=by-ay; vv=vx*vx+vy*vy
 if vv==0:return math.hypot(px-ax,py-ay)
 t=max(0,min(1,((px-ax)*vx+(py-ay)*vy)/vv)); q=(ax+t*vx,ay+t*vy); return math.hypot(px-q[0],py-q[1])
def radius(c,poly):
 if not vc.strictly_inside(c,poly):return 0
 return min(dist(c,a,b) for a,b in vc.edges(poly))
common_y=v116['E_F']['nominal_common_abs_y_mm']; req=v116['candidate']['required_radius_to_source_contour_mm']
common_scale=868.496683861459/(1048*2113/1344)
files={'E':'upc_E_source_contour_v43.json','F':'upc_F_connected_section_v11.json'}
rows=[]
for name in ('E','F'):
 rec=next(x for x in v113['sections'] if x['section']==name); source=next(s for s in base['profiles'] if s['name']==('F_R' if name=='F' else name)); poly=json.loads((srcdir/files[name]).read_text())['pixel_outline']
 scale=common_scale*rec['isotropic_factor']; axis=float(source['source_section_axis_pixel'][0]); off=common_y/scale; z=rec['optimal_centers_pixels'][0][1]
 left=(axis-off,z); right=(axis+off,z); rp=min(radius(left,poly),radius(right,poly),off); rmm=rp*scale
 rows.append({'section':name,'common_abs_y_mm':common_y,'pixel_offset_for_common_y':off,'retained_local_optimum_z_pixel':z,'available_radius_at_exact_common_y_mm':rmm,'required_radius_mm':req,'radial_margin_mm':rmm-req,'exact_common_lateral_center_pass':rmm>=req})
out={'status':'V117_EXACT_COMMON_LATERAL_CENTER_LOCAL_POLYGON_CHECK','source_v116':'analysis/propulsion_common_axis_v116.json','common_abs_y_mm':common_y,'sections':rows,'pass':all(x['exact_common_lateral_center_pass'] for x in rows),'limitations':['vertical centers remain independently optimized and not registered to one aircraft Z axis','no intermediate E-F source contours; continuous axial envelope still unproven'],'release':{'exact_E_F_lateral_center_local_pass':all(x['exact_common_lateral_center_pass'] for x in rows),'common_vertical_axis_verified':False,'continuous_3D_axis_verified':False,'propulsion_packaging_freeze':False,'flight_release':False}}
(root/'analysis/propulsion_common_axis_exact_v117.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))