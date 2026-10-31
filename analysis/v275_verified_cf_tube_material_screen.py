import json, math, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
M=1.5174751830707842*1000 # Nmm per tube
rows=[]
for od,id_ in [(6,4),(8,6)]:
    I=math.pi/64*(od**4-id_**4); sig=M*(od/2)/I
    rows.append({'OD_ID_mm':[od,id_],'I_mm4':I,'stress_MPa':sig,'FOS_using_250MPa_typical_lower_bound':250/sig,'FOS_using_400MPa_typical_upper_bound':400/sig})
a={'status':'V275_VERIFIED_CF_TUBE_MATERIAL_SCREEN','datasheet':{'supplier':'Easy Composites','document':'CFP Carbon Fibre Pultrusions TDS v1.0 revised 2024-09-20','sizes_explicitly_covered':['6(4) mm','8(6) mm'],'flexural_strength_lengthways_MPa':[250,400],'density_g_cm3':[1.30,1.50],'note':'datasheet states values are typical, not specification limits'},'load_reference':{'moment_share_per_tube_Nm':1.5174751830707842},'rows':rows,'decision':{'6x4_meets_FOS3_at_250MPa':rows[0]['FOS_using_250MPa_typical_lower_bound']>=3,'8x6_meets_FOS3_at_250MPa':rows[1]['FOS_using_250MPa_typical_lower_bound']>=3,'preferred_next_geometry':'8x6 if 8.3 mm bond cavity containment passes'},'gates':{'material_family_datasheet_verified':True,'supplier_lot_minimum_strength_certified':False,'proof_load':False,'flight_release':False}}
(R/'analysis/v275_verified_cf_tube_material_screen.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
