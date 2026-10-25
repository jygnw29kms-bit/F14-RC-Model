import json, pathlib, math
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
# inputs
j199=json.loads((R/'migration/freecad/freecad_v199_root_clearance_scan_audit.json').read_text(encoding='utf-8'))
pl=json.loads((R/'analysis/sketchfab_f14d_source_pivot_xy_plausibility.json').read_text(encoding='utf-8'))
# gather scan if present; audit only had summary, rebuild from known source-derived relations conservatively
# Design intent: choose no Z translation as geometry fix because base already locally interferes in current derived fuselage, and down-shifts worsen it.
# Compare strategies: move wing Z, reshape glove/fuselage lower surface locally, or trim wing root. Ranking is engineering/review only.
strategies=[
 {'id':'MOVE_WING_DOWN','effect':'worsens clearance across 490..520','reject':True,'reason':'all tested negative Z shifts increase interference; absolute pivot WL remains unverified'},
 {'id':'MOVE_WING_UP','effect':'could create clearance but lacks source-backed positive Z datum','reject':True,'reason':'would solve local collision by arbitrary translation and break fail-closed datum policy'},
 {'id':'TRIM_WING_ROOT','effect':'removes wing material near pivot','reject':True,'reason':'alters source-derived wing root and may weaken pivot/load path before glove OML is defined'},
 {'id':'LOCAL_GLOVE_ENVELOPE_REBUILD','effect':'rebuild fixed glove/body transition around source-backed X/Y pivot while preserving wing geometry','reject':False,'reason':'keeps wing source geometry, respects X/Y registration, and localizes unresolved Z to fixed glove OML zone'}
]
out={
 'status':'V200_WING_GLOVE_Z_STRATEGY_OPTIMIZATION',
 'verified_inputs':{
   'v199_critical_base_clearance_mm':j199['critical_base']['base_clearance_mm'],
   'v199_critical_x_mm':j199['critical_base']['x_mm'],
   'fit8_negative_range_mm':j199['fit8_negative_x_range_mm'],
   'omit2_negative_range_mm':j199['omit2_negative_x_range_mm'],
   'sketchfab_source_pivot_inside_wing_bbox':pl['checks']['mapped_lateral_inside_wing_bbox'] and pl['checks']['mapped_longitudinal_inside_wing_bbox']
 },
 'strategies':strategies,
 'decision':'LOCAL_GLOVE_ENVELOPE_REBUILD',
 'optimization_target':{
   'preserve_wing_source_geometry':True,
   'preserve_source_backed_pivot_XY':True,
   'do_not_freeze_absolute_Z':True,
   'create_local_fixed_glove_clearance_envelope':True,
   'minimum_review_clearance_target_mm':1.0
 },
 'gates':{'production_OML':False,'pivot_WL_verified':False,'master_changed':False,'production_release':False}
}
(R/'analysis/v200_wing_glove_z_strategy_optimization.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
