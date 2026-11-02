import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v305_RECENTERED_ADJUSTABLE_TAIL_SERVO.FCStd'
out=R/'migration/freecad/F14_v306_TAIL_SERVO_ADJUSTMENT_CASSETTE.FCStd'
audp=R/'migration/freecad/freecad_v306_tail_servo_adjustment_cassette_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v306_TAIL_SERVO_ADJUSTMENT_CASSETTE')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
rows=[]
# Candidate hardware: 4x M3 clamp points per servo, cross-slot +/-2 mm X/Y,
# 1 mm shim increments for -1/0/+1 mm Z relative to v305 nominal center.
slot_span=4.0; slot_w=3.4; washer_od=9.0; plate_t=2.0; shim_t=1.0
for side,sgn in [('R',1),('L',-1)]:
    cx=710.0; cy=sgn*20.0; cz=5.0
    # Lower cassette plate remains inside the proven v305 adjustment sweep.
    # Use the full proven v305 XY adjustment footprint as the cassette plate so
    # cross-slots retain a continuous material ligament around all four clamp points.
    plate=Part.makeBox(31.0,35.5,plate_t,App.Vector(cx-15.5,cy-17.75,cz-8.0))
    holes=[]; centers=[]
    for dx in (-10.0,10.0):
        for dy in (-12.0,12.0):
            px=cx+dx; py=cy+dy; pz=cz-8.5
            # cross-slot = orthogonal rounded capsules, allowing +/-2 mm X/Y travel.
            h1=Part.makeBox(slot_span+slot_w,slot_w,plate_t+1.0,App.Vector(px-(slot_span+slot_w)/2,py-slot_w/2,pz))
            h1=h1.fuse(Part.makeCylinder(slot_w/2,plate_t+1.0,App.Vector(px-slot_span/2,py,pz),App.Vector(0,0,1)))
            h1=h1.fuse(Part.makeCylinder(slot_w/2,plate_t+1.0,App.Vector(px+slot_span/2,py,pz),App.Vector(0,0,1)))
            h2=Part.makeBox(slot_w,slot_span+slot_w,plate_t+1.0,App.Vector(px-slot_w/2,py-(slot_span+slot_w)/2,pz))
            h2=h2.fuse(Part.makeCylinder(slot_w/2,plate_t+1.0,App.Vector(px,py-slot_span/2,pz),App.Vector(0,0,1)))
            h2=h2.fuse(Part.makeCylinder(slot_w/2,plate_t+1.0,App.Vector(px,py+slot_span/2,pz),App.Vector(0,0,1)))
            holes.append(h1.fuse(h2)); centers.append([px,py])
    for h in holes: plate=plate.cut(h)
    plate=plate.removeSplitter()
    # Nominal 1 mm shim. Removing it gives -1 mm Z, stacking a second gives +1 mm.
    shim=Part.makeBox(23.0,27.5,shim_t,App.Vector(cx-11.5,cy-13.75,cz-6.0-shim_t))
    po=doc.addObject('PartDesign::Feature','V306_ADJUSTMENT_PLATE_'+side); po.Shape=plate; po.Label='v306 tail servo XY adjustment plate '+side
    so=doc.addObject('PartDesign::Feature','V306_Z_SHIM_'+side); so.Shape=shim; so.Label='v306 1 mm removable servo Z shim '+side
    edf=doc.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape
    fit=doc.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    svc=doc.getObject('V305_TORQ_SERVICE_'+side).Shape
    sweep=doc.getObject('V305_ADJUSTMENT_SWEEP_'+side).Shape
    # Washer keepout envelopes at nominal screw stations. Their full OD must remain in OML and clear EDF.
    washers=[]
    for px,py in centers:
        washers.append(Part.makeCylinder(washer_od/2,1.0,App.Vector(px,py,cz-5.0),App.Vector(0,0,1)))
    washer_union=washers[0]
    for w in washers[1:]: washer_union=washer_union.fuse(w)
    rows.append({
        'side':side,'cross_slot_center_points_mm':centers,'slot_total_travel_xy_mm':[-2.0,2.0],
        'slot_width_mm':slot_w,'washer_od_mm':washer_od,'plate_thickness_mm':plate_t,
        'z_adjustment_mm':[-1.0,0.0,1.0],'shim_increment_mm':shim_t,
        'plate_valid':plate.isValid(),'plate_solid_count':len(plate.Solids),
        'plate_OML_fraction':plate.common(oml).Volume/plate.Volume,
        'shim_OML_fraction':shim.common(oml).Volume/shim.Volume,
        'plate_EDF_clearance_mm':plate.distToShape(edf)[0],
        'shim_EDF_clearance_mm':shim.distToShape(edf)[0],
        'plate_root_clearance_mm':plate.distToShape(fit)[0],
        'washer_keepout_OML_fraction':washer_union.common(oml).Volume/washer_union.Volume,
        'washer_keepout_EDF_clearance_mm':washer_union.distToShape(edf)[0],
        'service_to_plate_clearance_mm':svc.distToShape(plate)[0],
        'plate_inside_v305_adjustment_sweep_fraction':plate.common(sweep).Volume/plate.Volume
    })
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V306_TAIL_SERVO_ADJUSTMENT_CASSETTE','source_model':src.name,
     'architecture':{'xy_adjustment':'four M3 cross-slots per servo','xy_travel_each_axis_mm':[-2,2],
                     'z_adjustment':'removable 1 mm shim stack','z_positions_mm':[-1,0,1],
                     'candidate_fasteners':'4x M3 per servo with 9 mm washer keepout',
                     'servo_mount_tab_pattern_still_requires_measurement':True},
     'rows':rows,
     'gates':{'bilateral_adjustment_plate_valid_single_solid':all(r['plate_valid'] and r['plate_solid_count']==1 for r in rows),
              'plate_and_shim_OML_ge_0p999':all(r['plate_OML_fraction']>=0.999 and r['shim_OML_fraction']>=0.999 for r in rows),
              'plate_and_shim_EDF_clearance_ge_1p5mm':all(r['plate_EDF_clearance_mm']>=1.5 and r['shim_EDF_clearance_mm']>=1.5 for r in rows),
              'washer_keepout_OML_ge_0p999':all(r['washer_keepout_OML_fraction']>=0.999 for r in rows),
              'washer_keepout_EDF_clearance_ge_1p5mm':all(r['washer_keepout_EDF_clearance_mm']>=1.5 for r in rows),
              'plate_inside_v305_adjustment_sweep_ge_0p999':all(r['plate_inside_v305_adjustment_sweep_fraction']>=0.999 for r in rows),
              'physical_adjustment_slot_hardware_defined':True,
              'actual_servo_mount_tab_pattern_measured':False,
              'bench_adjustment_and_clamp_test':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))