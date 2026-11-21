"""Lokale Normalenprofile als Messstudie; Tangente bleibt aus Rasterkandidaten geschaetzt."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,math
O=Path(__file__).parent;R=O.parents[1];src=R/'references/UPC_Figure3_15_source_exact.png';a=np.array(Image.open(src).convert('L'),dtype=float);p=O/'AB_open_stroke_midpoint_guides.json';j=json.loads(p.read_text(encoding='utf-8'));rows=[]
def value(x,y):
 ix,iy=int(math.floor(x)),int(math.floor(y));u,v=x-ix,y-iy
 return float(a[iy,ix]*(1-u)*(1-v)+a[iy,ix+1]*u*(1-v)+a[iy+1,ix]*(1-u)*v+a[iy+1,ix+1]*u*v)
for sec,seg,y in [('A',1,300),('A',3,285),('B',0,560),('B',2,590)]:
 case=next(s for s in j['sections'] if s['section']==sec)['cases'][1];s=case['segments_pixel'][seg];i=next(i for i,q in enumerate(s) if q[1]==y);q=s[i];lo=max(0,i-3);hi=min(len(s)-1,i+3);slope=(s[hi][0]-s[lo][0])/(s[hi][1]-s[lo][1]);norm=math.hypot(1,slope);n=[1/norm,-slope/norm];ts=[k/10 for k in range(-80,81)];vals=[value(q[0]+t*n[0],q[1]+t*n[1]) for t in ts];thresholds=[]
 for threshold in [96,128,160]:
  center=80
  if vals[center]>=threshold:thresholds.append(dict(threshold=threshold,status='Kandidatenzentrum_nicht_dunkel'));continue
  l=r=center
  while l>0 and vals[l-1]<threshold:l-=1
  while r<len(vals)-1 and vals[r+1]<threshold:r+=1
  bounded=l>0 and r<len(vals)-1;thresholds.append(dict(threshold=threshold,bounded=bounded,run_start_t=ts[l],run_end_t=ts[r],sampled_width_pixel=ts[r]-ts[l],normal_midpoint_shift_pixel=(ts[l]+ts[r])/2 if bounded else None))
 rows.append(dict(section=sec,segment=seg,y_pixel=y,candidate_pixel=q,estimated_dx_dy=slope,estimated_normal=n,sample_step_pixel=.1,sample_t=ts,grayscale_bilinear=vals,threshold_runs=thresholds))
r=dict(status='VIER_LOKALE_NORMALPROFILE_BERECHNET_NUR_STUDIE',inputs={src.name:hashlib.sha256(src.read_bytes()).hexdigest(),p.name:hashlib.sha256(p.read_bytes()).hexdigest()},rows=rows,limits=['Tangente aus+/-3Zeilenfenster geschaetzt; kein unabhaengig gemessener Normalenvektor.','Bilineare0.1PixelAbtastung erhoeht keine Originalrasteraufloesung oder Messgenauigkeit.','Strich-/Schraffurvereinigung kann Normalprofile ebenfalls verzerren; keine semantische Freigabe.','Keine Konturpunkte ersetzt, keine Geometrie oder Produktionsfreigabe.'],production_release=False)
(O/'AB_local_normal_profile_study.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(r['section'],r['y_pixel'],r['threshold_runs']) for r in rows])
