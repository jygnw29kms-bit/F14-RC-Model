import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v262_SOURCE_STATION_WING_SEGMENTS.FCStd'; out=R/'migration/freecad/F14_v264_SEGMENTED_ENDMODEL_STATE.FCStd'; audp=R/'migration/freecad/freecad_v264_segmented_endmodel_state_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v264_SEGMENTED_ENDMODEL_STATE')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
req=['V262_WING_R_INNER','V262_WING_R_OUTER','V262_WING_L_INNER','V262_WING_L_OUTER','V260_WING_JOINER_R_FWD','V260_WING_JOINER_R_AFT','V260_WING_JOINER_L_FWD','V260_WING_JOINER_L_AFT','V253_ACCESS_BATTERY','V253_ACCESS_SWEEP','V253_ACCESS_TAIL_R','V253_ACCESS_TAIL_L','V221_CASSETTE_R','V221_CASSETTE_L','V225_SERVO_A80BHSF_V2','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L']
forbid=['WING_R','WING_L']
shapes=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
aud={'status':'V264_SEGMENTED_ENDMODEL_STATE','source':src.name,'shape_count':len(shapes),'required':{n:doc.getObject(n) is not None for n in req},'forbidden_present':[n for n in forbid if doc.getObject(n)],'gates':{'all_required_present':all(doc.getObject(n) is not None for n in req),'unsegmented_wings_absent':all(doc.getObject(n) is None for n in forbid),'all_shapes_valid':all(o.Shape.isValid() for o in shapes),'service_keepouts_retained':all(doc.getObject(n) is not None for n in ['V253_ACCESS_BATTERY','V253_ACCESS_SWEEP','V253_ACCESS_TAIL_R','V253_ACCESS_TAIL_L']),'aft_nacelle_OML_gate_open':True,'hatch_shell_cuts_frozen':False,'print_release':False,'flight_release':False}}
doc.recompute(); doc.saveAs(str(out)); aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
