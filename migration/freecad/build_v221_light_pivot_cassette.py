import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'; out=R/'migration/freecad/F14_v221_LIGHT_PIVOT_CASSETTE.FCStd'; audp=R/'migration/freecad/freecad_v221_light_pivot_cassette_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v221_LIGHT_PIVOT_CASSETTE'); px=504.3463093769572; py=125.20927023775282; rows=[]
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
for lab,sgn in [('R',1),('L',-1)]:
 lower=doc.getObject('V204_MONO_LOWER_'+lab).Shape; upper=doc.getObject('V204_UPPER_FORK_'+lab).Shape; c=App.Vector(px,sgn*py,-12.5); guard=Part.makeCylinder(22.0,25.0,c).cut(Part.makeCylinder(20.8,25.0,c))
 fused=lower.fuse(upper).fuse(guard).removeSplitter(); o=doc.addObject('PartDesign::Feature','V221_CASSETTE_'+lab); o.Shape=fused; o.Label='v221 lightweight monolithic pivot cassette '+lab+' / PPA-CF SCREEN / NOT RELEASED'
 wing=doc.getObject('WING_'+lab).Shape; slider=doc.getObject('V208_SLIDER_'+lab).Shape
 rows.append({'side':lab,'solid_count':len(fused.Solids),'valid':fused.isValid(),'volume_cm3':fused.Volume/1000.0,'cassette_to_wing_mm':fused.distToShape(wing)[0],'cassette_to_slider_mm':fused.distToShape(slider)[0]})
doc.recompute(); doc.saveAs(str(out)); pv=sum(r['volume_cm3'] for r in rows)
aud={'status':'V221_LIGHT_PIVOT_CASSETTE','guard':{'inner_radius_mm':20.8,'outer_radius_mm':22.0,'radial_thickness_mm':1.2,'height_mm':25.0,'print_line_equivalent_at_0p4mm':3.0},'rows':rows,'pair_volume_cm3':pv,'pair_mass_PPA_CF_g':pv*1.25,'pair_mass_PA6_CF_g':pv*1.09,'gates':{'single_solid_each_side':all(r['solid_count']==1 for r in rows),'all_valid':all(r['valid'] for r in rows),'wing_clearance_ge_1p5mm':min(r['cassette_to_wing_mm'] for r in rows)>=1.5,'slider_clearance_ge_1p5mm':min(r['cassette_to_slider_mm'] for r in rows)>=1.5,'guard_strength_verified':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))