"""F-14 v336: conservative internally bounded lightening channels.
Experimental closed internal bores in the v282 solid wing segments.
No structural or print release.
"""
import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
b=R/'migration/freecad'
src=App.openDocument(str(b/'F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd'))
doc=App.newDocument('F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE')
rows=[]
for side,sgn in (('R',1),('L',-1)):
 for seg in ('INNER','OUTER'):
  wing=src.getObject('V282_WING_'+side+'_'+seg).Shape.copy()
  bb=wing.BoundBox
  # Limit candidate bores to the inner 55% span and central chord, away from joiner trio.
  ys=[bb.YMin+bb.YLength*f for f in (0.37,0.57)] if sgn>0 else [bb.YMax-bb.YLength*f for f in (0.37,0.57)]
  tested=0;accepted=[];work=wing
  for x in (510.0,585.0,605.0):
   for y in ys:
    for z in (-1.0,0.5,-2.5):
     tested+=1
     axis=App.Vector(0,sgn,0)
     start=App.Vector(x,y,z)
     # Clearance envelope is wider and longer than actual cavity.
     radius=2.0; length=15.0; min_wall=1.5
     core=Part.makeCylinder(radius,length,start,axis)
     envelope=Part.makeCylinder(radius+min_wall,length+2*min_wall,start-axis*min_wall,axis)
     # Keep a solid min_wall envelope surrounding the entire channel.
     if envelope.cut(work).Volume>0.01:continue
     candidate=work.cut(core)
     if not candidate.isValid() or len(candidate.Solids)!=1:continue
     if candidate.Volume>=work.Volume-0.1:continue
     accepted.append({'x_mm':x,'y_mm':round(y,3),'z_mm':z,'radius_mm':radius,'length_mm':length})
     work=candidate
     break
   if len(accepted)>=4:break
  name='V336_WING_'+side+'_'+seg
  obj=doc.addObject('PartDesign::Feature',name);obj.Shape=work
  obj.Label='v336 closed channel wing '+side+' '+seg
  row={'side':side,'segment':seg,'tested':tested,'accepted':accepted,'solid_count':len(work.Solids),'valid':bool(work.isValid()),'original_volume_mm3':round(wing.Volume,3),'new_volume_mm3':round(work.Volume,3),'removed_volume_mm3':round(wing.Volume-work.Volume,3),'bbox_unmodified':all(abs(getattr(wing.BoundBox,k)-getattr(work.BoundBox,k))<0.001 for k in ('XMin','XMax','YMin','YMax','ZMin','ZMax'))}
  rows.append(row)
  print(json.dumps(row),flush=True)
doc.recompute()
out=b/'F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd';doc.saveAs(str(out))
audit={'classification':'EXPERIMENTAL_INTERNAL_CHANNELS','source':'F14_v282_THREE_8X6_WING_JOINER_ENDMODEL.FCStd','minimum_envelope_mm':1.5,'channel_d_mm':4.0,'closed_cavities_not_print_process_verified':True,'rows':rows,'mass_load_impact_validated':False,'slicer_verified':False,'print_release':False,'flight_release':False,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(b/'freecad_v336_internal_wing_channels_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('COMPLETE',flush=True)
