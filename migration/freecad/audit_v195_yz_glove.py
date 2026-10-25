import FreeCAD as App, json, os, math
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
path=os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')
d=App.openDocument(path)
rows={}
for n in ['WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L','WINGBOX_REF','FUSELAGE_CURRENT']:
 o=d.getObject(n); b=o.Shape.BoundBox; rows[n]={'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}
# sample wing root vertices near inner y edge
for n,sgn in [('WING_R',1),('WING_L',-1)]:
 o=d.getObject(n); verts=[v.Point for v in o.Shape.Vertexes]
 if sgn>0: inner=min(p.y for p in verts)
 else: inner=max(p.y for p in verts)
 tol=1.5
 near=[p for p in verts if abs(p.y-inner)<tol]
 rows[n]['inner_y']=inner
 rows[n]['inner_root_x']=[min(p.x for p in near),max(p.x for p in near)] if near else None
 rows[n]['inner_root_z']=[min(p.z for p in near),max(p.z for p in near)] if near else None
# fuselage bbox slice proxy around pivot x using vertices +/- 8mm
px=504.3463093769572
f=d.getObject('FUSELAGE_CURRENT'); pts=[v.Point for v in f.Shape.Vertexes if abs(v.Point.x-px)<8]
rows['FUSELAGE_PIVOT_VERTEX_PROXY']={'count':len(pts),'y':[min(p.y for p in pts),max(p.y for p in pts)] if pts else None,'z':[min(p.z for p in pts),max(p.z for p in pts)] if pts else None}
# CR172559 source-based rails at FS524.16 in current registered frame, interpolate from known quick geometry reference
cr=os.path.join(BASE,'migration','freecad','F14_CR172559_QUICK_GEOMETRY_REFERENCE.FCStd')
c=App.openDocument(cr)
features={}
for feat in ['FUP','FLO','SCPUP','SCPLO','MHB','CREASE']:
 rr=c.getObject(feat+'_R') or c.getObject('CR172559_'+feat+'_R')
 if rr:
  vs=[v.Point for v in rr.Shape.Vertexes]
  x= (524.16-93.0)*1.1697428086486623
  # nearest two by x and linear interpolate y,z
  vs=sorted(vs,key=lambda p:p.x)
  a,b=min(zip(vs[:-1],vs[1:]),key=lambda ab: abs((ab[0].x+ab[1].x)/2-x))
  t=0 if abs(b.x-a.x)<1e-9 else (x-a.x)/(b.x-a.x)
  features[feat]={'x_target':x,'y':a.y+t*(b.y-a.y),'z':a.z+t*(b.z-a.z)}
out={'status':'V195_YZ_GLOVE_SCREEN','v195':rows,'cr172559_at_FS524_16':features,'gates':{'X_supported':True,'Y_verified':False,'Z_verified':False,'glove_fit_verified':False,'master_changed':False}}
print(json.dumps(out,indent=2))
with open(os.path.join(BASE,'migration','freecad','freecad_v195_yz_glove_audit.json'),'w') as fh: json.dump(out,fh,indent=2)
