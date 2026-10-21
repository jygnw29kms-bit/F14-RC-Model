from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
J=ROOT/'analysis'/'original_front_sources'/'Navy_UPC_side_longitudinal_landmark_fit.json'
OUT=ROOT/'docs'/'images'/'f14_side_x_registration_summary_20261021.svg'
j=json.loads(J.read_text(encoding='utf-8')); lm=j['landmarks']; fit=j['nominal_fit']
W,H=1200,520; ml,mr=90,70
fsmin,fsmax=60,850
sx=lambda fs: ml+(fs-fsmin)/(fsmax-fsmin)*(W-ml-mr)
colors=['#c62828','#1565c0','#2e7d32']
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="{W/2}" y="34" text-anchor="middle" font-family="Arial" font-size="22">F-14 Seiten-X-Registrierung – Referenzstudie 21.10.2026</text>',f'<text x="{W/2}" y="58" text-anchor="middle" font-family="Arial" font-size="13">US Navy Figure 4-7 ↔ UPC Figure 3.15 | drei homologe Seitenlandmarken | keine OML-/Produktionsfreigabe</text>']
# Aircraft-FS line
for y,label in [(150,'Aircraft FS / Navy'),(290,'UPC-Seitenansicht auf Aircraft-FS registriert')]:
 svg.append(f'<line x1="{ml}" y1="{y}" x2="{W-mr}" y2="{y}" stroke="#222" stroke-width="2"/>')
 svg.append(f'<text x="{ml}" y="{y-16}" font-family="Arial" font-size="14">{label}</text>')
 for fs in range(100,851,100):
  x=sx(fs); svg.append(f'<line x1="{x:.1f}" y1="{y-6}" x2="{x:.1f}" y2="{y+6}" stroke="#555"/>'); svg.append(f'<text x="{x:.1f}" y="{y+24}" text-anchor="middle" font-family="Arial" font-size="11">FS {fs}</text>')
# landmarks
names=['FS93 / Radomaufweitung','mittlerer Canopy-Bow','hinterster Nozzle-Endpunkt']
for i,(rec,name) in enumerate(zip(lm,names)):
 fs=sum(rec['FS_in_interval'])/2; x=sx(fs); co=colors[i]
 for y in (150,290): svg.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="{co}" stroke="black"/>')
 svg.append(f'<line x1="{x:.1f}" y1="157" x2="{x:.1f}" y2="283" stroke="{co}" stroke-width="1.5" stroke-dasharray="5,5"/>')
 svg.append(f'<text x="{x:.1f}" y="{100+i*22}" text-anchor="middle" font-family="Arial" font-size="12" fill="{co}">{name} | FS≈{fs:.2f}</text>')
# fit box
boxy=365
svg.append(f'<rect x="140" y="{boxy}" width="920" height="105" rx="10" fill="#f5f5f5" stroke="#777"/>')
lines=[f"UPC-x = {fit['slope_px_per_FS_in']:.9f} · FS + {fit['FS0_x_px']:.4f}",f"longitudinaler UPC-Maßstab = {fit['scale_FS_in_per_px']:.9f} in/px",f"Fit-RMS = {fit['rms_px']:.3f} px | max. Residuum = {fit['max_abs_px']:.3f} px | Paar-Holdout max. = 1.421 px",'Ergebnis: Engineering-X-/FS-Kandidat unterstützt; Z/Waterline, Master, Druck und Flug bleiben gesperrt.']
for i,t in enumerate(lines): svg.append(f'<text x="170" y="{boxy+28+i*21}" font-family="Arial" font-size="14">{t}</text>')
svg.append('</svg>'); OUT.write_text('\n'.join(svg),encoding='utf-8');print(OUT)
