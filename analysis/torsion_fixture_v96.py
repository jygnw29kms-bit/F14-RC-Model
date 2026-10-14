import json, pathlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
a=json.loads((R/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v94_representative_joint_coupon_audit.json').read_text())
inner=next(b for b in a['bodies'] if b['source_body']=='CANDIDATE_HOLLOW_WING_R_INNER_NO_JOINTS')
outer=next(b for b in a['bodies'] if b['source_body']=='CANDIDATE_HOLLOW_WING_R_OUTER_NO_JOINTS')
spar_axis_x=690.2779671799674
outer_center=(outer['bbox_mm']['x'][0]+outer['bbox_mm']['x'][1])/2
axis_rel=spar_axis_x-outer_center
plate={
 'fixed':{'x_mm':112,'y_mm':18,'z_mm':8,'bolt_x_mm':[-51,51],'bolt_y_mm':[-4,4],'hole_d_mm':4.6},
 'moving':{'x_mm':108,'y_mm':18,'z_mm':8,'bolt_x_mm':[-49,49],'bolt_y_mm':[-4,4],'hole_d_mm':4.6,
           'lug':{'x_start_mm':54,'x_length_mm':30,'y_mm':18,'z_mm':20,'m5_hole_d_mm':5.5,'m5_x_mm':[62,76],'m5_y_mm':0}},
 'pad':{'material':'2 mm EVA/neoprene or equivalent compliant sheet','nominal_thickness_mm':2.0,'rule':'use broad full-jaw pads; tighten only to prevent slip without crushing shell'},
}
bar_start_rel=54.0
load_rel=axis_rel+250.0
bar={'material':'aluminium flat bar','cross_section_mm':[20,3],'suggested_length_mm':200,'bar_start_x_relative_plate_center_mm':bar_start_rel,
     'anchor_hole_x_from_bar_start_mm':[62-bar_start_rel,76-bar_start_rel],
     'load_line_x_from_bar_start_mm':load_rel-bar_start_rel,
     'torque_axis_x_relative_plate_center_mm':axis_rel,
     'lever_arm_mm':250.0,
     'sf3_force_N':2.242176391340641/0.25,'proof_force_N':1.1210881956703205/0.25}
result={'status':'V96_TORSION_FIXTURE_GEOMETRY_PREPARED','source_v94':'F14_v94_representative_joint_coupon_audit.json','inner_skin_bbox_mm':inner['bbox_mm'],'outer_skin_bbox_mm':outer['bbox_mm'],'spar_axis_x_mm':spar_axis_x,'outer_skin_center_x_mm':outer_center,'fixture':plate,'lever':bar,'assembly':{'fixed_clamp_y_center_mm':353.9687853,'moving_clamp_y_center_mm':373.9687853,'joint_y_mm':363.9687853,'clamp_clearance_from_joint_mm':1.0},'gates':{'fixture_cad_created':False,'fixture_printed':False,'v93_process_passed':False,'representative_coupon_real_carbon_installed':False,'sf3_both_directions_passed':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False}}
(R/'analysis/torsion_fixture_v96.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
# 1:1 drilling template for 20x3x200 mm lever bar
m=10; L=200; W=20; sc=3.7795275591; width=(L+2*m)*sc; height=(W+2*m)*sc
holes=bar['anchor_hole_x_from_bar_start_mm']; load=bar['load_line_x_from_bar_start_mm']
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{L+2*m}mm" height="{W+2*m}mm" viewBox="0 0 {width:.3f} {height:.3f}">', '<rect width="100%" height="100%" fill="white"/>']
svg.append(f'<rect x="{m*sc:.3f}" y="{m*sc:.3f}" width="{L*sc:.3f}" height="{W*sc:.3f}" fill="none" stroke="black" stroke-width="0.7"/>')
cy=(m+W/2)*sc
for x in holes:
    cx=(m+x)*sc; svg.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{2.75*sc:.3f}" fill="none" stroke="black" stroke-width="0.7"/>')
cx=(m+load)*sc; svg.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{1.5*sc:.3f}" fill="none" stroke="black" stroke-width="0.7"/>')
svg.append(f'<text x="{m*sc:.3f}" y="{6*sc:.3f}" font-size="10">F14 v96 lever drill template 1:1 - M5.5 anchors + load line</text>')
svg.append('</svg>')
mdir=R/'manufacturing'/'torsion_fixture_v96'; mdir.mkdir(parents=True,exist_ok=True); (mdir/'F14_v96_200mm_lever_drill_template.svg').write_text('\n'.join(svg),encoding='utf-8')
print(json.dumps({'axis_rel_mm':axis_rel,'load_line_from_bar_start_mm':load,'sf3_force_N':bar['sf3_force_N'],'proof_force_N':bar['proof_force_N']},indent=2))