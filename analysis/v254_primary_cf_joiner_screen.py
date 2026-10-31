import FreeCAD as App, Part, json, pathlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v253_SERVICE_ACCESS_KEEPOUTS.FCStd')); fus=d.getObject('FUSELAGE_CURRENT').Shape
hw=[]
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull() and any(k in o.Name for k in ['BATTERY','CASSETTE','SERVO','YOKE','EDF','ESC','CRADLE','ROOT_FITTING','CRANK']): hw.append((o.Name,o.Shape))
spec=[(220,30,20,-10,6,4,False),(440,38,60,-10,8,6,False),(620,40,15,30,8,6,True),(840,20,30,0,6,4,False)]
rows=[]
for x,hl,ay,z,od,id_,prov in spec:
 for sgn in (-1,1):
  y=sgn*ay; sh=Part.makeCylinder(od/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); inner=Part.makeCylinder(id_/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); tube=sh.cut(inner)
  frac=sh.common(fus).Volume/sh.Volume if sh.Volume else 0; ds=sorted((sh.distToShape(s)[0],n) for n,s in hw if not n.startswith('V253_ACCESS_'))
  rows.append({'cut_x_mm':x,'side':'R' if sgn>0 else 'L','center_y_mm':y,'z_mm':z,'OD_ID_mm':[od,id_],'length_mm':2*hl,'provisional':prov,'outer_envelope_containment':frac,'nearest_hardware':ds[0][1] if ds else None,'min_hardware_distance_mm':ds[0][0] if ds else 999,'tube_volume_cm3':tube.Volume/1000.0})
out={'status':'V254_PRIMARY_CF_JOINER_SCREEN','rows':rows,'architecture':{'6x4_CF_for_nose_tail':True,'8x6_CF_for_central_module':True,'X620_joiner_provisional_until_aft_nacelle_OML_gate':True,'central_wingbox_load_path_remains_self_contained':True},'gates':{'all_nonprovisional_outer_envelopes_contained_ge_0p995':all(r['outer_envelope_containment']>=0.995 for r in rows if not r['provisional']),'all_nonprovisional_hardware_clearance_ge_3mm':all(r['min_hardware_distance_mm']>=3 for r in rows if not r['provisional']),'X620_geometry_passes_screen':all(r['outer_envelope_containment']>=0.995 and r['min_hardware_distance_mm']>=3 for r in rows if r['cut_x_mm']==620),'bond_socket_design_open':True,'proof_load_open':True,'print_release':False,'flight_release':False}}
(R/'analysis/v254_primary_cf_joiner_screen.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))