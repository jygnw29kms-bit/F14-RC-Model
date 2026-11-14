from pathlib import Path
import json,hashlib,math
P=Path(__file__).resolve().parent; src=P/'NASA_CR172559_20deg_root_break_profiles.json';d=json.loads(src.read_text());a,b=d['rows'];g=d['common_chord_grid_xc'];ha,hb=a['header_raw_fields'],b['header_raw_fields'];ca=ha[2]-ha[0];cb=hb[2]-hb[0];result=[]
for side in ('upper','lower'):
 rows=[]
 for x,za,zb in zip(g,a['ordinate_'+side],b['ordinate_'+side]):
  dx=(hb[0]+x*cb)-(ha[0]+x*ca);dz=(hb[5]+zb*cb)-(ha[5]+za*ca)
  rows.append({'xc':x,'delta_x':dx,'delta_z':dz,'matched_xc_distance':math.sqrt(dx*dx+(hb[1]-ha[1])**2+dz*dz)})
 result.append({'side':side,'max_abs_delta_z':max(rows,key=lambda r:abs(r['delta_z'])),'rows':rows})
thickness=[{'xc':x,'inboard':(u-l)*ca,'outboard':(uu-ll)*cb} for x,u,l,uu,ll in zip(g,a['ordinate_upper'],a['ordinate_lower'],b['ordinate_upper'],b['ordinate_lower'])]
for r in thickness:r['delta']=r['outboard']-r['inboard']
# Independent cancellation check: upper-minus-lower displacement equals thickness change.
for i,r in enumerate(thickness):assert abs((result[0]['rows'][i]['delta_z']-result[1]['rows'][i]['delta_z'])-r['delta'])<1e-12
out=P/'NASA_20deg_root_break_discontinuity_screen.json';assert not out.exists();out.write_text(json.dumps({'status':'CONDITIONAL_MATCHED_XC_SOURCE_SECTION_COMPARISON','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'span_gap_raw':hb[1]-ha[1],'coordinate_hypothesis':'X=XPL+xc*chord;Y=rawspan;Z=field6+ordinate*chord','chords_raw':[ca,cb],'surface_displacements':result,'thickness_comparison':thickness,'maximum_abs_thickness_change':max(thickness,key=lambda r:abs(r['delta'])),'independent_upper_minus_lower_identity_passed':True,'limits':['Distances are corresponding-xc samples, not closest-surface distances','Source units only; no physical model scale','A near-zero span gap with different section contours does not establish a manufacturable transition','No bridge, blend, topology or source-error correction is authorized by this calculation','No factory OML, structural, print or flight release'],'production_release':False},indent=2)+'\n');print(json.dumps({'surface_maxima':[r['max_abs_delta_z'] for r in result],'thickness_max':max(thickness,key=lambda r:abs(r['delta']))}))
