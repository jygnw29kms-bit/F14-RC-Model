import json,pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
reserve_before=19.4194097652027; hatch=8.78724; auw=1174.574700301657
aud={'status':'V268_SERVICE_HATCH_MASS_BUDGET_UPDATE','source_projected_AUW_g':auw,'reserve_before_service_flange_g':reserve_before,'service_flange_PPA_CF_screen_g':hatch,'reserve_after_service_flange_g':reserve_before-hatch,'margin_to_1200_g':1200-auw,'interpretation':'Flange mass is allocated from existing reserve; projected AUW is not double-added.','gates':{'reserve_remaining_positive':reserve_before-hatch>0,'reserve_remaining_ge_10g':reserve_before-hatch>=10,'actual_print_mass_measured':False,'fastener_mass_measured':False,'AUW_frozen':False,'flight_release':False}}
(R/'analysis/v268_service_hatch_mass_budget_update.json').write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
