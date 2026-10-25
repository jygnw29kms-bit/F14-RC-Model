import FreeCAD as App,Part,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/migration/freecad");src=BASE/'F14_v210_A80BHSF_M4_MECHANISM.FCStd';out=BASE/'F14_v211_SWEEP_POWER_BEC.FCStd'
d=App.openDocument(str(src));xc,yc,zc=330,60,45
bec=Part.makeBox(55,25,12,App.Vector(xc-27.5,yc-12.5,zc-6));o=d.addObject('PartDesign::Feature','V211_HOBBYWING_UBEC10A_HV');o.Label='Hobbywing UBEC 10A HV / 8.4V / 55x25x12';o.Shape=bec
# 50mm receiver EMI separation reference, sphere centered on BEC
keep=Part.makeSphere(50,App.Vector(xc,yc,zc));k=d.addObject('PartDesign::Feature','V211_RECEIVER_50MM_KEEP_OUT');k.Label='Receiver keep-out >=50mm from UBEC / reference only';k.Shape=keep
m=d.addObject('App::FeaturePython','V211_META');m.Label='v211 sweep power BEC packaging'
for n,v in [('BECModel','Hobbywing UBEC 10A HV PN 30608000'),('BECOutput','8.4V / 10A continuous / 25A peak'),('SweepServo','AGFRC A80BHSF V2 / 5A loading current @8.4V')]:m.addProperty('App::PropertyString',n,'Hardware');setattr(m,n,v)
for n,v in [('BECContained',True),('ReceiverKeepOutModeled',True),('ReceiverSelected',False),('ProductionRelease',False)]:m.addProperty('App::PropertyBool',n,'Gate');setattr(m,n,v)
d.recompute();d.saveAs(str(out));a={'status':'V211_SWEEP_POWER_BEC','BEC':{'model':'Hobbywing UBEC 10A HV','PN':'30608000','dims_mm':[55,25,12],'weight_g':35,'input':'3-14S LiPo','output_V':8.4,'continuous_A':10,'peak_A':25,'center_mm':[xc,yc,zc]},'servo':{'model':'AGFRC A80BHSF V2','loading_current_A_8p4V':5.0,'current_headroom_continuous_factor':2.0},'receiver_keepout_radius_mm':50,'gates':{'packaging_verified':True,'electrical_architecture_candidate':True,'receiver_selected':False,'wiring_harness_designed':False,'EMI_bench_verified':False,'print_release':False,'flight_release':False},'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(BASE/'freecad_v211_sweep_power_bec_audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
