import FreeCAD as App, json, os
base=os.path.dirname(os.path.abspath(__file__))
fc=os.path.join(base,'F14_v187_FreeCAD_Native_Rebuild.FCStd')
out=os.path.join(base,'freecad_v188_wall_audit.json')
d=App.openDocument(fc)
rows=[]
for side in ('R','L'):
    o=d.getObject('ADAPTER_'+side)
    curves=[f for f in o.Shape.Faces if type(f.Surface).__name__!='Plane']
    planes=[f for f in o.Shape.Faces if type(f.Surface).__name__=='Plane']
    if len(curves)!=2 or len(planes)!=2:
        raise RuntimeError('unexpected adapter faces '+side)
    gap=curves[0].distToShape(curves[1])[0]
    fan=max(planes,key=lambda f:f.BoundBox.XMax)
    # two circular boundary edges on the fan face
    radii=[]
    for e in fan.Edges:
        c=e.Curve
        if hasattr(c,'Radius'):
            radii.append(float(c.Radius))
    radii=sorted(radii,reverse=True)
    fan_gap=(radii[0]-radii[1]) if len(radii)==2 else None
    rows.append(dict(side=side,native_minimum_curved_face_gap_mm=gap,minimum_0p8mm_screen_pass=gap>=0.8,fan_face_radii_mm=radii,fan_face_radial_gap_mm=fan_gap,fan_face_0p8mm_screen_pass=(fan_gap is not None and fan_gap>=0.8),adapter_valid=o.Shape.isValid(),adapter_solids=len(o.Shape.Solids)))
audit=dict(status='FREECAD_V188_NATIVE_WALL_THICKNESS_SCREEN',source_fcstd=fc,measurements=rows,bilateral_minimum_0p8mm_pass=all(r['minimum_0p8mm_screen_pass'] and r['fan_face_0p8mm_screen_pass'] for r in rows),minimum_release_screen_mm=0.8,freecad_native_verified=True,actual_print_tested=False,aerodynamic_smoothness_verified=False,print_release=False,flight_release=False)
with open(out,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps(audit,indent=2))
