import FreeCAD as App, Part, os, json
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
src=os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')
out=os.path.join(BASE,'migration','freecad','freecad_v199_root_clearance_scan_audit.json')
d=App.openDocument(src);f=d.getObject('FUSELAGE_CURRENT').Shape;w=d.getObject('WING_R').Shape;y=w.BoundBox.YMin
verts=[v.Point for v in w.Vertexes if abs(v.Point.y-y)<1e-6]
rows=[]
for x in [490+i for i in range(31)]:
 line=Part.makeLine(App.Vector(x,y,-100),App.Vector(x,y,120));fz=sorted(v.Point.z for v in f.section(line).Vertexes)
 near=sorted(verts,key=lambda p:abs(p.x-x))[:6]; wz=[p.z for p in near if abs(p.x-x)<=3.2]
 if len(fz)>=2 and wz:
  base=min(wz)-min(fz);fit8=base-0.5455409752222806;omit2=base-0.9126608357680936
  rows.append({'x_mm':x,'fuselage_lower_z_mm':min(fz),'wing_lower_base_z_mm':min(wz),'base_clearance_mm':base,'fit8_clearance_mm':fit8,'omit2_clearance_mm':omit2})
crit=min(rows,key=lambda r:r['base_clearance_mm']) if rows else None
cross_fit=[r for r in rows if r['fit8_clearance_mm']<0]; cross_omit=[r for r in rows if r['omit2_clearance_mm']<0]
a={'status':'V199_ROOT_CLEARANCE_SCAN_490_520','inner_root_y_mm':y,'rows':rows,'critical_base':crit,'fit8_negative_x_range_mm':[min(r['x_mm'] for r in cross_fit),max(r['x_mm'] for r in cross_fit)] if cross_fit else None,'omit2_negative_x_range_mm':[min(r['x_mm'] for r in cross_omit),max(r['x_mm'] for r in cross_omit)] if cross_omit else None,'gates':{'screen_only':True,'absolute_pivot_WL_verified':False,'glove_surface_verified':False,'master_changed':False}}
open(out,'w',encoding='utf-8').write(json.dumps(a,indent=2));print(json.dumps({'status':a['status'],'samples':len(rows),'critical_base':crit,'fit8_negative_x_range_mm':a['fit8_negative_x_range_mm'],'omit2_negative_x_range_mm':a['omit2_negative_x_range_mm']},indent=2))
