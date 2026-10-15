import json, pathlib, math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
oms=json.loads((root/'analysis/upc_fuselage_30stations_scaled.json').read_text())['stations']
Ereg=json.loads((root/'analysis/propulsion_sources_v113/upc_E_registration_v44.json').read_text())
Freg=json.loads((root/'analysis/propulsion_sources_v113/upc_F_registration_v12.json').read_text())
rel=json.loads((root/'analysis/propulsion_relative_axis_v118.json').read_text())
# E source side bounds from DE registration
DE=json.loads((root/'analysis/propulsion_sources_v113/upc_DE_registration_v12.json').read_text())
Esrc=next(s for s in DE['sections'] if s['name']=='E')
# F source side bounds directly from registration
Efrac=(Ereg['candidate_axis_side_pixel_y']-Esrc['side_body_top_pixel_y'])/(Esrc['side_body_bottom_pixel_y']-Esrc['side_body_top_pixel_y'])
Ffrac=(Freg['registered_candidate_section_axis_side_pixel_y']-Freg['side_top_pixel_y'])/(Freg['side_bottom_pixel_y']-Freg['side_top_pixel_y'])
def interp(x,key):
    a,b=None,None
    for s in oms:
        if s['x_mm']<=x: a=s
        if s['x_mm']>=x:
            b=s; break
    if a is None:a=oms[0]
    if b is None:b=oms[-1]
    if a['x_mm']==b['x_mm']: return a[key]
    t=(x-a['x_mm'])/(b['x_mm']-a['x_mm'])
    return a[key]+t*(b[key]-a[key])
def axis_z(x,f):
    zt=interp(x,'z_top_mm'); zb=interp(x,'z_bottom_mm')
    return zt-f*(zt-zb),zt,zb
out={}
for name,frac in [('E',Efrac),('F',Ffrac)]:
    x=rel[name]['x_mm']; z,zt,zb=axis_z(x,frac)
    out[name]={'x_mm':x,'source_vertical_fraction_top_to_bottom':frac,'model_z_top_mm':zt,'model_z_bottom_mm':zb,'mapped_axis_z_mm':z}
dx=out['F']['x_mm']-out['E']['x_mm']; dz=out['F']['mapped_axis_z_mm']-out['E']['mapped_axis_z_mm']
out['derived']={'delta_z_mm':dz,'pitch_deg':math.degrees(math.atan2(dz,dx)),'relative_source_pitch_deg_v118':rel['relative_axis']['pitch_deg'],'pitch_delta_deg':math.degrees(math.atan2(dz,dx))-rel['relative_axis']['pitch_deg']}
print(json.dumps(out,indent=2))