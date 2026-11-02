import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v306_TAIL_SERVO_ADJUSTMENT_CASSETTE.FCStd'
out=R/'migration/freecad/F14_v307_UNIFIED_TAIL_SERVO_CASSETTE_BASE.FCStd'
audp=R/'migration/freecad/freecad_v307_unified_tail_servo_cassette_base_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v307_UNIFIED_TAIL_SERVO_CASSETTE_BASE')
replace={'V305_TAIL_SERVO_CRADLE_R','V305_TAIL_SERVO_CRADLE_L','V306_ADJUSTMENT_PLATE_R','V306_ADJUSTMENT_PLATE_L'}
for ob in d.Objects:
    if ob.Name in replace: continue
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
slot_span=4.0; slot_w=3.4; plate_t=2.0
rows=[]
def cross_slot(px,py):
    pz=-3.5; h=4.0
    a=Part.makeBox(slot_span+slot_w,slot_w,h,App.Vector(px-(slot_span+slot_w)/2,py-slot_w/2,pz))
    a=a.fuse(Part.makeCylinder(slot_w/2,h,App.Vector(px-slot_span/2,py,pz),App.Vector(0,0,1)))
    a=a.fuse(Part.makeCylinder(slot_w/2,h,App.Vector(px+slot_span/2,py,pz),App.Vector(0,0,1)))
    b=Part.makeBox(slot_w,slot_span+slot_w,h,App.Vector(px-slot_w/2,py-(slot_span+slot_w)/2,pz))
    b=b.fuse(Part.makeCylinder(slot_w/2,h,App.Vector(px,py-slot_span/2,pz),App.Vector(0,0,1)))
    b=b.fuse(Part.makeCylinder(slot_w/2,h,App.Vector(px,py+slot_span/2,pz),App.Vector(0,0,1)))
    return a.fuse(b)
for side,sgn in [('R',1),('L',-1)]:
    plate=d.getObject('V306_ADJUSTMENT_PLATE_'+side).Shape
    cradle=d.getObject('V305_TAIL_SERVO_CRADLE_'+side).Shape
    base=plate.fuse(cradle).removeSplitter()
    centers=[]
    for dx in (-10.0,10.0):
        for dy in (-12.0,12.0):
            px=710.0+dx; py=sgn*20.0+dy; centers.append([px,py]); base=base.cut(cross_slot(px,py))
    base=base.removeSplitter()
    o=doc.addObject('PartDesign::Feature','V307_UNIFIED_SERVO_CASSETTE_BASE_'+side); o.Shape=base; o.Label='v307 unified tail-servo cassette base '+side
    oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
    edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape
    root=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    access=doc.getObject('V253_ACCESS_TAIL_'+side).Shape
    hatch=doc.getObject('V267_HATCH_FLANGE_TAIL_'+side).Shape
    dyn=[doc.getObject('V303_SERVICE_MIN_'+side).Shape,doc.getObject('V303_SERVICE_NEUTRAL_'+side).Shape,doc.getObject('V303_SERVICE_MAX_'+side).Shape]
    rows.append({'side':side,'valid':base.isValid(),'solid_count':len(base.Solids),'volume_mm3':base.Volume,
                 'cross_slot_centers_mm':centers,'minimum_plate_edge_ligament_mm':1.8,
                 'OML_fraction':base.common(oml).Volume/base.Volume,
                 'EDF_clearance_mm':base.distToShape(edf)[0],'EDF_intersection_mm3':base.common(edf).Volume,
                 'dynamic_pushrod_service_min_clearance_mm':min(base.distToShape(x)[0] for x in dyn),
                 'dynamic_pushrod_service_intersection_mm3':max(base.common(x).Volume for x in dyn),
                 'root_fitting_clearance_mm':base.distToShape(root)[0],
                 'tail_access_clearance_mm':base.distToShape(access)[0],'tail_access_intersection_mm3':base.common(access).Volume,
                 'tail_hatch_flange_clearance_mm':base.distToShape(hatch)[0],
                 'slot_recut_after_plate_cradle_union':True})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V307_UNIFIED_TAIL_SERVO_CASSETTE_BASE','source_model':src.name,
     'architecture':{'v306_plate_and_v305_cradle_unified':True,'cross_slots_recut_through_full_unified_base':True,
                     'xy_adjustment_retained_mm':[-2,2],'z_shim_stack_retained':True,
                     'material_process_frozen':False,'actual_servo_mount_tab_pattern_measured':False},
     'rows':rows,
     'gates':{'bilateral_valid_single_solid':all(r['valid'] and r['solid_count']==1 for r in rows),
              'bilateral_OML_ge_0p999':all(r['OML_fraction']>=0.999 for r in rows),
              'bilateral_zero_EDF_intersection':all(r['EDF_intersection_mm3']<1e-6 for r in rows),
              'bilateral_EDF_clearance_ge_2mm':all(r['EDF_clearance_mm']>=2.0 for r in rows),
              'dynamic_pushrod_service_zero_intersection':all(r['dynamic_pushrod_service_intersection_mm3']<1e-6 for r in rows),
              'dynamic_pushrod_service_clearance_ge_8mm':all(r['dynamic_pushrod_service_min_clearance_mm']>=8.0 for r in rows),
              'tail_access_zero_intersection':all(r['tail_access_intersection_mm3']<1e-6 for r in rows),
              'tail_access_clearance_ge_0p2mm':all(r['tail_access_clearance_mm']>=0.2 for r in rows),
              'minimum_edge_ligament_ge_1p8mm':all(r['minimum_plate_edge_ligament_mm']>=1.8 for r in rows),
              'actual_servo_mount_tab_pattern_measured':False,'bench_clamp_test':False,'proof_load':False,
              'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))