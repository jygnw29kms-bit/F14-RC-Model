"""ExpliziteLINE-Domaenen pruefen; Luecken niemals ueberbruecken."""
from pathlib import Path
import json,hashlib,math
O=Path(__file__).parent;p=O/'NASA_CR172559_sheet6_linear_entries.json';j=json.loads(p.read_text(encoding='utf-8'));rows=[]
for name,segs in j['variables'].items():
 chains=[];current=[];gaps=[]
 for seg in segs:
  x0,y0,x1,y1=seg;assert x1>x0 and all(math.isfinite(v) for v in seg)
  if current and current[-1][2]!=x0:
   gaps.append(dict(start=current[-1][2],end=x0,reason='NichtLINEdefinierterBereich; keineInterpolation'));chains.append(current);current=[]
  elif current:assert current[-1][3]==y0,(name,seg,'UnstetigerLINEAnschluss')
  current.append(seg)
 if current:chains.append(current)
 rows.append(dict(variable=name,segment_count=len(segs),continuous_LINE_domains=[[c[0][0],c[-1][2]] for c in chains],excluded_between_LINE_domains=gaps,slopes=[dict(x0=a,x1=c,slope=(d-b)/(c-a)) for a,b,c,d in segs]))
r=dict(status='EXPLIZITE_LINE_DOMAENEN_UND_ANSCHLUESSE_GEPRUEFT',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=rows,limits=['Koordinateneinheitenweiterunverifiziert; keineUmrechnunginmm.','ELLX/ELLY-Bereichefehlenbewusst.','StetigeLINE-EndpunktebelegenkeinevollstaendigeHaut/Querschnittsform oderOriginaltreue.'],production_release=False)
(O/'NASA_linear_body_domain_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['variable'],v['continuous_LINE_domains']) for v in rows])
