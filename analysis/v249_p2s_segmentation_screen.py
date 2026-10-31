import json, pathlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
SAFE=250.0
# Current model bounds and source-backed wing station used as a natural seam.
wing={'x':[479.4839172711096,640.8174422689683],'y_abs':[148.8263775443693,450.0],'z':[-12.425259506190798,9.094380028581725]}
scale=1.1697428086486623
wing_seam_wbl=274.36816; wing_seam_y=wing_seam_wbl*scale
# Conservative fuselage longitudinal modules; central broad modules split on centerline.
fuse_modules=[
 {'name':'NOSE','x':[0.5,220.0],'split_y':False},
 {'name':'FORWARD_CENTER','x':[220.0,440.0],'split_y':True},
 {'name':'WINGBOX_CENTER','x':[440.0,620.0],'split_y':True},
 {'name':'AFT_NACELLE','x':[620.0,840.0],'split_y':True},
 {'name':'TAIL_END','x':[840.0,879.0],'split_y':False},
]
# Approx current half-width envelope from v191 ruled-station source; split halves remain <=160 mm wide.
max_half_width=159.615
for m in fuse_modules:
 m['length_mm']=m['x'][1]-m['x'][0]; m['max_piece_width_mm']=max_half_width if m['split_y'] else 2*max_half_width
 m['length_within_safe']=m['length_mm']<=SAFE
 m['width_within_safe']=m['max_piece_width_mm']<=SAFE
# Nose/tail require local width verification because unsplit global max is irrelevant there.
# Mark as geometry-check rather than pretending global envelope applies.
fuse_modules[0]['width_within_safe']='LOCAL_GEOMETRY_CHECK_REQUIRED'
fuse_modules[-1]['width_within_safe']='LOCAL_GEOMETRY_CHECK_REQUIRED'
wing_parts=[
 {'name':'WING_INNER','y_abs':[wing['y_abs'][0],wing_seam_y]},
 {'name':'WING_OUTER','y_abs':[wing_seam_y,wing['y_abs'][1]]},
]
for p in wing_parts:
 p['spanwise_extent_mm']=p['y_abs'][1]-p['y_abs'][0]; p['spanwise_within_safe']=p['spanwise_extent_mm']<=SAFE
 p['chordwise_bbox_max_mm']=wing['x'][1]-wing['x'][0]; p['z_extent_mm']=wing['z'][1]-wing['z'][0]
 p['bbox_axes_within_safe']=max(p['spanwise_extent_mm'],p['chordwise_bbox_max_mm'],p['z_extent_mm'])<=SAFE
res={'status':'V249_P2S_SAFE_SEGMENTATION_SCREEN','safe_build_cube_mm':[SAFE,SAFE,SAFE],
 'wing':{'source_seam':{'WBL_in':wing_seam_wbl,'model_abs_y_mm':wing_seam_y},'parts':wing_parts,'decision':'split each moving wing at exact CR3992 defining WBL 274.36816; add structural join only after spar/load-path audit'},
 'fuselage_modules':fuse_modules,
 'service_constraints':['wingbox/pivot cassette remains removable central module','battery 70 mm travel corridor must remain accessible','sweep servo and yoke require top/bottom service access','tail servo cradle must remain removable','EDF aft-nacelle cuts remain provisional until nacelle OML/Z gate closes'],
 'gates':{'wing_bbox_safe_after_source_station_split':all(p['bbox_axes_within_safe'] for p in wing_parts),'central_fuselage_half_modules_length_width_safe':all(m['length_within_safe'] and (m['width_within_safe'] is True) for m in fuse_modules[1:4]),'nose_local_width_verified':False,'tail_end_local_width_verified':False,'aft_nacelle_final_cut_frozen':False,'joiner_geometry_designed':False,'print_release':False}}
out=R/'analysis/v249_p2s_segmentation_screen.json'; out.write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))
