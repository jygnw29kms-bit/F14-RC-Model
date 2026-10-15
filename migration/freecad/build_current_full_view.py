import FreeCAD as App, Part, json, math, os
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
OUT=os.path.join(BASE,'migration','freecad','F14_CURRENT_FULL_VIEW.FCStd')

def wire_xyz(points):
    pts=[App.Vector(*p) for p in points]
    if pts[0].distanceToPoint(pts[-1])>1e-9: pts.append(pts[0])
    return Part.makePolygon(pts)

def add_shape(doc,name,label,shape,color=None,transparency=0):
    o=doc.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=shape
    return o

def fuselage_section(x,half_w,ztop,zbot,frac):
    pts=[]
    if frac < 0.30:
        n=24; cz=(ztop+zbot)*0.5; h=max(1.0,(ztop-zbot)*0.5)
        expo=2.0+max(0.0,(frac-0.18)/0.12)*0.6; pear=max(0.0,min(1.0,(frac-0.10)/0.18))*0.16
        for i in range(n):
            t=2*math.pi*i/n; ct,st=math.cos(t),math.sin(t)
            y=half_w*(-1 if ct<0 else 1)*(abs(ct)**(2.0/expo))
            z=cz+h*(-1 if st<0 else 1)*(abs(st)**(2.0/2.15))
            if st<0: y*=1.0+pear*abs(st)
            pts.append((x,y,z))
    else:
        count=15; H=max(2.0,ztop-zbot); lobe=max(0.0,min(1.0,(frac-0.32)/0.18)); aft=max(0.0,min(1.0,(frac-0.68)/0.20))
        for i in range(count):
            u=-1+2*i/(count-1); edge_drop=H*(0.12+0.05*aft)*(abs(u)**2.8); center_crown=H*0.025*(1-aft)*math.exp(-(u/0.28)**2)
            pts.append((x,u*half_w,ztop-edge_drop+center_crown))
        for i in range(count):
            u=1-2*i/(count-1); ell=zbot+H*0.28*(1-math.sqrt(max(0,1-u*u))); bell=math.exp(-((abs(u)-0.55)/0.23)**2); twins=zbot+H*(0.36*(1-bell)); z=ell*(1-lobe)+twins*lobe
            pts.append((x,u*half_w,z))
    return pts

st=[
(8.793,8.401,25.046,-23.248,0.010000),(38.507,19.602,36.703,-23.248,0.043793),(68.220,25.202,41.699,-24.913,0.077586),(97.934,32.670,53.357,-23.248,0.111379),(127.648,34.537,70.010,-23.248,0.145172),(157.362,38.270,81.667,-21.582,0.178966),(187.075,38.270,88.328,-21.582,0.212759),(216.789,38.270,89.993,-21.582,0.246552),(246.503,40.137,89.993,-19.917,0.280345),(276.216,83.075,86.663,-18.252,0.314138),(305.930,86.808,83.332,-16.586,0.347931),(335.644,96.143,76.671,-16.586,0.381724),(365.358,107.344,71.675,-14.921,0.415517),(395.071,120.411,65.014,-28.244,0.449310),(424.785,133.479,60.018,-31.574,0.483103),(454.499,144.680,56.687,-33.240,0.516897),(484.213,159.615,53.357,-34.905,0.550690),(513.926,159.615,56.687,-36.570,0.584483),(543.640,150.281,56.687,-36.570,0.618276),(573.354,135.346,53.357,-38.236,0.652069),(603.067,114.811,46.695,-39.901,0.685862),(632.781,109.210,45.030,-39.901,0.719655),(662.495,109.210,38.369,-39.901,0.753448),(692.209,112.944,45.030,-36.570,0.787241),(721.922,112.944,50.026,-34.905,0.821034),(751.636,112.944,51.691,-31.574,0.854828),(781.350,111.077,53.357,-29.909,0.888621),(811.064,105.477,51.691,-28.244,0.922414),(840.777,98.009,40.034,-24.913,0.956207),(870.491,19.602,33.373,-19.917,0.990000)]
selected=[0,2,4,6,8,9,11,13,15,17,19,21,23,25,27,29]
wires=[wire_xyz(fuselage_section(0.5,0.8,1,-1,0.0))]
for idx in selected: wires.append(wire_xyz(fuselage_section(*st[idx])))
wires.append(wire_xyz(fuselage_section(879.0,1.2,1.2,-1.2,1.0)))
fuselage=Part.makeLoft(wires,True,False)

doc=App.newDocument('F14_CURRENT_FULL_VIEW')
outer=doc.addObject('App::DocumentObjectGroup','OUTER_AIRFRAME'); outer.Label='01 OUTER AIRFRAME / CURRENT SOURCE VIEW'
tech=doc.addObject('App::DocumentObjectGroup','TECH_CURRENT'); tech.Label='02 CURRENT ENGINEERING GEOMETRY'
ref=doc.addObject('App::DocumentObjectGroup','REFERENCE'); ref.Label='03 REFERENCE / NOT RELEASED'
body=add_shape(doc,'FUSELAGE_CURRENT','F14 current source-derived fuselage',fuselage,(0.72,0.74,0.78),15); outer.addObject(body)

# Wings from current Grumman/NASA source table
with open(os.path.join(BASE,'cad','fusion','F14TomcatRC','NASA_F14_basic_wing_v08.json'),encoding='utf-8') as f: wd=json.load(f)
factor=900.0/(2*wd['sections'][-1]['wbl_in'])
for label,sgn in [('R',1),('L',-1)]:
    ws=[]
    for sec in wd['sections']:
        y=sgn*sec['wbl_in']*factor; chord=sec['trailing_edge_fs_in']-sec['leading_edge_fs_in']; rows=sec['ordinates_xc_upper_lower']
        contour=[(x,u) for x,u,l in rows]+[(x,l) for x,u,l in rows[:0:-1]]
        pts=[((sec['leading_edge_fs_in']+x*chord)*factor,y,(sec['reference_vertical_wl_in']+z*chord)*factor) for x,z in contour]
        ws.append(wire_xyz(pts))
    sh=Part.makeLoft(ws,True,False); o=add_shape(doc,'WING_'+label,'F14 source wing '+label+' (20 deg source)',sh,(0.82,0.82,0.84),5); outer.addObject(o)

# Stabilators
stabL=[(841.45,-209.79),(802.38,-224.73),(662.14,-104.09),(750.29,-72.06),(804.39,-76.33),(825.42,-112.63)]
for lab,pts2 in [('L',stabL),('R',[(x,-y) for x,y in stabL])]:
    face=Part.Face(wire_xyz([(x,y,-2.75) for x,y in pts2])); sh=face.extrude(App.Vector(0,0,5.5)); o=add_shape(doc,'STABILATOR_'+lab,'Stabilator '+lab,sh,(0.78,0.78,0.80),5); outer.addObject(o)
# vertical tails
vt=[(595.5,18.9),(690.0,124.4),(725.3,135.6),(742.8,-5.6)]
for sgn,lab in [(-1,'L'),(1,'R')]:
    y=sgn*78.0-2.25; face=Part.Face(wire_xyz([(x,y,z) for x,z in vt])); sh=face.extrude(App.Vector(0,4.5,0)); o=add_shape(doc,'VTAIL_'+lab,'Vertical tail '+lab,sh,(0.76,0.76,0.79),5); outer.addObject(o)
# ventral fins
sf=900.0/1629.17; vf_len=239.75*sf; vf_depth=35.39*sf; x0=690.0; vf=[(x0,-31.0),(x0+0.15*vf_len,-31.0-vf_depth),(x0+0.92*vf_len,-31.0-0.25*vf_depth),(x0+vf_len,-31.0)]
for sgn,lab in [(-1,'L'),(1,'R')]:
    y=sgn*76.0-1.6; face=Part.Face(wire_xyz([(x,y,z) for x,z in vf])); sh=face.extrude(App.Vector(0,3.2,0)); o=add_shape(doc,'VENTRAL_'+lab,'Ventral fin '+lab,sh,(0.76,0.76,0.79),5); outer.addObject(o)

# Copy current v187 joined inlet/EDF geometry
srcpath=os.path.join(BASE,'migration','freecad','F14_v187_FreeCAD_Native_Rebuild.FCStd')
src=App.openDocument(srcpath)
for lab in ['R','L']:
    candidates=[o for o in src.Objects if ('JOINED '+lab) in o.Label.upper() or ('JOINED_'+lab) in o.Name.upper()]
    if candidates:
        sh=candidates[0].Shape.copy(); o=add_shape(doc,'INLET_EDF_'+lab,'v187 joined inlet + EDF adapter '+lab,sh,(0.25,0.55,0.85),0); tech.addObject(o)
App.closeDocument(src.Name)

# Current reference pivot/wingbox envelope, kept transparent
px=456.5; py=131.0; pz=24.0
box=Part.makeBox(83.0,318.0,26.0,App.Vector(px-38,-159,pz-13))
o=add_shape(doc,'WINGBOX_REF','Wingbox/pivot engineering envelope (reference)',box,(0.9,0.55,0.2),80); ref.addObject(o)
for sgn,lab in [(1,'R'),(-1,'L')]:
    cyl=Part.makeCylinder(12.0,26.0,App.Vector(px,sgn*py,pz-13),App.Vector(0,0,1)); o=add_shape(doc,'PIVOT_REF_'+lab,'Wing pivot reference '+lab,cyl,(0.9,0.55,0.2),60); ref.addObject(o)

doc.recompute(); doc.saveAs(OUT)
print('SAVED',OUT)
print('OBJECTS',len(doc.Objects))

