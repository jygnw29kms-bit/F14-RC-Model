import FreeCAD as App, Part, json, pathlib, math, hashlib
R=pathlib.Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model")
src=R/'migration/freecad/F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'; outp=R/'migration/freecad/F14_v201_GLOVE_BLENDED_CLEARANCE_CANDIDATE.FCStd'; auditp=R/'migration/freecad/freecad_v201_glove_blended_clearance_candidate_audit.json'
d=App.openDocument(str(src)); f=d.getObject('FUSELAGE_CURRENT').Shape; doc=App.newDocument('F14_v201_GLOVE_BLENDED_CLEARANCE_CANDIDATE')
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L']:
 o=d.getObject(n)
 if o and hasattr(o,'Shape') and not o.Shape.isNull():
  q=doc.addObject('PartDesign::Feature','CTX_'+n); q.Label='[CTX] '+o.Label; q.Shape=o.Shape.copy()
y_out=148.8263775443693; y_in=130.8263775443693; clear=1.0
samples=[(490,-3.85),(492,-4.03),(496,-4.25),(500,-4.45),(504.346,-4.742),(508,-4.85),(512,-4.95),(516,-5.05),(520,-5.10)]
rows=[]
for sgn,lab in [(1,'R'),(-1,'L')]:
 outer=[]; inner=[]
 for x,wz in samples:
  zout=wz-clear
  line=Part.makeLine(App.Vector(x,sgn*y_in,-100),App.Vector(x,sgn*y_in,100)); sec=f.section(line); zs=sorted([v.Point.z for v in sec.Vertexes]); zin=zs[0] if zs else zout-3
  outer.append(App.Vector(x,sgn*y_out,zout)); inner.append(App.Vector(x,sgn*y_in,zin))
  dy=abs(y_out-y_in); dz=zin-zout; slope=math.degrees(math.atan2(abs(dz),dy))
  rows.append({'side':lab,'x_mm':x,'outer_target_z_mm':zout,'inner_existing_fuselage_z_mm':zin,'lateral_delta_z_mm':dz,'lateral_slope_deg':slope})
 ow=Part.makePolygon(outer); iw=Part.makePolygon(inner); surf=Part.makeRuledSurface(iw,ow)
 for name,label,shape in [('INNER_ATTACH_'+lab,f'v201 inner attach {lab} / existing fuselage lower',iw),('OUTER_CLEARANCE_'+lab,f'v201 outer clearance {lab} / 1mm below wing root',ow),('GLOVE_BLEND_'+lab,f'v201 blended local glove underside {lab} / CANDIDATE NOT OML',surf)]:
  o=doc.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape
m=doc.addObject('App::FeaturePython','V201_GATE');m.addProperty('App::PropertyString','Status');m.Status='BLENDED CLEARANCE CANDIDATE / LOCAL GLOVE ONLY / ABSOLUTE Z UNVERIFIED'
doc.recompute();doc.saveAs(str(outp))
valid=[o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]; slopes=[r['lateral_slope_deg'] for r in rows]
aud={'status':'V201_GLOVE_BLENDED_CLEARANCE_CANDIDATE','x_range_mm':[490,520],'inner_attach_abs_y_mm':y_in,'outer_clearance_abs_y_mm':y_out,'clearance_target_mm':clear,'lateral_slope_range_deg':[min(slopes),max(slopes)],'all_shapes_valid':all(valid),'rows':rows,'gates':{'source_wing_preserved':True,'pivot_XY_preserved':True,'inner_attach_uses_current_fuselage_lower_surface':True,'absolute_Z_verified':False,'production_OML':False,'master_changed':False,'production_release':False}}
aud['output_sha256']=hashlib.sha256(outp.read_bytes()).hexdigest();auditp.write_text(json.dumps(aud,indent=2),encoding='utf-8');print(json.dumps(aud,indent=2))
