import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'analysis'/'original_front_sources';INP=SRC/'front_shared_frame_candidate.json';OUT=SRC/'ABC_shared_frame_consistency.json'
data=json.loads(INP.read_text(encoding='utf-8'));rows=[]
for q in data['profiles'][:3]:
 p=q['loops_xyz_candidate_mm'][0];ys=[float(v[1]) for v in p];zs=[float(v[2]) for v in p]
 rows.append(dict(section=q['section'],X_mm=float(q['station_X_candidate_mm']),Y_min_mm=min(ys),Y_max_mm=max(ys),width_mm=max(ys)-min(ys),Z_min_mm=min(zs),Z_max_mm=max(zs),height_mm=max(zs)-min(zs),axis_Z_mm=float(q['axis_Z_candidate_mm']),side_height_residual_pixels=float(q.get('side_height_residual_pixels',0.0)),scale_mm_per_pixel=float(q['isotropic_mm_per_section_pixel'])))
pairs=[]
for a,b in zip(rows,rows[1:]):
 dx=b['X_mm']-a['X_mm'];pairs.append(dict(from_section=a['section'],to_section=b['section'],dx_mm=dx,width_change_mm=b['width_mm']-a['width_mm'],height_change_mm=b['height_mm']-a['height_mm'],axis_Z_change_mm=b['axis_Z_mm']-a['axis_Z_mm'],width_slope_per_x=(b['width_mm']-a['width_mm'])/dx,height_slope_per_x=(b['height_mm']-a['height_mm'])/dx,axis_Z_slope_per_x=(b['axis_Z_mm']-a['axis_Z_mm'])/dx))
out=dict(status='ABC_GEMEINSAMER_RAHMEN_NUMERISCH_GEPRUEFT_KEINE_LOFTFREIGABE',input_sha256=hashlib.sha256(INP.read_bytes()).hexdigest(),sections=rows,pairwise=pairs,flags=dict(X_monotonic=all(rows[i]['X_mm']<rows[i+1]['X_mm'] for i in range(len(rows)-1)),width_monotonic=all(rows[i]['width_mm']<rows[i+1]['width_mm'] for i in range(len(rows)-1)),height_monotonic=all(rows[i]['height_mm']<rows[i+1]['height_mm'] for i in range(len(rows)-1)),C_side_height_residual_large=abs(rows[2]['side_height_residual_pixels'])>5.0),limits=['Historischer gemeinsamer Rahmen bleibt Kandidat, nicht verifiziert.','Sektion C enthaelt im gemeinsamen Rahmen einen grossen Seitenhoehen-Residualwert.','Keine Interpolation oder Loftfreigabe allein aus monotonen Spannweiten ableiten.','Master bleibt unveraendert.'],next_step='C-Registrierung gegen neu verifizierte C-Rasterreferenzen und neutralen Schliessungskandidaten pruefen, bevor A-B-C geloftet wird.',master_change_allowed=False,production_release=False)
OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps(out,indent=2,ensure_ascii=False))
