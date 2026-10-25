import FreeCAD as App, json, hashlib
from pathlib import Path
BASE=Path(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\migration\freecad")
srcp=BASE/'F14_v194_FAIL_CLOSED_REVIEW.FCStd'
outp=BASE/'F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd'
d=App.openDocument(str(srcp))
DX=-(93.0*1.1697428086486623)
exact={'WING_R','WING_L','WINGBOX_REF','PIVOT_REF_R','PIVOT_REF_L','SWEEP_REFERENCE_v192','SWEEP_LINKAGE_V193','SWEEP_SLIDER_R','SWEEP_SLIDER_L','SWEEP_SERVO_SERVICE_REF','DYNAMIC_LINKAGE_V194'}
prefixes=('WING_R_SWEEP_','WING_L_SWEEP_','V194_CRANK_','V194_ROD_','V194_SLIDER_')
shifted=[]
for o in d.Objects:
    if o.Name in exact or o.Name.startswith(prefixes):
        try:
            sh=o.Shape
            if sh and not sh.isNull():
                cp=sh.copy(); cp.translate(App.Vector(DX,0,0)); o.Shape=cp; shifted.append(o.Name)
        except Exception:
            pass
# metadata
meta=d.getObject('DATUM_V195') or d.addObject('App::FeaturePython','DATUM_V195'); meta.Label='V195 nose-relative wing/pivot/sweep datum candidate'
for name,typ in [('FS93Shift','App::PropertyLength'),('OldPivotX','App::PropertyLength'),('NewPivotX','App::PropertyLength')]:
    if not hasattr(meta,name): meta.addProperty(typ,name,'Datum')
meta.FS93Shift=DX; meta.OldPivotX=613.1323905812828; meta.NewPivotX=504.3463093769572
if not hasattr(meta,'Gate'): meta.addProperty('App::PropertyString','Gate','Datum')
meta.Gate='CANDIDATE ONLY; Y/Z/glove fit not yet released'
d.recompute(); d.saveAs(str(outp))
# audit selected bounds
rows=[]
for n in ['FUSELAGE_CURRENT','WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L','WINGBOX_REF']:
    o=d.getObject(n)
    if o and hasattr(o,'Shape') and not o.Shape.isNull():
        b=o.Shape.BoundBox; rows.append({'name':n,'x':[b.XMin,b.XMax],'y':[b.YMin,b.YMax],'z':[b.ZMin,b.ZMax]})
a={'status':'V195_NOSE_RELATIVE_WING_DATUM_CANDIDATE','source':'v194 fail-closed review','FS93_shift_mm':DX,'old_pivot_X_mm':613.1323905812828,'new_pivot_X_mm':504.3463093769572,'shifted_objects':shifted,'records':rows,'gates':{'nose_relative_X_candidate':True,'Y_verified':False,'Z_verified':False,'glove_fit_verified':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(outp.read_bytes()).hexdigest()}
(BASE/'freecad_v195_nose_relative_wing_datum_candidate_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
print(json.dumps(a,indent=2))

