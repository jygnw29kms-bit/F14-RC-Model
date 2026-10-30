import FreeCAD as App, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
data=json.loads((R/'legacy/fusion-addins/F14TomcatRC_v18/NASA_F14_basic_wing_v08.json').read_text())
d=App.openDocument(str(R/'migration/freecad/F14_v244_CURRENT_ENDMODEL_STATE.FCStd'))
w=d.getObject('WING_R').Shape
scale=1.1697428086486623; dx=93*scale; rows=[]
for s in data['sections']:
    x=s['leading_edge_fs_in']*scale-dx; y=s['wbl_in']*scale
    yc=s['ordinates_xc_upper_lower'][0][1]; chord=s['trailing_edge_fs_in']-s['leading_edge_fs_in']
    absz=(s['reference_vertical_wl_in']+yc*chord)*scale
    v=min(w.Vertexes,key=lambda vv:(vv.Point.x-x)**2+(vv.Point.y-y)**2)
    xy=((v.Point.x-x)**2+(v.Point.y-y)**2)**0.5
    rows.append({'wbl_in':s['wbl_in'],'target_xy_mm':[x,y],'cad_le_z_mm':v.Point.z,'source_abs_le_z_mm':absz,'translation_mm':absz-v.Point.z,'xy_match_error_mm':xy})
trans=[r['translation_mm'] for r in rows]
res={'status':'V245_CR3992_DIRECT_WING_WL_REGISTRATION','source':'NASA CR-3992 Appendix 2 Grumman basic F-14 wing','method':'Direct tabulated WBL/LE/TE/reference vertical location; no pivot-WL extrapolation','rows':rows,'translation_stats_mm':{'min':min(trans),'max':max(trans),'spread':max(trans)-min(trans),'mean':sum(trans)/len(trans)},'gates':{'all_station_xy_matches_lt_0p01mm':all(r['xy_match_error_mm']<0.01 for r in rows),'constant_translation_spread_lt_0p01mm':max(trans)-min(trans)<0.01,'wing_absolute_WL_source_backed':max(trans)-min(trans)<0.01,'pivot_axis_absolute_WL_verified':False,'fuselage_common_Z_registered':False,'production_OML':False,'flight_release':False}}
(R/'analysis/v245_cr3992_direct_wing_wl_registration.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))