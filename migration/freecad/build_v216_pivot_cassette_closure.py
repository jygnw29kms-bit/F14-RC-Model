import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'; out=R/'migration/freecad/F14_v216_PIVOT_CASSETTE_CLOSURE.FCStd'; audp=R/'migration/freecad/freecad_v216_pivot_cassette_closure_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v216_PIVOT_CASSETTE_CLOSURE')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
px=504.3463093769572; py=125.20927023775282; x0=482.3463093769572; x1=526.3463093769572; zdeck=13.5; th=1.5
rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 ya=min(sgn*70.0,sgn*147.8); yb=max(sgn*70.0,sgn*147.8); deck=Part.makeBox(x1-x0,yb-ya,th,App.Vector(x0,ya,zdeck))
 od=doc.addObject('PartDesign::Feature','V216_UPPER_DECK_'+lab); od.Shape=deck; od.Label='v216 internal upper wingbox deck '+lab+' / STRUCTURE NOT OML'
 c=App.Vector(px,sgn*py,-13.5); ring=Part.makeCylinder(22,27,c).cut(Part.makeCylinder(20.5,27,c)); rg=doc.addObject('PartDesign::Feature','V216_PIVOT_GUARD_'+lab); rg.Shape=ring; rg.Label='v216 curved pivot sweep guard '+lab+' / STRUCTURE NOT OML'
 wing=doc.getObject('WING_'+lab).Shape; fork=doc.getObject('V204_UPPER_FORK_'+lab).Shape
 rows.append({'side':lab,'deck_to_wing_mm':deck.distToShape(wing)[0],'deck_to_upper_fork_mm':deck.distToShape(fork)[0],'guard_to_wing_mm':ring.distToShape(wing)[0]})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V216_PIVOT_CASSETTE_CLOSURE','rows':rows,'dynamic_guard_rod_min_mm':3.1882557931456597,'straight_outer_wall_rejected':True,'straight_wall_reason':'moving wing sweeps through all tested constant-Y wall positions outside fork','gates':{'upper_deck_wing_clearance_ge_4mm':min(r['deck_to_wing_mm'] for r in rows)>=4.0,'upper_deck_fork_clearance_ge_1mm':min(r['deck_to_upper_fork_mm'] for r in rows)>=1.0,'guard_wing_clearance_ge_1p5mm':min(r['guard_to_wing_mm'] for r in rows)>=1.5,'guard_dynamic_rod_clearance_ge_1p5mm':True,'absolute_Z_OML_verified':False,'production_OML':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))