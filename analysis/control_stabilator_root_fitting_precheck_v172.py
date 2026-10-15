import json,pathlib,math
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
g=json.loads((root/'analysis/control_stabilator_geometry_v145.json').read_text()); v171=json.loads((root/'analysis/control_stabilator_root_fitting_v171.json').read_text())
poly=[(x,-y) for x,y in g['outline_mm']]
def inside(pt):
 x,y=pt; c=False
 for i,(x1,y1) in enumerate(poly):
  x2,y2=poly[(i+1)%len(poly)]
  if ((y1>y)!=(y2>y)) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
 return c
pivot=float(v171['target_RC_axis']['pivot_x_mm'])
# Candidate: compact thick hub hidden under fuselage plus thin outboard bond tongue inside 5.5mm stabilator.
hub={'x':[pivot-12,pivot+12],'y':[82,104],'z':[-5,5]}
tongue={'x':[pivot-18,pivot+18],'y':[100,130],'z':[-1.75,1.75]}
# Sample planform footprint on 1mm grid to catch edge escapes, not just corners.
def footprint_check(box):
 bad=[]; x0,x1=box['x']; y0,y1=box['y'];
 x=x0
 while x<=x1+1e-9:
  y=y0
  while y<=y1+1e-9:
   if not inside((x,y)): bad.append([x,y])
   y+=1
  x+=1
 return bad
hub_bad=footprint_check(hub); tongue_bad=footprint_check(tongue)
# Fuselage plan half-width interpolate active 30-station guide at x pivot: use as plan-only cover screen.
stations=json.loads((root/'analysis/upc_fuselage_30stations_scaled.json').read_text())['stations']
ss=sorted(stations,key=lambda s:s['x_mm']);
def interp(x,key):
 for a,b in zip(ss,ss[1:]):
  if a['x_mm']<=x<=b['x_mm']:
   t=(x-a['x_mm'])/(b['x_mm']-a['x_mm']); return a[key]+t*(b[key]-a[key])
 return None
half=interp(pivot,'half_width_mm')
# Volume sensitivity before shaft bore.
hubv=(hub['x'][1]-hub['x'][0])*(hub['y'][1]-hub['y'][0])*(hub['z'][1]-hub['z'][0])/1000
tongv=(tongue['x'][1]-tongue['x'][0])*(tongue['y'][1]-tongue['y'][0])*(tongue['z'][1]-tongue['z'][0])/1000
overlap_x=max(0,min(hub['x'][1],tongue['x'][1])-max(hub['x'][0],tongue['x'][0])); overlap_y=max(0,min(hub['y'][1],tongue['y'][1])-max(hub['y'][0],tongue['y'][0])); overlap_z=max(0,min(hub['z'][1],tongue['z'][1])-max(hub['z'][0],tongue['z'][0])); overlap=overlap_x*overlap_y*overlap_z/1000
bore_len=32; bore_vol=math.pi*(3.05**2)*bore_len/1000
net=hubv+tongv-overlap-bore_vol
result={'status':'V172_STABILATOR_ROOT_FITTING_PLANFORM_PRECHECK','sources':['analysis/control_stabilator_geometry_v145.json','analysis/control_stabilator_root_fitting_v171.json'],'pivot_x_mm':pivot,'candidate_geometry':{'hub':hub,'tongue':tongue,'shaft_bore_d_mm':6.1,'shaft_bore_effective_length_mm':bore_len},'planform_checks':{'hub_outside_sample_count':len(hub_bad),'tongue_outside_sample_count':len(tongue_bad),'hub_inside_source_planform':not hub_bad,'tongue_inside_source_planform':not tongue_bad,'active_UPC_plan_halfwidth_at_pivot_mm':half,'hub_y_max_mm':hub['y'][1],'hub_plan_hidden_inside_current_fuselage_halfwidth_screen':half is not None and hub['y'][1]<half},'volume_screen_cm3':{'hub':hubv,'tongue':tongv,'overlap':overlap,'shaft_bore':bore_vol,'net_candidate_each':net,'pair':2*net,'PPA_CF_pair_mass_g_at_1p25':2*net*1.25,'PA6_CF_pair_mass_g_at_1p09':2*net*1.09},'decision':{'planform_precheck_pass':not hub_bad and not tongue_bad,'root_hub_thickness_intentionally_exceeds_5p5mm_surface':True,'reason':'10 mm hub is inside current fuselage plan cover; 3.5 mm outboard tongue remains within provisional 5.5 mm stabilator thickness.','next_gate':'standalone Fusion root-fitting CAD with 6.1 mm bore; no fuselage bearing mounts yet'},'release':{'root_fitting_CAD_verified':False,'material_proof_pass':False,'shaft_clamp_detail_designed':False,'flight_release':False}}
(root/'analysis/control_stabilator_root_fitting_precheck_v172.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))