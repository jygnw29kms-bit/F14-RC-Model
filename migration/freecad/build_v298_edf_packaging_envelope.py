import FreeCAD as App, Part, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v297_ALLOWANCED_INLET_EDF_ADAPTER.FCStd'
out=R/'migration/freecad/F14_v298_EDF_PACKAGING_ENVELOPE.FCStd'
audp=R/'migration/freecad/freecad_v298_edf_packaging_envelope_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v298_EDF_PACKAGING_ENVELOPE')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
oml=doc.getObject('V296_SOURCE_BACKED_AFT_OML').Shape
x0=658.0; L=73.5; ay=66.28458486059378; z=-10.508688347971937
critical=[n for n in ['V293_X620_CF_TUBE_R','V293_X620_CF_TUBE_L','V293_X620_SLEEVE_R_AFT','V293_X620_SLEEVE_L_AFT','V295_C_CLAMP_X620_R','V295_C_CLAMP_X620_L','BATTERY_TRAY_v165','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V233_TORQ_SERVICE_R','V233_TORQ_SERVICE_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L'] if doc.getObject(n)]
rows=[]
for side,sgn in [('R',1),('L',-1)]:
    cy=sgn*ay
    side_rec={'side':side,'centerline_mm':[x0,cy,z],'length_mm':L,'envelopes':[]}
    for kind,dia in [('housing',52.5),('housing_skin_service',54.5),('mount_band',55.2)]:
        length=L if kind!='mount_band' else 8.0
        sh=Part.makeCylinder(dia/2,length,App.Vector(x0,cy,z),App.Vector(1,0,0))
        o=doc.addObject('PartDesign::Feature',f'V298_{kind.upper()}_{side}'); o.Shape=sh; o.Label=f'v298 {kind} {side}'
        inside=sh.common(oml).Volume; frac=inside/sh.Volume if sh.Volume else 0
        distances=[]
        for n in critical:
            other=doc.getObject(n).Shape
            dist=sh.distToShape(other)[0]
            inter=sh.common(other).Volume
            distances.append({'object':n,'distance_mm':dist,'intersection_mm3':inter})
        mind=min((q['distance_mm'] for q in distances),default=999)
        side_rec['envelopes'].append({'kind':kind,'diameter_mm':dia,'length_mm':length,'volume_mm3':sh.Volume,'oml_containment':frac,'outside_oml_mm3':max(0.0,sh.Volume-inside),'critical_min_distance_mm':mind,'critical_distances':distances})
    rows.append(side_rec)
doc.recompute(); doc.saveAs(str(out))
flat=[e for r in rows for e in r['envelopes']]
aud={'status':'V298_FREECAD_EDF_PACKAGING_ENVELOPE','source_model':src.name,'architecture':{'fan_face_x_mm':x0,'housing_length_mm':L,'axis_abs_y_mm':ay,'axis_z_mm':z,'housing_OD_assumed_mm':52.5,'skin_plus_service_OD_mm':54.5,'mount_OD_mm':55.2,'actual_EDF_hardware_measured':False},'rows':rows,'gates':{'housing_bilateral_oml_containment_ge_0p999':all(e['oml_containment']>=0.999 for e in flat if e['kind']=='housing'),'skin_service_bilateral_oml_containment_ge_0p999':all(e['oml_containment']>=0.999 for e in flat if e['kind']=='housing_skin_service'),'mount_bilateral_oml_containment_ge_0p999':all(e['oml_containment']>=0.999 for e in flat if e['kind']=='mount_band'),'critical_clearance_ge_1mm':all(e['critical_min_distance_mm']>=1.0 for e in flat),'actual_EDF_hardware_measured':False,'installed_bench_verified':False,'propulsion_packaging_freeze':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
