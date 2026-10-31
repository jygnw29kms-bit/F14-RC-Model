import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v255_CF_JOINERS_AND_SLEEVES.FCStd'; out=R/'migration/freecad/F14_v256_CONSOLIDATED_JOINER_STATE.FCStd'; audp=R/'migration/freecad/freecad_v256_consolidated_joiner_state_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v256_CONSOLIDATED_JOINER_STATE'); removed=[]
for o in d.Objects:
 if not hasattr(o,'Shape') or o.Shape.isNull(): continue
 n=o.Name
 if n.startswith('V252_ALIGN_KEY_') or n.startswith('V252_SOCKET_CLEARANCE_') or 'X620_' in n and (n.startswith('V255_CF_TUBE_') or n.startswith('V255_SLEEVE_')):
  removed.append(n); continue
 q=doc.addObject('PartDesign::Feature',n); q.Shape=o.Shape.copy(); q.Label=o.Label
# mass accounting from prior reserve and nonprovisional sleeves
reserve_before=19.4194097652027; sleeve_mass=9.236282401553993; reserve_after=reserve_before-sleeve_mass
shape_objs=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
required=['V255_CF_TUBE_X220_L','V255_CF_TUBE_X220_R','V255_CF_TUBE_X440_L','V255_CF_TUBE_X440_R','V255_CF_TUBE_X840_L','V255_CF_TUBE_X840_R','V253_ACCESS_BATTERY','V253_ACCESS_SWEEP','V253_ACCESS_TAIL_R','V253_ACCESS_TAIL_L']
aud={'status':'V256_CONSOLIDATED_JOINER_STATE','source':src.name,'shape_count':len(shape_objs),'removed_redundant_or_provisional':removed,'mass_budget':{'reserve_before_joiner_sleeves_g':reserve_before,'nonprovisional_sleeves_PPA_CF_g':sleeve_mass,'reserve_after_joiner_sleeves_g':reserve_after,'alignment_keys_removed_saving_g':5.76,'CF_tube_mass_still_hardware_gate':True},'required_objects':{n:doc.getObject(n) is not None for n in required},'gates':{'all_shapes_valid':all(o.Shape.isValid() for o in shape_objs),'all_required_present':all(doc.getObject(n) is not None for n in required),'no_alignment_key_duplicates':not any(o.Name.startswith('V252_ALIGN_KEY_') for o in doc.Objects),'no_active_X620_CF_joiner':not any('X620_' in o.Name and o.Name.startswith('V255_') for o in doc.Objects),'reserve_after_sleeves_positive':reserve_after>0,'bond_system_selected':False,'CF_tube_actual_mass_measured':False,'print_release':False,'flight_release':False}}
doc.recompute(); doc.saveAs(str(out)); aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))