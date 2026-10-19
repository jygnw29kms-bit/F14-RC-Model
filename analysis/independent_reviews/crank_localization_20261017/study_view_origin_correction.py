"""Nasendatum-Sensitivität; keine neue Außenkontur und keine Kreisfreigabe."""
import json,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
p=R/'analysis/original_front_sources/nose_to_A_stroke_center_samples.json';q=O/'UPC_probe_radome_transition_screen.json';j=json.loads(p.read_text());h=json.loads(q.read_text());rows=j['samples'];x=np.array([r['source_x_pixel'] for r in rows]);width=np.array([r['width_candidate_mm'] for r in rows]);height=np.array([r['height_candidate_mm'] for r in rows]);plan,side=[v['hinge_sensitivity_interval_px'] for v in h['views']];shifts=[side[0]-plan[1],sum(side)/2-sum(plan)/2,side[1]-plan[0]]
out=[]
for shift in shifts:
 r=[]
 for i,px in enumerate(x):
  sx=px+shift
  if sx<x.min() or sx>x.max():continue
  hh=float(np.interp(sx,x,height));r.append(dict(plan_x_px=float(px),side_x_px_candidate=float(sx),width_mm=float(width[i]),height_interpolated_mm=hh,width_minus_height_before_mm=float(width[i]-height[i]),width_minus_height_after_mm=float(width[i]-hh)))
 out.append(dict(side_x_minus_plan_x_px=shift,samples=r,rms_before_mm=float(np.sqrt(np.mean([v['width_minus_height_before_mm']**2 for v in r]))),rms_after_mm=float(np.sqrt(np.mean([v['width_minus_height_after_mm']**2 for v in r])))))
a=dict(status='GETRENNTE_NASENURSPRUENGE_NUMERISCH_UNTERSUCHT_KEINE_FORMFREIGABE',eingaben=[dict(path=str(t.relative_to(R)),sha256=hashlib.sha256(t.read_bytes()).hexdigest()) for t in [p,q]],faelle=out,hinweise=['Breite und Höhe stammen aus zwei Originalansichten; Gleichheit wäre nur für einen Kreisquerschnitt erforderlich.','Seitenhöhe linear zwischen vorhandenen Proben interpoliert; keine Quellkontur dazwischen bestätigt.','Keine Extrapolation; erste Probe außerhalb des gemeinsamen Bereichs ausgelassen.','Geringerer Fehler ist keine Bestätigung eines Kreises oder eines gemeinsamen metrischen Rahmens.','Keine Querschnitte oder CAD-Geometrie geändert.'],naechster_schritt='Ergebnis gegen Kreisannahme und originale SektionA prüfen; Ansichten nicht zum Kreis passend verformen.',produktion_freigegeben=False)
(O/'view_origin_correction_sensitivity.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print([(v['side_x_minus_plan_x_px'],v['rms_before_mm'],v['rms_after_mm']) for v in out])
