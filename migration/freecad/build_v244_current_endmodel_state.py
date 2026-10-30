import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v241_LIGHT_STABILATOR_CRANK.FCStd'
out=R/'migration/freecad/F14_v244_CURRENT_ENDMODEL_STATE.FCStd'
audp=R/'migration/freecad/freecad_v244_current_endmodel_state_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v244_CURRENT_ENDMODEL_STATE')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
key=['V221_CASSETTE_R','V221_CASSETTE_L','V225_SERVO_A80BHSF_V2','V225_SYNC_YOKE_M4_20','V227_HOBBYWING_UBEC10A_HV','V228_TAIL_UBEC10A_HV','V228_RECEIVER_RESERVE_MAX','V229_SKYWALKER50A_R','V229_SKYWALKER50A_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V235_D_ROOT_FITTING_R','V235_D_ROOT_FITTING_L','V237_D_SHAFT_R','V237_D_SHAFT_L','V241_LIGHT_D_CRANK_R','V241_LIGHT_D_CRANK_L']
legacy_forbidden=['V239_D_CRANK_M3_R','V239_D_CRANK_M3_L','STAB_SHAFT_R','STAB_SHAFT_L','STAB_CRANK_R','STAB_CRANK_L','V240_PUSHROD_CORRIDOR_R','V240_PUSHROD_CORRIDOR_L']
sh=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V244_CURRENT_ENDMODEL_STATE','source':str(src),'shape_count':len(sh),'required_current_objects':{n:(doc.getObject(n) is not None) for n in key},'forbidden_or_superseded_objects_present':[n for n in legacy_forbidden if doc.getObject(n) is not None],'mass_budget_source':'analysis/v243_tail_mass_budget_resolution.json','gates':{'all_required_current_objects_present':all(doc.getObject(n) is not None for n in key),'no_forbidden_tail_duplicates':not any(doc.getObject(n) is not None for n in legacy_forbidden),'all_shapes_valid':all(o.Shape.isValid() for o in sh),'absolute_OML_Z_gate_closed':True,'EDF_shroud_OD_gate_open':True,'physical_bench_gates_open':True,'production_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
