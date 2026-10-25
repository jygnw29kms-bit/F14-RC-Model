import FreeCAD as App, Part, os, json
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
src=os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')
out=os.path.join(BASE,'migration','freecad','freecad_v197_root_vertical_containment_audit.json')
d=App.openDocument(src)
f=d.getObject('FUSELAGE_CURRENT').Shape
w=d.getObject('WING_R').Shape
inner_y=w.BoundBox.YMin
cases=[('BASE',0.0),('FIT8',-0.5455409752222806),('OMIT2',-0.9126608357680936)]
xs=[479.4839172711096,504.3463093769572,550.0,600.0,627.4150906440201]
rows=[]
for x in xs:
    line=Part.makeLine(App.Vector(x,inner_y,-120),App.Vector(x,inner_y,140))
    sec=f.section(line)
    zs=sorted([v.Point.z for v in sec.Vertexes])
    # wing vertices near x on inner root
    verts=[v.Point for v in w.Vertexes if abs(v.Point.y-inner_y)<1e-6]
    near=sorted(verts,key=lambda p:abs(p.x-x))[:8]
    wz=[p.z for p in near if abs(p.x-x)<4.0]
    if not wz and near: wz=[p.z for p in near[:2]]
    row={'x_mm':x,'inner_y_mm':inner_y,'fuselage_intersections_z_mm':zs,'wing_base_near_z_mm':[min(wz),max(wz)] if wz else None,'cases':[]}
    for name,dz in cases:
        if wz:
            lo=min(wz)+dz;hi=max(wz)+dz
            inside=False
            if len(zs)>=2:
                inside=(lo>=min(zs) and hi<=max(zs))
            row['cases'].append({'case':name,'delta_z_mm':dz,'wing_z_mm':[lo,hi],'inside_fuselage_vertical_interval':inside})
    rows.append(row)
a={'status':'V197_ROOT_VERTICAL_CONTAINMENT_SCREEN','method':'vertical line section through v195 fuselage at inner wing-root Y; wing Z sampled from nearest root vertices','rows':rows,'gates':{'shape_section_screen_only':True,'absolute_pivot_WL_verified':False,'glove_surface_verified':False,'master_changed':False,'production_release':False}}
open(out,'w',encoding='utf-8').write(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
