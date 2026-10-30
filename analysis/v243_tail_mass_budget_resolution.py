import json
from pathlib import Path
R=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
base=json.loads((R/'analysis/v223_light_cassette_mass_cg_update.json').read_text())
crank=json.loads((R/'migration/freecad/freecad_v241_light_stabilator_crank_audit.json').read_text())
shaft=json.loads((R/'analysis/v242_7075_stabilator_shaft_screen.json').read_text())
fit=json.loads((R/'migration/freecad/freecad_v235_stabilator_root_fitting_current_audit.json').read_text())
projected=base['scenarios'][0]['projected_AUW_g']
hw_budget=35.0; reserve_budget=50.0
crank_g=crank['mass']['pair_7075_mass_g']; shaft_g=shaft['mass']['7075_pair_g']; hardware_known=crank_g+shaft_g
fit_vol=sum(r['volume_cm3'] for r in fit['rows']); fit_ppa=fit_vol*1.25
res={
 'status':'V243_TAIL_MASS_BUDGET_RESOLUTION',
 'source_projected_AUW_g':projected,
 'note':'Projected AUW already contains 35 g fasteners/bearings/inserts budget and 50 g reserve; current tail hardware is allocated inside those budgets, not added again.',
 'tail_hardware':{'7075_D_shafts_pair_g':shaft_g,'7075_light_cranks_pair_g':crank_g,'known_subtotal_g':hardware_known,'generic_hardware_budget_g':hw_budget,'remaining_for_4x_bearings_collars_washers_fasteners_g':hw_budget-hardware_known},
 'root_fittings':{'pair_volume_cm3':fit_vol,'PPA_CF_screen_g':fit_ppa,'allocated_from_existing_50g_reserve':True,'reserve_remaining_after_root_fittings_g':reserve_budget-fit_ppa},
 'mass_accounting':{'projected_AUW_remains_g':projected,'margin_to_1175_g':1175-projected,'margin_to_1200_g':1200-projected,'unallocated_reserve_after_root_fittings_g':reserve_budget-fit_ppa},
 'gates':{'hardware_budget_not_exceeded_before_bearings':hardware_known<hw_budget,'root_fittings_fit_existing_reserve':fit_ppa<reserve_budget,'bearing_actual_masses_measured':False,'retention_actual_masses_measured':False,'AUW_frozen':False,'flight_release':False}
}
(R/'analysis/v243_tail_mass_budget_resolution.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
