import json, pathlib, numpy as np, math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
oms=json.loads((root/'analysis/upc_fuselage_30stations_scaled.json').read_text())['stations']
DE=json.loads((root/'analysis/propulsion_sources_v113/upc_DE_registration_v12.json').read_text())
F=json.loads((root/'analysis/propulsion_sources_v113/upc_F_registration_v12.json').read_text())
rel=json.loads((root/'analysis/propulsion_relative_axis_v118.json').read_text())
def interp(x,key):
    a,b=None,None
    for s in oms:
        if s['x_mm']<=x:a=s
        if s['x_mm']>=x:
            b=s; break
    if a is None:a=oms[0]
    if b is None:b=oms[-1]
    if a['x_mm']==b['x_mm']:return a[key]
    t=(x-a['x_mm'])/(b['x_mm']-a['x_mm'])
    return a[key]+t*(b[key]-a[key])
pts=[]
# D/E source side top/bottom
for name in ['D','E']:
    s=next(x for x in DE['sections'] if x['name']==name)
    x_mm= next(x for x in json.loads((root/'analysis/propulsion_local_packaging_v113.json').read_text())['sections'] if x['section']==name)['x_mm']
    pts += [(s['side_body_top_pixel_y'],interp(x_mm,'z_top_mm'),name,'top'),(s['side_body_bottom_pixel_y'],interp(x_mm,'z_bottom_mm'),name,'bottom')]
# F
x_mm=rel['F']['x_mm']
pts += [(F['side_top_pixel_y'],interp(x_mm,'z_top_mm'),'F','top'),(F['side_bottom_pixel_y'],interp(x_mm,'z_bottom_mm'),'F','bottom')]
A=np.array([[p[0],1.0] for p in pts],float)
b=np.array([p[1] for p in pts],float)
coef=np.linalg.lstsq(A,b,rcond=None)[0]
scale,offset=coef
pred=A@coef
res=pred-b
rows=[]
for p,pr,e in zip(pts,pred,res):rows.append({'section':p[2],'surface':p[3],'source_y_px':p[0],'model_z_target_mm':p[1],'fit_z_mm':float(pr),'residual_mm':float(e)})
Eaxis=float(scale*next(x for x in DE['sections'] if x['name']=='E')['candidate_section_axis_side_pixel_y']+offset)
Faxis=float(scale*F['registered_candidate_section_axis_side_pixel_y']+offset)
dx=rel['F']['x_mm']-rel['E']['x_mm']; pitch=math.degrees(math.atan2(Faxis-Eaxis,dx))
out={'status':'V125_GLOBAL_SIDEVIEW_TO_ACTIVE_OML_AFFINE_FIT','fit':{'z_mm_per_source_pixel':float(scale),'offset_mm':float(offset),'rms_residual_mm':float(np.sqrt(np.mean(res**2))),'max_abs_residual_mm':float(np.max(np.abs(res)))},'anchors':rows,'mapped_axes':{'E_z_mm':Eaxis,'F_z_mm':Faxis,'delta_z_mm':Faxis-Eaxis,'pitch_deg':pitch},'v121_limit_mm':0.20,'pass':bool(np.max(np.abs(res))<=0.20),'interpretation':'One global vertical scale and offset only; no per-station stretch.'}
(root/'analysis/propulsion_global_sideview_fit_v125.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))