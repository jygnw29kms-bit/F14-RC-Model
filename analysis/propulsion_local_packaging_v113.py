import json, math, hashlib, pathlib, importlib.util
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
folder=root/'analysis'/'propulsion_sources_v113'
spec=importlib.util.spec_from_file_location('vc',folder/'validate_source_contours.py'); vc=importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
def _distance(p,a,b):
    px,py=p; ax,ay=a; bx,by=b; vx=bx-ax; vy=by-ay; vv=vx*vx+vy*vy
    if vv==0: return math.hypot(px-ax,py-ay)
    t=max(0.0,min(1.0,((px-ax)*vx+(py-ay)*vy)/vv)); qx=ax+t*vx; qy=ay+t*vy
    return math.hypot(px-qx,py-qy)
def disk_radius(center,polygon):
    if not vc.strictly_inside(center,polygon): return 0.0
    return min(_distance(center,a,b) for a,b in vc.edges(polygon))
base=json.loads((folder/'upc_source_section_candidates_v07.json').read_text())
corrected_d=json.loads((folder/'upc_D_source_contour_v49.json').read_text()); d_fit=json.loads((folder/'upc_D_registration_v50.json').read_text())
corrected_e=json.loads((folder/'upc_E_source_contour_v43.json').read_text()); e_fit=json.loads((folder/'upc_E_registration_v44.json').read_text())
corrected_f=json.loads((folder/'upc_F_connected_section_v11.json').read_text()); de=json.loads((folder/'upc_DE_registration_v12.json').read_text()); f_fit=json.loads((folder/'upc_F_registration_v12.json').read_text())
common_scale=868.496683861459/(1048*2113/1344)
housing=52.5; radial_service=0.75; skin=0.8; required=housing+2*(skin+radial_service)
results=[]
for name in ['D','E','F']:
    source=next(s for s in base['profiles'] if s['name']==('F_R' if name=='F' else name))
    polygon=(corrected_f['pixel_outline'] if name=='F' else corrected_e['pixel_outline'] if name=='E' else corrected_d['pixel_outline'])
    axis=source['source_section_axis_pixel'][0]
    fit=(f_fit['isotropic_section_width_multiplier'] if name=='F' else next(s for s in de['sections'] if s['name']==name)['isotropic_multiplier'])
    if name=='E':fit=e_fit['isotropic_multiplier']
    if name=='D':fit=d_fit['isotropic_multiplier']
    half=(max(p[0] for p in polygon)-min(p[0] for p in polygon))/2
    lo,hi=int(min(p[1] for p in polygon)),math.ceil(max(p[1] for p in polygon))
    best=(0,None,None)
    for offset in range(math.floor(half*.35),math.ceil(half*.85)+1):
      for z in range(lo,hi+1):
        left,right=(axis-offset,z),(axis+offset,z); radius=min(disk_radius(left,polygon),disk_radius(right,polygon),offset)
        if radius>best[0]:best=(radius,left,right)
    dia=2*best[0]*common_scale*fit
    x=source['station_fraction_candidate']*868.496683861459
    results.append({'section':name,'x_mm':x,'available_disk_diameter_mm':dia,'required_clear_diameter_mm':required,'diameter_margin_mm':dia-required,'local_pass':dia>=required,'optimal_centers_pixels':[best[1],best[2]],'isotropic_factor':fit})
out={'status':'V113_ACTIVE_REPRODUCTION_FMS_LOCAL_PACKAGING','source_manifest':'analysis/propulsion_sources_v113/manifest.json','candidate':{'bare_shroud_od_mm':housing,'skin_allowance_mm':skin,'desired_radial_service_mm':radial_service,'required_clear_diameter_mm':required,'overall_length_mm':73.5},'sections':results,'source_station_gaps_mm':[results[i+1]['x_mm']-results[i]['x_mm'] for i in range(2)],'checks':{'D_pass':results[0]['local_pass'],'E_pass':results[1]['local_pass'],'F_pass':results[2]['local_pass'],'E_to_F_axial_span_mm':results[2]['x_mm']-results[1]['x_mm'],'E_to_F_body_length_reserve_mm':results[2]['x_mm']-results[1]['x_mm']-73.5},'limitations':['section centers are independently optimized and do not prove one straight EDF axis','metric station registration remains provisional in promoted historical source set','only D/E/F source sections are available; continuous clearance between E and F is not source-proven','60 mm intake lip is not included and must not be installed in the constrained internal duct'],'release':{'local_section_screen_pass':results[1]['local_pass'] and results[2]['local_pass'],'continuous_axis_pass':False,'hardware_frozen':False,'propulsion_packaging_freeze':False,'flight_release':False}}
(root/'analysis'/'propulsion_local_packaging_v113.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))