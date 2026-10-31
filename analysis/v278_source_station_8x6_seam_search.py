import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=json.load(open(R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
scale=1.1697428086486623; shift=187.59240693460868; fs0=93.0
secs=d['sections']; target_wbls=[200.79919,237.58369,274.36816]

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
results=[]
for wbl in target_wbls:
  seam=wbl*scale; ys=[seam-20,seam,seam+20]; profiles=[profile_at_y(y)[1] for y in ys]
  # x range from local chord around seam, broad enough for all candidates
  cands=[]
  for x in [525+i*0.5 for i in range(151)]:
    for z in [-12+i*0.25 for i in range(65)]:
      ms=[margin(poly,(x,z)) for poly in profiles]; m=min(ms)
      if m>=4.15: cands.append({'x_mm':x,'z_mm':z,'min_margin_mm':m,'margins_mm':ms})
  cands.sort(key=lambda r:r['min_margin_mm'],reverse=True)
  pairs=[]
  for i,a in enumerate(cands):
    for b in cands[i+1:]:
      sp=math.hypot(a['x_mm']-b['x_mm'],a['z_mm']-b['z_mm'])
      if sp>=10: pairs.append({'a':a,'b':b,'spacing_mm':sp,'worst_margin_mm':min(a['min_margin_mm'],b['min_margin_mm'])})
  pairs.sort(key=lambda p:(p['worst_margin_mm'],p['spacing_mm']),reverse=True)
  results.append({'WBL_in':wbl,'model_y_mm':seam,'candidate_count':len(cands),'best_pair':pairs[0] if pairs else None,'pair_found':bool(pairs)})
valid=[r for r in results if r['pair_found']]
preferred=max(valid,key=lambda r:r['WBL_in']) if valid else None
out={'status':'V278_SOURCE_STATION_8X6_SEAM_SEARCH','required_radius_mm':4.15,'embed_each_side_mm':20,'results':results,'preferred_outermost_valid_station':preferred,'gates':{'valid_source_station_found':preferred is not None}}
(R/'analysis/v278_source_station_8x6_seam_search.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))

