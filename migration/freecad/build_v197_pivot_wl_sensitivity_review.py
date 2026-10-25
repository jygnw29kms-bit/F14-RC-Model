import FreeCAD as App, Part, os, json, hashlib
BASE=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'
src=os.path.join(BASE,'migration','freecad','F14_v195_NOSE_RELATIVE_WING_DATUM_CANDIDATE.FCStd')
out=os.path.join(BASE,'migration','freecad','F14_v197_PIVOT_WL_SENSITIVITY_REVIEW.FCStd')
auditp=os.path.join(BASE,'migration','freecad','freecad_v197_pivot_wl_sensitivity_review_audit.json')
base_wl=187.59240693460868
cases=[('BASE_2STATION',187.59240693460868),('FIT8',188.13794790983096),('FIT_OMIT2',188.50506777037677)]
s=App.openDocument(src)
d=App.newDocument('F14_v197_PIVOT_WL_SENSITIVITY_REVIEW')

def add(name,label,shape,color=None,trans=0):
    o=d.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape
    return o
# context body/tails as neutral reference
for n in ['FUSELAGE_CURRENT','STABILATOR_L','STABILATOR_R','VTAIL_L','VTAIL_R']:
    o=s.getObject(n)
    if o and hasattr(o,'Shape') and not o.Shape.isNull(): add('CTX_'+n,'CTX '+o.Label,o.Shape.copy())
# three wing/pivot/wingbox Z cases
rows=[]
for tag,wl in cases:
    dz=-(wl-base_wl)
    grp=d.addObject('App::DocumentObjectGroup',tag)
    for n in ['WING_R','WING_L','PIVOT_REF_R','PIVOT_REF_L','WINGBOX_REF']:
        o=s.getObject(n)
        if not o or not hasattr(o,'Shape') or o.Shape.isNull(): continue
        sh=o.Shape.copy(); sh.translate(App.Vector(0,0,dz))
        no=add(f'{tag}_{n}',f'{tag} dz={dz:.3f} mm | {o.Label}',sh);grp.addObject(no)
    rows.append({'case':tag,'pivot_wl_model_mm':wl,'delta_z_vs_v195_mm':dz})
# add horizontal datum markers across center box
for tag,wl in cases:
    dz=-(wl-base_wl)
    line=Part.makePolygon([App.Vector(430,-190,dz),App.Vector(570,-190,dz),App.Vector(570,190,dz),App.Vector(430,190,dz),App.Vector(430,-190,dz)])
    add('PLANE_'+tag,f'Z sensitivity plane {tag} dz={dz:.3f} mm',line)
meta=d.addObject('App::FeaturePython','V197_META');meta.Label='V197 PIVOT WL SENSITIVITY / REVIEW ONLY'
for prop,val in [('BasePivotWLModelMM',base_wl),('BandMinMM',min(x[1] for x in cases)),('BandMaxMM',max(x[1] for x in cases)),('BandWidthMM',max(x[1] for x in cases)-min(x[1] for x in cases))]:
    meta.addProperty('App::PropertyFloat',prop,'Sensitivity');setattr(meta,prop,val)
meta.addProperty('App::PropertyString','Gate','Sensitivity');meta.Gate='ABSOLUTE PIVOT WL NOT VERIFIED – NO MASTER/PRODUCTION RELEASE'
d.recompute();d.saveAs(out)
a={'status':'V197_PIVOT_WL_SENSITIVITY_REVIEW','source_v195':hashlib.sha256(open(src,'rb').read()).hexdigest(),'cases':rows,'band_width_mm':max(x[1] for x in cases)-min(x[1] for x in cases),'interpretation':'Candidate band from prior Grumman/NASA wing-reference WL regressions; visual sensitivity only, not physical pivot-WL verification.','gates':{'absolute_pivot_WL_verified':False,'master_changed':False,'production_release':False},'output_sha256':hashlib.sha256(open(out,'rb').read()).hexdigest()}
open(auditp,'w',encoding='utf-8').write(json.dumps(a,indent=2))
print(json.dumps(a,indent=2))
