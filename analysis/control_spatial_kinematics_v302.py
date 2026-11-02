import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
servo_body={'xmin':698.5,'xmax':721.5,'ymin':6.25,'ymax':33.75}
crank_center=(736.0078983334656,76.0,0.0); crank_r=15.0
target_throw=17.843481128270785

def dist(a,b): return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))
def crank(phi_deg):
 p=math.radians(phi_deg); return (crank_center[0]+crank_r*math.cos(p),crank_center[1],crank_center[2]+crank_r*math.sin(p))
def horn(axis,r,alpha_deg):
 a=math.radians(alpha_deg); return (axis[0]+r*math.cos(a),axis[1]+r*math.sin(a),axis[2])
def servo_roots(axis,r,alpha0,L0,phi_target):
 cp=crank(phi_target); roots=[]; step=0.5; lo=-85.0
 f0=dist(horn(axis,r,alpha0+lo),cp)-L0
 a=lo+step
 while a<=85.0001:
  f1=dist(horn(axis,r,alpha0+a),cp)-L0
  if f1==0 or f0*f1<0:
   x0,x1=a-step,a; q0=dist(horn(axis,r,alpha0+x0),cp)-L0
   for _ in range(45):
    xm=(x0+x1)/2; qm=dist(horn(axis,r,alpha0+xm),cp)-L0
    if q0*qm<=0: x1=xm
    else: x0=xm; q0=qm
   roots.append((x0+x1)/2)
  f0=f1; a+=step
 return roots
cands=[]
for tip_step in range(5):  # 722.0 .. 724.0 in 0.5 mm
 tipx=722.0+0.5*tip_step
 for tipy in [18.0,19.0,20.0,21.0,22.0]:
  for r_i in range(8,17):
   r=r_i/2.0
   for alpha0 in range(-180,181,5):
    tip0=(tipx,tipy,12.0); a0=math.radians(alpha0)
    axis=(tipx-r*math.cos(a0),tipy-r*math.sin(a0),12.0)
    if not (servo_body['xmin']<=axis[0]<=servo_body['xmax'] and servo_body['ymin']<=axis[1]<=servo_body['ymax']): continue
    L0=dist(tip0,crank(0.0))
    rm=servo_roots(axis,r,alpha0,L0,-target_throw); rp=servo_roots(axis,r,alpha0,L0,target_throw)
    if not rm or not rp: continue
    # Choose opposite-sign endpoints with minimum absolute travel. Direction can be reversed in transmitter.
    pairs=[]
    for m in rm:
     for p in rp:
      if m*p>=0: continue
      pairs.append((m,p,max(abs(m),abs(p)),abs(abs(m)-abs(p))))
    if not pairs: continue
    m,p,maxtravel,asym=min(pairs,key=lambda q:(q[2],q[3]))
    if maxtravel>70: continue
    # Prefer near-6mm horn, near-neutral target x723.5/y20, and symmetric endpoints.
    score=maxtravel+asym*1.5+abs(r-6)*3+abs(tipx-723.5)*1.0+abs(tipy-20)*0.5
    cands.append({'neutral_horn_tip_mm':tip0,'spline_axis_mm':axis,'horn_radius_mm':r,'neutral_horn_angle_deg':alpha0,'pushrod_length_mm':L0,'servo_deg_for_stabilator_minus_target':m,'servo_deg_for_stabilator_plus_target':p,'max_servo_half_travel_deg':maxtravel,'servo_endpoint_asymmetry_deg':asym,'stabilator_target_half_throw_deg':target_throw,'score':score})
cands.sort(key=lambda q:q['score'])
# Dynamic EDF clearance pre-screen on the best analytical candidates. The EDF service envelope is a
# finite X-axis cylinder x=658..731.5, radius 27.25 mm, centered at Y=66.2846 / Z=-10.5087.
edf_y=66.28458486059378; edf_z=-10.508688347971937; edf_x_end=731.5; edf_r=27.25; service_r=2.0
def solve_phi_for_candidate(c,theta,guess):
    axis=tuple(c['spline_axis_mm']); r=c['horn_radius_mm']; a0=c['neutral_horn_angle_deg']; L0=c['pushrod_length_mm']
    hp=horn(axis,r,a0+theta); roots=[]; step=0.25; lo=-30.0; f0=dist(hp,crank(lo))-L0; x=lo+step
    while x<=30.0001:
        f1=dist(hp,crank(x))-L0
        if f1==0 or f0*f1<0:
            aa,bb=x-step,x; fa=dist(hp,crank(aa))-L0
            for _ in range(35):
                mm=(aa+bb)/2; fm=dist(hp,crank(mm))-L0
                if fa*fm<=0: bb=mm
                else: aa=mm; fa=fm
            roots.append((aa+bb)/2)
        f0=f1; x+=step
    return min(roots,key=lambda p:abs(p-guess)) if roots else None
def line_edf_service_clearance(a,b):
    dx=b[0]-a[0]
    tmax=1.0 if dx<=0 else min(1.0,max(0.0,(edf_x_end-a[0])/dx))
    dy=b[1]-a[1]; dz=b[2]-a[2]; y0=a[1]-edf_y; z0=a[2]-edf_z
    den=dy*dy+dz*dz
    t=0.0 if den<1e-12 else -(y0*dy+z0*dz)/den
    t=max(0.0,min(tmax,t))
    radial=math.hypot(y0+dy*t,z0+dz*t)
    return radial-edf_r-service_r
for c in cands[:400]:
    s0=c['servo_deg_for_stabilator_plus_target']; s1=c['servo_deg_for_stabilator_minus_target']; guess=target_throw
    clear=[]; valid=True
    for ii in range(17):
        theta=s0+(s1-s0)*ii/16.0
        phi=solve_phi_for_candidate(c,theta,guess)
        if phi is None: valid=False; break
        guess=phi; hp=horn(tuple(c['spline_axis_mm']),c['horn_radius_mm'],c['neutral_horn_angle_deg']+theta); cp=crank(phi)
        clear.append(line_edf_service_clearance(hp,cp))
    c['dynamic_service_EDF_clearance_min_mm']=min(clear) if valid else -999.0
    c['dynamic_screen_valid']=valid
# Prefer candidates with >=1.5 mm dynamic service clearance, then low servo travel/asymmetry.
screened=[c for c in cands[:400] if c.get('dynamic_screen_valid') and c.get('dynamic_service_EDF_clearance_min_mm',-999)>=1.0]
if screened:
    screened.sort(key=lambda c:(-c['dynamic_service_EDF_clearance_min_mm'],c['max_servo_half_travel_deg'],c['servo_endpoint_asymmetry_deg'],abs(c['horn_radius_mm']-6)))
    best=screened[0]
else:
    best=cands[0] if cands else None
out={'status':'V302_SPATIAL_LINKAGE_PROGRAMMABLE_ENDPOINT_FEASIBILITY','assumptions':{'servo_output_axis':'Z','stabilator_crank_axis':'Y','servo_body_xy_bounds_mm':servo_body,'servo_horn_radius_search_mm':[4,8],'neutral_horn_tip_search_x_mm':[722,724],'neutral_horn_tip_search_y_mm':[18,22],'target_stabilator_half_throw_deg':target_throw,'programmable_independent_servo_endpoints_allowed':True,'exact_real_servo_spline_axis_still_unmeasured':True},'candidate_count':len(cands),'dynamic_screened_count':len(screened),'best':best,'top_candidates':screened[:20] if screened else cands[:20],'gates':{'mathematical_solution_exists':best is not None,'servo_half_travel_le_70deg':bool(best and best['max_servo_half_travel_deg']<=70),'endpoint_asymmetry_le_10deg':bool(best and best['servo_endpoint_asymmetry_deg']<=10),'horn_radius_between_4_and_8mm':bool(best and 4<=best['horn_radius_mm']<=8),'dynamic_service_EDF_clearance_ge_1mm_analytic':bool(best and best.get('dynamic_service_EDF_clearance_min_mm',-999)>=1.0),'exact_real_servo_spline_axis_measured':False,'dynamic_CAD_clearance_verified':False,'bench_throw_verified':False,'flight_release':False}}
(R/'analysis/control_spatial_kinematics_v302.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'status':out['status'],'candidate_count':len(cands),'best':best,'gates':out['gates']},indent=2))
