"""Geordneter Konturplan; ueberlappende Proben nicht automatisch verschmelzen."""
from pathlib import Path
import json,hashlib,math
import numpy as np
O=Path(__file__).parent
U='C_upper_raster_guides';L='C_lower_raster_guides';T='C_tips_shoulders';A='C_axis_corner_fragments';S='C_inlet_lower_sides';V='C_inlet_outer_upper_sides';J='C_inner_inlet_joins'
order=[(U,0,True),(T,0,False),(L,0,False),(T,2,False),(L,1,False),(A,0,False),(A,2,False),(V,0,False),(S,0,False),(L,2,False),(S,1,True),(J,0,True),(L,3,False),(L,4,False),(J,1,False),(S,2,False),(L,5,False),(S,3,True),(V,1,True),(A,3,True),(A,1,False),(L,6,False),(T,3,True),(L,7,False),(T,1,True),(U,1,True)]
expected={5:'linke_horizontale_Achse',12:'untere_vertikale_Achse',19:'rechte_horizontale_Achse',25:'obere_vertikale_Achse'}
names=list(dict.fromkeys(v[0] for v in order));data={n:json.loads((O/(n+'.json')).read_text(encoding='utf-8')) for n in names};rows=[]
assert len(set((n,i) for n,i,r in order))==26
for k,t in enumerate([96,128,160]):
 segs=[list(reversed(data[n]['cases'][k]['segments_pixel'][i])) if rev else data[n]['cases'][k]['segments_pixel'][i] for n,i,rev in order];joins=[]
 assert sum(len(data[n]['cases'][k]['segments_pixel']) for n in names)==26
 for i,a in enumerate(segs):
  b=segs[(i+1)%26];aa=np.array(a);bb=np.array(b);ds=((aa[:,None,:]-bb[None,:,:])**2).sum(axis=2);u,v=np.unravel_index(ds.argmin(),ds.shape);gap=math.sqrt(float(ds[u,v]));open_gap=i in expected
  assert (gap>math.sqrt(2)+1e-9)==open_gap,(t,i,gap)
  joins.append(dict(after_index=i,next_index=(i+1)%26,minimum_sample_distance_pixel=gap,directed_endpoint_distance_pixel=math.dist(a[-1],b[0]),nearest_a=a[u],nearest_b=b[v],status='UNGEMESSENE_ACHSENLUECKE' if open_gap else 'NAEHE_ODER_UEBERLAPPUNG_NICHT_VERSCHMOLZEN',region=expected.get(i),bridge_created=False))
 rows.append(dict(threshold=t,joins=joins))
report=dict(status='C_GEORDNETER_REFERENZPLAN_VORBEREITET_UND_ABSTANDSGEPRUEFT',inputs={n:hashlib.sha256((O/(n+'.json')).read_bytes()).hexdigest() for n in names},order=[dict(source=n,segment=i,reverse=rev) for n,i,rev in order],rows=rows,limits=['Reihenfolge anhand Originaloverlay; vier Achsenluecken bleiben offen.','Benachbarte Segmente ueberlappen teils. Minimalpunktnaehe ist keine gemeinsame Endpunkt-Topologie.','Vor nativer Gesamtlinie sind Zuschnitt, eindeutige Uebergangspunkte und Selbstschnittpruefung erforderlich.','Keine geschlossene Sektion, Originalhaut, metrische Registrierung oder Produktionsfreigabe.'],production_release=False)
(O/'C_ordered_reference_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('26 eindeutige Segmente je Schwelle, exakt4ausdruecklich offene Achsenuebergaenge; keine Verschmelzung.')
