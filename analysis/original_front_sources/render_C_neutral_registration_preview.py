import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'analysis'/'original_front_sources'
frame=json.loads((SRC/'front_shared_frame_candidate.json').read_text(encoding='utf-8'));sens=json.loads((SRC/'C_axis_closure_sensitivity.json').read_text(encoding='utf-8'));pix=json.loads((SRC/'front_sections_pixel_candidates.json').read_text(encoding='utf-8'));reg=json.loads((SRC/'C_side_projection_registration_screen.json').read_text(encoding='utf-8'))
f=frame['profiles'][2];p=pix['profiles'][2];case=next(c for c in sens['cases'] if c['threshold']==128 and c['offset_pixel']==0);scale=float(f['isotropic_mm_per_section_pixel']);axis=p['source_section_axis_pixel']
y=[(x-axis[0])*scale for x,q in case['points_pixel']];z=[float(f['axis_Z_candidate_mm'])+(axis[1]-q)*scale for x,q in case['points_pixel']]
# Nur die sichtbare SVG-Vorschau wird ausgedünnt; Analyse und native CAD-Geometrie behalten alle Punkte.
step=12;idx=list(range(0,len(y),step));idx += [] if idx[-1]==len(y)-1 else [len(y)-1];yd=[y[i] for i in idx];zd=[z[i] for i in idx];yd.append(yd[0]);zd.append(zd[0])
target=reg['interpolated_side_envelope_at_C'];dz=float(target['center_Z_mm'])-(min(z)+max(z))/2;ztd=[v+dz for v in zd];W,H=1200,700;ml,mr,mt,mb=90,40,70,80;ymin,ymax=min(y)-10,max(y)+10;zmin=min(min(z),float(target['bottom_Z_mm']))-10;zmax=max(max(z)+dz,float(target['top_Z_mm']))+10
sx=lambda v:ml+(v-ymin)/(ymax-ymin)*(W-ml-mr);sy=lambda v:mt+(zmax-v)/(zmax-zmin)*(H-mt-mb);pts=lambda ys,zs:' '.join(f'{sx(a):.1f},{sy(b):.1f}' for a,b in zip(ys,zs))
def hline(v,stroke,dash=''):
 d=f' stroke-dasharray="{dash}"' if dash else '';return f'<line x1="{sx(ymin):.1f}" y1="{sy(v):.1f}" x2="{sx(ymax):.1f}" y2="{sy(v):.1f}" stroke="{stroke}" stroke-width="2"{d}/>'
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="{W/2}" y="32" text-anchor="middle" font-family="Arial" font-size="22">F-14 Sektion C – Registrierungsstudie – Entwicklungsstand 20.10.2026</text>']
for gv in range(-100,101,25):
 if ymin<=gv<=ymax:svg.append(f'<line x1="{sx(gv):.1f}" y1="{sy(zmin):.1f}" x2="{sx(gv):.1f}" y2="{sy(zmax):.1f}" stroke="#dddddd" stroke-width="1"/>')
for gv in range(-50,76,10):
 if zmin<=gv<=zmax:svg.append(f'<line x1="{sx(ymin):.1f}" y1="{sy(gv):.1f}" x2="{sx(ymax):.1f}" y2="{sy(gv):.1f}" stroke="#dddddd" stroke-width="1"/>')
svg += [f'<polyline points="{pts(yd,zd)}" fill="none" stroke="#1f77b4" stroke-width="2"/>',f'<polyline points="{pts(yd,ztd)}" fill="none" stroke="#ff7f0e" stroke-width="2"/>',hline(float(target['top_Z_mm']),'#2ca02c','8,6'),hline(float(target['bottom_Z_mm']),'#d62728','8,6'),hline(float(target['center_Z_mm']),'#9467bd','3,5'),f'<line x1="{ml}" y1="{H-mb}" x2="{W-mr}" y2="{H-mb}" stroke="black"/>',f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{H-mb}" stroke="black"/>',f'<text x="{W/2}" y="{H-25}" text-anchor="middle" font-family="Arial" font-size="16">Y [mm]</text>',f'<text x="25" y="{H/2}" transform="rotate(-90 25 {H/2})" text-anchor="middle" font-family="Arial" font-size="16">Z [mm]</text>']
for i,(c,txt) in enumerate([('#1f77b4','C neutral 128/0 im historischen Rahmen'),('#ff7f0e','C neutral nur Z-verschoben'),('#2ca02c','interpolierte Seitenhülle oben'),('#d62728','interpolierte Seitenhülle unten'),('#9467bd','interpolierte Seitenhüllenmitte')]):
 yy=90+i*24;svg.append(f'<line x1="800" y1="{yy}" x2="840" y2="{yy}" stroke="{c}" stroke-width="3"/><text x="850" y="{yy+5}" font-family="Arial" font-size="13">{txt}</text>')
svg.append(f'<text x="90" y="655" font-family="Arial" font-size="12">Vorschau aus {len(yd)-1} von {len(y)} Rasterpunkten; native CAD-Geometrie unverändert vollständig.</text>');svg.append('</svg>');out=ROOT/'docs'/'images'/'f14_C_registration_study_20261020.svg';out.parent.mkdir(parents=True,exist_ok=True);out.write_text('\n'.join(svg),encoding='utf-8');print(out)
