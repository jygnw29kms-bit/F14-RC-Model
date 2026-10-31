from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent;old=R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json';ref=json.loads(old.read_text());names=['NASA_CR172559_20deg_root_break_profiles.json','NASA_CR172559_combined20_span164p01460_profile.json','NASA_CR172559_combined20_span200p79919_profile.json','NASA_CR172559_combined20_span237_274_profiles.json','NASA_CR172559_combined20_span274p36816_complete_profile.json','NASA_CR172559_combined20_span311p15283_profile.json','NASA_CR172559_combined20_span347p93726_profile.json','NASA_CR172559_combined20_span384p69995_profile.json'];rows=[]
for i,n in enumerate(names):
 d=json.loads((P/n).read_text());r=d['rows'][1] if i==0 else d['rows'][0] if 'rows' in d else d;g=d.get('grid_xc',d.get('common_chord_grid_xc'));s=ref['sections'][i];m=[];grid=[]
 for k,(x,u,l) in enumerate(s['ordinates_xc_upper_lower']):
  if abs(x-g[k])>1e-9:grid.append({'index':k,'combined':g[k],'CR3992':x})
  for side,v in [('upper',u),('lower',l)]:
   actual=r['ordinate_'+side][k]
   if abs(v-actual)>1e-9:m.append({'index':k,'side':side,'combined':actual,'CR3992':v})
 rows.append({'combined_span':r['header_raw_fields'][1],'CR3992_span':s['wbl_in'],'ordinate_mismatch_count':len(m),'ordinate_mismatches':m,'grid_differences':grid})
out=P/'NASA_combined20_vs_CR3992_ordinate_crosscheck.json';assert not out.exists();out.write_text(json.dumps({'status':'INDEPENDENT_EXISTING_TRANSCRIPTION_COMPARISON_NOT_AUTOMATIC_CORRECTION','CR3992_dataset_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'combined_input_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in names},'rows':rows,'limits':['Existing CR3992 transcription is corroboration, not an infallible original','Every mismatch needs original page review; no automatic replacement','Different grids and root headers retained; index comparison is not physical point identity','No native CAD modification, factory OML or production acceptance']},indent=2)+'\n');print([(r['combined_span'],r['ordinate_mismatch_count']) for r in rows]);print([(r['combined_span'],r['ordinate_mismatches']) for r in rows if r['ordinate_mismatches']])
