import FreeCAD as App, Part, os, json, hashlib
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
src=os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')
out=os.path.join(BASE,'migration','freecad','F14_v198_PIVOT_STATION_VERTICAL_CLEARANCE_REVIEW.FCStd')
auditp=os.path.join(BASE,'migration','freecad','freecad_v198_pivot_station_vertical_clearance_review_audit.json')
x=504.3463093769572
cases=[('BASE',0.0),('FIT8',-0.5455409752222806),('OMIT2',-0.9126608357680936)]
s=App.openDocument(src);f=s.getObject('FUSELAGE_CURRENT').Shape;wr=s.getObject('WING_R').Shape;wl=s.getObject('WING_L').Shape
# plane normal X at pivot station
plane=Part.makePlane(900,300,App.Vector(x,-450,-120),App.Vector(1,0,0))
d=App.newDocument('F14_v198_PIVOT_STATION_VERTICAL_CLEARANCE_REVIEW')
def add(name,label,shape):
 o=d.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape;return o
fsec=f.section(plane);add('FUSELAGE_SECTION','Fuselage section @ pivot X',fsec)
rows=[]
for tag,dz in cases:
 for side,sh in [('R',wr),('L',wl)]:
  c=sh.copy();c.translate(App.Vector(0,0,dz));sec=c.section(plane);add(f'WING_{tag}_{side}',f'Wing {side} {tag} dz={dz:.3f}mm',sec)
# critical vertical line at inner root Y right
inner_y=wr.BoundBox.YMin
line=Part.makeLine(App.Vector(x,inner_y,-80),App.Vector(x,inner_y,100));add('CRITICAL_LINE_R',f'Critical root line Y={inner_y:.3f}',line)
# compute exact section intervals on this line
fz=sorted(v.Point.z for v in f.section(line).Vertexes)
verts=[v.Point for v in wr.Vertexes if abs(v.Point.y-inner_y)<1e-6]
near=sorted(verts,key=lambda p:abs(p.x-x))[:8];wz=[p.z for p in near if abs(p.x-x)<4.0]
for tag,dz in cases:
 lo=min(wz)+dz;hi=max(wz)+dz; lower_clear=lo-min(fz) if len(fz)>=2 else None; upper_clear=max(fz)-hi if len(fz)>=2 else None
 rows.append({'case':tag,'delta_z_mm':dz,'fuselage_z_mm':[min(fz),max(fz)],'wing_z_mm':[lo,hi],'lower_clearance_mm':lower_clear,'upper_clearance_mm':upper_clear,'vertically_contained':bool(lower_clear is not None and lower_clear>=0 and upper_clear>=0)})
# clearance markers at critical line
for i,r in enumerate(rows):
 z=r['wing_z_mm'][0]; add('LOWER_POINT_'+r['case'],f"{r['case']} lower wing z={z:.3f}",Part.makeSphere(2.0,App.Vector(x,inner_y,z)))
add('FUSE_LOWER_POINT',f'Fuselage lower z={min(fz):.3f}',Part.makeSphere(2.0,App.Vector(x,inner_y,min(fz))))
d.recompute();d.saveAs(out)
a={'status':'V198_PIVOT_STATION_VERTICAL_CLEARANCE_REVIEW','pivot_x_mm':x,'inner_root_y_mm':inner_y,'rows':rows,'finding':'v195 base has only ~0.056 mm lower geometric clearance at pivot station; downward WL sensitivity cases cross below the current source-derived fuselage interval.','gates':{'section_screen_only':True,'absolute_pivot_WL_verified':False,'glove_3D_verified':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(open(out,'rb').read()).hexdigest()}
open(auditp,'w',encoding='utf-8').write(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
