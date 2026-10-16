"""Derive source-pixel axis candidates without assuming one waterline."""
from pathlib import Path
import json,hashlib
p=Path(__file__).parent
traces=p/'front_sections_pixel_candidates.json';envelopes=p/'front_AB_envelope_comparison.json'
profiles=json.loads(traces.read_text())['profiles'];comparisons=json.loads(envelopes.read_text())['comparisons'];rows=[]
for v in comparisons:
    profile=next(x for x in profiles if x['section']==v['section'])
    lo,hi=profile['loop_summary'][0]['bounds_pixels'];axis=profile['source_section_axis_pixel'][1]
    scale=v['plan_derived_isotropic_multiplier'];upper,lower=v['edge_centers_y_pixel'][2:]
    top_anchor=upper+(axis-lo[1])*scale
    bottom_anchor=lower-(hi[1]-axis)*scale
    rows.append(dict(section=v['section'],axis_from_upper_contour_pixel=top_anchor,axis_from_lower_contour_pixel=bottom_anchor,anchor_disagreement_pixels=abs(top_anchor-bottom_anchor),equal_residual_translation_axis_candidate_pixel=(top_anchor+bottom_anchor)/2,interpretation='Equal-weight vertical translation only; isotropic section scale remains width-derived. This midpoint is an explicit least-squares candidate, not a verified source datum.'))
report=dict(status='FRONT_VERTICAL_REGISTRATION_CANDIDATES_NOT_VERIFIED',inputs=[dict(path=x.name,sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in [traces,envelopes]],profiles=rows,common_waterline_verified=False,production_loft_allowed=False,assumptions=['Plan and side stations correspond by raster X; both views share horizontal placement.','Separately drawn section horizontal axes are local drawing annotations; a shared aircraft waterline is not inferred.','Equal upper/lower weighting is a study choice; no anisotropic deformation is applied.'],next_required='Review source trace/contour selection and independently register C plus original side silhouette before a continuous front loft.')
(p/'front_vertical_registration_candidates.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,indent=2))
