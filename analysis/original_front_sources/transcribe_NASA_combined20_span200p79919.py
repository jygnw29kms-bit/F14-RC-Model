from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;src=P/'NASA_CR172559_inboard_first_three_profiles.json';base=json.loads(src.read_text());g=base['common_chord_grid_xc']
u=list(map(float,''' .00722 .01327 .01657 .02033 .02564 .03300 .03852
.04301 .04682 .05010 .05294 .05540 .05751 .05930
.06078 .06198 .06291 .06359 .06402 .06421 .06419
.06395 .06351 .06287 .06205 .06105 .05989 .05856
.05708 .05546 .05182 .04770 .04317 .03828 .03572
.03310 .03042 .02770 .02492 .02211 .01927 .01640
.01351 .01061 .00770 .00478 .00185 -.00107 -.00400
-.00692'''.split()))
l=list(map(float,''' .00722 .00165 -.00173 -.00503 -.00897 -.01357 -.01650
-.01863 -.02029 -.02164 -.02277 -.02375 -.02461 -.02537
-.02606 -.02668 -.02723 -.02772 -.02816 -.02853 -.02884
-.02909 -.02928 -.02940 -.02945 -.02944 -.02936 -.02921
-.02900 -.02871 -.02795 -.02694 -.02570 -.02424 -.02343
-.02256 -.02166 -.02074 -.01977 -.01876 -.01772 -.01665
-.01556 -.01445 -.01332 -.01217 -.01102 -.00986 -.00869
-.00753'''.split()))
assert len(g)==len(u)==len(l)==50 and u[0]==l[0] and all(x>=y for x,y in zip(u,l));t=[x-y for x,y in zip(u,l)]
out=P/'NASA_CR172559_combined20_span200p79919_profile.json';assert not out.exists();out.write_text(json.dumps({'status':'ONE_COMBINED20_OUTBOARD_PROFILE_VISUALLY_TRANSCRIBED','source_sha256':base['source_sha256'],'source_pdf_page':22,'review_image':'NASA_CR172559_combined_page22_outboard_review.png','nominal_sweep_deg':20,'grid_xc':g,'header_raw_fields':[529.58618,200.79919,632.64380,0,1,158.07434],'ordinate_upper':u,'ordinate_lower':l,'max_normalized_thickness':max(t),'trailing_edge_gap':t[-1],'normalized_piecewise_linear_area':sum((g[i+1]-g[i])*(t[i+1]+t[i])/2 for i in range(49)),'visual_checks':['50 upper and 50 lower values visible entirely on PDF22','Upper sixth row .03310 .03042 .02770 .02492 .02211 .01927 .01640','Upper endpoint -.00692; lower endpoint -.00753','Combined source grid .00496 retained, not isolated .00491'],'limits':['No CAD execution, interpolation to neighbouring stations, physical registration or factory OML acceptance','Source computational profile only; no structural print or flight release'],'production_release':False},indent=2)+'\n');print('50+50 values checked; thickness',max(t),'TE gap',t[-1])
