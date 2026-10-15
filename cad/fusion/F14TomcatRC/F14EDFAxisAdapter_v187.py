import adsk.core, adsk.fusion, json, os, hashlib, math


def run_review(app, builder, mm, outdir):
    base = os.path.dirname(__file__)
    with open(os.path.join(base, 'F14_v187_section_inputs.json'), encoding='utf-8') as stream:
        cfg = json.load(stream)
    if hashlib.sha256(open(cfg['source_path'], 'rb').read()).hexdigest() != cfg['source_sha256']:
        raise RuntimeError('v187 source changed')

    prior = app.activeDocument
    imported = app.importManager.importToNewDocument(
        app.importManager.createFusionArchiveImportOptions(cfg['source_path']))
    src = adsk.fusion.Design.cast(app.activeProduct)
    temp = adsk.fusion.TemporaryBRepManager.get()
    source = next(b for b in src.rootComponent.bRepBodies if b.name == 'REFERENCE_INTERPOLATED_SOURCE_LOFT')
    source_copy = temp.copy(source)
    inlet_copies = {}
    for side in ['R', 'L']:
        inlet_copies[side] = temp.copy(next(
            b for b in src.rootComponent.bRepBodies if b.name.startswith('CANDIDATE_INLET_WALL_' + side)))

    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name = 'F14_EDF_AXIS_ADAPTER_v187_WALL_CORRECTED_NO_PRINT_RELEASE'
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent
    records = []

    for side, sgn in [('R', 1), ('L', -1)]:
        wall = root.bRepBodies.add(inlet_copies[side])
        wall.name = 'CANDIDATE_INLET_WALL_' + side + '_v187'
        iface = next(
            f for f in wall.faces
            if adsk.core.Plane.cast(f.geometry)
            and abs(adsk.core.Plane.cast(f.geometry).origin.x * 10.0 - cfg['interface_x_mm']) < 1e-6)
        loops = sorted(list(iface.loops), key=lambda q: sum(e.length for e in q.edges), reverse=True)
        if len(loops) != 2:
            raise RuntimeError('v187 expected annular inlet interface for ' + side)

        targets = []
        for idx, loop in enumerate(loops):
            start_ci = root.constructionPlanes.createInput()
            start_ci.setByOffset(root.yZConstructionPlane, adsk.core.ValueInput.createByReal(mm(cfg['interface_x_mm'])))
            start_plane = root.constructionPlanes.add(start_ci)
            start = root.sketches.add(start_plane)
            start.name = 'V187_' + side + ('_OUTER_START' if idx == 0 else '_INNER_START')
            for edge in loop.edges:
                start.project(edge)
            if start.profiles.count != 1:
                raise RuntimeError('v187 inlet projection ambiguous for ' + side)

            end_ci = root.constructionPlanes.createInput()
            end_ci.setByOffset(root.yZConstructionPlane, adsk.core.ValueInput.createByReal(mm(cfg['fan_face_x_mm'])))
            end_plane = root.constructionPlanes.add(end_ci)
            end = root.sketches.add(end_plane)
            end.name = 'V187_' + side + ('_OUTER_FAN_FACE' if idx == 0 else '_INNER_FAN_FACE')
            center = end.modelToSketchSpace(adsk.core.Point3D.create(
                mm(cfg['fan_face_x_mm']), mm(sgn * cfg['fan_axis_center_y_mm']), mm(cfg['fan_axis_center_z_mm'])))
            radius = cfg['adapter_outer_diameter_mm'] / 2.0 if idx == 0 else cfg['fan_inner_diameter_mm'] / 2.0
            end.sketchCurves.sketchCircles.addByCenterRadius(center, mm(radius))

            li = root.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            li.loftSections.add(start.profiles.item(0))
            li.loftSections.add(end.profiles.item(0))
            loft = root.features.loftFeatures.add(li)
            if not loft or loft.bodies.count != 1:
                raise RuntimeError('v187 loft failed for ' + side)
            targets.append(loft.bodies.item(0))

        adapter_temp = temp.copy(targets[0])
        if not temp.booleanOperation(adapter_temp, temp.copy(targets[1]), adsk.fusion.BooleanTypes.DifferenceBooleanType):
            raise RuntimeError('v187 hollow adapter failed for ' + side)
        adapter = root.bRepBodies.add(adapter_temp)
        adapter.name = 'CANDIDATE_EDF_AXIS_ADAPTER_' + side + '_v187_UNMEASURED_FAN'
        if not adapter.isValid or not adapter.isSolid:
            raise RuntimeError('v187 invalid adapter for ' + side)

        joined = temp.copy(wall)
        if not temp.booleanOperation(joined, temp.copy(adapter), adsk.fusion.BooleanTypes.UnionBooleanType):
            raise RuntimeError('v187 inlet/adapter union failed for ' + side)
        joined_body = root.bRepBodies.add(joined)
        joined_body.name = 'CANDIDATE_JOINED_INLET_EDF_' + side + '_v187_NO_PRINT_RELEASE'
        if not joined_body.isValid or not joined_body.isSolid:
            raise RuntimeError('v187 joined body invalid for ' + side)

        bad_edges = [e.tempId for e in joined_body.edges if e.coEdges.count != 2]
        graph = {f.tempId: set() for f in joined_body.faces}
        for edge in joined_body.edges:
            ids = [f.tempId for f in edge.faces]
            for one in ids:
                graph[one].update(ids)
        visited = set()
        pending = [next(iter(graph))]
        while pending:
            one = pending.pop()
            if one in visited:
                continue
            visited.add(one)
            pending.extend(graph[one] - visited)
        topology_pass = not bad_edges and len(visited) == len(graph)
        if not topology_pass:
            raise RuntimeError('v187 joined topology failed for ' + side)

        packaging = []
        cy = sgn * cfg['fan_axis_center_y_mm']
        cz = cfg['fan_axis_center_z_mm']
        for kind, diameter, length in [
            ('housing', cfg['housing_od_assumed_mm'], cfg['housing_length_assumed_mm']),
            ('housing_skin_service', cfg['housing_od_assumed_mm'] + 2.0 * (cfg['skin_radial_allowance_mm'] + cfg['service_radial_allowance_mm']), cfg['housing_length_assumed_mm']),
            ('mount', cfg['mount_od_candidate_mm'], cfg['mount_length_mm'])]:
            cylinder = temp.createCylinderOrCone(
                adsk.core.Point3D.create(mm(cfg['fan_face_x_mm']), mm(cy), mm(cz)), mm(diameter / 2.0),
                adsk.core.Point3D.create(mm(cfg['fan_face_x_mm'] + length), mm(cy), mm(cz)), mm(diameter / 2.0))
            total = cylinder.volume
            inside = temp.copy(cylinder)
            if not temp.booleanOperation(inside, temp.copy(source_copy), adsk.fusion.BooleanTypes.IntersectionBooleanType):
                raise RuntimeError('v187 packaging intersection failed')
            outside = max(0.0, total - inside.volume)
            packaging.append(dict(kind=kind, diameter_mm=diameter, length_mm=length,
                                  outside_candidate_source_cm3=outside,
                                  containment_pass=outside <= cfg['containment_tolerance_cm3']))

        records.append(dict(
            side=side,
            adapter_volume_cm3=adapter.volume,
            joined_volume_cm3=joined_body.volume,
            joined_face_count=joined_body.faces.count,
            joined_edge_count=joined_body.edges.count,
            all_edges_two_coedges=(len(bad_edges) == 0),
            face_graph_connected=(len(visited) == len(graph)),
            fan_axis_center_mm=[cfg['fan_face_x_mm'], cy, cz],
            center_shift_from_old_candidate_mm=math.hypot(cfg['fan_axis_center_y_mm'] - 65.0, cfg['fan_axis_center_z_mm'] + 10.0),
            packaging=packaging,
            packaging_containment_pass=all(p['containment_pass'] for p in packaging)))

        wall.isVisible = False
        adapter.isVisible = False
        for target in targets:
            target.isVisible = False

    audit = dict(
        status='V187_WALL_CORRECTED_CENTERLINE_ALIGNED_EDF_ADAPTER',
        source=cfg,
        records=records,
        bilateral_topology_pass=all(r['all_edges_two_coedges'] and r['face_graph_connected'] for r in records),
        bilateral_packaging_screen_pass=all(r['packaging_containment_pass'] for r in records),
        fan_dimensions_measured=False,
        normal_wall_thickness_verified=False,
        wall_thickness_correction_basis='v186 selected 51.64 mm outer diameter; independent v187 thickness verification still required',
        aerodynamic_smoothness_verified=False,
        mechanism_clearance_verified=False,
        slicer_verified=False,
        print_release=False,
        flight_release=False)

    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, 'F14_v187_WALL_CORRECTED_EDF_ADAPTER.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)):
        raise RuntimeError('v187 archive export failed')
    with open(os.path.join(outdir, 'F14_v187_wall_corrected_edf_adapter_audit.json'), 'w', encoding='utf-8') as stream:
        json.dump(audit, stream, indent=2)
    app.activeViewport.fit()
    app.activeViewport.saveAsImageFile(os.path.join(outdir, 'F14_v187_wall_corrected_edf_adapter_review.png'), 1600, 1000)
    doc.close(False)
    imported.close(False)
    if prior:
        prior.activate()
    return audit
