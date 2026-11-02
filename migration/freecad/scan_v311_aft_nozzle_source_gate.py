import FreeCAD as App, Part, pathlib, json, math, hashlib, itertools
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v310_STRUCTURAL_BYPASS_FREEFLOW.FCStd'
aud_path=R/'migration/freecad/freecad_v311_aft_nozzle_source_gate_audit.json'
v134=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text(encoding='utf-8'))
nasa=json.loads((R/'analysis/nasa_station_envelopes.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src))
fan=50.0; hub=28.0; fsa=math.pi/4.0*(fan**2-hub**2); radius=math.sqrt(fsa/math.pi)
axis_y=66.28458486059378; axis_z=-10.508688347971937
x0=754.962281164333; x1=836.8779269494012; dx=0.5

def interp(rows,x,key,xkey='x_mm'):
    rows=sorted(rows,key=lambda q:float(q[xkey]))
    for a,b in zip(rows[:-1],rows[1:]):
        xa=float(a[xkey]); xb=float(b[xkey])
        if xa<=x<=xb:
            t=(x-xa)/(xb-xa); return float(a[key])+t*(float(b[key])-float(a[key]))
    raise ValueError('x outside interpolation range')

def union_names(names):
    ss=[d.getObject(n).Shape for n in names if d.getObject(n)]
    u=ss[0]
    for s in ss[1:]: u=u.fuse(s)
    return u.removeSplitter()

def dilate(shape,pad):
    copies=[]
    for ox,oy,oz in itertools.product((-pad,0,pad),repeat=3):
        q=shape.copy(); q.translate(App.Vector(ox,oy,oz)); copies.append(q)
    u=copies[0]
    for q in copies[1:]: u=u.fuse(q)
    return u.removeSplitter()

# Structural obstruction aft of F using the same hybrid clearance policy as v309/v310.
surfaces=dilate(union_names(['STABILATOR_R','VTAIL_R','VENTRAL_R']),0.5)
hardware=dilate(union_names(['STAB_BEARING_R_1','STAB_HOUSING_R_1','STAB_BEARING_R_2','STAB_HOUSING_R_2','V234_BEARING_INBOARD_COLLAR_R','V234_BEARING_OUTER_SHOULDER_R','V234_SURFACE_INNER_COLLAR_R','V234_SURFACE_OUTER_WASHER_R','V234_END_FASTENER_HEAD_R','V237_D_SHAFT_R','V241_LIGHT_D_CRANK_R','V284_LIGHT_D_ROOT_FITTING_R']),1.3)
keep=surfaces.fuse(hardware).removeSplitter()
core=Part.makeCylinder(radius,x1-x0,App.Vector(x0,axis_y,axis_z),App.Vector(1,0,0))
struct_rows=[]; x=x0
while x<x1-1e-9:
    w=min(dx,x1-x); slab=Part.makeBox(w,300,300,App.Vector(x,-150,-150)); c=core.common(slab)
    gross=c.Volume/w; blocked=c.common(keep).Volume/w
    struct_rows.append({'x_mm':x+w/2,'blocked_area_mm2':blocked,'block_fraction':blocked/gross if gross else 0.0,'net_FSA_ratio':(gross-blocked)/fsa if fsa else 0.0}); x+=w
active=[q for q in struct_rows if q['blocked_area_mm2']>0.01]
structure_clear_after_x=(active[-1]['x_mm']+dx/2.0) if active else x0

# FUSELAGE_CURRENT is only a procedural/source-derived candidate, never final OML.
fus=d.getObject('FUSELAGE_CURRENT').Shape
contain_rows=[]; x=x0
while x<x1-1e-9:
    w=min(dx,x1-x); slab=Part.makeBox(w,300,300,App.Vector(x,-150,-150)); c=core.common(slab)
    total=c.Volume; inside=c.common(fus).Volume
    contain_rows.append({'x_mm':x+w/2,'containment_fraction':inside/total if total else 1.0,'outside_area_mm2':(total-inside)/w if w else 0.0}); x+=w

# Directly compare the old NASA percentile envelope against active UPC v134 at a common post-F x.
compare_x=767.562100387307
upc_plan=interp(v134['plan_samples'],compare_x,'expected_half_width_mm','x_model_mm')
upc_side=next(q for q in v134['side_samples'] if abs(float(q['x_model_mm'])-compare_x)<1e-6)
nasa_half=interp(nasa,compare_x,'half_width_mm')
nasa_top=interp(nasa,compare_x,'z_top_mm')
nasa_bottom=interp(nasa,compare_x,'z_bottom_mm')
source_compare={'x_mm':compare_x,'UPC_half_width_mm':upc_plan,'NASA_raw_half_width_mm':nasa_half,'half_width_abs_delta_mm':abs(nasa_half-upc_plan),
                'UPC_z_top_mm':float(upc_side['expected_z_top_mm']),'NASA_raw_z_top_mm':nasa_top,'z_top_abs_delta_mm':abs(nasa_top-float(upc_side['expected_z_top_mm'])),
                'UPC_z_bottom_mm':float(upc_side['expected_z_bottom_mm']),'NASA_raw_z_bottom_mm':nasa_bottom,'z_bottom_abs_delta_mm':abs(nasa_bottom-float(upc_side['expected_z_bottom_mm']))}
nasa_aft_clean=source_compare['half_width_abs_delta_mm']<=5 and source_compare['z_top_abs_delta_mm']<=5 and source_compare['z_bottom_abs_delta_mm']<=5

aud={'status':'V311_AFT_NOZZLE_SOURCE_GATE','source_model':src.name,
     'structural_scan':{'x_range_mm':[x0,x1],'sample_dx_mm':dx,'one_FSA_radius_mm':radius,'last_blocked_sample_x_mm':active[-1]['x_mm'] if active else None,'structure_clear_after_x_mm':structure_clear_after_x,'maximum_block_fraction':max(q['block_fraction'] for q in struct_rows),'minimum_net_FSA_ratio':min(q['net_FSA_ratio'] for q in struct_rows)},
     'post_F_candidate_fuselage_screen':{'label':'FUSELAGE_CURRENT procedural ruled station loft; packaging reference only','overall_1p00_FSA_core_containment_fraction':core.common(fus).Volume/core.Volume,'first_slice_containment_fraction':contain_rows[0]['containment_fraction'],'worst_slice_containment_fraction':min(q['containment_fraction'] for q in contain_rows),'original_OML_verified':False,'accepted_as_final_post_F_OML':False},
     'independent_source_screen':{'UPC_source':'analysis/propulsion_source_silhouette_constraints_v134.json','NASA_source':'analysis/nasa_station_envelopes.json','comparison':source_compare,'NASA_raw_aft_envelope_clean':nasa_aft_clean,'interpretation':'NASA percentile envelope is contaminated by tail surfaces/annotations in aft region and cannot define nacelle OML.'},
     'decision':{'structural_contraction_start_must_be_aft_of_x_mm':structure_clear_after_x,'post_F_full_3D_OML_available':False,'final_nozzle_contraction_allowed':False,'next_gate':'recover or register an independent aft nacelle/nozzle OML covering at least x~810 onward; do not use FUSELAGE_CURRENT or raw NASA percentile envelope as production OML'},
     'gates':{'hybrid_tail_structure_clears_before_x811mm':structure_clear_after_x<=811.0,'FUSELAGE_CURRENT_acceptable_post_F_OML':False,'NASA_raw_envelope_acceptable_post_F_OML':nasa_aft_clean,'post_F_full_3D_OML_registered':False,'final_nozzle_geometry_defined':False,'print_release':False,'flight_release':False}}
aud['study_source_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(); aud_path.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))