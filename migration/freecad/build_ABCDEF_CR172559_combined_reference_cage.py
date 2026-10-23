import FreeCAD as App, Part, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).parent
src1=BASE/'F14_ABCDEF_X_REGISTERED_LOCAL_Z_STUDY.FCStd'
src2=BASE/'F14_CR172559_QUICK_GEOMETRY_REFERENCE.FCStd'

def clone_shapes(src_path,prefix,doc,skip_names=()):
    src=App.openDocument(str(src_path)); rows=[]
    for o in src.Objects:
        if not hasattr(o,'Shape') or o.Shape.isNull(): continue
        if o.Name in skip_names: continue
        n=doc.addObject('PartDesign::Feature',prefix+o.Name)
        n.Label=f'{prefix}{o.Label}'
        n.Shape=o.Shape.copy()
        rows.append({'source_name':o.Name,'target_name':n.Name,'label':n.Label})
    App.closeDocument(src.Name)
    return rows

doc=App.newDocument('F14_ABCDEF_CR172559_COMBINED_REFERENCE_CAGE')
a=clone_shapes(src1,'ABCDEF_',doc)
# Skip the deliberately offset UPC C duplicate in the CR file; A-F study already contains C local-Z once.
b=clone_shapes(src2,'CR172559_',doc,skip_names=('UPC_C_LocalZ_Comparison','UPC_C_LocalAxis'))
# Add explicit explanatory markers to prevent visual misreading.
note1=doc.addObject('App::FeaturePython','Gate_CommonZ')
note1.addProperty('App::PropertyString','Status'); note1.Status='COMMON AIRCRAFT Z NOT REGISTERED – NO LOFT'
note2=doc.addObject('App::FeaturePython','Gate_CR172559')
note2.addProperty('App::PropertyString','Status'); note2.Status='CR172559 QUICK GEOMETRY = REFERENCE ONLY, NOT PRODUCTION OML'
doc.recompute()
out=BASE/'F14_ABCDEF_CR172559_COMBINED_REFERENCE_CAGE.FCStd'; doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={
 'status':'ABCDEF_X_LOCALZ_PLUS_CR172559_RAILS_COMBINED_NATIVE_REFERENCE_CAGE',
 'inputs':{src1.name:hashlib.sha256(src1.read_bytes()).hexdigest(),src2.name:hashlib.sha256(src2.read_bytes()).hexdigest()},
 'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'ABCDEF_objects':len(a),'CR172559_objects':len(b),
 'gates':{'side_X_engineering_candidate_used':True,'global_WL145_reference_present':True,'common_aircraft_Z_registered':False,'loft_created':False,'master_changed':False,'production_release':False},
 'limits':['A-F remain local-Z section candidates positioned only in X.','CR172559 rails are independent quick-geometry references from a 1/40 three-view model.','Objects are co-located for engineering review only; proximity is not proof of OML correspondence.','No loft or production geometry is created.']
}
(BASE/'freecad_ABCDEF_CR172559_combined_reference_cage_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
