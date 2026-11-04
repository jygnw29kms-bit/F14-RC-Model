from pathlib import Path
import json,hashlib,math
p=Path(__file__).resolve().parent
src=p/'NASA_CR172559_inboard_sweep_grid_comparison.json'
b=json.loads(src.read_text())
raw={25:["-.00040 .00148 .00250 .00361 .00515 .00736 .00921 .01093 .01257 .01414 .01563 .01703 .01834 .01956 .02068 .02169 .02260 .02341 .02412 .02473 .02524 .02566 .02600 .02625 .02643 .02653 .02656 .02653 .02644 .02628 .02580 .02507 .02408 .02279 .02203 .02117 .02022 .01919 .01806 .01684 .01553 .01414 .01267 .01114 .00955 .00791 .00624 .00453 .00279 .00105","-.00040 -.00150 -.00210 -.00278 -.00377 -.00507 -.00609 -.00700 -.00782 -.00856 -.00923 -.00982 -.01034 -.01078 -.01116 -.01148 -.01173 -.01192 -.01207 -.01215 -.01220 -.01220 -.01216 -.01208 -.01197 -.01184 -.01167 -.01148 -.01128 -.01105 -.01055 -.00999 -.00937 -.00869 -.00832 -.00793 -.00751 -.00707 -.00660 -.00610 -.00557 -.00502 -.00445 -.00386 -.00327 -.00266 -.00205 -.00145 -.00085 -.00024"],35:["-.00040 .00153 .00261 .00373 .00532 .00760 .00950 .01126 .01295 .01455 .01609 .01753 .01889 .02015 .02130 .02236 .02331 .02415 .02489 .02554 .02609 .02654 .02691 .02719 .02739 .02752 .02758 .02757 .02749 .02735 .02688 .02612 .02507 .02367 .02283 .02188 .02082 .01967 .01841 .01705 .01561 .01412 .01256 .01096 .00934 .00769 .00600 .00429 .00256 .00082","-.00040 -.00152 -.00216 -.00285 -.00386 -.00522 -.00626 -.00719 -.00802 -.00878 -.00946 -.01005 -.01056 -.01101 -.01138 -.01169 -.01194 -.01212 -.01225 -.01233 -.01236 -.01235 -.01230 -.01220 -.01209 -.01194 -.01176 -.01157 -.01135 -.01111 -.01060 -.01002 -.00937 -.00864 -.00825 -.00782 -.00738 -.00691 -.00641 -.00588 -.00534 -.00476 -.00418 -.00358 -.00299 -.00238 -.00178 -.00119 -.00060 -.00002"]}
rows=[]
for r in b['records']:
 angle=r['nominal_sweep_deg'];x=r['grid_xc'];u,l=[list(map(float,t.split())) for t in raw[angle]]
 assert len(x)==len(u)==len(l)==50
 assert all(math.isfinite(v) for v in x+u+l)
 assert u[0]==l[0] and all(a>=z for a,z in zip(u,l))
 thick=[a-z for a,z in zip(u,l)]
 area=sum((x[i+1]-x[i])*(thick[i+1]+thick[i])/2 for i in range(49))
 rows.append({'nominal_sweep_deg':angle,'source_pdf_page':r['source_pdf_page'],'header_raw_fields':r['first_three_headers'][0]['raw_header'],'grid_xc':x,'ordinate_upper':u,'ordinate_lower':l,'max_normalized_thickness_at_sample':max(thick),'normalized_piecewise_linear_area':area,'trailing_edge_gap':thick[-1]})
out={'status':'TWO_COMPLETE_CENTERLINE_COMPUTATIONAL_PROFILES_VISUALLY_TRANSCRIBED','source_sha256':b['source_sha256'],'grid_dataset_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':rows,'visual_digit_checks':['35deg upper penultimate value .00256; OCR .00258 rejected','35deg lower penultimate value -.00060; OCR -.00080 rejected'],'limits':['Centerline computational continuation, not exposed fixed-glove skin','No vertical registration or sixth-field interpretation','No invariant skin claim from normalized ordinates','No CAD geometry generated'],'production_release':False}
(p/'NASA_CR172559_centerline_25_35_profiles.json').write_text(json.dumps(out,indent=2)+'\n')
print([(r['nominal_sweep_deg'],r['max_normalized_thickness_at_sample'],r['normalized_piecewise_linear_area']) for r in rows])
