import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v210_GLOVE_STRUCTURE_INTEGRATED.FCStd'
out=R/'migration/freecad/F14_v211_UPPER_GLOVE_STRUCTURAL_ENCLOSURE.FCStd'
audp=R/'migration/freecad/freecad_v211_upper_glove_structural_enclosure_audit.json'
d=App.openDocument(str(src)); fuse=d.getObject('FUSELAGE_CURRENT').Shape; wr=d.getObject('WING_R').Shape; wl=d.getObject('WING_L').Shape
upperR=d.getObject('V204_UPPER_FORK_R').Shape; upperL=d.getObject('V204_UPPER_FORK_L').Shape
doc=App.newDocument('F14_v211_UPPER_GLOVE_STRUCTURAL_ENCLOSURE')
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','V204_UPPER_FORK_R','V204_UPPER_FORK_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Shape=o.Shape.copy(); q.Label='[CTX] '+o.Label
yout=148.8263775443693; yin=130.8263775443693; clear=1.0; yfork=137.20927023775283; fork_top=12.5; skin_clear=1.0
xs=[482.346,488.346,496.346,504.346,512.346,520.346,526.346]; rows=[]
for sgn,lab,wing in [(1,'R',wr),(-1,'L',wl)]:
 inner=[]; outer=[]
 for x in xs:
  fl=Part.makeLine(App.Vector(x,sgn*yin,-100),App.Vector(x,sgn*yin,120)); fs=fuse.section(fl); fzs=sorted(v.Point.z for v in fs.Vertexes); zin=fzs[-1]
  wl0=Part.makeLine(App.Vector(x,sgn*yout,-100),App.Vector(x,sgn*yout,120)); ws=wing.section(wl0); wzs=sorted(v.Point.z for v in ws.Vertexes); wup=wzs[-1]
  frac=(yfork-yin)/(yout-yin); req_outer=zin+(fork_top+skin_clear-zin)/frac
  zout=max(wup+clear,req_outer)
  zfork=zin+frac*(zout-zin)
  inner.append(App.Vector(x,sgn*yin,zin)); outer.append(App.Vector(x,sgn*yout,zout))
  rows.append({'side':lab,'x_mm':x,'inner_fuselage_upper_z_mm':zin,'wing_upper_outer_z_mm':wup,'outer_skin_target_z_mm':zout,'wing_clearance_mm':zout-wup,'predicted_skin_z_at_fork_outer_y_mm':zfork,'fork_top_clearance_mm':zfork-fork_top,'lateral_slope_deg':math.degrees(math.atan2(abs(zout-zin),yout-yin))})
 iw=Part.makePolygon(inner); ow=Part.makePolygon(outer); surf=Part.makeRuledSurface(iw,ow)
 for nm,sh in [('INNER_UPPER_'+lab,iw),('OUTER_UPPER_'+lab,ow),('UPPER_GLOVE_'+lab,surf)]: o=doc.addObject('PartDesign::Feature',nm); o.Shape=sh; o.Label='v211 '+nm+' / STRUCTURAL CANDIDATE NOT OML'
doc.recompute(); doc.saveAs(str(out))
wc=[r['wing_clearance_mm'] for r in rows]; fc=[r['fork_top_clearance_mm'] for r in rows]; sl=[r['lateral_slope_deg'] for r in rows]
aud={'status':'V211_UPPER_GLOVE_STRUCTURAL_ENCLOSURE','wing_clearance_range_mm':[min(wc),max(wc)],'fork_top_clearance_range_mm':[min(fc),max(fc)],'lateral_slope_range_deg':[min(sl),max(sl)],'all_shapes_valid':all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()),'rows':rows,'gates':{'wing_upper_clearance_ge_1mm':min(wc)>=0.999,'upper_fork_enclosed_ge_1mm':min(fc)>=0.999,'absolute_Z_OML_verified':False,'production_OML':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))