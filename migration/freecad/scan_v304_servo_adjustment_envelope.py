import FreeCAD as App, Part, pathlib, json
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v303_DYNAMIC_STABILATOR_LINKAGE_SWEEP.FCStd'
v302=json.loads((R/'analysis/control_spatial_kinematics_v302.json').read_text(encoding='utf-8'))
d=App.openDocument(str(src)); oml=d.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
targetR=tuple(v302['best']['spline_axis_mm'])
rows=[]
for side,sgn in [('R',1),('L',-1)]:
    edf=d.getObject('V298_HOUSING_SKIN_SERVICE_'+side).Shape; fit=d.getObject('V284_LIGHT_D_ROOT_FITTING_'+side).Shape
    vals=[]
    for dx in (-2.0,0.0,2.0):
      for dyabs in (-2.0,0.0,2.0):
       for dz in (-1.0,0.0,1.0):
        cx=710.0+dx; ay=20.0+dyabs; cy=sgn*ay; cz=5.0+dz
        sh=Part.makeBox(27,31.5,16,App.Vector(cx-13.5,cy-15.75,cz-8))
        omfrac=sh.common(oml).Volume/sh.Volume; ed=sh.distToShape(edf)[0]; fd=sh.distToShape(fit)[0]
        target=(targetR[0],sgn*targetR[1],targetR[2]); local=[target[0]-cx,target[1]-cy,target[2]-cz]
        vals.append({'side':side,'shift_mm':[dx,dyabs,dz],'body_center_mm':[cx,cy,cz],'service_OML_fraction':omfrac,'service_EDF_clearance_mm':ed,'service_root_clearance_mm':fd,'required_local_spline_axis_offset_from_body_center_mm':local,'pass':omfrac>=0.999 and ed>=1.5})
    rows.append({'side':side,'positions':vals,'pass_count':sum(q['pass'] for q in vals)})
# A translation is bilateral only if the same dx, |dy| and dz passes on both sides.
def key(q): return tuple(q['shift_mm'])
maps=[{key(q):q for q in r['positions']} for r in rows]; common=[]
for k in sorted(set(maps[0]).intersection(maps[1])):
    r,l=maps[0][k],maps[1][k]
    common.append({'shift_mm':list(k),'R_pass':r['pass'],'L_pass':l['pass'],'bilateral_pass':r['pass'] and l['pass'],'min_OML_fraction':min(r['service_OML_fraction'],l['service_OML_fraction']),'min_EDF_clearance_mm':min(r['service_EDF_clearance_mm'],l['service_EDF_clearance_mm']),'min_root_clearance_mm':min(r['service_root_clearance_mm'],l['service_root_clearance_mm']),'required_local_spline_offset_abs_mm':[targetR[0]-(710+k[0]),targetR[1]-(20+k[1]),targetR[2]-(4+k[2])]})
passed=[q for q in common if q['bilateral_pass']]
# Check whether each requested axis adjustment is independently available while other axes remain nominal.
req={(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,1),(0,0,-1),(0,0,0)}
lookup={tuple(q['shift_mm']):q for q in common}
independent=all(tuple(map(float,k)) in lookup and lookup[tuple(map(float,k))]['bilateral_pass'] for k in req)
# Full 3x3x3 cube is stronger and directly supports a slotted mount without coupled restrictions.
fullcube=len(passed)==27
if passed:
    offs=[q['required_local_spline_offset_abs_mm'] for q in passed]
    offrange={'x_mm':[min(v[0] for v in offs),max(v[0] for v in offs)],'y_abs_mm':[min(v[1] for v in offs),max(v[1] for v in offs)],'z_mm':[min(v[2] for v in offs),max(v[2] for v in offs)]}
else: offrange={}
out={'status':'V304_TAIL_SERVO_ADJUSTMENT_ENVELOPE','source_model':src.name,'kinematic_target_axis_R_mm':targetR,'proposed_servo_body_center_R_mm':[710,20,5],'proposed_servo_body_center_L_mm':[710,-20,5],'recenter_from_v299_mm':[0,0,1],'service_dims_mm':[27,31.5,16],'tested_adjustments_mm':{'x':[-2,0,2],'abs_y':[-2,0,2],'z':[-1,0,1]},'acceptance':{'service_OML_fraction_min':0.999,'service_EDF_clearance_min_mm':1.5},'rows':rows,'bilateral_positions':common,'bilateral_pass_count':len(passed),'abs_local_spline_offset_range_absorbable_on_passing_grid':offrange,'gates':{'nominal_position_pass':lookup.get((0.0,0.0,0.0),{}).get('bilateral_pass',False),'independent_plusminus_2mm_XY_plusminus_1mm_Z_available':independent,'full_3x3x3_adjustment_cube_pass':fullcube,'actual_servo_spline_offset_measured':False,'mount_slot_geometry_created':False,'print_release':False,'flight_release':False}}
outp=R/'migration/freecad/freecad_v304_servo_adjustment_envelope_audit.json';outp.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'status':out['status'],'bilateral_pass_count':len(passed),'offset_range':offrange,'gates':out['gates'],'failures':[q for q in common if not q['bilateral_pass']]},indent=2))
