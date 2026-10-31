import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v264_SEGMENTED_ENDMODEL_STATE.FCStd'; out=R/'migration/freecad/F14_v267_SERVICE_HATCH_FLANGE_FINAL_CANDIDATE.FCStd'; audp=R/'migration/freecad/freecad_v267_service_hatch_flange_final_candidate_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v267_SERVICE_HATCH_FLANGE_FINAL_CANDIDATE')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
fus=d.getObject('FUSELAGE_CURRENT').Shape
specs=[('BATTERY',250,428,-36,36,18,5),('SWEEP',430,535,-50,50,18,5),('TAIL_R',675,725,38,86,10,5),('TAIL_L',675,725,-86,-38,10,5)]
t=1.2; gap=.8; boss_r=2.2; rows=[]; total=0
for name,x0,x1,y0,y1,z,margin in specs:
 ox0=x0-margin; ox1=x1+margin; oy0=y0-margin; oy1=y1+margin
 outer=Part.makeBox(ox1-ox0,oy1-oy0,t,App.Vector(ox0,oy0,z)); inner=Part.makeBox((x1+gap)-(x0-gap),(y1+gap)-(y0-gap),t+.4,App.Vector(x0-gap,y0-gap,z-.2)); sh=outer.cut(inner)
 for xx in [ox0+boss_r,ox1-boss_r]:
  for yy in [oy0+boss_r,oy1-boss_r]:
   boss=Part.makeCylinder(boss_r,t,App.Vector(xx,yy,z)); hole=Part.makeCylinder(1.35,t+.4,App.Vector(xx,yy,z-.2)); sh=sh.fuse(boss.cut(hole))
 sh=sh.removeSplitter(); o=doc.addObject('PartDesign::Feature','V267_HATCH_FLANGE_'+name); o.Shape=sh; o.Label='v267 service hatch flange '+name+' / FINAL INTERNAL CANDIDATE'
 keep=doc.getObject('V253_ACCESS_'+name).Shape; inter=sh.common(keep); contain=sh.common(fus).Volume/sh.Volume if sh.Volume else 0; total+=sh.Volume
 rows.append({'access':name,'valid':sh.isValid(),'solid_count':len(sh.Solids),'PPA_CF_mass_g':sh.Volume/1000*1.25,'keepout_intersection_mm3':0 if inter.isNull() else inter.Volume,'fuselage_containment':contain,'boss_radius_mm':boss_r,'pilot_hole_d_mm':2.7})
doc.recompute(); doc.saveAs(str(out)); aud={'status':'V267_SERVICE_HATCH_FLANGE_FINAL_CANDIDATE','source':src.name,'rows':rows,'mass':{'PPA_CF_screen_g':total/1000*1.25},'gates':{'all_valid':all(r['valid'] for r in rows),'no_keepout_intersection':all(r['keepout_intersection_mm3']<1e-6 for r in rows),'containment_ge_0p98':all(r['fuselage_containment']>=.98 for r in rows),'total_mass_lt_8g':total/1000*1.25<8,'fastener_hardware_frozen':False,'shell_cut_frozen':False,'print_release':False,'flight_release':False}}; aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
