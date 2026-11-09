"""V330 Integrationssicht aus nativen v312-KÃ¶rpern plus geprÃ¼ften v326-Meshes.
Nicht als Produktions-Master oder druckfertige Gesamtgeometrie interpretieren."""
import FreeCAD as App, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad')
s=App.openDocument(str(R/'F14_v312_POST_F_SOURCE_CONSTRAINED_OML.FCStd'))
m=App.openDocument(str(R/'F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd'))
d=App.newDocument('F14_v330_INTEGRATED_ASSEMBLY_REVIEW')
groups={}
for group in ['OUTER_REFERENCE','WING_AND_TAIL','EDF_AND_INLET','INNER_STRUCTURE']:
 groups[group]=d.addObject('App::DocumentObjectGroup',group)
choices={
'OUTER_REFERENCE':['FUSELAGE_CURRENT','V312_POST_F_SOURCE_CONSTRAINED_OML'],
'WING_AND_TAIL':['V282_WING_R_INNER','V282_WING_R_OUTER','V282_WING_L_INNER','V282_WING_L_OUTER','STABILATOR_L','STABILATOR_R','VTAIL_L','VTAIL_R','VENTRAL_L','VENTRAL_R'],
'EDF_AND_INLET':['V297_JOINED_INLET_ADAPTER_R','V297_JOINED_INLET_ADAPTER_L'],
'INNER_STRUCTURE':['BATTERY_TRAY_v165','V282_WING_JOINER_R_FWD','V282_WING_JOINER_R_MID','V282_WING_JOINER_R_AFT','V282_WING_JOINER_L_FWD','V282_WING_JOINER_L_MID','V282_WING_JOINER_L_AFT']}
items=[]
for group,names in choices.items():
 for name in names:
  source=s.getObject(name)
  if not source or not hasattr(source,'Shape') or source.Shape.isNull(): raise RuntimeError('missing shape '+name)
  o=d.addObject('PartDesign::Feature','REVIEW_'+name)
  o.Shape=source.Shape.copy();o.Label='REVIEW '+name;groups[group].addObject(o)
  if group=='OUTER_REFERENCE' and o.ViewObject is not None:o.ViewObject.Visibility=False
  b=o.Shape.BoundBox
  items.append({'name':name,'source':'v312','solids':len(o.Shape.Solids),'bounds_mm':[round(b.XMin,2),round(b.XMax,2),round(b.YMin,2),round(b.YMax,2),round(b.ZMin,2),round(b.ZMax,2)]})
for side in ('R','L'):
 source=m.getObject('V326_TRANSITION_WALL_'+side)
 if not source:raise RuntimeError('missing validated mesh '+side)
 o=d.addObject('Mesh::Feature','REVIEW_EDF_TRANSITION_'+side)
 o.Mesh=source.Mesh.copy();o.Label='v326 EDF TRANSITION '+side+' (development)';groups['EDF_AND_INLET'].addObject(o)
 items.append({'name':o.Name,'source':'v326','facets':o.Mesh.CountFacets,'solid':bool(o.Mesh.isSolid()),'nonmanifolds':bool(o.Mesh.hasNonManifolds())})
d.recompute()
out=R/'F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd';d.saveAs(str(out))
audit={'status':'INTEGRATION_REVIEW_ONLY','sources':[s.FileName,m.FileName],'objects':items,'overall_geometry_validated':False,'assembly_collision_checked':False,'print_release':False,'flight_release':False,'file_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(R/'freecad_v330_integrated_assembly_review_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps({'file':out.name,'objects':len(items),'groups':list(groups),'sha256':audit['file_sha256']},indent=2),flush=True)

