import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v214_CURRENT_ENDMODEL_DEVELOPMENT_STATE.FCStd';out=BASE/'F14_v215_TORQ_STABILATOR_SERVOS.FCStd'
d=App.openDocument(str(src)); xc=700; ay=60; zc=0
for sign,lab in [(1,'R'),(-1,'L')]:
 body=Part.makeBox(23,27.5,12,App.Vector(xc-11.5,sign*ay-13.75,-6));o=d.addObject('PartDesign::Feature',f'V215_TORQ_TCM1022_{lab}');o.Label=f'TORQ TCM-1022 stabilator servo {lab} / 23x12x27.5 reoriented';o.Shape=body
 env=Part.makeBox(27,31.5,16,App.Vector(xc-13.5,sign*ay-15.75,-8));e=d.addObject('PartDesign::Feature',f'V215_TORQ_SERVICE_{lab}');e.Label=f'TCM-1022 service envelope {lab}';e.Shape=env
m=d.addObject('App::FeaturePython','V215_META');m.Label='v215 TORQ stabilator servo candidate'
for n,v in [('ServoModel','TORQ TCM-1022'),('RatedData','14.5 kgcm @8.4V / 0.055s / 22g / 23x12x27.5'),('Architecture','one servo per stabilator; independent pitch+taileron mix')]:m.addProperty('App::PropertyString',n,'Hardware');setattr(m,n,v)
for n,v in [('TorqueGatePass',True),('CurrentMeasured',False),('MountingEarsMeasured',False),('SplineOffsetMeasured',False),('BenchProof',False),('FlightRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out));a={'status':'V215_TORQ_STABILATOR_SERVOS','servo':{'model':'TORQ TCM-1022','dims_mm':[23,12,27.5],'weight_g_each':22,'stall_kgcm_8p4V':14.5,'speed_s_60_8p4V':0.055,'centers_mm':[[xc,ay,zc],[xc,-ay,zc]],'service_dims_mm':[27,31.5,16]},'current_model_clearance':{'contained':True,'min_to_ESC_mm':14.647952075290252,'to_EDF_mm':28.5},'gates':{'torque_gate_v168_pass':True,'packaging_reverified_v214':True,'actual_stall_current_measured':False,'mounting_ears_measured':False,'output_spline_measured':False,'bench_proof':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v215_torq_stabilator_servos_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
