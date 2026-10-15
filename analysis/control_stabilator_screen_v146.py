"""Reproduce v145 stabilator geometry and v146 servo-torque sensitivity."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PTS=[(841.45,-209.79),(802.38,-224.73),(662.14,-104.09),(750.29,-72.06),(804.39,-76.33),(825.42,-112.63)]

def polygon_properties(points):
    A=Cx=Cy=0.0
    for i,(x,y) in enumerate(points):
        x2,y2=points[(i+1)%len(points)]; c=x*y2-x2*y
        A+=c; Cx+=(x+x2)*c; Cy+=(y+y2)*c
    A*=0.5
    return abs(A),Cx/(6*A),Cy/(6*A)

def run():
    area,cx,cy=polygon_properties(PTS)
    span=max(abs(y) for x,y in PTS)-min(abs(y) for x,y in PTS)
    geom={
      'status':'V145_STABILATOR_GEOMETRY_AND_CONTROL_ARCHITECTURE',
      'source':'cad/fusion/F14TomcatRC/F14TomcatRC.py / NASA CR-163098 Fig.4 calibrated plan view',
      'outline_mm':PTS,'one_side_area_mm2':area,'one_side_area_dm2':area/10000.0,
      'centroid_model_mm':[cx,cy],'lateral_span_mm':span,'area_over_span_mean_chord_mm':area/span,
      'architecture':{'left_stabilator_servo':'independent','right_stabilator_servo':'independent','mixing':'pitch + differential roll (taileron baseline)','wing_aileron_servos_baseline':False,'additional_roll_devices':'optional only if measured taileron roll authority is insufficient'},
      'mechanism_benchmark':'Freewing F-14 manual may be used for packaging/mechanism cross-check only; no Freewing dimensions override NASA/full-scale geometry.',
      'release':{'pivot_axis_verified':False,'roll_authority_verified':False,'servo_hardware_frozen':False,'flight_release':False}}
    (ROOT/'analysis/control_stabilator_geometry_v145.json').write_text(json.dumps(geom,indent=2),encoding='utf-8')
    rho=1.225; S=area/1e6; rows=[]
    for V in (30,40,50,60):
        q=0.5*rho*V*V
        for cn in (0.6,0.8,1.0):
            F=q*S*cn
            for arm in (5,10,15,20):
                mh=F*arm/1000.0
                servo=mh*(10.0/15.0)/0.70*2.0
                rows.append({'speed_mps':V,'speed_kmh':V*3.6,'dynamic_pressure_Pa':q,'normal_force_coefficient':cn,'surface_force_N':F,'effective_CP_offset_from_pivot_mm':arm,'hinge_moment_Nm':mh,'required_servo_torque_with_linkage_and_2x_factor_Nm':servo,'required_servo_torque_kgcm':servo*10.19716213})
    def pick(V,c,a): return next(x for x in rows if x['speed_mps']==V and x['normal_force_coefficient']==c and x['effective_CP_offset_from_pivot_mm']==a)
    out={'status':'V146_STABILATOR_SERVO_TORQUE_SENSITIVITY_NOT_RELEASED','source_geometry':'analysis/control_stabilator_geometry_v145.json','assumptions':{'air_density_kg_m3':rho,'servo_arm_mm':10,'stabilator_crank_mm':15,'linkage_effectiveness':0.70,'design_factor':2.0,'note':'CP offset is a sensitivity until source-backed stabilator pivot/hinge moment is verified.'},'screen_cases':rows,'hardware_class_screen':{'design_reference':pick(50,0.8,15),'severe_envelope':pick(60,1.0,20)},'decision':{'do_not_freeze_below_kgcm':6,'preferred_minimum_nominal_servo_torque_kgcm_before_dynamic_derating':14,'candidate_voltage':'7.4-8.4V HV preferred','metal_output_and_external_metal_stabilator_shaft_required':True},'release':{'pivot_axis_verified':False,'hinge_moment_verified':False,'servo_hardware_frozen':False,'bench_load_verified':False,'flutter_verified':False,'flight_release':False}}
    (ROOT/'analysis/control_stabilator_torque_v146.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'area_mm2':area,'design':out['hardware_class_screen']['design_reference'],'severe':out['hardware_class_screen']['severe_envelope']},indent=2))
if __name__=='__main__': run()
