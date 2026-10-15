import json,math,pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
g=json.loads((root/'analysis/control_stabilator_geometry_v145.json').read_text())
poly=[(x,-y) for x,y in g['outline_mm']]
# polygon area centroid is already known; compute planform area-weighted quarter-chord axis via spanwise strip integration.
def intervals_at_y(y):
    xs=[]
    for i,(x1,y1) in enumerate(poly):
        x2,y2=poly[(i+1)%len(poly)]
        if abs(y2-y1)<1e-12: continue
        if min(y1,y2)<=y<max(y1,y2):
            t=(y-y1)/(y2-y1); xs.append(x1+t*(x2-x1))
    xs.sort(); return [(xs[i],xs[i+1]) for i in range(0,len(xs)-1,2)]
ymin=min(y for x,y in poly); ymax=max(y for x,y in poly)
step=.1
A=0; Q=0; strips=[]; y=ymin+step/2
while y<ymax:
    ints=intervals_at_y(y)
    for le,te in ints:
        c=te-le; ac=le+.25*c; dA=c*step; A+=dA; Q+=ac*dA
        strips.append((y,le,te,c,ac,dA))
    y+=step
xac=Q/A
# Root physical common corridor from v167
v167=json.loads((root/'analysis/control_stabilator_pivot_corridor_v167.json').read_text())
lo,hi=v167['full_78_110mm_band']['common_x_corridor_mm']
# Evaluate candidate pivot positions across corridor against global AC. Require pivot ahead of global quarter-chord reference.
cands=[]
for p in [lo+i*1.0 for i in range(int((hi-lo)//1)+1)]+[hi]:
    off=xac-p
    if off>0:
        # v146 severe force with global-AC offset as a first-order screen
        force=33.50791900575004; hinge=force*off/1000; servo=hinge*(8/20)/.7*2; kgcm=servo/.0980665
        cands.append({'pivot_x_mm':p,'global_quarter_chord_offset_mm':off,'severe_hinge_Nm':hinge,'servo_required_kgcm':kgcm})
# Prefer 8-15 mm ahead of area-weighted quarter-chord for positive balance but modest hinge moment.
preferred=[c for c in cands if 8<=c['global_quarter_chord_offset_mm']<=15]
selected=min(preferred,key=lambda c:abs(c['global_quarter_chord_offset_mm']-10)) if preferred else min(cands,key=lambda c:abs(c['global_quarter_chord_offset_mm']-10))
result={'status':'V170_AREA_WEIGHTED_STABILATOR_PIVOT_SCREEN','source':'NASA-planform v145','method':'spanwise integration of local quarter-chord weighted by strip area; first-order RC balance screen only','one_side_integrated_area_mm2':A,'area_weighted_quarter_chord_x_mm':xac,'v145_polygon_area_mm2':g['one_side_area_mm2'],'area_integration_relative_error':(A-g['one_side_area_mm2'])/g['one_side_area_mm2'],'root_common_physical_corridor_mm':[lo,hi],'candidate_rows':cands,'selected_candidate':selected,'decision':{'local_per_strip_25pct_constraint_rejected_as_wrong_axis criterion':True,'selected_RC_pivot_x_mm':selected['pivot_x_mm'],'selected_global_AC_offset_mm':selected['global_quarter_chord_offset_mm'],'14kgcm_servo_gate_retained':True,'next_gate':'local shaft/bearing/crank geometry in source-backed root; later validate hinge moment by bench/CFD and common tail-fuselage packaging'},'release':{'aerodynamic_center_verified':False,'RC_pivot_axis_planform_candidate':True,'bearing_packaging_verified':False,'crank_packaging_verified':False,'flight_release':False}}
(root/'analysis/control_stabilator_pivot_axis_v170.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'area':A,'xac':xac,'corridor':[lo,hi],'selected':selected,'area_error':result['area_integration_relative_error']},indent=2))