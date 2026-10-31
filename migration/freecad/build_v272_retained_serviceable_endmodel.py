import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v271_C_RING_SEGMENT_RETENTION.FCStd'; out=R/'migration/freecad/F14_v272_RETAINED_SERVICEABLE_ENDMODEL.FCStd'; audp=R/'migration/freecad/freecad_v272_retained_serviceable_endmodel_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v272_RETAINED_SERVICEABLE_ENDMODEL')
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
req=['V262_WING_R_INNER','V262_WING_R_OUTER','V262_WING_L_INNER','V262_WING_L_OUTER','V267_HATCH_FLANGE_BATTERY','V267_HATCH_FLANGE_SWEEP','V267_HATCH_FLANGE_TAIL_R','V267_HATCH_FLANGE_TAIL_L']+[f'V271_C_CLAMP_X{x}_{s}' for x in (220,440,840) for s in ('L','R')]
missing=[n for n in req if not doc.getObject(n)]
shapes=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
doc.recompute(); doc.saveAs(str(out))
a={'status':'V272_RETAINED_SERVICEABLE_ENDMODEL','source':src.name,'shape_count':len(shapes),'missing_required':missing,'architecture':{'rider_segments_removable':True,'primary_load_path':'CF tube + printed sleeve','alignment':'v252 keys','axial_retention':'v271 C-ring M3 clamps','X620_retention':'provisional / omitted while aft-nacelle OML gate open'},'mass_budget':{'projected_AUW_g':1174.574700301657,'reserve_before_clamps_g':10.6321697652027,'v271_clamp_PPA_CF_g':2.253238409441419,'reserve_after_clamps_g':8.378931355761281,'M3_fasteners_allocated_to_generic_hardware_budget':True},'gates':{'all_required_present':not missing,'all_shapes_valid':all(o.Shape.isValid() for o in shapes),'reserve_remaining_positive':8.378931355761281>0,'X620_gate_open':True,'actual_M3_fastener_mass_measured':False,'clamp_bench_test_required':True,'proof_load':False,'print_release':False,'flight_release':False}}
a['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
