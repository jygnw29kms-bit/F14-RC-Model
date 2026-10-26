import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'; out=R/'migration/freecad/F14_v212_WINGBOX_UPPER_STRUCTURAL_DECK.FCStd'; audp=R/'migration/freecad/freecad_v212_wingbox_upper_structural_deck_audit.json'
d=App.openDocument(str(src)); wr=d.getObject('WING_R').Shape; wl=d.getObject('WING_L').Shape
doc=App.newDocument('F14_v212_WINGBOX_UPPER_STRUCTURAL_DECK')
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L','V204_MONO_LOWER_R','V204_MONO_LOWER_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Shape=o.Shape.copy(); q.Label='[CTX] '+o.Label
x0=482.3463093769572; x1=526.3463093769572; yin=70.0; yout=147.8; zdeck=13.5; th=1.5; rows=[]
for sgn,lab,wing in [(1,'R',wr),(-1,'L',wl)]:
 ya=min(sgn*yin,sgn*yout); yb=max(sgn*yin,sgn*yout)
 deck=Part.makeBox(x1-x0,yb-ya,th,App.Vector(x0,ya,zdeck))
 o=doc.addObject('PartDesign::Feature','V212_DECK_'+lab); o.Shape=deck; o.Label='v212 internal wingbox upper deck '+lab+' / NOT OML'
 # outer closure wall remains 1.026 mm inboard of moving wing root
 wall=Part.makeBox(x1-x0,1.5,27.0,App.Vector(x0,(yout-1.5 if sgn>0 else -yout),-13.5))
 w=doc.addObject('PartDesign::Feature','V212_OUTER_WALL_'+lab); w.Shape=wall; w.Label='v212 internal outer closure wall '+lab+' / NOT OML'
 # conservative distances
 rows.append({'side':lab,'deck_to_wing_mm':deck.distToShape(wing)[0],'wall_to_wing_mm':wall.distToShape(wing)[0],'deck_to_upper_fork_mm':deck.distToShape(d.getObject('V204_UPPER_FORK_'+lab).Shape)[0]})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V212_WINGBOX_UPPER_STRUCTURAL_DECK','rows':rows,'gates':{'deck_wing_clearance_ge_3mm':min(r['deck_to_wing_mm'] for r in rows)>=3.0,'outer_wall_wing_clearance_ge_1mm':min(r['wall_to_wing_mm'] for r in rows)>=1.0,'deck_upper_fork_clearance_ge_1mm':min(r['deck_to_upper_fork_mm'] for r in rows)>=1.0,'production_OML':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))