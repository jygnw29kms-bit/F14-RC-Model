import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; out=R/'migration/freecad/F14_v262_SOURCE_STATION_WING_SEGMENTS.FCStd'; audp=R/'migration/freecad/freecad_v262_source_station_wing_segments_audit.json'
wd=json.load(open(R/'legacy/fusion-addins/F14TomcatRC_v18/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
scale=900.0/(2*wd['sections'][-1]['wbl_in']); xshift=93.0*scale; zshift=187.59240693460868; seam_idx=4
joiners=[('FWD',569.9475331358894,-4.299519854236053),('AFT',581.1120872253817,-4.231136960437908)]
def wire_xyz(pts):
 v=[App.Vector(*p) for p in pts]; v.append(v[0]); return Part.makePolygon(v)
def secwire(sec,sgn):
 y=sgn*sec['wbl_in']*scale; chord=sec['trailing_edge_fs_in']-sec['leading_edge_fs_in']; rows=sec['ordinates_xc_upper_lower']; contour=[(x,u) for x,u,l in rows]+[(x,l) for x,u,l in rows[:0:-1]]
 pts=[((sec['leading_edge_fs_in']+x*chord)*scale-xshift,y,(sec['reference_vertical_wl_in']+z*chord)*scale-zshift) for x,z in contour]
 return wire_xyz(pts)
d=App.openDocument(str(src)); doc=App.newDocument('F14_v262_SOURCE_STATION_WING_SEGMENTS')
for o in d.Objects:
 if o.Name in ['WING_R','WING_L']: continue
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 sections=wd['sections']; ranges=[('INNER',sections[:seam_idx+1]),('OUTER',sections[seam_idx:])]
 for pname,slist in ranges:
  sh=Part.makeLoft([secwire(s,sgn) for s in slist],True,False)
  for tag,x,z in joiners:
   cav=Part.makeCylinder(3.15,40,App.Vector(x,sgn*(sections[seam_idx]['wbl_in']*scale-20),z),App.Vector(0,sgn,0)); sh=sh.cut(cav)
  sh=sh.removeSplitter(); o=doc.addObject('PartDesign::Feature',f'V262_WING_{lab}_{pname}'); o.Shape=sh; o.Label=f'v262 {lab} wing {pname.lower()} / CR3992 station split'
  b=sh.BoundBox; rows.append({'side':lab,'segment':pname,'valid':sh.isValid(),'solid_count':len(sh.Solids),'bounds_mm':{'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]},'bbox_extents_mm':[b.XLength,b.YLength,b.ZLength],'volume_cm3':sh.Volume/1000.0,'p2s_safe_250_cube':max(b.XLength,b.YLength,b.ZLength)<=250})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V262_SOURCE_STATION_WING_SEGMENTS','source_table':'NASA CR-3992 Appendix 2 basic Grumman wing','seam':{'index':seam_idx,'WBL_in':wd['sections'][seam_idx]['wbl_in'],'abs_y_mm':wd['sections'][seam_idx]['wbl_in']*scale},'transform':{'x_nose_shift_mm':-xshift,'z_sourceWL_to_local_mm':-zshift},'bond_cavities':{'diameter_mm':6.3,'embed_each_side_mm':20},'rows':rows,'gates':{'four_segments_created':len(rows)==4,'all_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'all_segment_bbox_axes_le_250':all(r['p2s_safe_250_cube'] for r in rows),'source_station_exact_split':True,'adhesive_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
