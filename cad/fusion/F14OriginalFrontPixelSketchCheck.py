"""Native sketch transfer check, deliberately not an aircraft-scale model."""
import adsk.core,adsk.fusion,json,os,hashlib
SOURCE=r'C:/Users/dezen/Desktop/F14-RC-Model/analysis/original_front_sources/front_sections_pixel_candidates.json'
EXPECTED='5635bfc21e3301d5ec98fe6301162e830c418cd18122b4d434a640cca39903ed'
def run_review(app,builder,mm,outdir):
    raw=open(SOURCE,'rb').read()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise RuntimeError('Source traces changed; re-audit before transfer')
    data=json.loads(raw);prior=app.activeDocument
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name='F14_SOURCE_PIXEL_SKETCH_CHECK_NOT_AIRCRAFT_SCALE'
    design=adsk.fusion.Design.cast(app.activeProduct);root=design.rootComponent;records=[]
    for row in data['profiles']:
        sk=root.sketches.add(root.xYConstructionPlane);sk.name='SOURCE_'+row['section']+'_ONE_PIXEL_PER_MM_NOT_MODEL_SCALE'
        ax,ay=row['source_section_axis_pixel']
        for loop in row['loops_pixel']:
            for a,b in zip(loop,loop[1:]+loop[:1]):
                sk.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(mm(a[0]-ax),mm(ay-a[1]),0),adsk.core.Point3D.create(mm(b[0]-ax),mm(ay-b[1]),0))
        wanted=len(row['loops_pixel'])
        matches=[v for v in sk.profiles if v.profileLoops.count==wanted]
        if len(matches)!=1:raise RuntimeError('Expected one section region with '+str(wanted)+' boundaries in '+row['section'])
        native_area=matches[0].areaProperties().area*100
        areas=[abs(v['signed_area_pixels2']) for v in row['loop_summary']]
        expected=areas[0]-sum(areas[1:])
        if abs(native_area-expected)>max(.001,expected*1e-6):raise RuntimeError('Native sketch area mismatch')
        records.append(dict(section=row['section'],native_profile_count=sk.profiles.count,region_loop_count=wanted,native_area_arbitrary_mm2=native_area,pixel_polygon_area=expected))
        sk.isVisible=row['section']=='C'
    audit=dict(status='NATIVE_SOURCE_PIXEL_SKETCH_TRANSFER_CHECK',source_sha256=EXPECTED,records=records,one_pixel_per_arbitrary_mm=True,aircraft_metric_registration=False,production_geometry=False,print_release=False)
    os.makedirs(outdir,exist_ok=True)
    design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_ORIGINAL_FRONT_PIXEL_SKETCH_CHECK.f3d')))
    with open(os.path.join(outdir,'F14_original_front_pixel_sketch_audit.json'),'w') as f:json.dump(audit,f,indent=2)
    doc.close(False)
    if prior:prior.activate()
    return audit
