import json, pathlib, math, csv
R=pathlib.Path(r"C:\Users\dezen\Desktop\F14-RC-Model")
v63=json.loads((R/'analysis/source_spar_section_properties_v63.json').read_text())
v94=json.loads((R/'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v94_representative_joint_coupon_audit.json').read_text())
st=v63['stations']
y0,y1=map(float,v94['crop_y_mm']); yj=float(v94['source']['joint_y_mm']) if 'joint_y_mm' in v94.get('source',{}) else 363.9687853

def interp(y,keyfn):
    for a,b in zip(st[:-1],st[1:]):
        ya,yb=a['model_y_mm'],b['model_y_mm']
        if ya<=y<=yb:
            t=(y-ya)/(yb-ya)
            return keyfn(a)+(keyfn(b)-keyfn(a))*t
    raise ValueError(y)

def vals(y):
    return {
      'y_mm':y,
      'cap_width_mm':interp(y,lambda s:s['width_mm']),
      'total_height_mm':interp(y,lambda s:s['shifted_and_trimmed']['total_height_mm']),
      'web_height_mm':interp(y,lambda s:s['shifted_and_trimmed']['web_height_mm']),
      'cap_centroid_separation_mm':interp(y,lambda s:s['shifted_and_trimmed']['cap_centroid_separation_mm']),
      'web_area_mm2':interp(y,lambda s:s['shifted_and_trimmed']['web_area_mm2']),
    }
for y in (y0,yj,y1):
    v=vals(y); v['implied_web_thickness_mm']=v['web_area_mm2']/v['web_height_mm']; print(json.dumps(v,indent=2))

# dense cut template every 2 mm
ys=[]; y=y0
while y<y1-1e-9: ys.append(round(y,6)); y+=2.0
ys.append(y1)
rows=[]
for y in ys:
    v=vals(y); v['implied_web_thickness_mm']=v['web_area_mm2']/v['web_height_mm']; rows.append(v)
mdir=R/'manufacturing'/'carbon_v95'; mdir.mkdir(parents=True,exist_ok=True)
with open(mdir/'F14_v95_coupon_carbon_dimensions.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
# SVG cap-strip top view at 1:1: x=Y distance; width vertical. add 10mm scale bar, text labels only outside pattern
scale=3.7795275591 # px/mm at 96dpi
margin=12
pts_top=[]; pts_bot=[]
for row in rows:
    x=(row['y_mm']-y0)*scale+margin*scale; half=row['cap_width_mm']/2*scale; cy=20*scale
    pts_top.append((x,cy-half)); pts_bot.append((x,cy+half))
poly=pts_top+list(reversed(pts_bot))
points=' '.join(f'{x:.3f},{y:.3f}' for x,y in poly)
wpx=(40+2*margin)*scale; hpx=40*scale
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{40+2*margin}mm" height="40mm" viewBox="0 0 {wpx:.3f} {hpx:.3f}">\n<rect x="0" y="0" width="100%" height="100%" fill="white"/>\n<polygon points="{points}" fill="none" stroke="black" stroke-width="0.7"/>\n<line x1="{margin*scale:.3f}" y1="{34*scale:.3f}" x2="{(margin+10)*scale:.3f}" y2="{34*scale:.3f}" stroke="black" stroke-width="1"/>\n<text x="{margin*scale:.3f}" y="{38*scale:.3f}" font-size="10">10 mm scale</text>\n<text x="{margin*scale:.3f}" y="{5*scale:.3f}" font-size="10">F14 v95 cap strip coupon template - 1:1</text>\n</svg>'''
(mdir/'F14_v95_coupon_cap_strip_template.svg').write_text(svg,encoding='utf-8')
# torsion fixture loads
Tsf3=2.242176391340641
Tproof=1.1210881956703205
arms=[0.10,0.15,0.20,0.25,0.30]
fixture=[]
for arm in arms:
    fixture.append({'lever_arm_mm':arm*1000,'sf3_force_N':Tsf3/arm,'sf3_equivalent_kgf':Tsf3/arm/9.80665,'proof_force_N':Tproof/arm,'proof_equivalent_kgf':Tproof/arm/9.80665})
result={
 'status':'V95_CARBON_FABRICATION_AND_TORSION_FIXTURE_PLAN',
 'source_v63':'analysis/source_spar_section_properties_v63.json',
 'source_v94':'workspace/RC-F14-Tomcat/Fusion/Exports/Current/source_shell_v53/F14_v94_representative_joint_coupon_audit.json',
 'coupon_y_range_mm':[y0,y1],
 'coupon_length_mm':y1-y0,
 'local_sections':[dict(vals(y),implied_web_thickness_mm=vals(y)['web_area_mm2']/vals(y)['web_height_mm']) for y in (y0,yj,y1)],
 'candidate_carbon_build':{
   'upper_cap':'1.0 mm nominal carbon laminate/strip cut to v95 taper; candidate only until stock/material verified',
   'lower_cap':'same as upper cap',
   'web':'~0.8 mm nominal carbon laminate/web cut to local web-height taper; candidate only until stock/material verified',
   'coupon_length_mm':y1-y0,
   'critical_rule':'do not replace real carbon with printed polymer for structural qualification',
 },
 'torsion_fixture':{
   'sacrificial_joint_target_Nm':Tsf3,
   'flight_article_proof_target_Nm':Tproof,
   'lever_options':fixture,
   'recommended_coupon_lever_arm_mm':250,
   'recommended_sf3_force_N':Tsf3/0.25,
   'recommended_sf3_equivalent_kgf':Tsf3/0.25/9.80665,
   'recommended_flight_proof_force_N':Tproof/0.25,
   'recommended_flight_proof_equivalent_kgf':Tproof/0.25/9.80665,
   'fixture_rules':['clamp/support the skin coupon in broad conformal cradles, not point clamps','apply torque about the spar/joint axis with a rigid lever','measure lever arm from torque axis to load line','load both torsional directions','use a load cell or securely constrained calibrated force source','inspect for slip, cracks, whitening, bond separation and permanent set'],
 },
 'gates':{'actual_carbon_stock_selected':False,'carbon_template_fit_verified':False,'v93_bond_process_verified':False,'representative_joint_built_with_real_carbon':False,'representative_joint_sf3_torsion_verified':False,'flight_article_proof_verified':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False}
}
(R/'analysis/carbon_fabrication_v95.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('250mm SF3 N/kgf',Tsf3/.25,Tsf3/.25/9.80665)
print('250mm proof N/kgf',Tproof/.25,Tproof/.25/9.80665)