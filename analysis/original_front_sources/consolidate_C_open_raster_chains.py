"""Vier offene Rasterketten; keine Verbindung ueber Achsenueberdeckung."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
O=Path(__file__).parent;R=O.parents[1];m=json.loads((O/'C_ordered_reference_manifest.json').read_text(encoding='utf-8'));data={n:json.loads((O/(n+'.json')).read_text(encoding='utf-8')) for n in m['inputs']};cases=[]
for k,t in enumerate([96,128,160]):
 segs=[list(reversed(data[v['source']]['cases'][k]['segments_pixel'][v['segment']])) if v['reverse'] else data[v['source']]['cases'][k]['segments_pixel'][v['segment']] for v in m['order']];chains=[];logs=[]
 for lo,hi in [(0,5),(6,12),(13,19),(20,25)]:
  starts={lo:0};ends={hi:len(segs[hi])-1}
  for i in range(lo,hi):
   a=np.array(segs[i]);b=np.array(segs[i+1]);ds=((a[:,None,:]-b[None,:,:])**2).sum(axis=2);best=ds.min();assert best<=2
   options=np.argwhere(ds==best)
   # Deterministischer Zuschnitt: spaetester passender Punkt auf dem vorigen Segment.
   u,v=max(options.tolist(),key=lambda z:(z[0],-z[1]));ends[i]=u;starts[i+1]=v
   logs.append(dict(after=i,index_a=u,index_b=v,gap_pixel=math.sqrt(float(best))))
  chain=[]
  for i in range(lo,hi+1):
   assert starts[i]<=ends[i],(t,i,starts[i],ends[i])
   for point in segs[i][starts[i]:ends[i]+1]:
    if not chain or point!=chain[-1]:chain.append(point)
  assert len(chain)==len(set(map(tuple,chain))),(t,lo,'Wiederholter Punkt')
  chains.append(chain)
 cases.append(dict(threshold=t,segments_pixel=chains,trimming=logs))
j=dict(status='C_VIER_OFFENE_RASTERKETTEN_KONSOLIDIERT',manifest_sha256=hashlib.sha256((O/'C_ordered_reference_manifest.json').read_bytes()).hexdigest(),cases=cases,method='Gerichtete26Referenzen an naechsten Rasterpunkten zuschneiden; maximal sqrt2px benachbarte Rasterpunkte verbinden, keine Achsenbruecken.',limits=['Zuschnittregel deterministisch, keine nachgewiesene Strichmitte oder exakte Haut.','Keine wiederholten Punkte; geometrische Selbstschnittpruefung und native Ausfuehrung stehen separat aus.','Vier Achsenluecken bleiben offen; keine geschlossene Sektion oder Produktionsfreigabe.'],production_release=False)
(O/'C_open_raster_chains.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');im=Image.open(R/'references/UPC_Figure3_15_source_exact.png').convert('RGB').crop((805,520,1330,700)).resize((1575,540));dr=ImageDraw.Draw(im)
for s,c in zip(cases[1]['segments_pixel'],['red','blue','green','magenta']):dr.line([((x-805)*3,(y-520)*3) for x,y in s],fill=c,width=1)
im.save(O/'C_open_raster_chains_overlay.png');print([(c['threshold'],[len(s) for s in c['segments_pixel']]) for c in cases])
