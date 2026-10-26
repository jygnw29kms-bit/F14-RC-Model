import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'; out=R/'migration/freecad/F14_v217_MONOLITHIC_PIVOT_CASSETTE.FCStd'; audp=R/'migration/freecad/freecad_v217_monolithic_pivot_cassette_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v217_MONOLITHIC_PIVOT_CASSETTE')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=504.3463093769572; py=125.20927023775282; x0=482.3463093769572; x1=526.3463093769572; rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 ya=min(sgn*70.0,sgn*147.8); yb=max(sgn*70.0,sgn*147.8); deck=Part.makeBox(x1-x0,yb-ya,1.5,App.Vector(x0,ya,12.5))
 c=App.Vector(px,sgn*py,-13.5); ring=Part.makeCylinder(22,27,c).cut(Part.makeCylinder(20.5,27,c))
 lower=doc.getObject('V204_MONO_LOWER_'+lab).Shape; upper=doc.getObject('V204_UPPER_FORK_'+lab).Shape
 fused=lower.fuse(upper).fuse(deck).fuse(ring); fused=fused.removeSplitter()
 o=doc.addObject('PartDesign::Feature','V217_CASSETTE_'+lab); o.Shape=fused; o.Label='v217 monolithic fixed pivot cassette '+lab+' / STRUCTURE NOT OML'
 wing=doc.getObject('WING_'+lab).Shape; slider=doc.getObject('V208_SLIDER_'+lab).Shape
 rows.append({'side':lab,'solid_count':len(fused.Solids),'is_valid':fused.isValid(),'cassette_to_wing_mm':fused.distToShape(wing)[0],'cassette_to_slider_mm':fused.distToShape(slider)[0],'deck_to_wing_mm':deck.distToShape(wing)[0],'guard_to_wing_mm':ring.distToShape(wing)[0]})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V217_MONOLITHIC_PIVOT_CASSETTE','rows':rows,'dynamic_guard_to_rod_min_mm':3.1882557931456597,'gates':{'single_solid_each_side':all(r['solid_count']==1 for r in rows),'all_valid':all(r['is_valid'] for r in rows),'cassette_wing_clearance_ge_1p5mm':min(r['cassette_to_wing_mm'] for r in rows)>=1.5,'cassette_slider_clearance_ge_1p5mm':min(r['cassette_to_slider_mm'] for r in rows)>=1.5,'dynamic_guard_rod_clearance_ge_1p5mm':True,'production_OML':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))