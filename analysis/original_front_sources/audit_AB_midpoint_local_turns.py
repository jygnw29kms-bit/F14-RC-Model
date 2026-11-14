"""Lokale Rasterzacken markieren, nicht glaetten oder als Schraffur klassifizieren."""
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;p=O/'AB_open_stroke_midpoint_guides.json';j=json.loads(p.read_text(encoding='utf-8'));rows=[]
for section in j['sections']:
 for c in section['cases']:
  flags=[]
  for k,s in enumerate(c['segments_pixel']):
   for i in range(1,len(s)-1):
    a,b,d=s[i-1:i+2];assert b[1]-a[1]==d[1]-b[1]==1
    dx0=b[0]-a[0];dx1=d[0]-b[0];second=dx1-dx0
    if abs(second)>1:
     flags.append(dict(segment=k,index=i,point=b,previous_dx=dx0,next_dx=dx1,second_difference_pixel=second,semantic_identity_verified=False))
  rows.append(dict(section=section['section'],threshold=c['threshold'],flag_count=len(flags),flags=flags))
r=dict(status='AB_LOKALE_RICHTUNGSWECHSEL_NUR_SCREENING',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,method='Zweite horizontale Differenz bei1PixelZeilenabstand; Betrag>1Pixel markiert. Originalpunkte unveraendert.',limits=['Heuristische Kandidaten, keine automatische Schraffuridentifikation.','Echte Konturstufen/Kruemmung koennen ebenfalls markiert werden; kein automatisches Loeschen oder Glaetten.','Kein Toleranznachweis, keine neue Konturgeometrie oder Produktionsfreigabe.'],production_release=False)
(O/'AB_midpoint_local_turn_screen.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['section'],v['threshold'],v['flag_count']) for v in rows])
