"""Vorhandene Originalproben auf abgeschnittene Dunkelläufe prüfen; nichts nachzeichnen."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent;src=R/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(src).convert('L'));rows=[]
inputs=['nose_to_A_stroke_center_samples.json','nose_intermediate_projection_check_samples.json']
for name in inputs:
 j=json.loads((O/name).read_text())
 for s in j['samples']:
  x=s['source_x_pixel'];bands=s.get('selected_view_bands',s.get('view_bands'));cols=sorted(set([int(np.floor(x)),int(np.ceil(x))]))
  for index,(lo,hi) in enumerate(bands):
   for col in cols:
    yy=np.where(a[lo:hi,col]<128)[0]+lo
    if not len(yy):status='KEIN_STRICH'
    elif yy.min()==lo or yy.max()==hi-1:status='BLOCKIERT_ROI_RAND_BERUEHRT'
    else:status='KEIN_ABSCHNITT_AM_ROI_RAND_ERKANNT'
    rows.append(dict(eingabe=name,x_spalte=col,ansicht='plan' if index==0 else 'side',roi_y=[lo,hi],status=status,oben_abgeschnitten=bool(len(yy) and yy.min()==lo),unten_abgeschnitten=bool(len(yy) and yy.max()==hi-1)))
report=dict(status='PROJEKTIONS_ROI_RANDSCHUTZ_AUSGEFUEHRT',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),eingaben=[dict(path=n,sha256=hashlib.sha256((O/n).read_bytes()).hexdigest()) for n in inputs],pruefungen=rows,blockierte=[v for v in rows if v['status']!='KEIN_ABSCHNITT_AM_ROI_RAND_ERKANNT'],grenze='Ein nicht berührter ROI-Rand bestätigt keine Konturidentität. Zusammenlaufende Radomfuge bei537 benötigt weiterhin visuelle Semantikprüfung.',originaldaten_geaendert=False,produktionsfreigabe=False)
assert any(v['x_spalte']==634 and v['ansicht']=='side' and v['unten_abgeschnitten'] for v in report['blockierte'])
(O/'projection_roi_clipping_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report['blockierte']))
