import json, pathlib, numpy as np, math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
data=json.loads((root/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json').read_text())
pivot=json.loads((root/'cad/fusion/F14TomcatRC/F14_pivot_datum_v16.json').read_text())
xs=np.array([s['wbl_in'] for s in data['sections']],float)
zs=np.array([s['reference_vertical_wl_in'] for s in data['sections']],float)
coef=np.polyfit(xs,zs,1)
pred=np.polyval(coef,xs)
res=zs-pred
xp=float(pivot['derived_full_scale_pivot_bl_in'])
zp=float(np.polyval(coef,xp))
factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
# regression prediction uncertainty for mean trend at xp, then model scale mm
n=len(xs); s2=float(np.sum(res**2)/(n-2)); xbar=float(xs.mean()); Sxx=float(np.sum((xs-xbar)**2))
se_mean=math.sqrt(s2*(1/n+(xp-xbar)**2/Sxx))
se_pred=math.sqrt(s2*(1+1/n+(xp-xbar)**2/Sxx))
out={'status':'V127_GRUMMAN_REFERENCE_WL_LINEAR_REGRESSION','source_sections':[{'wbl_in':float(x),'reference_vertical_wl_in':float(z),'fit_wl_in':float(p),'residual_in':float(r)} for x,z,p,r in zip(xs,zs,pred,res)],'fit':{'slope_wl_per_wbl':float(coef[0]),'intercept_wl_in':float(coef[1]),'rms_residual_in':float(np.sqrt(np.mean(res**2))),'max_abs_residual_in':float(np.max(np.abs(res))),'pivot_bl_in':xp,'pivot_wl_in':zp,'pivot_model_z_mm':zp*factor,'mean_trend_1sigma_in':se_mean,'single_station_prediction_1sigma_in':se_pred,'mean_trend_1sigma_model_mm':se_mean*factor,'single_station_prediction_1sigma_model_mm':se_pred*factor},'v121_limit_mm':0.20}
(root/'analysis/airframe_pivot_wl_regression_v127.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))