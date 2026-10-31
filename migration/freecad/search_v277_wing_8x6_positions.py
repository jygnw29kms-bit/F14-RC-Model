import FreeCAD as App, Part, pathlib, json, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v260_DUAL_WING_SEGMENT_JOINERS.FCStd'; d=App.openDocument(str(src)); wing=d.getObject('WING_R').Shape; seam=320.94018208216556
rows=[]
for x in [548+i*2 for i in range(24)]:
  for z in [-8+i*0.5 for i in range(22)]:
    cyl=Part.makeCylinder(4.15,40,App.Vector(x,seam-20,z),App.Vector(0,1,0)); c=cyl.common(wing).Volume/cyl.Volume
    if c>=0.99: rows.append({'x_mm':x,'z_mm':z,'containment':c})
rows.sort(key=lambda r:r['containment'],reverse=True)
# pair search: >=10 mm center spacing and both >=0.995 preferred; maximize worst containment then spacing.
pairs=[]
for i,a in enumerate(rows):
  for b in rows[i+1:]:
    dist=math.hypot(a['x_mm']-b['x_mm'],a['z_mm']-b['z_mm'])
    if dist>=10:
      pairs.append({'a':a,'b':b,'spacing_mm':dist,'worst_containment':min(a['containment'],b['containment'])})
pairs.sort(key=lambda p:(p['worst_containment'],p['spacing_mm']),reverse=True)
a={'status':'V277_WING_8X6_POSITION_SEARCH','source':src.name,'cavity_d_mm':8.3,'embed_total_mm':40,'grid':{'x_mm':[548,594,2],'z_mm':[-8,2.5,0.5]},'candidate_count_ge_0p99':len(rows),'best_candidates':rows[:20],'best_pairs':pairs[:20],'gates':{'pair_ge_0p995_found':any(p['worst_containment']>=0.995 for p in pairs),'pair_spacing_ge_10mm':bool(pairs)}}
(R/'analysis/v277_wing_8x6_position_search.json').write_text(json.dumps(a,indent=2),encoding='utf-8'); print(json.dumps(a,indent=2))
