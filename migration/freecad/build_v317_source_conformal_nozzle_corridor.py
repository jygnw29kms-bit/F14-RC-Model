import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'; out=R/'migration/freecad/F14_v317_SOURCE_CONFORMAL_NOZZLE_CORRIDOR.FCStd'; audp=R/'migration/freecad/freecad_v317_source_conformal_nozzle_corridor_audit.json'
p135=json.loads((R/'analysis/propulsion_intermediate_profiles_v135.json').read_text(encoding='utf-8')); v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8')); trace=json.loads((R/'analysis/post_F_side_trace_v312.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); doc=App.newDocument('F14_v317_SOURCE_CONFORMAL_NOZZLE_CORRIDOR')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull(): q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V312_POST_F_SOURCE_CONSTRAINED_OML').Shape; F=next(x for x in p135['base_profiles'] if x['name']=='F')
fy=[p[0] for p in F['points']]; fz=[p[1] for p in F['points']]; yc=(min(fy)+max(fy))/2; hw=(max(fy)-min(fy))/2; zmin=min(fz); h=max(fz)-zmin
plan=sorted([(x['x_model_mm'],x['expected_half_width_mm']) for x in v134['plan_samples'] if x['x_model_mm']>=F['x_mm']]); tr=trace['rows']
def interp(arr,x,key=None):
    a=[(r['x_model_mm'],r[key]) for r in arr] if key else arr
    for (x0,y0),(x1,y1) in zip(a,a[1:]):
        if x0<=x<=x1: return y0+(y1-y0)*(x-x0)/(x1-x0)
    return a[-1][1]
def section_face(x):
    w=interp(plan,x); zt=interp(tr,x,'z_top_mm'); zb=interp(tr,x,'z_bottom_mm'); pts=[App.Vector(x,(y-yc)/hw*w,zb+(z-zmin)/h*(zt-zb)) for y,z in F['points']]; pts.append(pts[0]); return Part.Face(Part.makePolygon(pts))
def clip_face(x,side,web):
    y0=web if side=='R' else -200; y1=200 if side=='R' else -web; pts=[App.Vector(x,y0,-100),App.Vector(x,y1,-100),App.Vector(x,y1,100),App.Vector(x,y0,100),App.Vector(x,y0,-100)]; return Part.Face(Part.makePolygon(pts))
def inward(face,dist):
    cand=[]
    for s in (-dist,dist):
        try:
            sh=face.OuterWire.makeOffset2D(s,join=2,fill=False)
            ws=list(sh.Wires) if sh.ShapeType!='Wire' else [sh]
            for w in ws:
                f=Part.Face(w); frac=f.common(face).Area/f.Area if f.Area else 0
                if f.Area<face.Area and frac>0.999: cand.append(f)
        except Exception: pass
    if not cand: raise RuntimeError('no inward offset')
    return max(cand,key=lambda f:f.Area)
FSA=1347.7432483900213; reserve=1.33; web=3.0; stations=[810.5,816.5,822.5,828.5,834.5]; rows=[]; wires={'R':[],'L':[]}
for x in stations:
    base=section_face(x)
    row={'x_mm':x,'sides':{}}
    for side in ('R','L'):
        raw=base.common(clip_face(x,side,web)); rf=max(raw.Faces,key=lambda f:f.Area); flow=inward(rf,reserve); wires[side].append(flow.OuterWire)
        row['sides'][side]={'raw_lobe_area_mm2':rf.Area,'flow_area_mm2':flow.Area,'area_ratio_to_FSA':flow.Area/FSA}
    rows.append(row)
lofts=[]
for side in ('R','L'):
    sh=Part.makeLoft(wires[side],True,True); o=doc.addObject('PartDesign::Feature','V317_SOURCE_CONFORMAL_FLOW_'+side); o.Shape=sh; o.Label='v317 source-conformal nozzle flow corridor '+side
    common=sh.common(oml); lofts.append({'side':side,'valid':sh.isValid(),'solid_count':len(sh.Solids),'containment_fraction':common.Volume/sh.Volume,'volume_mm3':sh.Volume})
doc.recompute(); doc.saveAs(str(out)); ratios=[s['area_ratio_to_FSA'] for r in rows for s in r['sides'].values()]
aud={'status':'V317_SOURCE_CONFORMAL_NOZZLE_CORRIDOR','source_model':src.name,'architecture':{'center_web_half_width_mm':web,'combined_OML_clearance_plus_wall_reserve_mm':reserve,'reserve_breakdown_mm':{'OML_clearance':0.53,'printable_wall':0.8}},'stations':rows,'lofts':lofts,'summary':{'minimum_flow_area_ratio_to_FSA':min(ratios),'terminal_R_ratio':rows[-1]['sides']['R']['area_ratio_to_FSA'],'terminal_L_ratio':rows[-1]['sides']['L']['area_ratio_to_FSA']},'gates':{'bilateral_lofts_valid_single_solids':all(q['valid'] and q['solid_count']==1 for q in lofts),'bilateral_loft_containment_ge_0p999':all(q['containment_fraction']>=0.999 for q in lofts),'minimum_flow_area_ratio_ge_0p85':min(ratios)>=0.85,'minimum_flow_area_ratio_ge_0p90':min(ratios)>=0.90,'minimum_flow_area_ratio_ge_1p00':min(ratios)>=1.0,'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))