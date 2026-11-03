import FreeCAD as App, Part, pathlib, json, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; out=R/'migration/freecad/F14_v314_VARIABLE_ELLIPTIC_NOZZLE_CANDIDATE.FCStd'; audp=R/'migration/freecad/freecad_v314_variable_elliptic_nozzle_candidate_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); trace=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v314_VARIABLE_ELLIPTIC_NOZZLE_CANDIDATE')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape; F=next(x for x in p135['base_profiles'] if x['name']=='F')
fy=[p[0] for p in F['points']]; fz=[p[1] for p in F['points']]; yc=(min(fy)+max(fy))/2; hw=(max(fy)-min(fy))/2; zmin=min(fz); h=max(fz)-zmin
plan=sorted([(x['x_model_mm'],x['expected_half_width_mm']) for x in v134['plan_samples'] if x['x_model_mm']>=F['x_mm']]); tr=trace['rows']
def interp(arr,x,key=None):
    a=[(r['x_model_mm'],r[key]) for r in arr] if key else arr
    for (x0,y0),(x1,y1) in zip(a,a[1:]):
        if x0<=x<=x1: return y0+(y1-y0)*(x-x0)/(x1-x0)
    return a[-1][1]
def section_poly(x):
    w=interp(plan,x); zt=interp(tr,x,'z_top_mm'); zb=interp(tr,x,'z_bottom_mm')
    return [((y-yc)/hw*w, zb+(z-zmin)/h*(zt-zb)) for y,z in F['points']]
def pip(y,z,poly):
    inside=False; j=len(poly)-1
    for i,(yi,zi) in enumerate(poly):
        yj,zj=poly[j]
        if ((zi>z)!=(zj>z)) and y < (yj-yi)*(z-zi)/(zj-zi+1e-30)+yi: inside=not inside
        j=i
    return inside
def fits(poly,cy,cz,ay,az,n=48):
    for sgn in (1,-1):
        for i in range(n):
            t=2*math.pi*i/n
            if not pip(sgn*cy+ay*math.cos(t),cz+az*math.sin(t),poly): return False
    return True
def frange(a,b,s):
    n=int(round((b-a)/s)); return [a+i*s for i in range(n+1)]
def search(poly,center=None):
    best=None
    ranges=(frange(56,66,1),frange(-12,0,1),frange(16,28,1),frange(10,19,1)) if center is None else tuple(frange(v-1,v+1,0.25) for v in center)
    for cy in ranges[0]:
      for cz in ranges[1]:
       for ay in ranges[2]:
        for az in ranges[3]:
         area=math.pi*ay*az
         if best and area<=best['area_mm2']: continue
         if fits(poly,cy,cz,ay,az,48 if center is None else 72): best={'axis_abs_y_mm':cy,'z_center_mm':cz,'ay_mm':ay,'az_mm':az,'area_mm2':area}
    return best
FSA=1347.7432483900213; stations=[810.5,816.5,822.5,828.5,834.5]; rows=[]; wr=[]; wl=[]
for x in stations:
    poly=section_poly(x); c=search(poly); b=search(poly,(c['axis_abs_y_mm'],c['z_center_mm'],c['ay_mm'],c['az_mm'])); b['x_mm']=x; b['area_ratio_to_FSA']=b['area_mm2']/FSA; rows.append(b)
    for sgn,wires in ((1,wr),(-1,wl)):
        pts=[App.Vector(x,sgn*b['axis_abs_y_mm']+b['ay_mm']*math.cos(2*math.pi*i/72),b['z_center_mm']+b['az_mm']*math.sin(2*math.pi*i/72)) for i in range(72)]; pts.append(pts[0]); wires.append(Part.makePolygon(pts))
lofts=[]
for side,wires in [('R',wr),('L',wl)]:
    sh=Part.makeLoft(wires,True,True); o=doc.addObject('PartDesign::Feature','V314_VARIABLE_NOZZLE_'+side); o.Shape=sh; o.Label='v314 variable elliptic nozzle candidate '+side
    common=sh.common(oml); lofts.append({'side':side,'valid':sh.isValid(),'solid_count':len(sh.Solids),'containment_fraction':common.Volume/sh.Volume,'volume_mm3':sh.Volume})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V314_VARIABLE_ELLIPTIC_NOZZLE_CANDIDATE','source_model':src.name,'method':'analytic source-section scan plus final BRep containment','stations':rows,'lofts':lofts,'summary':{'minimum_area_ratio_to_FSA':min(r['area_ratio_to_FSA'] for r in rows),'maximum_area_ratio_to_FSA':max(r['area_ratio_to_FSA'] for r in rows),'terminal_area_ratio_to_FSA':rows[-1]['area_ratio_to_FSA']},'gates':{'bilateral_lofts_valid_single_solids':all(q['valid'] and q['solid_count']==1 for q in lofts),'bilateral_loft_containment_ge_0p995':all(q['containment_fraction']>=0.995 for q in lofts),'minimum_area_ratio_ge_0p70':min(r['area_ratio_to_FSA'] for r in rows)>=0.70,'minimum_area_ratio_ge_0p80':min(r['area_ratio_to_FSA'] for r in rows)>=0.80,'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))