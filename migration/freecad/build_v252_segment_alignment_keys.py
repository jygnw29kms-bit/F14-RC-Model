import FreeCAD as App, Part, json, pathlib, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); src=R/'migration/freecad/F14_v250_PRINT_SEGMENTATION_REVIEW.FCStd'; out=R/'migration/freecad/F14_v252_SEGMENT_ALIGNMENT_KEYS.FCStd'; audp=R/'migration/freecad/freecad_v252_segment_alignment_keys_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v252_SEGMENT_ALIGNMENT_KEYS')
for o in d.Objects:
 if hasattr(o,'Shape') and not o.Shape.isNull(): q=doc.addObject('PartDesign::Feature',o.Name); q.Shape=o.Shape.copy(); q.Label=o.Label
spec=[(220,20,0),(440,40,0),(620,15,30),(840,40,0)]; rows=[]
fus=doc.getObject('FUSELAGE_CURRENT').Shape
hw=[]
for n in ['BATTERY_TRAY_v165','V221_CASSETTE_R','V221_CASSETTE_L','V225_SERVO_SERVICE','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L']:
 o=doc.getObject(n)
 if o: hw.append((n,o.Shape))
for x,ay,z in spec:
 for sgn in (-1,1):
  y=sgn*ay; key=Part.makeBox(12,8,6,App.Vector(x-6,y-4,z-3)); sock=Part.makeBox(12.5,8.5,6.5,App.Vector(x-6.25,y-4.25,z-3.25))
  lab=f'X{x}_{"P" if sgn>0 else "N"}'
  ko=doc.addObject('PartDesign::Feature','V252_ALIGN_KEY_'+lab); ko.Shape=key; ko.Label=f'v252 alignment key {lab} / non-primary-load'
  so=doc.addObject('PartDesign::Feature','V252_SOCKET_CLEARANCE_'+lab); so.Shape=sock; so.Label=f'v252 socket clearance {lab} / 0.25 mm per face'
  frac=key.common(fus).Volume/key.Volume; ds=sorted((key.distToShape(sh)[0],n) for n,sh in hw)
  rows.append({'cut_x_mm':x,'y_mm':y,'z_mm':z,'key_valid':key.isValid(),'socket_valid':sock.isValid(),'containment_fraction':frac,'nearest_hardware':ds[0][1],'min_hardware_distance_mm':ds[0][0]})
doc.recompute(); doc.saveAs(str(out)); vol=sum(doc.getObject(n).Shape.Volume for n in [o.Name for o in doc.Objects if o.Name.startswith('V252_ALIGN_KEY_')])/1000.0
aud={'status':'V252_SEGMENT_ALIGNMENT_KEYS','source':src.name,'geometry':{'key_mm':[12,8,6],'socket_clearance_per_face_mm':0.25,'key_count':8},'rows':rows,'mass_screen':{'total_key_volume_cm3':vol,'PPA_CF_1p25_g_cm3_g':vol*1.25},'architecture':{'alignment_only':True,'primary_structural_joiner_still_required':True,'X620_aft_nacelle_keys_provisional_until_OML_gate':True},'gates':{'all_keys_valid':all(r['key_valid'] and r['socket_valid'] for r in rows),'all_contained':all(r['containment_fraction']>=0.999 for r in rows),'hardware_clearance_ge_4mm':all(r['min_hardware_distance_mm']>=4 for r in rows),'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))