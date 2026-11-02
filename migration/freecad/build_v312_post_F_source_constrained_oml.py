import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'; out=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; audp=R/'migration/freecad/freecad_v312_post_F_source_constrained_oml_audit.json'
trace=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8')); p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v312_POST_F_SOURCE_CONSTRAINED_OML')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull(): q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
F=next(x for x in p135['base_profiles'] if x['name']=='F'); fy=[p[0] for p in F['points']]; fz=[p[1] for p in F['points']]; yc=(min(fy)+max(fy))/2; zmin=min(fz); zmax=max(fz); h=zmax-zmin; hw=(max(fy)-min(fy))/2
plan=sorted([(x['x_model_mm'],x['expected_half_width_mm']) for x in v134['plan_samples'] if x['x_model_mm']>=F['x_mm']],key=lambda t:t[0]); tr=trace['rows']
def interp(rows,x,key=None):
    arr=rows
    if key: arr=[(r['x_model_mm'],r[key]) for r in rows]
    for i in range(len(arr)-1):
        x0,y0=arr[i]; x1,y1=arr[i+1]
        if x0<=x<=x1: return y0+(y1-y0)*(x-x0)/(x1-x0)
    return arr[-1][1]
stations=[754.962281164333,782.5849221136924,804.1967007376154,821.0644303953113,835.2965772939922]
wires=[]; rows=[]
for x in stations:
    tw=interp(plan,x); zt=interp(tr,x,'z_top_mm'); zb=interp(tr,x,'z_bottom_mm'); pts=[]
    for y,z in F['points']:
        ny=(y-yc)/hw; nz=(z-zmin)/h
        pts.append(App.Vector(x,ny*tw,zb+nz*(zt-zb)))
    pts.append(pts[0]); wire=Part.makePolygon(pts); wires.append(wire); rows.append({'x_mm':x,'half_width_mm':tw,'z_top_mm':zt,'z_bottom_mm':zb})
loft=Part.makeLoft(wires,True,True)
o=doc.addObject('PartDesign::Feature','V312_POST_F_SOURCE_CONSTRAINED_OML'); o.Shape=loft; o.Label='v312 source-constrained post-F OML candidate'
# Screen a circular 1.00-FSA core from x811 to terminal station at y +/-66.2846, z -10.5087
r=20.71231517720798; x0=810.462281164333; x1=835.2965772939922; screens=[]
for side,sgn in [('R',1),('L',-1)]:
    cyl=Part.makeCylinder(r,x1-x0,App.Vector(x0,sgn*66.28458486059378,-10.508688347971937),App.Vector(1,0,0)); frac=cyl.common(loft).Volume/cyl.Volume
    screens.append({'side':side,'one_FSA_core_containment_fraction':frac,'outside_mm3':cyl.Volume-cyl.common(loft).Volume})
doc.recompute(); doc.saveAs(str(out)); aud={'status':'V312_POST_F_SOURCE_CONSTRAINED_OML_CANDIDATE','source_model':src.name,'source_trace':'analysis/post_F_side_trace_v312.json','stations':rows,'oml_valid':loft.isValid(),'solid_count':len(loft.Solids),'one_FSA_core_screen':screens,'gates':{'trace_source_hash_match':trace['gates']['exact_source_hash_match'],'trace_F_anchor_within_0p3mm':trace['gates']['known_F_anchor_top_bottom_within_0p3mm'],'post_F_candidate_valid_single_solid':loft.isValid() and len(loft.Solids)==1,'one_FSA_core_bilateral_containment_ge_0p995':all(s['one_FSA_core_containment_fraction']>=0.995 for s in screens),'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
