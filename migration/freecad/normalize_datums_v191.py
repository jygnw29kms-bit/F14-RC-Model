import FreeCAD as App, Part, math, json, os
BASE=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(BASE,'F14_CURRENT_FULL_VIEW_v190.FCStd')
out=os.path.join(BASE,'F14_CURRENT_FULL_VIEW_v191.FCStd')
auditp=os.path.join(BASE,'freecad_v191_datum_audit.json')
SHIFT=187.59240693460868
PX=613.1323905812828
PY=125.20927023775282

d=App.openDocument(src)

def section(x,half_w,ztop,zbot,frac):
    pts=[]
    if frac<0.30:
        n=48; cz=(ztop+zbot)*0.5; h=max(1,(ztop-zbot)*0.5); expo=2+max(0,(frac-0.18)/0.12)*0.6; pear=max(0,min(1,(frac-0.10)/0.18))*0.16
        for i in range(n):
            t=2*math.pi*i/n; ct,st=math.cos(t),math.sin(t); y=half_w*(-1 if ct<0 else 1)*(abs(ct)**(2/expo)); z=cz+h*(-1 if st<0 else 1)*(abs(st)**(2/2.15));
            if st<0: y*=1+pear*abs(st)
            pts.append((x,y,z))
    else:
        count=30; H=max(2,ztop-zbot); lobe=max(0,min(1,(frac-0.32)/0.18)); aft=max(0,min(1,(frac-0.68)/0.20))
        for i in range(count):
            u=-1+2*i/(count-1); edge_drop=H*(0.12+0.05*aft)*(abs(u)**2.8); center_crown=H*0.025*(1-aft)*math.exp(-(u/0.28)**2); pts.append((x,u*half_w,ztop-edge_drop+center_crown))
        for i in range(count):
            u=1-2*i/(count-1); ell=zbot+H*0.28*(1-math.sqrt(max(0,1-u*u))); bell=math.exp(-((abs(u)-0.55)/0.23)**2); twins=zbot+H*(0.36*(1-bell)); z=ell*(1-lobe)+twins*lobe; pts.append((x,u*half_w,z))
    return pts

def resample(pts,n=60):
    cyc=pts+[pts[0]]; seg=[]; total=0
    for a,b in zip(cyc[:-1],cyc[1:]):
        l=math.hypot(b[1]-a[1],b[2]-a[2]); seg.append(l); total+=l
    out=[]; j=0; acc=0
    for k in range(n):
        t=total*k/n
        while j<len(seg)-1 and acc+seg[j]<t: acc+=seg[j]; j+=1
        a,b=cyc[j],cyc[j+1]; u=0 if seg[j]==0 else (t-acc)/seg[j]
        out.append((a[0],a[1]+u*(b[1]-a[1]),a[2]+u*(b[2]-a[2])))
    return out

def wire(pts):
    v=[App.Vector(*p) for p in pts]; v.append(v[0]); return Part.makePolygon(v)
st=[(8.793,8.401,25.046,-23.248,0.010000),(38.507,19.602,36.703,-23.248,0.043793),(68.220,25.202,41.699,-24.913,0.077586),(97.934,32.670,53.357,-23.248,0.111379),(127.648,34.537,70.010,-23.248,0.145172),(157.362,38.270,81.667,-21.582,0.178966),(187.075,38.270,88.328,-21.582,0.212759),(216.789,38.270,89.993,-21.582,0.246552),(246.503,40.137,89.993,-19.917,0.280345),(276.216,83.075,86.663,-18.252,0.314138),(305.930,86.808,83.332,-16.586,0.347931),(335.644,96.143,76.671,-16.586,0.381724),(365.358,107.344,71.675,-14.921,0.415517),(395.071,120.411,65.014,-28.244,0.449310),(424.785,133.479,60.018,-31.574,0.483103),(454.499,144.680,56.687,-33.240,0.516897),(484.213,159.615,53.357,-34.905,0.550690),(513.926,159.615,56.687,-36.570,0.584483),(543.640,150.281,56.687,-36.570,0.618276),(573.354,135.346,53.357,-38.236,0.652069),(603.067,114.811,46.695,-39.901,0.685862),(632.781,109.210,45.030,-39.901,0.719655),(662.495,109.210,38.369,-39.901,0.753448),(692.209,112.944,45.030,-36.570,0.787241),(721.922,112.944,50.026,-34.905,0.821034),(751.636,112.944,51.691,-31.574,0.854828),(781.350,111.077,53.357,-29.909,0.888621),(811.064,105.477,51.691,-28.244,0.922414),(840.777,98.009,40.034,-24.913,0.956207),(870.491,19.602,33.373,-19.917,0.990000)]
sel=[0,2,4,6,8,9,11,13,15,17,19,21,23,25,27,29]
w=[wire(resample(section(0.5,0.8,1,-1,0),60))]
for i in sel: w.append(wire(resample(section(*st[i]),60)))
w.append(wire(resample(section(879,1.2,1.2,-1.2,1),60)))
fuse=Part.makeLoft(w,True,True)
d.getObject('FUSELAGE_CURRENT').Shape=fuse
d.getObject('FUSELAGE_CURRENT').Label='F14 source-derived fuselage / ruled station loft v191'
# Move source-WL items into registered local fuselage CAD frame.
for name in ['WING_R','WING_L','BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','BATTERY_RETENTION_HOLE_REFS']:
    o=d.getObject(name)
    if o:
        pl=o.Placement; pl.Base=App.Vector(pl.Base.x,pl.Base.y,pl.Base.z-SHIFT); o.Placement=pl
# Correct pivot/wingbox references to source-backed FS/BL, local z=0.
wb=d.getObject('WINGBOX_REF'); wb.Shape=Part.makeBox(83.0,2*(PY+28.0),26.0,App.Vector(PX-38.0,-PY-28.0,-13.0)); wb.Label='Source-backed pivot wingbox engineering envelope v191'
for sgn,lab in [(1,'R'),(-1,'L')]:
    o=d.getObject('PIVOT_REF_'+lab); o.Shape=Part.makeCylinder(12.0,26.0,App.Vector(PX,sgn*PY,-13.0),App.Vector(0,0,1)); o.Label='Source-backed wing pivot '+lab+' v191'
# Datum metadata object.
meta=d.getObject('DATUM_V191') or d.addObject('App::FeaturePython','DATUM_V191'); meta.Label='V191 common local CAD datum';
for prop in [('SourceWLtoLocalZShift','App::PropertyLength'),('PivotX','App::PropertyLength'),('PivotAbsY','App::PropertyLength')]:
    if not hasattr(meta,prop[0]): meta.addProperty(prop[1],prop[0],'Datum')
meta.SourceWLtoLocalZShift=SHIFT; meta.PivotX=PX; meta.PivotAbsY=PY

d.recompute(); d.saveAs(out)
# Audit key bounds and sanity.
keys=['FUSELAGE_CURRENT','WING_R','WING_L','INLET_EDF_R','INLET_EDF_L','BATTERY_TRAY_v165','STABILATOR_R','STAB_SHAFT_R','WINGBOX_REF','PIVOT_REF_R']
rows=[]
for n in keys:
    o=d.getObject(n); b=o.Shape.BoundBox
    rows.append({'name':n,'valid':o.Shape.isValid(),'solids':len(o.Shape.Solids),'bounds_mm':{'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]}})
audit={'status':'FREECAD_V191_COMMON_LOCAL_DATUM','source_wl_to_local_z_shift_mm':-SHIFT,'registered_fuselage_shift_evidence_mm':SHIFT,'source_backed_pivot_local_mm':[PX,PY,0.0],'fuselage_ruled_station_loft':True,'records':rows,'common_fuselage_wing_datum_engineering_registered':True,'source_traceable_absolute_waterline_still_not_flight_released':True,'print_release':False,'flight_release':False}
with open(auditp,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps(audit,indent=2))
