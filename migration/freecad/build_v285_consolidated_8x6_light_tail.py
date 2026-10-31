import FreeCAD as App, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd'
fit=R/'migration/freecad/F14_v284_LIGHT_STABILATOR_ROOT_FITTING_FIXED.FCStd'
out=R/'migration/freecad/F14_v285_CONSOLIDATED_8X6_LIGHT_TAIL.FCStd'
audp=R/'migration/freecad/freecad_v285_consolidated_8x6_light_tail_audit.json'
d=App.openDocument(str(src)); f=App.openDocument(str(fit)); doc=App.newDocument('F14_v285_CONSOLIDATED_8X6_LIGHT_TAIL')
skip={'V235_D_ROOT_FITTING_R','V235_D_ROOT_FITTING_L'}
for o in d.Objects:
    if o.Name in skip: continue
    if hasattr(o,'Shape') and not o.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
for name in ['V284_LIGHT_D_ROOT_FITTING_R','V284_LIGHT_D_ROOT_FITTING_L']:
    o=f.getObject(name); q=doc.addObject('PartDesign::Feature',name); q.Shape=o.Shape.copy(); q.Label=o.Label
# mass delta from verified audits
old_tube_cm3=2.513274122871835
new_tube_cm3=5.277875658030853
root_saving_g=11.875783540954647
reserve_before=10.6321697652027
extra_cf=[(new_tube_cm3-old_tube_cm3)*1.30,(new_tube_cm3-old_tube_cm3)*1.50]
reserve_after=[reserve_before+root_saving_g-extra_cf[1], reserve_before+root_saving_g-extra_cf[0]]
doc.recompute(); doc.saveAs(str(out))
shape_objs=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
req=['V282_WING_R_INNER','V282_WING_R_OUTER','V282_WING_L_INNER','V282_WING_L_OUTER','V284_LIGHT_D_ROOT_FITTING_R','V284_LIGHT_D_ROOT_FITTING_L']
aud={'status':'V285_CONSOLIDATED_8X6_LIGHT_TAIL','source':[src.name,fit.name],'shape_count':len(shape_objs),'required':{n:doc.getObject(n) is not None for n in req},'forbidden_heavy_root_fittings_present':[n for n in skip if doc.getObject(n) is not None],'mass_delta':{'reserve_before_g':reserve_before,'root_fitting_saving_g':root_saving_g,'extra_8x6_CF_tube_mass_range_g':extra_cf,'reserve_after_range_g':reserve_after},'gates':{'all_required_present':all(doc.getObject(n) is not None for n in req),'heavy_root_fittings_absent':all(doc.getObject(n) is None for n in skip),'all_shapes_valid':all(o.Shape.isValid() for o in shape_objs),'reserve_after_ge_18g':min(reserve_after)>=18.0,'wing_material_lot_cert_open':True,'adhesive_bond_open':True,'root_fitting_coupon_open':True,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
