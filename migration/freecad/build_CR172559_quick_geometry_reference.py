import FreeCAD as App, Part, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).parent
SRC=ROOT/'analysis'/'original_front_sources'
XREG=json.loads((SRC/'ABCDEF_FS_from_Navy_UPC_side_registration.json').read_text(encoding='utf-8'))
FRAME=json.loads((SRC/'ABCDEF_shared_frame_candidate.json').read_text(encoding='utf-8'))
scale=float(XREG['rc_scale_mm_per_fullscale_in'])
FS0=93.0
WL0=145.0
# CR-172559 Table 1 quick-geometry knots, restricted to line-defined FS>=352 region.
Y={
'MHB':[(352,31),(414.5,29.5),(433,75),(497,74),(546,73),(600,76.5),(650,79)],
'CREASE':[(352,16),(405,13),(497,0),(650,79),(697,80.5),(780,81)],
'FUP':[(352,31),(497,19.5),(546,14),(600,11),(650,0),(697,49.5),(780,51)],
'SCPUP':[(352,31),(405,23.5),(497,14),(546,7.5),(600,5),(650,0)],
'SCPCAN':[(352,16),(405,9.5),(497,0),(650,81.5),(697,82.5),(780,83)],
'SCPLO':[(352,31),(414.5,29.5),(425,39.79),(433,75),(497,76.2),(546,77.7),(600,79),(650,81.5)],
'FLO':[(352,31),(414.5,29.5),(425,39.79),(433,42),(497,46.3),(546,47.5),(600,48.5),(650,49.5),(697,49.75),(780,51)],
'INLTUP':[(352,66.5),(433,66.5),(497,66.5),(546,68),(600,74.5),(650,77),(697,78.5),(780,80)],
'INLTLO':[(352,67),(433,75),(497,66.5),(546,61),(600,57),(650,57.5),(697,58),(780,59)],
}
Z={
'MHB':[(352,130.5),(414.5,127.93),(433,119),(497,125.5),(546,139),(600,139.5),(650,140)],
'CREASE':[(352,183.5),(405,182),(497,174.5),(650,140),(697,141),(780,140)],
'FUP':[(352,155),(497,163),(546,163.5),(600,163),(650,160.5),(697,165.5),(780,162.75)],
'SCPUP':[(352,173),(497,174.5),(546,169.5),(600,165),(650,160.5)],
'SCPCAN':[(352,199.5),(497,174.5),(650,105.5),(697,110),(780,116)],
'SCPLO':[(352,121.75),(425,123.43),(433,119),(497,113),(546,110),(600,105),(650,105.5)],
'FLO':[(352,150),(414.5,127.93),(425,123.43),(433,117),(497,107.8),(546,104.7),(600,103),(650,104),(697,107),(780,113)],
'INLTUP':[(352,162.5),(433,169),(497,171.5),(546,170),(600,165),(650,162),(697,160),(780,155.5)],
'INLTLO':[(352,156.5),(433,119),(497,111),(546,107),(600,104),(650,104),(697,108),(780,114)],
}
def interp(knots,x):
    knots=sorted(knots)
    if x<knots[0][0] or x>knots[-1][0]: return None
    for (x0,v0),(x1,v1) in zip(knots,knots[1:]):
        if x0<=x<=x1:
            if x1==x0:return v0
            return v0+(x-x0)*(v1-v0)/(x1-x0)
    return knots[-1][1]
def rcx(fs):return (fs-FS0)*scale
def rcz(wl):return (wl-WL0)*scale

doc=App.newDocument('F14_CR172559_QUICK_GEOMETRY_REFERENCE')
rows=[]
for name in sorted(set(Y)&set(Z)):
    xs=sorted(set([a for a,_ in Y[name]]+[a for a,_ in Z[name]]))
    xs=[x for x in xs if interp(Y[name],x) is not None and interp(Z[name],x) is not None]
    pts_pos=[]; pts_neg=[]
    for fs in xs:
        yy=interp(Y[name],fs)*scale; zz=rcz(interp(Z[name],fs)); xx=rcx(fs)
        pts_pos.append(App.Vector(xx,yy,zz)); pts_neg.append(App.Vector(xx,-yy,zz))
    if len(pts_pos)>=2:
        for side,pts in [('R',pts_pos),('L',pts_neg)]:
            o=doc.addObject('PartDesign::Feature',f'{name}_{side}')
            o.Label=f'CR172559 {name} {side} – Quick-Geometry Referenz'
            o.Shape=Part.makePolygon(pts)
        rows.append({'feature':name,'FS_range_in':[xs[0],xs[-1]],'point_count':len(xs)})
# Global WL145 reference rail, source-converged engineering datum candidate only.
wl=doc.addObject('PartDesign::Feature','WL145_Reference')
wl.Label='WL145.0 globale Engineering-Referenz – keine C-Z-Registrierung'
wl.Shape=Part.makeLine(App.Vector(rcx(352),-110,0),App.Vector(rcx(780),-110,0))
# Mark C longitudinal station through actual quick-geometry rail field.
crow=next(r for r in XREG['sections'] if r['section']=='C')
cx=float(crow['nose_relative_X_nominal_mm'])
mark=doc.addObject('PartDesign::Feature','Section_C_FS_Marker')
mark.Label=f'Sektion C FS{crow["FS_nominal_in"]:.3f} / X={cx:.3f} mm'
mark.Shape=Part.makeLine(App.Vector(cx,-110,-60),App.Vector(cx,-110,60))
# Add UPC C profile in a clearly separated comparison lane: Y offset +145 mm, local Z preserved.
prof=next(p for p in FRAME['profiles'] if p['section']=='C')
z0=float(prof.get('axis_Z_candidate_mm',0.0)); shapes=[]
for loop in prof['loops_xyz_candidate_mm']:
    pts=[App.Vector(cx,float(q[1])+145.0,float(q[2])-z0) for q in loop]
    if len(pts)>=2: shapes.append(Part.makePolygon(pts+[pts[0]]))
cobj=doc.addObject('PartDesign::Feature','UPC_C_LocalZ_Comparison')
cobj.Label='UPC Sektion C – lokales Z, +145mm Y-Versatz – NICHT registriert'
cobj.Shape=Part.makeCompound(shapes)
# local axis for separated C lane
caxis=doc.addObject('PartDesign::Feature','UPC_C_LocalAxis')
caxis.Label='UPC C lokale Z=0 Achse – keine Aircraft-WL'
caxis.Shape=Part.makeLine(App.Vector(cx,90,0),App.Vector(cx,200,0))
doc.recompute()
out=BASE/'F14_CR172559_QUICK_GEOMETRY_REFERENCE.FCStd'; doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={
 'status':'CR172559_QUICK_GEOMETRY_3D_RAIL_REFERENCE_WITH_C_LOCALZ_COMPARISON',
 'source':'NASA CR-172559 Table 1 F-14A Wing-Fuselage-Glove quick-geometry model',
 'source_model_limit':'Report states fuselage-nacelle quick geometry was formulated from a 1/40 scale F-14A three-view and did not exactly represent aft-end nacelles.',
 'coordinate_reference':{'FS0_fullscale_in':FS0,'WL0_fullscale_in':WL0,'rc_scale_mm_per_fullscale_in':scale},
 'rails':rows,
 'C':{'FS_nominal_in':crow['FS_nominal_in'],'X_mm':cx,'segment':'INLET TO NACELLE AFT FAIRING FS425-433','UPC_profile_y_display_offset_mm':145.0,'UPC_profile_Z_registered':False},
 'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'gates':{'quick_geometry_reference_only':True,'C_absolute_Z_registered':False,'loft_allowed':False,'master_changed':False,'production_release':False},
 'limits':['CR-172559 rails are an engineering cross-check, not production OML.','UPC C is deliberately displayed in a separate Y lane with local Z preserved.','WL145 line is a global engineering datum candidate, not a translation instruction for UPC C.']
}
(BASE/'freecad_CR172559_quick_geometry_reference_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
