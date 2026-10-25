import FreeCAD as App, Part, json, pathlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v208_SWEEP_PACKAGING_INTEGRATED.FCStd'
out=R/'migration/freecad/F14_v209_FIXED_GLOVE_STRUCTURAL_ENCLOSURE.FCStd'
aud=R/'migration/freecad/freecad_v209_fixed_glove_structural_enclosure_audit.json'
d=App.openDocument(str(src)); f=d.getObject('FUSELAGE_CURRENT').Shape; wr=d.getObject('WING_R').Shape; wl=d.getObject('WING_L').Shape
# Structural enclosure only, not production OML.
y_in=115.0; y_out=148.8263775443693; pad_bottom=-12.5; pad_skin_clear=1.0; wing_clear=1.0
xs=[482.346,488.346,496.346,504.346,512.346,520.346,526.346]
doc=App.newDocument('F14_v209_FIXED_GLOVE_STRUCTURAL_ENCLOSURE')
# context
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','V204_MONO_LOWER_R','V204_MONO_LOWER_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','V205_SWEEP_SERVO_SERVICE']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Label='[CTX] '+o.Label; q.Shape=o.Shape.copy()
rows=[]
for sgn,lab,wing in [(1,'R',wr),(-1,'L',wl)]:
 inner=[]; outer=[]
 for x in xs:
  # existing fuselage lower at inner attach
  line=Part.makeLine(App.Vector(x,sgn*y_in,-100),App.Vector(x,sgn*y_in,100)); sec=f.section(line); fz=min(v.Point.z for v in sec.Vertexes)
  # exact wing lower at outer rail if present, else use nearby root lower via vertical section
  linew=Part.makeLine(App.Vector(x,sgn*y_out,-100),App.Vector(x,sgn*y_out,100)); wsec=wing.section(linew)
  wz=min(v.Point.z for v in wsec.Vertexes) if wsec.Vertexes else 0.0
  # target below both moving wing and lower hardpoint by 1 mm
  z_outer=min(wz-wing_clear, pad_bottom-pad_skin_clear)
  inner.append(App.Vector(x,sgn*y_in,fz)); outer.append(App.Vector(x,sgn*y_out,z_outer))
  rows.append({'side':lab,'x_mm':x,'inner_fuselage_lower_z_mm':fz,'wing_lower_outer_z_mm':wz,'outer_skin_target_z_mm':z_outer,'pad_bottom_z_mm':pad_bottom,'wing_clearance_mm':wz-z_outer,'pad_clearance_mm':pad_bottom-z_outer,'lateral_slope_deg':math.degrees(math.atan2(abs(fz-z_outer),abs(y_out-y_in)))})
 iw=Part.makePolygon(inner); ow=Part.makePolygon(outer); surf=Part.makeRuledSurface(iw,ow)
 for name,shape in [('V209_INNER_ATTACH_'+lab,iw),('V209_OUTER_SKIN_RAIL_'+lab,ow),('V209_FIXED_GLOVE_UNDERSIDE_'+lab,surf)]:
  o=doc.addObject('PartDesign::Feature',name); o.Label=name+' / STRUCTURAL CANDIDATE NOT OML'; o.Shape=shape
m=doc.addObject('App::FeaturePython','V209_GATE');m.addProperty('App::PropertyString','Status');m.Status='FIXED GLOVE STRUCTURAL ENCLOSURE / ABSOLUTE Z OML STILL OPEN'
doc.recompute();doc.saveAs(str(out))
wingc=[r['wing_clearance_mm'] for r in rows]; padc=[r['pad_clearance_mm'] for r in rows]; slopes=[r['lateral_slope_deg'] for r in rows]
res={'status':'V209_FIXED_GLOVE_STRUCTURAL_ENCLOSURE','rows':rows,'wing_clearance_range_mm':[min(wingc),max(wingc)],'pad_clearance_range_mm':[min(padc),max(padc)],'lateral_slope_range_deg':[min(slopes),max(slopes)],'gates':{'wing_root_clearance_ge_1mm':min(wingc)>=0.999,'lower_pad_enclosed_with_1mm_clearance':min(padc)>=0.999,'all_shapes_valid':all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()),'absolute_Z_OML_verified':False,'production_OML':False,'print_release':False,'flight_release':False}}
aud.write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps(res,indent=2))
