import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'analysis'/'original_front_sources'
j=json.loads((SRC/'C_open_raster_chains.json').read_text(encoding='utf-8'));c=next(x for x in j['cases'] if x['threshold']==128);chains=c['segments_pixel']
W,H=1200,620;ml,mr,mt,mb=80,50,70,70;xs=[p[0] for s in chains for p in s];ys=[p[1] for s in chains for p in s];xmin,xmax=min(xs)-15,max(xs)+15;ymin,ymax=min(ys)-15,max(ys)+15
sx=lambda x:ml+(x-xmin)/(xmax-xmin)*(W-ml-mr);sy=lambda y:mt+(y-ymin)/(ymax-ymin)*(H-mt-mb)
colors=['#d62728','#1f77b4','#2ca02c','#9467bd'];names=['Kette 0 oben/links','Kette 1 unten/links','Kette 2 unten/rechts','Kette 3 oben/rechts']
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="{W/2}" y="30" text-anchor="middle" font-family="Arial" font-size="22">F-14 Sektion C – vier offene Rasterketten – Referenzstudie 20.10.2026</text>']
# horizontales Achsenband explizit als verdeckt markieren
svg.append(f'<rect x="{sx(xmin):.1f}" y="{sy(607):.1f}" width="{sx(xmax)-sx(xmin):.1f}" height="{sy(612)-sy(607):.1f}" fill="#eeeeee" stroke="#999999" stroke-dasharray="5,5"/>')
svg.append(f'<text x="{sx(xmin)+8:.1f}" y="{sy(609)+4:.1f}" font-family="Arial" font-size="12">Achsenüberdeckung y=607..612, Kontur dort ungemessen</text>')
for i,s in enumerate(chains):
 step=max(1,len(s)//180);d=s[::step];
 if d[-1]!=s[-1]:d.append(s[-1])
 pts=' '.join(f'{sx(x):.1f},{sy(y):.1f}' for x,y in d);svg.append(f'<polyline points="{pts}" fill="none" stroke="{colors[i]}" stroke-width="2"/>')
 for p in (s[0],s[-1]):svg.append(f'<circle cx="{sx(p[0]):.1f}" cy="{sy(p[1]):.1f}" r="4" fill="{colors[i]}" stroke="black"/>')
# unbekannte Verbindungen nur gestrichelt als Distanz, nicht als Kontur
pairs=[(chains[0][0],chains[3][-1]),(chains[1][-1],chains[2][0]),(chains[0][-1],chains[1][0]),(chains[2][-1],chains[3][0])]
for a,b in pairs:svg.append(f'<line x1="{sx(a[0]):.1f}" y1="{sy(a[1]):.1f}" x2="{sx(b[0]):.1f}" y2="{sy(b[1]):.1f}" stroke="#555555" stroke-width="1.5" stroke-dasharray="4,5"/>')
for i,(co,nm) in enumerate(zip(colors,names)):
 y=75+i*22;svg.append(f'<line x1="850" y1="{y}" x2="885" y2="{y}" stroke="{co}" stroke-width="3"/><text x="895" y="{y+5}" font-family="Arial" font-size="13">{nm}</text>')
svg += [f'<line x1="{ml}" y1="{H-mb}" x2="{W-mr}" y2="{H-mb}" stroke="black"/>',f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{H-mb}" stroke="black"/>',f'<text x="{W/2}" y="{H-22}" text-anchor="middle" font-family="Arial" font-size="14">Quellbild-x [Pixel]</text>',f'<text x="24" y="{H/2}" transform="rotate(-90 24 {H/2})" text-anchor="middle" font-family="Arial" font-size="14">Quellbild-y [Pixel]</text>',f'<text x="80" y="585" font-family="Arial" font-size="12">Gestrichelte Verbindungen zeigen nur offene Endpunktabstände. Sie sind ausdrücklich keine rekonstruierte Haut.</text>','</svg>']
out=ROOT/'docs'/'images'/'f14_C_open_chain_semantics_20261020.svg';out.parent.mkdir(parents=True,exist_ok=True);out.write_text('\n'.join(svg),encoding='utf-8');print(out)
