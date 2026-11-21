from pathlib import Path
import json
P=Path(__file__).resolve().parent;b=json.loads((P/'NASA_CR172559_inboard_first_three_profiles.json').read_text());g=b['common_chord_grid_xc']
u=list(map(float,'''-.00919 -.00300 .00061 .00452 .01008 .01787 .02378
.02865 .03287 .03659 .03993 .04294 .04566 .04810
.05030 .05226 .05399 .05550 .05679 .05788 .05876
.05944 .05992 .06022 .06033 .06026 .06001 .05960
.05902 .05828 .05634 .05384 .05083 .04735 .04545
.04347 .04139 .03923 .03700 .03471 .03235 .02994
.02749 .02500 .02249 .01994 .01738 .01481 .01223
.00965'''.split()))
l=list(map(float,'''-.00919 -.01499 -.01831 -.02131 -.02487 -.02883 -.03118
-.03278 -.03396 -.03488 -.03563 -.03626 -.03679 -.03722
-.03758 -.03786 -.03806 -.03818 -.03822 -.03818 -.03805
-.03784 -.03753 -.03715 -.03667 -.03610 -.03545 -.03470
-.03387 -.03296 -.03087 -.02846 -.02573 -.02272 -.02111
-.01943 -.01769 -.01590 -.01404 -.01214 -.01019 -.00820
-.00617 -.00410 -.00201 .00011 .00225 .00440 .00656
.00873'''.split()))
assert len(g)==len(u)==len(l)==50 and u[0]==l[0] and all(x>=y for x,y in zip(u,l));t=[x-y for x,y in zip(u,l)];out=P/'NASA_CR172559_combined20_span311p15283_profile.json';assert not out.exists();out.write_text(json.dumps({'status':'COMBINED20_PROFILE_VISUALLY_TRANSCRIBED','source_sha256':b['source_sha256'],'source_pdf_page':23,'nominal_sweep_deg':20,'grid_xc':g,'header_raw_fields':[569.77783,311.15283,637.55469,0,1,154.44666],'ordinate_upper':u,'ordinate_lower':l,'max_normalized_thickness':max(t),'trailing_edge_gap':t[-1],'visual_checks':['Leading edge -.00919 on both surfaces','Upper final .00965 and lower final .00873','Initial page value .00171 belongs to preceding274 profile, excluded here'],'limits':['Computational source only; no CAD execution or physical factory registration','No print structural or flight release'],'production_release':False},indent=2)+'\n');print(max(t),t[-1])
