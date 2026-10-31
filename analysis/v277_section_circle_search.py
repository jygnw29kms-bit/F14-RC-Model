import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=json.load(open(R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
scale=1.1697428086486623; shift=187.59240693460868; fs0=93.0
secs=d['sections']; seam=274.36816*scale; ys=[seam-20,seam,seam+20]

def lerp(a,b,t): return a+(b-a)*t

def profile_at_y(y_mm):
    w=y_mm/scale
    lo=hi=None
    for a,b in zip(secs[:-1],secs[1:]):
        if a['wbl_in']<=w<=b['wbl_in']: lo,hi=a,b; break
    if lo is None: raise ValueError(w)
    t=(w-lo['wbl_in'])/(hi['wbl_in']-lo['wbl_in'])
    le=lerp(lo['leading_edge_fs_in'],hi['leading_edge_fs_in'],t); te=lerp(lo['trailing_edge_fs_in'],hi['trailing_edge_fs_in'],t); chord=te-le; ref=lerp(lo['reference_vertical_wl_in'],hi['reference_vertical_wl_in'],t)
    # ordinates share same xc grid
    rows=[]
    for ra,rb in zip(lo['ordinates_xc_upper_lower'],hi['ordinates_xc_upper_lower']):
        xc=ra[0]; up=lerp(ra[1],rb[1],t); low=lerp(ra[2],rb[2],t)
        x=(le+xc*chord-fs0)*scale; zu=(ref+up*chord)*scale-shift; zl=(ref+low*chord)*scale-shift
        rows.append((xc,x,zu,zl))
    poly=[(r[1],r[2]) for r in rows]+[(r[1],r[3]) for r in reversed(rows)]
    return rows,poly

def inside(poly,p):
    x,y=p; c=False
    j=len(poly)-1
    for i in range(len(poly)):
        xi,yi=poly[i]; xj,yj=poly[j]
        if ((yi>y)!=(yj>y)) and x < (xj-xi)*(y-yi)/(yj-yi+1e-15)+xi: c=not c
        j=i
    return c

def segdist(p,a,b):
    px,py=p; ax,ay=a; bx,by=b; vx=bx-ax; vy=by-ay; wx=px-ax; wy=py-ay; vv=vx*vx+vy*vy
    t=0 if vv==0 else max(0,min(1,(wx*vx+wy*vy)/vv)); qx=ax+t*vx; qy=ay+t*vy
    return math.hypot(px-qx,py-qy)

def margin(poly,p):
    if not inside(poly,p): return -1
    return min(segdist(p,poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
profiles=[profile_at_y(y)[1] for y in ys]
# search x/z grid around useful chord region
cands=[]
for x in [550+i*0.5 for i in range(81)]:
  for z in [-8+i*0.25 for i in range(41)]:
    ms=[margin(poly,(x,z)) for poly in profiles]; m=min(ms)
    if m>=4.15: cands.append({'x_mm':x,'z_mm':z,'min_margin_mm':m,'margins_mm':ms})
cands.sort(key=lambda r:r['min_margin_mm'],reverse=True)
pairs=[]
for i,a in enumerate(cands):
  for b in cands[i+1:]:
    sp=math.hypot(a['x_mm']-b['x_mm'],a['z_mm']-b['z_mm'])
    if sp>=10:
      pairs.append({'a':a,'b':b,'spacing_mm':sp,'worst_margin_mm':min(a['min_margin_mm'],b['min_margin_mm'])})
pairs.sort(key=lambda p:(p['worst_margin_mm'],p['spacing_mm']),reverse=True)
out={'status':'V277_SECTION_CIRCLE_SEARCH','y_samples_mm':ys,'required_radius_mm':4.15,'candidate_count':len(cands),'best_candidates':cands[:20],'best_pairs':pairs[:20],'gates':{'pair_found':bool(pairs),'pair_margin_ge_4p15':bool(pairs and pairs[0]['worst_margin_mm']>=4.15)}}
(R/'analysis/v277_section_circle_search.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
