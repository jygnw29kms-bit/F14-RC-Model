"""v184: export current v176 centerline-aligned joined inlet/EDF bodies as native-mm STL candidates."""
import adsk.core, adsk.fusion, json, os, hashlib


def run_review(app, builder, mm, outdir):
    source = r'C:/Users/dezen/Desktop/F14-RC-Model/analysis/independent_reviews/edf_axis_adapter_v176_20261015/F14_v176_CENTERLINE_ALIGNED_EDF_ADAPTER.f3d'
    source_sha = 'ea6fab92314b3e9cc58afb0cdc3cddbd5a416df548012ffde3036bc45f17431a'
    if hashlib.sha256(open(source,'rb').read()).hexdigest() != source_sha:
        raise RuntimeError('v184 v176 source changed')
    prior = app.activeDocument
    doc = app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(source))
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    bodies = [b for b in root.bRepBodies if b.name.startswith('CANDIDATE_JOINED_INLET_EDF_') and '_v176_' in b.name]
    if len(bodies) != 2:
        raise RuntimeError('v184 expected exactly two joined v176 bodies, got %d' % len(bodies))
    os.makedirs(outdir, exist_ok=True)
    rows=[]
    for body in bodies:
        side = 'R' if '_R_' in body.name else 'L'
        path = os.path.join(outdir, 'F14_INLET_EDF_'+side+'_v184_NOT_RELEASED.stl')
        opt = design.exportManager.createSTLExportOptions(body, path)
        opt.unitType = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
        opt.isBinaryFormat = True
        opt.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        if not design.exportManager.execute(opt):
            raise RuntimeError('v184 STL export failed '+side)
        bb=body.boundingBox
        rows.append(dict(
            side=side,
            body_name=body.name,
            path=path,
            native_volume_mm3=body.volume*1000.0,
            native_bounds_mm=[[bb.minPoint.x*10,bb.minPoint.y*10,bb.minPoint.z*10],[bb.maxPoint.x*10,bb.maxPoint.y*10,bb.maxPoint.z*10]],
            stl_sha256=hashlib.sha256(open(path,'rb').read()).hexdigest()))
    audit=dict(
        status='V184_V176_CENTERLINE_ALIGNED_INLET_STL_EXPORT',
        source_path=source,
        source_sha256=source_sha,
        files=rows,
        source_revision='v176',
        centerline_alignment_verified_in_v176=True,
        slicer_verified=False,
        actual_print_tested=False,
        print_release=False,
        flight_release=False,
        study_source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    with open(os.path.join(outdir,'F14_v184_inlet_STL_export_audit.json'),'w',encoding='utf-8') as f:
        json.dump(audit,f,indent=2)
    doc.close(False)
    if prior:
        try: prior.activate()
        except: pass
    return audit
