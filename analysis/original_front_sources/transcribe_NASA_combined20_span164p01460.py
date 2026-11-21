from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;src=P/'NASA_CR172559_inboard_first_three_profiles.json';base=json.loads(src.read_text());g=base['common_chord_grid_xc']
u=list(map(float,''' .00878 .01488 .01831 .02205 .02742 .03498 .04063
.04519 .04901 .05226 .05502 .05737 .05934 .06097
.06229 .06331 .06406 .06456 .06481 .06483 .06464
.06424 .06365 .06288 .06193 .06081 .05953 .05811
.05654 .05484 .05107 .04685 .04224 .03730 .03473
.03209 .02939 .02665 .02386 .02103 .01818 .01529
.01239 .00947 .00655 .00359 .00064 -.00231 -.00526
-.00821'''.split()))
l=list(map(float,''' .00878 .00324 -.00023 -.00362 -.00778 -.01273 -.01589
-.01819 -.01997 -.02142 -.02263 -.02366 -.02455 -.02534
-.02604 -.02665 -.02720 -.02767 -.02808 -.02843 -.02871
-.02893 -.02909 -.02918 -.02920 -.02917 -.02907 -.02890
-.02868 -.02839 -.02765 -.02668 -.02552 -.02417 -.02343
-.02266 -.02185 -.02100 -.02013 -.01923 -.01831 -.01736
-.01639 -.01541 -.01442 -.01342 -.01241 -.01139 -.01037
-.00935'''.split()))
assert len(g)==len(u)==len(l)==50 and u[0]==l[0] and all(x>=y for x,y in zip(u,l));t=[x-y for x,y in zip(u,l)]
out=P/'NASA_CR172559_combined20_span164p01460_profile.json';assert not out.exists();out.write_text(json.dumps({'status':'ONE_COMBINED20_OUTBOARD_PROFILE_VISUALLY_TRANSCRIBED_ACROSS_PAGE_JOIN','source_sha256':base['source_sha256'],'source_pdf_pages':[21,22],'nominal_sweep_deg':20,'grid_xc':g,'header_raw_fields':[516.19336,164.01460,631.00684,0,1,159.12769],'ordinate_upper':u,'ordinate_lower':l,'max_normalized_thickness':max(t),'trailing_edge_gap':t[-1],'normalized_piecewise_linear_area':sum((g[i+1]-g[i])*(t[i+1]+t[i])/2 for i in range(49)),'visual_checks':['Upper 50 and first 21 lower values on PDF21; remaining 29 lower on PDF22 before next header','Lower page join: -.02871 then -.02893','Upper endpoint -.00821; lower endpoint -.00935','Combined grid .00496 preserved'],'limits':['No CAD loft or physical factory registration','Computational source profile; no structural print or flight acceptance'],'production_release':False},indent=2)+'\n');print('Verified 50+50; max thickness',max(t),'TE gap',t[-1])
