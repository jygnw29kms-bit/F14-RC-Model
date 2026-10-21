"""Schwellwertsensitivitaet ist keine vollstaendige Messunsicherheit."""
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;frame=json.loads((O/'front_shared_frame_candidate.json').read_text(encoding='utf-8'));rows=[];inputs={}
for sec,name,key in [('A','A_raster_envelope_v2_candidates.json','loop_pixel'),('B','B_raster_envelope_v2_candidates.json','loop_pixel'),('C','C_axis_closure_sensitivity.json','points_pixel')]:
 p=O/name;inputs[name]=hashlib.sha256(p.read_bytes()).hexdigest();j=json.loads(p.read_text(encoding='utf-8'));scale=next(x for x in frame['profiles'] if x['section']==sec)['isotropic_mm_per_section_pixel'];cases=[]
 for c in j['cases']:
  if sec=='C' and c['offset_pixel']!=0:continue
  pts=c[key];w=max(x for x,y in pts)-min(x for x,y in pts);h=max(y for x,y in pts)-min(y for x,y in pts)
  cases.append(dict(threshold=c['threshold'],width_pixel=w,height_pixel=h,area_pixel2=c['area_pixel2'],width_candidate_mm=w*scale,height_candidate_mm=h*scale,area_candidate_mm2=c['area_pixel2']*scale**2))
 ranges={k:dict(min=min(c[k] for c in cases),max=max(c[k] for c in cases),spread=max(c[k] for c in cases)-min(c[k] for c in cases)) for k in ['width_pixel','height_pixel','area_pixel2','width_candidate_mm','height_candidate_mm','area_candidate_mm2']}
 rows.append(dict(section=sec,candidate_scale_mm_per_pixel=scale,cases=cases,ranges=ranges))
inputs['front_shared_frame_candidate.json']=hashlib.sha256((O/'front_shared_frame_candidate.json').read_bytes()).hexdigest()
r=dict(status='ABC_SCHWELLWERTSENSITIVITAET_DIMENSIONEN_BERECHNET',inputs=inputs,sections=rows,limits=['Nur drei Schwellwerte96/128/160 und feste Extraktionsfenster.','Keine Konfidenzintervalle oder vollstaendige Messunsicherheit; Strichdicke, Pixelkalibrierung, Stationsidentitaet und Rahmenfehler nicht erfasst.','C nutzt gerade hypothetische Achsenbruecken. A/B enthalten ebenfalls ungemessene Achsenbruecken.','Kleine Schwellwertstreuung beweist weder Originaltreue noch korrekte Metrik. Historische A/B/C-Skalen unterscheiden sich.'],production_release=False)
(O/'ABC_threshold_dimension_sensitivity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(s['section'],{k:v['spread'] for k,v in s['ranges'].items() if k.endswith('mm') or k.endswith('mm2')}) for s in rows])
