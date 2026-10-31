import FreeCAD as App, Part, json, pathlib, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v273_SEGMENT_CLAMP_TOOL_ACCESS.FCStd'; out=R/'migration/freecad/F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd'; audp=R/'migration/freecad/freecad_v282_three_8x6_wing_joiner_endmodel_audit.json'
wd=json.load(open(R/'legacy/fusion-addins/F14TomcatRC_v18/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
scale=900.0/(2*wd['sections'][-1]['wbl_in']); xshift=93.0*scale; zshift=187.59240693460868; seam_idx=2; seam_sec=wd['sections'][seam_idx]; seam_y=seam_sec['wbl_in']*scale
joiners=[('FWD',542.0,-1.0),('MID',552.0,-1.0),('AFT',562.0,-1.0)]
def wire_xyz(pts):
 v=[App.Vector(*p) for p in pts]; v.append(v[0]); return Part.makePolygon(v)
def secwire(sec,sgn):
 y=sgn*sec['wbl_in']*scale; chord=sec['trailing_edge_fs_in']-sec['leading_edge_fs_in']; rows=sec['ordinates_xc_upper_lower']; contour=[(x,u) for x,u,l in rows]+[(x,l) for x,u,l in rows[:0:-1]]
 pts=[((sec['leading_edge_fs_in']+x*chord)*scale-xshift,y,(sec['reference_vertical_wl_in']+z*chord)*scale-zshift) for x,z in contour]
 return wire_xyz(pts)
d=App.openDocument(str(src)); doc=App.newDocument('F14_v282_THREE_8X6_WING_JOINER_ENDMODEL')
for o in d.Objects:
    if o.Name.startswith('V262_WING_') or o.Name.startswith('V260_WING_JOINER_'): continue
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
rows=[]
for lab,sgn in [('R',1),('L',-1)]:
    sections=wd['sections']; ranges=[('INNER',sections[:seam_idx+1]),('OUTER',sections[seam_idx:])]
    for pname,slist in ranges:
        sh=Part.makeLoft([secwire(s,sgn) for s in slist],True,False)
        for tag,x,z in joiners:
            cav=Part.makeCylinder(4.15,40,App.Vector(x,sgn*(seam_y-20),z),App.Vector(0,sgn,0)); sh=sh.cut(cav)
        sh=sh.removeSplitter(); o=doc.addObject('PartDesign::Feature',f'V282_WING_{lab}_{pname}'); o.Shape=sh; o.Label=f'v282 {lab} wing {pname.lower()} / CR3992 WBL200.79919 / three 8x6 joiners'
        b=sh.BoundBox; rows.append({'side':lab,'segment':pname,'valid':sh.isValid(),'solid_count':len(sh.Solids),'bbox_extents_mm':[b.XLength,b.YLength,b.ZLength],'p2s_safe_250':max(b.XLength,b.YLength,b.ZLength)<=250,'volume_cm3':sh.Volume/1000})
    for tag,x,z in joiners:
        tube=Part.makeCylinder(4.0,40,App.Vector(x,sgn*(seam_y-20),z),App.Vector(0,sgn,0)).cut(Part.makeCylinder(3.0,40,App.Vector(x,sgn*(seam_y-20),z),App.Vector(0,sgn,0)))
        o=doc.addObject('PartDesign::Feature',f'V282_WING_JOINER_{lab}_{tag}'); o.Shape=tube; o.Label=f'v282 8x6 CF wing joiner {lab} {tag}'
doc.recompute(); doc.saveAs(str(out))
# material/mass screen from verified Easy Composites pultrusion family TDS
vol_one_cm3=math.pi*(4.0**2-3.0**2)*40/1000; total_tube_cm3=6*vol_one_cm3
mass_range=[total_tube_cm3*1.30,total_tube_cm3*1.50]
# conservative bending from v275
stress=81.79525662904923; fos=250.0/stress
aud={'status':'V282_THREE_8X6_WING_JOINER_ENDMODEL','source':src.name,'seam':{'CR3992_WBL_in':seam_sec['wbl_in'],'model_abs_y_mm':seam_y},'joiners':{'OD_ID_mm':[8,6],'cavity_d_mm':8.3,'embed_each_side_mm':20,'positions_mm':joiners},'rows':rows,'mass':{'total_CF_tube_volume_cm3':total_tube_cm3,'datasheet_density_g_cm3':[1.30,1.50],'tube_mass_range_g':mass_range},'load_screen':{'seam_moment_per_tube_Nm':2.8105806894846723,'outer_fiber_stress_MPa':stress,'datasheet_flexural_lower_typical_MPa':250,'FOS_lower_typical':fos},'gates':{'four_valid_segments':len(rows)==4 and all(r['valid'] and r['solid_count']==1 for r in rows),'all_segments_p2s_safe':all(r['p2s_safe_250'] for r in rows),'FOS_ge_3_using_250MPa_typical_lower':fos>=3,'supplier_lot_minimum_strength_certified':False,'adhesive_bond_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))

