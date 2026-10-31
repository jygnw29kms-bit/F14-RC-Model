import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v253_SERVICE_ACCESS_KEEPOUTS.FCStd'; out=R/'migration/freecad/F14_v255_CF_JOINERS_AND_SLEEVES.FCStd'; audp=R/'migration/freecad/freecad_v255_cf_joiners_and_sleeves_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v255_CF_JOINERS_AND_SLEEVES')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
# x, half length, abs y, z, OD, ID, provisional
spec=[(220,30,20,-10,6,4,False),(440,38,60,-10,8,6,False),(620,40,15,30,8,6,True),(840,20,30,0,6,4,False)]
fus=doc.getObject('FUSELAGE_CURRENT').Shape; rows=[]; sleeve_mass=0.0
for x,hl,ay,z,od,id_,prov in spec:
 for sgn in (-1,1):
  y=sgn*ay; outer=Part.makeCylinder(od/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); inner=Part.makeCylinder(id_/2,2*hl,App.Vector(x-hl,y,z),App.Vector(1,0,0)); tube=outer.cut(inner)
  tag=f'X{x}_{"R" if sgn>0 else "L"}'; to=doc.addObject('PartDesign::Feature','V255_CF_TUBE_'+tag); to.Shape=tube; to.Label=f'v255 CF tube {od}x{id_} {tag}'+(' / PROVISIONAL' if prov else '')
  # 0.15 mm radial clearance, 1.2 mm printed sleeve wall, 20 mm each side of seam
  bore_r=od/2+0.15; sleeve_or=bore_r+1.2; sleeves=[]
  for side,start in [('FWD',x-20),('AFT',x)]:
   so=Part.makeCylinder(sleeve_or,20,App.Vector(start,y,z),App.Vector(1,0,0)); bi=Part.makeCylinder(bore_r,20,App.Vector(start,y,z),App.Vector(1,0,0)); sl=so.cut(bi); sleeves.append(sl)
   o=doc.addObject('PartDesign::Feature',f'V255_SLEEVE_{tag}_{side}'); o.Shape=sl; o.Label=f'v255 PPA-CF sleeve {tag} {side}'+(' / PROVISIONAL' if prov else '')
   if not prov: sleeve_mass += sl.Volume/1000.0*1.25
  scomp=sleeves[0].fuse(sleeves[1]); rows.append({'cut_x_mm':x,'side':'R' if sgn>0 else 'L','provisional':prov,'tube_valid':tube.isValid(),'sleeves_valid':all(s.isValid() for s in sleeves),'tube_outer_containment':outer.common(fus).Volume/outer.Volume,'sleeve_outer_containment':Part.makeCylinder(sleeve_or,40,App.Vector(x-20,y,z),App.Vector(1,0,0)).common(fus).Volume/Part.makeCylinder(sleeve_or,40,App.Vector(x-20,y,z),App.Vector(1,0,0)).Volume,'sleeve_wall_mm':1.2,'radial_clearance_mm':0.15})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V255_CF_JOINERS_AND_SLEEVES','source':src.name,'rows':rows,'mass_screen':{'nonprovisional_printed_sleeves_PPA_CF_g':sleeve_mass,'CF_tube_mass_not_assumed':True},'architecture':{'X620_objects_present_but_provisional':True,'central_wingbox_load_path_unchanged':True,'alignment_keys_remain_separate_from_primary_CF_joiners':True},'gates':{'all_nonprovisional_valid':all(r['tube_valid'] and r['sleeves_valid'] for r in rows if not r['provisional']),'all_nonprovisional_tubes_contained':all(r['tube_outer_containment']>=0.995 for r in rows if not r['provisional']),'all_nonprovisional_sleeves_contained':all(r['sleeve_outer_containment']>=0.995 for r in rows if not r['provisional']),'CF_tube_actual_mass_measured':False,'bond_system_selected':False,'proof_load':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))