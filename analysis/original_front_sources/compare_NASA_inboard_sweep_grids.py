from pathlib import Path
import json, hashlib
p=Path(__file__).resolve().parent
old=p/'NASA_CR172559_inboard_first_three_profiles.json'
b=json.loads(old.read_text())
common=[0,.00201,.00501,.01002,.02005,.04,.05997,.08,.10,.12,.14002,.16,.18,.20,.22,.24,.26,.28,.30,.32,.34,.36,.38,.40,.42,.44,.46,.48,.50,.52,.56,.60,.64,.68,.69998,.72,.74,.76,.78,.80,.82,.84,.86,.88,.90,.92,.94,.96,.98,1]
g35=[0,.00198,.00506,.01,.02,.04005,.06,.08,.10,.12,.14006,.16,.18,.20,.22,.24,.26,.28,.30,.32,.34,.36,.38,.40,.42,.44,.46,.48,.50,.52,.56,.60,.64,.68,.70,.72,.74,.76,.78,.80,.82,.84,.86,.88,.90,.92,.94,.96,.98,1]
headers={25:[[187.90012,0,615.17920,0,1,162.45967],[357.44357,68.5,624.19702,0,1,161.10240],[432.93372,99,628.21216,0,1,160.49806]],35:[[187.90012,0,599.60083,0,1,162.59918],[357.44357,68.5,621.27344,0,1,161.17725],[432.93372,99,630.92334,0,1,160.54413]]}
records=[]
for angle,grid in [(25,common),(35,g35)]:
 assert len(grid)==50 and all(y>x for x,y in zip(grid,grid[1:]))
 rows=[]
 for prev,new in zip(b['rows'],headers[angle]):
  raw=prev['header_raw_fields'];assert raw[:2]==new[:2]
  rows.append({'raw_header':new,'trailing_edge_X_change_from_20':new[2]-raw[2],'chord_source_units':new[2]-new[0],'sixth_field_change_uninterpreted':new[5]-raw[5]})
 records.append({'nominal_sweep_deg':angle,'source_pdf_page':29 if angle==25 else 33,'grid_xc':grid,'max_grid_difference_from_20':max(abs(x-y) for x,y in zip(grid,b['common_chord_grid_xc'])),'differing_grid_indices_zero_based':[i for i,(x,y) in enumerate(zip(grid,b['common_chord_grid_xc'])) if x!=y],'first_three_headers':rows})
out={'status':'VISUALLY_VERIFIED_SHARED_GRID_AND_FIRST_THREE_HEADERS_ONLY','source_sha256':b['source_sha256'],'baseline_dataset_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'records':records,'finding':'Each sweep uses its own common 50-point normalized chord grid and different trailing-edge X coordinates even at equal inboard span positions. Equal array index does not guarantee equal normalized or dimensional X.','limits':['Upper/lower ordinates for 25/35 not transcribed by this script','No vertical registration or sixth-field interpretation','No demonstrated invariant fixed-glove skin; compare at common dimensional X after resolving ordinate conventions','Centerline is computational continuation, not automatically exposed skin'],'geometry_changed':False,'production_release':False}
(p/'NASA_CR172559_inboard_sweep_grid_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print([(r['nominal_sweep_deg'],r['max_grid_difference_from_20']) for r in records])
