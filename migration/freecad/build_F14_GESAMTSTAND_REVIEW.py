import FreeCAD as App, Part, json, hashlib
from pathlib import Path
ROOT=Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
BASE=ROOT/'migration'/'freecad'
SOURCES=[('LEGACY_FULL','F14_v194_FAIL_CLOSED_REVIEW.FCStd'),('CURRENT_SURFACE','F14_ABCDEF_CR172559_SURFACE_REVIEW_CAGE.FCStd'),('RADOME_GUIDES','F14_ORIGINAL_RADOME_SEAM_GUIDES.FCStd'),('NOSE_GUIDES','F14_ORIGINAL_NOSE_PROJECTION_GUIDES.FCStd'),('GLOVE_GUIDES','F14_ORIGINAL_GLOVE_PLAN_GUIDES.FCStd'),('NOSE_A_SENS','F14_NOSE_A_SHAPE_SENSITIVITY.FCStd')]
COLORS={'LEGACY_FULL':((0.72,0.72,0.72),(0.35,0.35,0.35),78,1.0),'CURRENT_SURFACE':((0.95,0.55,0.18),(1.0,0.80,0.25),12,2.0),'RADOME_GUIDES':((1.0,0.20,0.20),(1.0,0.20,0.20),0,4.0),'NOSE_GUIDES':((0.20,1.0,0.30),(0.20,1.0,0.30),0,4.0),'GLOVE_GUIDES':((0.15,0.75,1.0),(0.15,0.75,1.0),0,4.0),'NOSE_A_SENS':((0.95,0.20,0.95),(0.95,0.20,0.95),0,3.0)}
out=BASE/'F14_GESAMTSTAND_REVIEW.FCStd'
doc=App.newDocument('F14_GESAMTSTAND_REVIEW')
summary=[]
for tag,name in SOURCES:
    p=BASE/name
    if not p.exists(): summary.append({'tag':tag,'file':name,'status':'missing'}); continue
    src=App.openDocument(str(p)); grp=doc.addObject('App::DocumentObjectGroup',tag); copied=0
    sc,lc,tr,lw=COLORS[tag]
    for obj in src.Objects:
        if not hasattr(obj,'Shape'): continue
        try:
            sh=obj.Shape
            if sh.isNull(): continue
        except: continue
        o=doc.addObject('PartDesign::Feature',f'{tag}_{obj.Name}'); o.Label=f'[{tag}] {obj.Label}'; o.Shape=sh.copy(); grp.addObject(o); copied+=1
        try:
            o.ViewObject.ShapeColor=sc; o.ViewObject.LineColor=lc; o.ViewObject.Transparency=tr; o.ViewObject.LineWidth=lw
        except: pass
    App.closeDocument(src.Name)
    summary.append({'tag':tag,'file':name,'objects_copied':copied,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
xaxis=doc.addObject('PartDesign::Feature','GESAMT_X_AXIS'); xaxis.Label='Gesamtstand X-Referenz'; xaxis.Shape=Part.makeLine(App.Vector(-50,0,0),App.Vector(850,0,0)); xaxis.ViewObject.LineColor=(1.0,1.0,1.0)
meta=doc.addObject('App::FeaturePython','GESAMTSTAND_META'); meta.addProperty('App::PropertyString','Status'); meta.Status='ENTWICKLUNGSSTAND / REVIEW - KEINE PRODUKTIONSFREIGABE'; meta.addProperty('App::PropertyString','Hinweis'); meta.Hinweis='Legacy-Geometrie nur visueller Kontext; aktuelle Referenzgeometrie bleibt fail-closed.'
doc.recompute(); doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={'status':'F14_GESAMTSTAND_REVIEW','sources':summary,'gates':{'legacy_not_master':True,'current_reference_fail_closed':True,'production_release':False},'note':'Jeweils letzter relevanter Stand pro Konstruktionslinie; historische Duplikate nicht mehrfach importiert.'}
(BASE/'freecad_F14_GESAMTSTAND_REVIEW_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
