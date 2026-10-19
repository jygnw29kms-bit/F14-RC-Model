"""Explizite Formhypothese: normierte A-Kontur vorwaerts skalieren. KEINE Originalaussenform."""
import FreeCAD as App,Part,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent
paths=[R/'analysis/original_front_sources/front_sections_pixel_candidates.json',R/'analysis/original_front_sources/nose_to_A_stroke_center_samples.json',R/'analysis/propulsion_source_silhouette_constraints_v134.json'];hs={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};a,n,f=[json.loads(p.read_text()) for p in paths];a=next(t for t in a['profiles'] if t['section']=='A')['loops_pixel'][0]
lo=[min(p[i] for p in a) for i in [0,1]];hi=[max(p[i] for p in a) for i in [0,1]]
normalized=[((p[0]-lo[0])/(hi[0]-lo[0]),1-(p[1]-lo[1])/(hi[1]-lo[1])) for p in a]
d=App.newDocument('F14_NOSE_A_SHAPE_SENSITIVITY');wires=[];rows=[];scale=f['common_scale_mm_per_pixel']
for k,t in enumerate(n['samples']):
 ylo=(t['plan_stroke_center_y_pixels'][0]-1296.25)*scale;yhi=(t['plan_stroke_center_y_pixels'][1]-1296.25)*scale;zlo=t['side_bottom_Z_candidate_mm'];zhi=t['side_top_Z_candidate_mm'];x=t['X_candidate_mm'];pts=[App.Vector(x,ylo+u*(yhi-ylo),zlo+v*(zhi-zlo)) for u,v in normalized]
 if pts[0].distanceToPoint(pts[-1])>1e-9:pts.append(pts[0])
 w=Part.makePolygon(pts);face=Part.Face(w);assert face.isValid();wires.append(w);o=d.addObject('PartDesign::Feature','HYPOTHESE_'+str(k));o.Shape=w;rows.append(dict(x_candidate_mm=x,width_mm=yhi-ylo,height_mm=zhi-zlo,area_hypothesis_mm2=face.Area,valid=face.isValid()))
loft=Part.makeLoft(wires,True,True);assert loft.isValid() and len(loft.Solids)==1
o=d.addObject('PartDesign::Feature','FORMHYPOTHESE');o.Label='NICHT ORIGINAL / A-Form vorwaerts skaliert / Sensitivitaet';o.Shape=loft;d.recompute();out=B/'F14_NOSE_A_SHAPE_SENSITIVITY.FCStd';d.saveAs(str(out));App.closeDocument(d.Name)
assert hs=={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
audit=dict(status='NATIVE_FORMHYPOTHESE_ERZEUGT_NICHT_ORIGINALE_NASENGEOMETRIE',inputs=hs,annahme='Anisotrop normierte originale A-Polygonform an jeder Station auf die Projektionsbreite/-hoehe skalieren. Form vorA ist damit angenommen, nicht aus Originalquerschnitten rekonstruiert.',sections=rows,native_valid=loft.isValid(),solids=len(loft.Solids),hypothesis_volume_mm3=loft.Volume,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),einschraenkungen=['Keine neue Quellenkontur; keine exakte Originalaussenform.','Ruled-Loft zwischen9Proben; Zwischenprojektionen ungeprueft.','Gemeinsame X-Abbildung und metrischer Rahmen ungeprueft.','Bereich beginnt hinter Nasenapex; keine vollstaendige Nase.','A-Endprofil auf Projektionsmasse skaliert, NICHT unveraenderte originale SektionA.','Bestehende Radom- und Originalquerschnittssperren bleiben aktiv.'],originalquerschnitte_geaendert=False,master_geaendert=False,produktion_freigegeben=False)
(B/'freecad_nose_A_shape_sensitivity_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps({'valid':audit['native_valid'],'solids':audit['solids'],'hypothesis_volume_mm3':loft.Volume}))
