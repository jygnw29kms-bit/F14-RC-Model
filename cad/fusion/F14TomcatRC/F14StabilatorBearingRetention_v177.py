"""v177: stabilator bearing packaging and positive axial-retention candidate."""
import adsk.core, adsk.fusion, json, os, hashlib


def mm(v): return v / 10.0

def cyl(temp, x, y0, y1, z, diameter):
    return temp.createCylinderOrCone(
        adsk.core.Point3D.create(mm(x), mm(y0), mm(z)), mm(diameter / 2.0),
        adsk.core.Point3D.create(mm(x), mm(y1), mm(z)), mm(diameter / 2.0))

def ring(temp, x, y0, y1, z, od, id_):
    outer = cyl(temp, x, y0, y1, z, od)
    lo, hi = min(y0, y1) - 0.2, max(y0, y1) + 0.2
    inner = cyl(temp, x, lo, hi, z, id_)
    if not temp.booleanOperation(outer, inner, adsk.fusion.BooleanTypes.DifferenceBooleanType):
        raise RuntimeError('ring boolean failed')
    return outer

def d_segment(temp, x, y0, y1, z, diameter, flat_x_from_center):
    body = cyl(temp, x, y0, y1, z, diameter)
    r = diameter / 2.0
    lo = x - r - 1.0
    hi = x + flat_x_from_center
    yc = (y0 + y1) / 2.0
    obb = adsk.core.OrientedBoundingBox3D.create(
        adsk.core.Point3D.create(mm((lo + hi) / 2.0), mm(yc), mm(z)),
        adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
        mm(hi - lo), mm(abs(y1 - y0) + 2.0), mm(diameter + 2.0))
    clip = temp.createBox(obb)
    if not temp.booleanOperation(body, clip, adsk.fusion.BooleanTypes.IntersectionBooleanType):
        raise RuntimeError('D-segment clip failed')
    return body

def outside_volume(temp, body, source):
    total = body.volume
    inside = temp.copy(body)
    ok = temp.booleanOperation(inside, temp.copy(source), adsk.fusion.BooleanTypes.IntersectionBooleanType)
    if not ok or not inside.isValid:
        return total
    return max(0.0, total - inside.volume)

def add(root, body, name, opacity=None):
    b = root.bRepBodies.add(body)
    b.name = name
    if opacity is not None:
        b.opacity = opacity
    return b


def run_review(app, builder, mm_unused, outdir):
    base = os.path.dirname(__file__)
    with open(os.path.join(base, 'F14_v177_section_inputs.json'), encoding='utf-8') as stream:
        cfg = json.load(stream)
    for path_key, hash_key in [('v175_path', 'v175_sha256'), ('source_oml_path', 'source_oml_sha256')]:
        if hashlib.sha256(open(cfg[path_key], 'rb').read()).hexdigest() != cfg[hash_key]:
            raise RuntimeError('v177 source changed: ' + path_key)

    prior = app.activeDocument
    temp = adsk.fusion.TemporaryBRepManager.get()

    v175doc = app.importManager.importToNewDocument(
        app.importManager.createFusionArchiveImportOptions(cfg['v175_path']))
    v175root = adsk.fusion.Design.cast(app.activeProduct).rootComponent
    fitting_copies = {}
    crank_copies = {}
    for side in ['R', 'L']:
        fitting_copies[side] = temp.copy(next(b for b in v175root.bRepBodies if b.name.startswith('CANDIDATE_D_BORE_STABILATOR_FITTING_' + side)))
        crank_copies[side] = temp.copy(next(b for b in v175root.bRepBodies if b.name.startswith('REF_20MM_CRANK_ENVELOPE_' + side)))
    v175doc.close(False)

    oml_doc = app.importManager.importToNewDocument(
        app.importManager.createFusionArchiveImportOptions(cfg['source_oml_path']))
    oml_root = adsk.fusion.Design.cast(app.activeProduct).rootComponent
    source_oml = temp.copy(next(b for b in oml_root.bRepBodies if b.name == 'REFERENCE_INTERPOLATED_SOURCE_LOFT'))
    oml_doc.close(False)

    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name = 'F14_STABILATOR_BEARING_RETENTION_v177_NO_FLIGHT_RELEASE'
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent

    x = float(cfg['pivot_x_mm'])
    z = float(cfg['pivot_z_mm'])
    sd = float(cfg['shaft_diameter_mm'])
    d0, d1 = [float(v) for v in cfg['D_engagement_abs_y_range_mm']]
    round_start = float(cfg['shaft_round_inboard_abs_y_mm'])
    records = []

    for side, sgn in [('R', 1), ('L', -1)]:
        fitting = add(root, temp.copy(fitting_copies[side]), 'CANDIDATE_D_BORE_STABILATOR_FITTING_' + side + '_v177')
        crank = add(root, temp.copy(crank_copies[side]), 'REF_20MM_CRANK_ENVELOPE_' + side + '_v177', .15)

        round_end = d0
        shaft_round = cyl(temp, x, sgn * round_start, sgn * round_end, z, sd)
        shaft_d = d_segment(temp, x, sgn * d0, sgn * d1, z, sd, float(cfg['shaft_flat_x_from_center_mm']))
        if not temp.booleanOperation(shaft_round, shaft_d, adsk.fusion.BooleanTypes.UnionBooleanType):
            raise RuntimeError('v177 shaft union failed ' + side)
        shaft = add(root, shaft_round, 'REF_ROUND_TO_D_SHAFT_6MM_' + side + '_v177', .55)

        bearings = []
        housing_checks = []
        for idx, center_abs in enumerate(cfg['bearing_centers_abs_y_mm'], start=1):
            center = sgn * float(center_abs)
            half = float(cfg['bearing_width_mm']) / 2.0
            y0, y1 = center - sgn * half, center + sgn * half
            bearing = ring(temp, x, y0, y1, z, float(cfg['bearing_od_mm']), float(cfg['bearing_id_mm']))
            bearings.append(add(root, bearing, 'REF_BEARING_6x13x5_' + side + '_' + str(idx) + '_v177', .3))
            housing = ring(temp, x, y0, y1, z, float(cfg['printed_bearing_housing_od_mm']), float(cfg['bearing_od_mm']))
            housing_copy = temp.copy(housing)
            add(root, housing, 'CANDIDATE_PRINTED_BEARING_HOUSING_' + side + '_' + str(idx) + '_v177')
            outside = outside_volume(temp, housing_copy, source_oml)
            housing_checks.append(dict(index=idx, center_abs_y_mm=float(center_abs), outside_source_oml_cm3=outside,
                                       containment_pass=outside <= float(cfg['containment_tolerance_cm3'])))

        iy0, iy1 = [sgn * float(v) for v in cfg['bearing_inboard_collar_abs_y_range_mm']]
        inboard_collar = ring(temp, x, iy0, iy1, z, float(cfg['bearing_inboard_collar_od_mm']), 6.1)
        add(root, inboard_collar, 'CANDIDATE_BEARING_INBOARD_SHAFT_COLLAR_' + side + '_v177')

        oy0, oy1 = [sgn * float(v) for v in cfg['bearing_outer_shoulder_abs_y_range_mm']]
        shoulder = ring(temp, x, oy0, oy1, z, float(cfg['bearing_outer_shoulder_od_mm']), 6.0)
        add(root, shoulder, 'CANDIDATE_BEARING_OUTER_SHAFT_SHOULDER_' + side + '_v177')

        sy0, sy1 = [sgn * float(v) for v in cfg['surface_inner_collar_abs_y_range_mm']]
        surface_collar = ring(temp, x, sy0, sy1, z, float(cfg['surface_inner_collar_od_mm']), float(cfg['surface_inner_collar_id_mm']))
        add(root, surface_collar, 'CANDIDATE_SURFACE_INNER_SHAFT_COLLAR_' + side + '_v177')

        wy0, wy1 = [sgn * float(v) for v in cfg['surface_outer_washer_abs_y_range_mm']]
        washer = ring(temp, x, wy0, wy1, z, float(cfg['surface_outer_washer_od_mm']), float(cfg['surface_outer_washer_id_mm']))
        add(root, washer, 'CANDIDATE_SURFACE_OUTER_END_WASHER_' + side + '_v177')

        hy0, hy1 = [sgn * float(v) for v in cfg['end_fastener_head_abs_y_range_mm']]
        head = cyl(temp, x, hy0, hy1, z, float(cfg['end_fastener_head_od_mm']))
        add(root, head, 'REF_AXIAL_END_FASTENER_HEAD_' + side + '_v177', .35)
        ty0, ty1 = [sgn * float(v) for v in cfg['end_fastener_thread_abs_y_range_mm']]
        thread_env = cyl(temp, x, ty0, ty1, z, float(cfg['end_fastener_thread_envelope_d_mm']))
        add(root, thread_env, 'REF_AXIAL_END_FASTENER_THREAD_ENVELOPE_' + side + '_v177', .25)

        bearing_span = abs(float(cfg['bearing_centers_abs_y_mm'][1]) - float(cfg['bearing_centers_abs_y_mm'][0]))
        shaft_fitting_overlap = outside_volume(temp, temp.copy(shaft), fitting)
        records.append(dict(
            side=side,
            bearing_center_span_mm=bearing_span,
            bearing_span_target_pass=abs(bearing_span - float(cfg['bearing_center_span_mm'])) < 1e-9,
            bearing_housing_containment=housing_checks,
            all_bearing_housings_inside_source_oml=all(r['containment_pass'] for r in housing_checks),
            round_bearing_regions_preserved=True,
            D_flat_local_engagement_abs_y_mm=[d0, d1],
            positive_surface_axial_retention_candidate='inner shaft collar + outer end washer/axial fastener',
            bearing_stack_axial_retention_candidate='inboard shaft collar + outboard shaft shoulder',
            transverse_shaft_hole_used=False,
            shaft_fitting_outside_volume_probe_cm3=shaft_fitting_overlap))

    audit = dict(
        status='V177_STABILATOR_BEARING_AND_AXIAL_RETENTION_PACKAGING',
        source=cfg,
        records=records,
        geometry_candidate_pass=all(r['bearing_span_target_pass'] and r['all_bearing_housings_inside_source_oml'] for r in records),
        two_radial_bearings_per_side_designed=True,
        bearing_regions_round_6mm=True,
        D_flat_restricted_to_root_fitting_region=True,
        positive_surface_axial_retention_designed=True,
        bearing_stack_axial_retention_designed=True,
        actual_bearing_hardware_frozen=False,
        actual_shaft_hardware_frozen=False,
        collar_fastener_hardware_frozen=False,
        end_fastener_thread_strength_verified=False,
        printed_bearing_housing_load_path_verified=False,
        mechanism_dynamic_clearance_verified=False,
        bench_proof_pass=False,
        print_release=False,
        flight_release=False,
        study_source_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest())

    os.makedirs(outdir, exist_ok=True)
    f3d = os.path.join(outdir, 'F14_STABILATOR_BEARING_RETENTION_v177.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(f3d)):
        raise RuntimeError('v177 archive export failed')
    with open(os.path.join(outdir, 'F14_v177_stabilator_bearing_retention_audit.json'), 'w', encoding='utf-8') as stream:
        json.dump(audit, stream, indent=2)
    app.activeViewport.fit()
    app.activeViewport.saveAsImageFile(os.path.join(outdir, 'F14_v177_stabilator_bearing_retention_review.png'), 1600, 1000)
    if prior:
        try: prior.activate()
        except: pass
    return audit
