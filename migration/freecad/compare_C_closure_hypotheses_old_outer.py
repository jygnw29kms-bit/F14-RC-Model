import FreeCAD as App,Part,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent;O=R/'analysis/original_front_sources';paths=[B/'F14_C_AXIS_CLOSURE_HYPOTHESES.FCStd',O/'front_sections_pixel_candidates.json',O/'front_shared_frame_candidate.json'];hs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};raw=json.loads(paths[1].read_text(encoding='utf-8'))['profiles'][2];f=json.loads(paths[2].read_text(encoding='utf-8'))['profiles'][2];ax=raw['source_section_axis_pixel'];s=f['isotropic_mm_per_section_pixel'];pts=[App.Vector(f['station_X_candidate_mm'],(x-ax[0])*s,f['axis_Z_candidate_mm']+(ax[1]-y)*s) for x,y in raw['loops_pixel'][0]];old=Part.Face(Part.makePolygon(pts+[pts[0]]));assert old.isValid();doc=App.openDocument(str(paths[0]));rows=[]
def area(sh):
 if sh.isNull():return 0.0
 assert sh.isValid();return sh.Area
for obj in doc.Objects:
 if not hasattr(obj,'Shape') or obj.Shape.isNull():continue
 sh=obj.Shape;assert sh.isValid();overlap=area(sh.common(old));minus_old=area(sh.cut(old));minus_new=area(old.cut(sh));assert abs(sh.Area-overlap-minus_old)<1e-5 and abs(old.Area-overlap-minus_new)<1e-5
 rows.append(dict(object=obj.Name,old_outer_area_mm2=old.Area,hypothesis_outer_area_mm2=sh.Area,intersection_area_mm2=overlap,hypothesis_minus_old_area_mm2=minus_old,old_minus_hypothesis_area_mm2=minus_new,width_delta_mm=sh.BoundBox.YLength-old.BoundBox.YLength,height_delta_mm=sh.BoundBox.ZLength-old.BoundBox.ZLength))
App.closeDocument(doc.Name);assert len(rows)==9 and hs=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(B/'freecad_C_closure_old_outer_comparison.json').write_text(json.dumps(dict(status='C_HYPOTHESEN_GEGEN_ALTE_AUSSENKONTUR_NATIV_VERGLICHEN',inputs=hs,rows=rows,limits=['AlteKontur grobeNachzeichnung, neueStrichaussenkante plusvierangenommeneBruecken.','Flaechenvergleich prueft keine Originalhaut, Strichmitte oder Registrierung.','Keine Geometrie oder Masterdatei geaendert.'],production_release=False),ensure_ascii=False,indent=2),encoding='utf-8');print(rows)
