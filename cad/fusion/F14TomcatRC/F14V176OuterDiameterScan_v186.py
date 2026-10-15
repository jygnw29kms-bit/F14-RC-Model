"""v186: scan the smallest fan-face outer diameter that restores >=0.80 mm native curved-face gap bilaterally."""
import adsk.core, adsk.fusion, json, os, hashlib


def run_review(app, builder, mm, outdir):
    base = os.path.dirname(__file__)
    cfg = json.load(open(os.path.join(base, 'F14_v176_section_inputs.json'), encoding='utf-8'))
    if hashlib.sha256(open(cfg['source_path'], 'rb').read()).hexdigest() != cfg['source_sha256']:
        raise RuntimeError('v186 base source changed')
    prior = app.activeDocument
    imported = app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['source_path']))
    src = adsk.fusion.Design.cast(app.activeProduct)
    inlet_copies = {}
    for side in ['R', 'L']:
        inlet_copies[side] = adsk.fusion.TemporaryBRepManager.get().copy(next(
            b for b in src.rootComponent.bRepBodies if b.name.startswith('CANDIDATE_INLET_WALL_' + side)))
    imported.close(False)

    candidates = [51.62 + 0.01 * i for i in range(0, 13)]
    rows = []
    for outer_d in candidates:
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.DirectDesignType
        root = design.rootComponent
        side_rows = []
        for side, sgn in [('R', 1), ('L', -1)]:
            wall = root.bRepBodies.add(adsk.fusion.TemporaryBRepManager.get().copy(inlet_copies[side]))
            iface = next(f for f in wall.faces if adsk.core.Plane.cast(f.geometry)
                         and abs(adsk.core.Plane.cast(f.geometry).origin.x * 10.0 - cfg['interface_x_mm']) < 1e-6)
            loops = sorted(list(iface.loops), key=lambda q: sum(e.length for e in q.edges), reverse=True)
            loft_bodies = []
            for idx, loop in enumerate(loops):
                start_ci = root.constructionPlanes.createInput()
                start_ci.setByOffset(root.yZConstructionPlane, adsk.core.ValueInput.createByReal(mm(cfg['interface_x_mm'])))
                start_plane = root.constructionPlanes.add(start_ci)
                start = root.sketches.add(start_plane)
                for edge in loop.edges:
                    start.project(edge)
                if start.profiles.count != 1:
                    raise RuntimeError('v186 ambiguous start profile')
                end_ci = root.constructionPlanes.createInput()
                end_ci.setByOffset(root.yZConstructionPlane, adsk.core.ValueInput.createByReal(mm(cfg['fan_face_x_mm'])))
                end_plane = root.constructionPlanes.add(end_ci)
                end = root.sketches.add(end_plane)
                center = end.modelToSketchSpace(adsk.core.Point3D.create(
                    mm(cfg['fan_face_x_mm']), mm(sgn * cfg['fan_axis_center_y_mm']), mm(cfg['fan_axis_center_z_mm'])))
                radius = outer_d / 2.0 if idx == 0 else cfg['fan_inner_diameter_mm'] / 2.0
                end.sketchCurves.sketchCircles.addByCenterRadius(center, mm(radius))
                li = root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                li.loftSections.add(start.profiles.item(0)); li.loftSections.add(end.profiles.item(0))
                loft = root.features.loftFeatures.add(li)
                loft_bodies.append(loft.bodies.item(0))
            curved_outer = next(f for f in loft_bodies[0].faces if adsk.core.Plane.cast(f.geometry) is None)
            curved_inner = next(f for f in loft_bodies[1].faces if adsk.core.Plane.cast(f.geometry) is None)
            gap = app.measureManager.measureMinimumDistance(curved_outer, curved_inner).value * 10.0
            side_rows.append(dict(side=side, minimum_curved_face_gap_mm=gap, pass_0p8=gap >= 0.8))
        rows.append(dict(outer_diameter_mm=outer_d, sides=side_rows,
                         bilateral_pass=all(s['pass_0p8'] for s in side_rows),
                         worst_gap_mm=min(s['minimum_curved_face_gap_mm'] for s in side_rows)))
        doc.close(False)
    passing = [r for r in rows if r['bilateral_pass']]
    selected = passing[0] if passing else None
    if selected is None:
        raise RuntimeError('v186 no passing outer diameter in scan range')
    audit = dict(status='V186_MINIMUM_OUTER_DIAMETER_WALL_THICKNESS_SCAN', source=cfg,
                 fixed_inner_diameter_mm=cfg['fan_inner_diameter_mm'], scan_rows=rows,
                 selected_minimum_outer_diameter=selected,
                 added_outer_diameter_vs_v176_mm=selected['outer_diameter_mm'] - cfg['adapter_outer_diameter_mm'],
                 added_radial_material_vs_v176_mm=(selected['outer_diameter_mm'] - cfg['adapter_outer_diameter_mm']) / 2.0,
                 centerline_unchanged=True, inner_flow_path_unchanged=True,
                 actual_hardware_verified=False, aerodynamic_smoothness_verified=False,
                 print_release=False, flight_release=False,
                 study_source_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest())
    os.makedirs(outdir, exist_ok=True)
    json.dump(audit, open(os.path.join(outdir, 'F14_v186_outer_diameter_scan.json'), 'w'), indent=2)
    if prior:
        try: prior.activate()
        except: pass
    return audit
