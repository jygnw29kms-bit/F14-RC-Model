import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v300_STRAIGHT_STABILATOR_PUSHROD.FCStd'
out=R/'migration/freecad/F14_v303_DYNAMIC_STABILATOR_LINKAGE_SWEEP.FCStd'
audp=R/'migration/freecad/freecad_v303_dynamic_stabilator_linkage_sweep_audit.json'
v302=json.loads((R/'analysis/control_spatial_kinematics_v302.json').read_text(encoding='utf-8'))
best=v302['best']; d=App.openDocument(str(src)); doc=App.newDocument('F14_v303_DYNAMIC_STABILATOR_LINKAGE_SWEEP')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
axisR=tuple(best['spline_axis_mm']); r=float(best['horn_radius_mm']); alpha0=float(best['neutral_horn_angle_deg']); L0=float(best['pushrod_length_mm'])
cc=(736.0078983334656,76.0,0.0); cr=15.0; rod_r=1.5; svc_r=2.0
smin=float(best['servo_deg_for_stabilator_plus_target']); smax=float(best['servo_deg_for_stabilator_minus_target'])

def horn(axis,theta,sgn):
    # Mirror the right-side horn geometry and rotation across aircraft centerplane.
    a=math.radians(alpha0+theta)
    x=axis[0]+r*math.cos(a); y=axis[1]+r*math.sin(a)
    return App.Vector(x,sgn*y,axis[2])
def crank(phi,sgn):
    p=math.radians(phi); return App.Vector(cc[0]+cr*math.cos(p),sgn*cc[1],cc[2]+cr*math.sin(p))
def length_for(theta,phi):
    return horn(axisR,theta,1).distanceToPoint(crank(phi,1))
def solve_phi(theta,guess):
    # Find all roots in +/-30deg and select branch nearest previous sample.
    roots=[]; step=0.25; lo=-30.0; f0=length_for(theta,lo)-L0; x=lo+step
    while x<=30.0001:
        f1=length_for(theta,x)-L0
        if f1==0 or f0*f1<0:
            a,b=x-step,x; fa=length_for(theta,a)-L0
            for _ in range(45):
                m=(a+b)/2; fm=length_for(theta,m)-L0
                if fa*fm<=0: b=m
                else: a=m; fa=fm
            roots.append((a+b)/2)
        f0=f1; x+=step
    if not roots: raise RuntimeError('no crank root at servo angle '+str(theta))
    return min(roots,key=lambda p:abs(p-guess))
def rod(a,b,rad):
    v=b.sub(a); return Part.makeCylinder(rad,v.Length,a,v.normalize())

samples=[]; prev=-17.843481128270785
N=25
for i in range(N):
    theta=smin+(smax-smin)*i/(N-1)
    phi=solve_phi(theta,prev); prev=phi
    rec={'servo_deg':theta,'stabilator_deg':phi,'sides':[]}
    for side,sgn in [('R',1),('L',-1)]:
        hp=horn(axisR,theta,sgn); cp=crank(phi,sgn); rr=rod(hp,cp,rod_r); svc=rod(hp,cp,svc_r)
        edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape; fit=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
        cradle=doc.getObject('V299_TAIL_SERVO_CRADLE_'+side).Shape
        rec['sides'].append({'side':side,'horn_tip_mm':[hp.x,hp.y,hp.z],'crank_pin_mm':[cp.x,cp.y,cp.z],
          'rod_length_mm':hp.distanceToPoint(cp),'rod_OML_containment':rr.common(oml).Volume/rr.Volume,'service_OML_containment':svc.common(oml).Volume/svc.Volume,
          'rod_EDF_clearance_mm':rr.distToShape(edf)[0],'service_EDF_clearance_mm':svc.distToShape(edf)[0],
          'rod_EDF_intersection_mm3':rr.common(edf).Volume,'service_EDF_intersection_mm3':svc.common(edf).Volume,
          'service_root_clearance_mm':svc.distToShape(fit)[0],'service_cradle_clearance_mm':svc.distToShape(cradle)[0]})
    samples.append(rec)
# Add endpoint/neutral service-corridor bodies only, avoiding 50 overlapping solids in the file.
for lab,idx in [('MIN',0),('NEUTRAL',min(range(N),key=lambda i:abs(samples[i]['servo_deg']))),('MAX',N-1)]:
    s=samples[idx]
    for side,sgn in [('R',1),('L',-1)]:
        hp=App.Vector(*next(q for q in s['sides'] if q['side']==side)['horn_tip_mm']); cp=App.Vector(*next(q for q in s['sides'] if q['side']==side)['crank_pin_mm'])
        sh=rod(hp,cp,svc_r); o=doc.addObject('PartDesign::Feature',f'V303_SERVICE_{lab}_{side}'); o.Shape=sh; o.Label=f'v303 dynamic service corridor {lab} {side}'
doc.recompute();doc.saveAs(str(out))
flat=[q for s in samples for q in s['sides']]
phis=[s['stabilator_deg'] for s in samples]
aud={'status':'V303_DYNAMIC_STABILATOR_LINKAGE_SWEEP','source_model':src.name,'kinematic_source':'analysis/control_spatial_kinematics_v302.json','assumed_spline_axis_R_mm':axisR,'mirrored_left_axis_mm':[axisR[0],-axisR[1],axisR[2]],'horn_radius_mm':r,'servo_range_deg':[smin,smax],'stabilator_range_deg':[min(phis),max(phis)],'sample_count':N,'samples':samples,'summary':{'minimum_rod_EDF_clearance_mm':min(q['rod_EDF_clearance_mm'] for q in flat),'minimum_service_EDF_clearance_mm':min(q['service_EDF_clearance_mm'] for q in flat),'minimum_service_root_clearance_mm':min(q['service_root_clearance_mm'] for q in flat),'minimum_service_cradle_clearance_mm':min(q['service_cradle_clearance_mm'] for q in flat),'minimum_rod_OML_containment':min(q['rod_OML_containment'] for q in flat),'minimum_service_OML_containment':min(q['service_OML_containment'] for q in flat),'max_pushrod_length_error_mm':max(abs(q['rod_length_mm']-L0) for q in flat)},'gates':{'full_target_throw_reached':min(phis)<=-17.8 and max(phis)>=17.8,'rod_OML_containment_ge_0p999':all(q['rod_OML_containment']>=0.999 for q in flat),'service_OML_containment_ge_0p999':all(q['service_OML_containment']>=0.999 for q in flat),'zero_EDF_intersection':all(q['rod_EDF_intersection_mm3']<1e-6 and q['service_EDF_intersection_mm3']<1e-6 for q in flat),'service_EDF_clearance_ge_1mm':all(q['service_EDF_clearance_mm']>=1.0 for q in flat),'service_root_clearance_ge_5mm':all(q['service_root_clearance_mm']>=5.0 for q in flat),'service_cradle_clearance_ge_5mm':all(q['service_cradle_clearance_mm']>=5.0 for q in flat),'constant_length_error_le_0p01mm':max(abs(q['rod_length_mm']-L0) for q in flat)<=0.01,'exact_real_servo_spline_axis_measured':False,'purchased_servo_revision_verified':False,'bench_throw_verified':False,'proof_load':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps({'status':aud['status'],'servo_range_deg':aud['servo_range_deg'],'stabilator_range_deg':aud['stabilator_range_deg'],'summary':aud['summary'],'gates':aud['gates']},indent=2))
