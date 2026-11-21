from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];p=R/'analysis/v192_y300_short_sleeve_trade_study.json';d=json.loads(p.read_text());short=d['new_bond_length_each_mm'];long=d['old_bond_length_each_mm'];assert short==3.8 and long==9.8
rows=[]
for radius in [2.0,2.1]:
 a=2*math.pi*radius*short;b=2*math.pi*radius*long
 assert abs(a/b-d['new_to_old_bond_area_ratio'])<1e-14
 rows.append({'nominal_radius_mm':radius,'short_analytic_area_mm2':a,'long_analytic_area_mm2':b,'short_F_over_A_MPa_per_N':1/a,'long_F_over_A_MPa_per_N':1/b,'same_force_proxy_increase_factor':b/a})
out=R/'analysis/v192_short_sleeve_analytic_area_trade.json';assert not out.exists()
out.write_text(json.dumps({'status':'ANALYTIC_NOMINAL_CYLINDER_AREA_TRADE_CALCULATED_NOT_NATIVE_CONTACT_MEASUREMENT','source_report_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':rows,'short_to_long_area_ratio':short/long,'nominal_area_reduction_percent':100*(1-short/long),'limits':['Native short contact measurement still deferred while external CAD job active','F/A per1N is scalar bookkeeping, not actual curved shear/peel stress or joint capacity','No sleeve load assigned, no material allowable, stiffness sharing or strength acceptance','Do not add serial interface areas; each side assessed separately'],'print_release':False,'flight_release':False},indent=2)+'\n');print(rows)
