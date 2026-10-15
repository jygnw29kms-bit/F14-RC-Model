import FreeCAD as App, Part, json, os, math
base=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(base,'F14_CURRENT_FULL_VIEW_v191.FCStd')
out=os.path.join(base,'F14_CURRENT_FULL_VIEW_v192.FCStd')
auditp=os.path.join(base,'freecad_v192_sweep_audit.json')
PX=613.1323905812828; PY=125.20927023775282

d=App.openDocument(src)
g=d.getObject('SWEEP_REFERENCE_v192') or d.addObject('App::DocumentObjectGroup','SWEEP_REFERENCE_v192'); g.Label='Wing sweep references 20-68 deg v192'
# base wings are the 20 degree source definition. Build transformed copies at 40/54/68 for both sides.
rows=[]
for sweep in (20,30,40,50,54,60,68):
    side_bounds={}
    for lab,sgn in [('R',1),('L',-1)]:
        basewing=d.getObject('WING_'+lab).Shape
        sh=basewing.copy()
        if sweep!=20:
            sh.rotate(App.Vector(PX,sgn*PY,0),App.Vector(0,0,1),-sgn*(sweep-20.0))
        b=sh.BoundBox
        side_bounds[lab]={'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax],'volume_mm3':sh.Volume,'valid':sh.isValid()}
        if sweep in (40,54,68):
            o=d.getObject('WING_%s_SWEEP_%02d'%(lab,sweep)) or d.addObject('PartDesign::Feature','WING_%s_SWEEP_%02d'%(lab,sweep))
            o.Label='Wing %s sweep %d deg reference'%(lab,sweep); o.Shape=sh; g.addObject(o)
    semi=max(abs(side_bounds['R']['y'][0]),abs(side_bounds['R']['y'][1]),abs(side_bounds['L']['y'][0]),abs(side_bounds['L']['y'][1]))
    rows.append({'sweep_deg':sweep,'span_mm':2*semi,'R':side_bounds['R'],'L':side_bounds['L'],'bilateral_volume_delta_mm3':abs(side_bounds['R']['volume_mm3']-side_bounds['L']['volume_mm3'])})
# symmetry checks use mirrored absolute bounds.
def sym(row,tol=1e-6):
    r=row['R']; l=row['L']
    return abs(r['x'][0]-l['x'][0])<tol and abs(r['x'][1]-l['x'][1])<tol and abs(r['z'][0]-l['z'][0])<tol and abs(r['z'][1]-l['z'][1])<tol and abs(r['y'][0]+l['y'][1])<tol and abs(r['y'][1]+l['y'][0])<tol
for row in rows: row['bilateral_symmetry_pass']=sym(row)
# source reference 38.2 ft fully swept, scaled by same 900 mm/Grumman tip-WBL full span source.
with open(r'C:/Users/dezen/Desktop/F14-RC-Model/cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json',encoding='utf-8') as f: wd=json.load(f)
factor=900.0/(2*wd['sections'][-1]['wbl_in'])
ref68=(38.2*12.0)*factor
row68=next(r for r in rows if r['sweep_deg']==68)
audit={'status':'FREECAD_V192_SOURCE_BACKED_SWEEP_KINEMATICS','pivot_local_mm':[PX,PY,0.0],'source_wing_baseline_deg':20,'rows':rows,'reference_68deg_span_mm_from_38p2ft_spec':ref68,'computed_68deg_span_mm':row68['span_mm'],'span68_discrepancy_mm':row68['span_mm']-ref68,'all_bilateral_symmetry_pass':all(r['bilateral_symmetry_pass'] for r in rows),'sweep_geometry_valid':all(r['R']['valid'] and r['L']['valid'] for r in rows),'body_glove_collision_verified':False,'mechanical_linkage_packaging_verified':False,'print_release':False,'flight_release':False}
d.recompute(); d.saveAs(out)
with open(auditp,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps({'status':audit['status'],'computed_68deg_span_mm':audit['computed_68deg_span_mm'],'reference_68deg_span_mm':ref68,'span68_discrepancy_mm':audit['span68_discrepancy_mm'],'all_bilateral_symmetry_pass':audit['all_bilateral_symmetry_pass'],'sweep_geometry_valid':audit['sweep_geometry_valid']},indent=2))
