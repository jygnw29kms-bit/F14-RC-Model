"""Read-only source-code/frame audit; no native geometry or assembly correction."""
import ast, hashlib, json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
files=['migration/freecad/build_current_full_view.py','migration/freecad/normalize_datums_v191.py','migration/freecad/build_sweep_v192.py','migration/freecad/verify_dynamic_linkage_v194.py']
records=[]
for rel in files:
 p=R/rel; text=p.read_text(encoding="utf-8-sig"); tree=ast.parse(text)
 px=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PX' for t in n.targets): px.append(ast.literal_eval(n.value))
 records.append(dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),PX_literals=px))
wing=json.loads((R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json').read_text())
s=900/(2*wing['sections'][-1]['wbl_in'])
f=json.loads((R/'analysis/propulsion_source_silhouette_constraints_v134.json').read_text())
x0=f['x_mapping']['E_source_px']-f['x_mapping']['E_model_mm']/f['common_scale_mm_per_pixel']
build=(R/files[0]).read_text(encoding="utf-8-sig")
assert "(sec['leading_edge_fs_in']+x*chord)*factor" in build
assert all(abs(x-524.16*s)<1e-9 for rec in records for x in rec['PX_literals'])
report=dict(status='STATIC_CODE_TRACE_CONFIRMS_ABSOLUTE_FS_WING_AND_PIVOT_PLACEMENT',records=records,scale_mm_per_source_in=s,wing_builder_formula='(leading_edge_fs_in + xc * chord_in) * factor; no FS93 subtraction',v191_followup='Changes wing Placement Z only; no X datum correction in this script.',pivot_absolute_mm=524.16*s,pivot_nose_relative_candidate_mm=(524.16-93)*s,delta_mm=-93*s,UPC_frame_implied_zero_source_pixel=x0,UPC_zero_is_verified_aircraft_nose=False,assessment='Wing and pivot consistently share absolute FS frame. Fuselage/UPC frame correspondence is still unverified. Subtracting FS93 only from pivot would break existing wing-pivot relationship.',safe_next='Verify UPC nose and at least one independent source landmark; then create separate candidate shifting wing AND pivot/mechanism consistently. Do not alter current master or claim native containment from this static audit.',native_execution=False,geometry_changed=False,production_release=False)
Path(__file__).with_name('longitudinal_placement_code_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['delta_mm','pivot_nose_relative_candidate_mm','UPC_frame_implied_zero_source_pixel']}))
