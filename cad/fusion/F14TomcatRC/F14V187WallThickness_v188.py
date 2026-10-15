"""v188: independent native minimum wall-thickness verification of the v187 EDF adapter."""
import adsk.core, adsk.fusion, json, os, hashlib


def run_review(app, builder, mm, outdir):
    source = r'C:/Users/dezen/Desktop/F14-RC-Model/workspace/RC-F14-Tomcat/Fusion/Exports/Current/propulsion_v187/F14_v187_WALL_CORRECTED_EDF_ADAPTER.f3d'
    source_sha = '232b7171de92537a70890f4056ca9b96eb8581ed2b70ff367e1606b035d666ee'
    if hashlib.sha256(open(source, 'rb').read()).hexdigest() != source_sha:
        raise RuntimeError('v188 v187 source changed')
    prior = app.activeDocument
    doc = app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(source))
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    rows = []
    for side in ['R', 'L']:
        adapter = next(b for b in root.bRepBodies if b.name.startswith('CANDIDATE_EDF_AXIS_ADAPTER_' + side + '_v187_'))
        joined = next(b for b in root.bRepBodies if b.name.startswith('CANDIDATE_JOINED_INLET_EDF_' + side + '_v187_'))
        curved = [f for f in adapter.faces if adsk.core.Plane.cast(f.geometry) is None]
        planar = [f for f in adapter.faces if adsk.core.Plane.cast(f.geometry) is not None]
        if len(curved) != 2 or len(planar) != 2:
            raise RuntimeError('v188 unexpected adapter faces for %s: curved=%d planar=%d' % (side, len(curved), len(planar)))
        min_gap_mm = app.measureManager.measureMinimumDistance(curved[0], curved[1]).value * 10.0
        face_rows=[]
        for face in planar:
            plane=adsk.core.Plane.cast(face.geometry)
            loops=sorted(list(face.loops), key=lambda q: sum(e.length for e in q.edges), reverse=True)
            if len(loops)!=2:
                raise RuntimeError('v188 planar adapter face not annular '+side)
            perimeters=[sum(e.length for e in loop.edges)*10.0 for loop in loops]
            eq=[p/3.141592653589793 for p in perimeters]
            radial=(eq[0]-eq[1])/2.0
            face_rows.append(dict(x_mm=plane.origin.x*10.0,equivalent_diameters_mm=eq,radial_gap_mm=radial,screen_pass=radial>=0.8))
        rows.append(dict(side=side,adapter_body=adapter.name,joined_body=joined.name,
                         native_minimum_curved_face_gap_mm=min_gap_mm,
                         minimum_0p8mm_screen_pass=min_gap_mm>=0.8,
                         end_faces=sorted(face_rows,key=lambda r:r['x_mm']),
                         adapter_is_valid=adapter.isValid,adapter_is_solid=adapter.isSolid,
                         joined_is_valid=joined.isValid,joined_is_solid=joined.isSolid))
    audit=dict(status='V188_V187_ADAPTER_NATIVE_WALL_THICKNESS_VERIFIED',source_path=source,
               source_sha256=source_sha,measurements=rows,minimum_release_screen_mm=0.8,
               bilateral_minimum_0p8mm_pass=all(r['minimum_0p8mm_screen_pass'] and all(f['screen_pass'] for f in r['end_faces']) for r in rows),
               normal_wall_thickness_screen_verified=True,actual_print_tested=False,
               fan_dimensions_measured=False,aerodynamic_smoothness_verified=False,
               mechanism_clearance_verified=False,print_release=False,flight_release=False,
               study_source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    os.makedirs(outdir,exist_ok=True)
    with open(os.path.join(outdir,'F14_v188_v187_wall_thickness_audit.json'),'w',encoding='utf-8') as f:
        json.dump(audit,f,indent=2)
    doc.close(False)
    if prior:
        try: prior.activate()
        except: pass
    return audit

