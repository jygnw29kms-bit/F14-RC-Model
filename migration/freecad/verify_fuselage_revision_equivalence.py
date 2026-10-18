import FreeCAD as App,json,os,hashlib
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
NAMES=['F14_CURRENT_FULL_VIEW_v191.FCStd','F14_CURRENT_FULL_VIEW_v192.FCStd','F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd']
shapes=[];records=[]
for name in NAMES:
 path=os.path.join(BASE,'migration/freecad',name);sha=hashlib.sha256(open(path,'rb').read()).hexdigest();doc=App.openDocument(path);shape=doc.getObject('FUSELAGE_CURRENT').Shape.copy()
 if shape.isNull() or not shape.isValid():raise RuntimeError('Invalid fuselage input')
 shapes.append(shape);records.append(dict(archive=name,archive_sha256=sha,volume_mm3=shape.Volume,area_mm2=shape.Area,face_count=len(shape.Faces),solid_count=len(shape.Solids)));App.closeDocument(doc.Name)
comparisons=[]
for index in [1,2]:
 a,b=shapes[0],shapes[index]
 try: ab=a.cut(b);ba=b.cut(a)
 except Exception as exc:raise RuntimeError('Native equivalence boolean failed') from exc
 for result in [ab,ba]:
  if not result.isNull() and not result.isValid():raise RuntimeError('Invalid equivalence result')
 av=0 if ab.isNull() else ab.Volume;bv=0 if ba.isNull() else ba.Volume
 comparisons.append(dict(reference=NAMES[0],candidate=NAMES[index],reference_minus_candidate_mm3=av,candidate_minus_reference_mm3=bv,volumetric_difference_below_1e_6_mm3=abs(av)<1e-6 and abs(bv)<1e-6))
report=dict(status='NATIVE_FUSELAGE_REVISION_VOLUMETRIC_EQUIVALENCE',records=records,comparisons=comparisons,scope='Bidirectional solid-volume difference only; not identical topology or original-aircraft fidelity.',original_OML_verified=False,production_geometry=False)
with open(os.path.join(BASE,'analysis/independent_reviews/fuselage_lineage_20261018/native_equivalence.json'),'w') as f:json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
