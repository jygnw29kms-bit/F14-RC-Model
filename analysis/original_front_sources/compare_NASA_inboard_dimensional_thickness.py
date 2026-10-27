from pathlib import Path
import json,hashlib
import numpy as np
p=Path(__file__).resolve().parent
names=['NASA_CR172559_inboard_first_three_profiles.json','NASA_CR172559_centerline_25_35_profiles.json','NASA_CR172559_span68p5_25_35_profiles.json','NASA_CR172559_span99_25_35_profiles.json']
docs={n:json.loads((p/n).read_text()) for n in names}
profiles={}
for r in docs[names[0]]['rows']:
 profiles[(20,r['header_raw_fields'][1])]=(docs[names[0]]['common_chord_grid_xc'],r)
for n in names[1:]:
 for r in docs[n]['rows']:profiles[(r['nominal_sweep_deg'],r['header_raw_fields'][1])]=(r['grid_xc'],r)
def curve(key):
 grid,r=profiles[key];h=r['header_raw_fields'];c=h[2]-h[0]
 x=h[0]+np.array(grid)*c;t=(np.array(r['ordinate_upper'])-r['ordinate_lower'])*c
 assert len(x)==len(t)==50 and np.all(np.diff(x)>0) and np.all(t>=0)
 return x,t
records=[]
for span in (0,68.5,99):
 x0,t0=curve((20,span))
 for angle in (25,35):
  x,t=curve((angle,span));lo=max(x0[0],x[0]);hi=min(x0[-1],x[-1])
  knots=np.unique(np.concatenate(([lo,hi],x0[(x0>=lo)&(x0<=hi)],x[(x>=lo)&(x<=hi)])))
  delta=np.interp(knots,x,t)-np.interp(knots,x0,t0)
  i=int(np.argmax(np.abs(delta)))
  # Difference of piecewise-linear functions is linear between union knots;
  # its maximum absolute value on the common domain is attained at a knot.
  samples=[]
  for f in (0,.1,.25,.5,.75,1):
   xx=lo+f*(hi-lo);a=float(np.interp(xx,x0,t0));z=float(np.interp(xx,x,t))
   samples.append({'fraction_of_common_domain':f,'X_source_units':xx,'thickness_20':a,'thickness_other':z,'difference':z-a})
  records.append({'span_source_units':span,'other_sweep_deg':angle,'common_X_domain':[lo,hi],'union_knots':len(knots),'max_abs_piecewise_linear_thickness_difference_source_units':float(abs(delta[i])),'at_X_source_units':float(knots[i]),'signed_difference_at_max':float(delta[i]),'samples':samples})
assert len(profiles)==9 and len(records)==6
out={'status':'CONDITIONAL_CHORD_SCALED_THICKNESS_COMPARISON_NOT_PHYSICAL_REGISTRATION','inputs':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names},'assumption':'X=XPL+xc*(XPT-XPL); thickness=(upper-lower)*(XPT-XPL). This chord normalization is an explicit working hypothesis pending original reader verification.','vertical_offset_independent':True,'method':'Linear interpolation on each original grid; union-knot maximum is exact for the piecewise-linear interpolants, not the underlying curved aircraft skin.','records':records,'limits':['Sixth header field never used','Does not prove equal upper/lower absolute position, camber or exposed fixed skin','Different thickness is conditional on chord scaling; no claim of physical aircraft inconsistency','No native CAD, master edit, structural or print release'],'production_release':False}
(p/'NASA_CR172559_inboard_dimensional_thickness_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print([(r['span_source_units'],r['other_sweep_deg'],round(r['max_abs_piecewise_linear_thickness_difference_source_units'],6)) for r in records])
