import FreeCAD as App, Part, json, hashlib
from pathlib import Path
BASE=Path(__file__).parent
ROOT=BASE.parents[1]
inputs=[BASE/'F14_ABCDEF_CR172559_COMBINED_REFERENCE_CAGE.FCStd',BASE/'F14_CR172559_REFERENCE_SURFACE_PATCHES.FCStd']
out=BASE/'F14_ABCDEF_CR172559_SURFACE_REVIEW_CAGE.FCStd'
doc=App.newDocument('F14_ABCDEF_CR172559_SURFACE_REVIEW_CAGE')
counts=[]
for src in inputs:
    sd=App.openDocument(str(src)); n=0
    for obj in sd.Objects:
        if hasattr(obj,'Shape') and not obj.Shape.isNull():
            no=doc.addObject('PartDesign::Feature',f'{src.stem}_{obj.Name}')
            no.Label=f'{obj.Label} | aus {src.stem}'
            no.Shape=obj.Shape.copy(); n+=1
    counts.append({'file':src.name,'objects':n,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
    App.closeDocument(sd.Name)
doc.recompute(); doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={'status':'ABCDEF_CR172559_SURFACE_REVIEW_CAGE_STUDY','inputs':counts,'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'gates':{'ABCDEF_common_Z_registered':False,'CR172559_surface_patches_reference_only':True,'loft_created':False,'master_changed':False,'production_release':False},'purpose':'Gemeinsame visuelle Review-Datei fuer A-F-X-Sektionen, NASA/Grumman-Rails und begrenzte Referenzflaechen.'}
(BASE/'freecad_ABCDEF_CR172559_surface_review_cage_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
