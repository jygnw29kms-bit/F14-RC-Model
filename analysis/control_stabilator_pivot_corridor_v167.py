import json, math, pathlib
root=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
g=json.loads((root/'analysis/control_stabilator_geometry_v145.json').read_text())
# Use mirrored right-side polygon in positive Y.
poly=[(x,-y) for x,y in g['outline_mm']]

def x_intervals_at_y(poly,y):
    xs=[]
    n=len(poly)
    for i in range(n):
        x1,y1=poly[i]; x2,y2=poly[(i+1)%n]
        if abs(y2-y1)<1e-12: continue
        if (y>=min(y1,y2)) and (y<max(y1,y2)):
            t=(y-y1)/(y2-y1); xs.append(x1+t*(x2-x1))
    xs.sort()
    return [(xs[i],xs[i+1]) for i in range(0,len(xs)-1,2)]
# Scan plausible root band from y=78 to110 mm. We seek a contiguous x corridor present at every y.
rows=[]
for y in [78+i for i in range(33)]:
    ints=x_intervals_at_y(poly,y)
    rows.append({'y_mm':y,'x_intervals_mm':ints})
# For each y, choose interval containing the broad root body (not a detached projection; polygon has one interval here).
left=max(r['x_intervals_mm'][0][0] for r in rows if r['x_intervals_mm'])
right=min(r['x_intervals_mm'][0][1] for r in rows if r['x_intervals_mm'])
width=right-left
# Candidate shaft x at midpoint; margins to corridor boundaries.
xmid=(left+right)/2
# Test narrower bearing bands, because two bearings can live inboard of surface and only shaft must enter the root.
bands=[]
for ya,yb in [(78,90),(80,95),(82,100),(85,105),(90,110)]:
    rr=[r for r in rows if ya<=r['y_mm']<=yb and r['x_intervals_mm']]
    l=max(r['x_intervals_mm'][0][0] for r in rr); q=min(r['x_intervals_mm'][0][1] for r in rr)
    bands.append({'y_band_mm':[ya,yb],'common_x_corridor_mm':[l,q],'width_mm':q-l,'mid_x_mm':(l+q)/2})
result={
 'status':'V167_SOURCE_BACKED_STABILATOR_ROOT_PIVOT_CORRIDOR',
 'source':'analysis/control_stabilator_geometry_v145.json / NASA CR-163098 Fig.4 outline',
 'policy':'This is an RC packaging corridor inside the source-backed stabilator root, not a claim of the original F-14 pivot axis.',
 'right_stabilator_polygon_mm':poly,
 'root_scan':rows,
 'full_78_110mm_band':{'common_x_corridor_mm':[left,right],'width_mm':width,'mid_x_mm':xmid},
 'candidate_subbands':bands,
 'hardware_envelope':{'shaft_d_mm':6,'bearing_ID_OD_width_mm':[6,13,5],'stabilator_crank_radius_mm':20,'servo_arm_radius_mm':8},
 'decision':{
   'root_has_common_shaft_corridor':width>=6,
   'shaft_x_not_frozen':True,
   'preferred_next_step':'Select the widest robust sub-band and then test bearing/crank placement against a common tail-fuselage datum once aft fuselage registration is available.',
   'do_not_use_center_wingbox_Z_frame_for_tail_packaging':True
 },
 'release':{'RC_pivot_axis_selected':False,'bearing_packaging_verified':False,'crank_packaging_verified':False,'CAD_release':False,'flight_release':False}
}
(root/'analysis/control_stabilator_pivot_corridor_v167.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'full':result['full_78_110mm_band'],'bands':bands,'decision':result['decision']},indent=2))