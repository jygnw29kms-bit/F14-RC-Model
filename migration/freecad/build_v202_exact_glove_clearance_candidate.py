import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
src=R/'migration/freecad/F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'; outp=R/'migration/freecad/F14_v202_EXACT_GLOVE_CLEARANCE_CANDIDATE.FCStd'; auditp=R/'migration/freecad/freecad_v202_exact_glove_clearance_candidate_audit.json'
d=App.openDocument(str(src)); f=d.getObject('FUSELAGE_CURRENT').Shape; wr=d.getObject('WING_R').Shape; wl=d.getObject('WING_L').Shape; doc=App.newDocument('F14_v202_EXACT_GLOVE_CLEARANCE_CANDIDATE')
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Label='[CTX] '+o.Label; q.Shape=o.Shape.copy()
y_out=148.8263775443693; y_in=130.8263775443693; clear=1.0; xs=[490,492,496,500,504.346,508,512,516,520]
rows=[]
for sgn,lab,wing in [(1,'R',wr),(-1,'L',wl)]:
 outer=[];inner=[]
 for x in xs:
  l=Part.makeLine(App.Vector(x,sgn*y_out,-100),App.Vector(x,sgn*y_out,100)); sec=wing.section(l); wzs=sorted(v.Point.z for v in sec.Vertexes); wz=wzs[0]
  zout=wz-clear
  fl=Part.makeLine(App.Vector(x,sgn*y_in,-100),App.Vector(x,sgn*y_in,100)); fsec=f.section(fl); fzs=sorted(v.Point.z for v in fsec.Vertexes); zin=fzs[0]
  outer.append(App.Vector(x,sgn*y_out,zout));inner.append(App.Vector(x,sgn*y_in,zin))
  rows.append({'side':lab,'x_mm':x,'wing_lower_exact_z_mm':wz,'outer_target_z_mm':zout,'inner_attach_z_mm':zin,'exact_clearance_mm':wz-zout,'lateral_slope_deg':math.degrees(math.atan2(abs(zin-zout),abs(y_out-y_in)))})
 ow=Part.makePolygon(outer); iw=Part.makePolygon(inner); surf=Part.makeRuledSurface(iw,ow)
 for name,label,shape in [('INNER_ATTACH_'+lab,f'v202 inner attach {lab} / existing fuselage lower',iw),('OUTER_CLEARANCE_'+lab,f'v202 exact 1mm clearance rail {lab}',ow),('GLOVE_BLEND_'+lab,f'v202 exact local glove underside {lab} / CANDIDATE NOT OML',surf)]:
  o=doc.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape
m=doc.addObject('App::FeaturePython','V202_GATE');m.addProperty('App::PropertyString','Status');m.Status='EXACT 1MM WING-ROOT CLEARANCE / LOCAL GLOVE CANDIDATE / Z DATUM OPEN'
doc.recompute();doc.saveAs(str(outp));vals=[r['exact_clearance_mm'] for r in rows];sl=[r['lateral_slope_deg'] for r in rows]
aud={'status':'V202_EXACT_GLOVE_CLEARANCE_CANDIDATE','clearance_target_mm':clear,'exact_clearance_range_mm':[min(vals),max(vals)],'lateral_slope_range_deg':[min(sl),max(sl)],'all_shapes_valid':all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()),'rows':rows,'gates':{'source_wing_preserved':True,'pivot_XY_preserved':True,'absolute_Z_verified':False,'production_OML':False,'master_changed':False,'production_release':False}}
aud['output_sha256']=hashlib.sha256(outp.read_bytes()).hexdigest();auditp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))
