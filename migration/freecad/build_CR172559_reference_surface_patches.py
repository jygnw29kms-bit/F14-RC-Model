import FreeCAD as App, Part, json, hashlib, importlib.util
from pathlib import Path
BASE=Path(__file__).parent
ROOT=BASE.parents[1]
src=BASE/'build_CR172559_quick_geometry_reference.py'
spec=importlib.util.spec_from_file_location('qg',src)
qg=importlib.util.module_from_spec(spec); spec.loader.exec_module(qg)
PAIRS=[('SCPUP','FUP','upper_body_reference_patch'),('SCPLO','FLO','lower_body_reference_patch'),('INLTUP','INLTLO','inlet_side_reference_patch')]
doc=App.newDocument('F14_CR172559_REFERENCE_SURFACE_PATCHES')
rows=[]
for a,b,label in PAIRS:
    xs=sorted(set([x for x,_ in qg.Y[a]]+[x for x,_ in qg.Z[a]]+[x for x,_ in qg.Y[b]]+[x for x,_ in qg.Z[b]]))
    xs=[x for x in xs if qg.interp(qg.Y[a],x) is not None and qg.interp(qg.Z[a],x) is not None and qg.interp(qg.Y[b],x) is not None and qg.interp(qg.Z[b],x) is not None]
    for side,sgn in [('R',1),('L',-1)]:
        A=[];B=[]
        for fs in xs:
            A.append(App.Vector(qg.rcx(fs),sgn*qg.interp(qg.Y[a],fs)*qg.scale,qg.rcz(qg.interp(qg.Z[a],fs))))
            B.append(App.Vector(qg.rcx(fs),sgn*qg.interp(qg.Y[b],fs)*qg.scale,qg.rcz(qg.interp(qg.Z[b],fs))))
        faces=[]
        for i in range(len(xs)-1):
            tris=[(A[i],A[i+1],B[i+1]),(A[i],B[i+1],B[i])]
            for p0,p1,p2 in tris:
                try:
                    faces.append(Part.Face(Part.makePolygon([p0,p1,p2,p0])))
                except:
                    pass
        obj=doc.addObject('PartDesign::Feature',f'{label}_{side}')
        obj.Label=f'CR172559 {label} {side} – REFERENZPATCH'
        obj.Shape=Part.makeCompound(faces)
        rows.append({'pair':[a,b],'side':side,'FS_range_in':[xs[0],xs[-1]],'stations':len(xs),'faces':len(faces)})
# datum and C station
wl=doc.addObject('PartDesign::Feature','WL145_Reference'); wl.Label='WL145 globale Referenz'; wl.Shape=Part.makeLine(App.Vector(qg.rcx(352),-120,0),App.Vector(qg.rcx(780),-120,0))
crow=next(r for r in qg.XREG['sections'] if r['section']=='C'); cx=float(crow['nose_relative_X_nominal_mm'])
cm=doc.addObject('PartDesign::Feature','C_FS_Marker'); cm.Label='Sektion C FS428.031 – X Marker'; cm.Shape=Part.makeLine(App.Vector(cx,-120,-70),App.Vector(cx,-120,70))
doc.recompute(); out=BASE/'F14_CR172559_REFERENCE_SURFACE_PATCHES.FCStd'; doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={'status':'CR172559_LIMITED_REFERENCE_SURFACE_PATCHES_STUDY','source':'NASA CR-172559 quick geometry Table 1','pairs':rows,'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'gates':{'reference_only':True,'full_skin_created':False,'UPC_C_Z_registered':False,'master_changed':False,'production_release':False},'limits':['Nur semantisch eng zusammengehoerige Rail-Paare verbunden.','Quick-Geometry basiert laut Quelle auf 1/40-Dreiseitenansicht und ist keine Produktions-OML.','Keine Interpolation zu UPC-C und keine Freigabe.']}
(BASE/'freecad_CR172559_reference_surface_patches_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))

