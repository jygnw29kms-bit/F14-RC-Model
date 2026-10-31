import FreeCAD as App, Part, pathlib, json, hashlib

R = pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src = R / 'migration/freecad/F14_v295_X620_CAPTIVE_M3_RETENTION_CANDIDATE.FCStd'
profiles_path = R / 'analysis/propulsion_intermediate_profiles_v135.json'
constraints_path = R / 'analysis/propulsion_source_silhouette_constraints_v134.json'
out = R / 'migration/freecad/F14_v296_SOURCE_BACKED_AFT_OML.FCStd'
aud_path = R / 'migration/freecad/freecad_v296_source_backed_aft_oml_audit.json'

profile_data = json.loads(profiles_path.read_text(encoding='utf-8'))
constraints = json.loads(constraints_path.read_text(encoding='utf-8'))
expected_source_sha = '63413c7958648165ca381ebda27ef31a4d6aabed725b84d3e2f804da5bafb5b4'
if profile_data.get('source_image_sha256') != expected_source_sha:
    raise RuntimeError('v135 source-image provenance mismatch')
if constraints.get('source_image_sha256') != expected_source_sha:
    raise RuntimeError('v134 constraint provenance mismatch')

base = {p['name']: p for p in profile_data['base_profiles']}
guides = {p['name']: p for p in profile_data['guide_profiles']}
ordered = [base.get(name, guides.get(name)) for name in profile_data['profile_order']]
if any(p is None for p in ordered):
    raise RuntimeError('profile order references missing section')
if any(len(p['points']) != profile_data['point_count_each'] for p in ordered):
    raise RuntimeError('profile point-count mismatch')

source_doc = App.openDocument(str(src))
doc = App.newDocument('F14_v296_SOURCE_BACKED_AFT_OML')
for ob in source_doc.Objects:
    if hasattr(ob, 'Shape') and not ob.Shape.isNull():
        cp = doc.addObject('PartDesign::Feature', ob.Name)
        cp.Shape = ob.Shape.copy()
        cp.Label = ob.Label

wires = []
section_rows = []
for prof in ordered:
    x = float(prof['x_mm'])
    pts = [App.Vector(x, float(y), float(z)) for y, z in prof['points']]
    edges = [Part.makeLine(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
    wire = Part.Wire(edges)
    if not wire.isClosed():
        raise RuntimeError('open section wire: ' + prof['name'])
    wires.append(wire)
    ys = [p.y for p in pts]
    zs = [p.z for p in pts]
    section_rows.append({
        'name': prof['name'], 'x_mm': x, 'point_count': len(pts),
        'y_min_mm': min(ys), 'y_max_mm': max(ys),
        'z_min_mm': min(zs), 'z_max_mm': max(zs),
        'source_kind': 'traced' if prof['name'] in ('D','E','F') else 'constrained_interpolation'
    })

# The v135 guide sections already constrain the transition. Use ruled spans between
# the seven sections to avoid spline overshoot outside the source-derived section envelope.
loft = Part.makeLoft(wires, True, True)
if loft.isNull() or not loft.isValid() or len(loft.Solids) != 1:
    raise RuntimeError('source-backed aft OML loft invalid')
oml = doc.addObject('PartDesign::Feature', 'V296_SOURCE_BACKED_AFT_OML')
oml.Shape = loft
oml.Label = 'v296 source-backed aft OML D-F'

checks = []
# Evaluate only the portion of each X620 part that lies inside the aft-OML X domain.
# The 80 mm CF tubes extend forward of station D by design; judging their full length
# against an OML that starts at D would create a false failure.
xmin = min(float(p['x_mm']) for p in ordered)
xmax = max(float(p['x_mm']) for p in ordered)
domain_box = Part.makeBox(xmax - xmin + 0.02, 500.0, 500.0, App.Vector(xmin - 0.01, -250.0, -250.0))
for name in ['V293_X620_CF_TUBE_R','V293_X620_CF_TUBE_L','V293_X620_SLEEVE_R_AFT','V293_X620_SLEEVE_L_AFT','V295_C_CLAMP_X620_R','V295_C_CLAMP_X620_L']:
    ob = doc.getObject(name)
    if not ob or ob.Shape.isNull():
        raise RuntimeError('missing X620 object: ' + name)
    domain_part = ob.Shape.common(domain_box)
    domain_vol = domain_part.Volume
    inside = domain_part.common(loft).Volume if domain_vol else 0.0
    frac = inside / domain_vol if domain_vol else 1.0
    checks.append({'object': name, 'full_volume_mm3': ob.Shape.Volume, 'aft_domain_volume_mm3': domain_vol,
                   'inside_oml_mm3': inside, 'aft_domain_containment_fraction': frac})

# Cross-check directly traced D/E/F vertical extrema against the independent v134 source constraints.
constraint_by_name = {s['name']: s for s in constraints.get('side_samples', []) if s.get('kind') == 'DE_station'}
trace_checks = []
for row in section_rows:
    if row['name'] in constraint_by_name:
        c = constraint_by_name[row['name']]
        top_err = abs(row['z_max_mm'] - float(c['expected_z_top_mm']))
        bot_err = abs(row['z_min_mm'] - float(c['expected_z_bottom_mm']))
        trace_checks.append({'name': row['name'], 'z_top_error_mm': top_err, 'z_bottom_error_mm': bot_err,
                             'pass': top_err <= constraints['acceptance']['z_top_abs_error_mm'] and bot_err <= constraints['acceptance']['z_bottom_abs_error_mm']})

bbox = loft.BoundBox
doc.recompute()
doc.saveAs(str(out))

audit = {
    'status': 'V296_SOURCE_BACKED_AFT_OML_FREECAD_MIGRATION',
    'source_model': src.name,
    'source_profiles': str(profiles_path.relative_to(R)).replace('\\','/'),
    'source_constraints': str(constraints_path.relative_to(R)).replace('\\','/'),
    'source_image_sha256': expected_source_sha,
    'profile_order': profile_data['profile_order'],
    'section_rows': section_rows,
    'trace_checks': trace_checks,
    'oml': {
        'valid': loft.isValid(), 'solid_count': len(loft.Solids), 'volume_mm3': loft.Volume,
        'bbox_mm': {'xmin': bbox.XMin, 'xmax': bbox.XMax, 'ymin': bbox.YMin, 'ymax': bbox.YMax, 'zmin': bbox.ZMin, 'zmax': bbox.ZMax}
    },
    'x620_checks': checks,
    'gates': {
        'source_provenance_match': True,
        'seven_profile_loft_valid': loft.isValid() and len(loft.Solids) == 1 and len(wires) == 7,
        'traced_DE_constraints_pass': all(c['pass'] for c in trace_checks) and len(trace_checks) == 2,
        'x620_joiner_and_retention_aft_domain_inside_oml_ge_0p995': all(c['aft_domain_containment_fraction'] >= 0.995 for c in checks),
        'aft_nacelle_OML_registered': True,
        'intermediate_profiles_source_measured': False,
        'actual_EDF_hardware_measured': False,
        'print_release': False,
        'flight_release': False
    }
}
audit['sha256'] = hashlib.sha256(out.read_bytes()).hexdigest()
aud_path.write_text(json.dumps(audit, indent=2), encoding='utf-8')
print(json.dumps(audit, indent=2))
