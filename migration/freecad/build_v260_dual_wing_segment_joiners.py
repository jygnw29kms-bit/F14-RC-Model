import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v256_CONSOLIDATED_JOINER_STATE.FCStd'; out=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; audp=R/'migration/freecad/freecad_v260_dual_wing_segment_joiners_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v260_DUAL_WING_SEGMENT_JOINERS')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
seam_y=320.94018208216556; specs=[('FWD',569.9475331358894,-4.299519854236053,0.30),('AFT',581.1120872253817,-4.231136960437908,0.42)]; rows=[]
for lab,sgn in [('R',1),('L',-1)]:
 wing=doc.getObject('WING_'+lab).Shape
 for tag,x,z,xc in specs:
  start=App.Vector(x,sgn*(seam_y-20),z); ax=App.Vector(0,sgn,0); outer=Part.makeCylinder(3.0,40,start,ax); inner=Part.makeCylinder(2.0,40,start,ax); tube=outer.cut(inner); cavity=Part.makeCylinder(3.15,40,start,ax)
  to=doc.addObject('PartDesign::Feature',f'V260_WING_JOINER_{lab}_{tag}'); to.Shape=tube; to.Label=f'v260 6x4 CF wing segment joiner {lab} {tag} / xc={xc:.2f}'
  co=doc.addObject('PartDesign::Feature',f'V260_WING_BOND_CAVITY_{lab}_{tag}'); co.Shape=cavity; co.Label=f'v260 6.3 mm bond cavity {lab} {tag} / REFERENCE CUT'
  rows.append({'side':lab,'joiner':tag,'xc':xc,'tube_valid':tube.isValid(),'tube_containment':outer.common(wing).Volume/outer.Volume,'cavity_containment':cavity.common(wing).Volume/cavity.Volume,'tube_volume_cm3':tube.Volume/1000.0})
doc.recompute(); doc.saveAs(str(out)); total_vol=sum(r['tube_volume_cm3'] for r in rows)
load=json.load(open(R/'analysis/v259_dual_wing_joiner_load_screen.json',encoding='utf-8'))
aud={'status':'V260_DUAL_WING_SEGMENT_JOINERS','source':src.name,'seam':{'WBL_in':274.36816,'abs_y_mm':seam_y},'rows':rows,'mass':{'total_CF_tube_volume_cm3':total_vol,'actual_tube_density_and_mass_gate_open':True},'load_screen_reference':{'uniform_spanload_scaled_seam_moment_Nm':load['load_screen']['uniform_spanload_scaled_seam_moment_Nm'],'candidate_FOS':load['load_screen']['candidate_FOS'],'material_values_verified':False},'gates':{'all_tubes_valid':all(r['tube_valid'] for r in rows),'all_tubes_contained_ge_0p999':all(r['tube_containment']>=0.999 for r in rows),'all_cavities_contained_ge_0p999':all(r['cavity_containment']>=0.999 for r in rows),'adhesive_system_selected':False,'tube_datasheet_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))