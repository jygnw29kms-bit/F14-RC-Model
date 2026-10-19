import FreeCAD as App,Part,json,hashlib,math
from pathlib import Path
B=Path(__file__).parent;R=B.parents[1];files=[B/'F14_A_RASTER_ENVELOPE_V2_REFERENCES.FCStd',B/'F14_ORIGINAL_ABCDEF_SECTION_CANDIDATES.FCStd'];hs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files};d=App.openDocument(str(files[0]));e=App.openDocument(str(files[1]));old=e.getObject('SOURCE_SECTION_A').Shape;target=json.loads((R/'analysis/original_front_sources/nose_to_A_stroke_center_samples.json').read_text())['samples'][-1];rows=[]
for threshold in [96,128,160]:
 sh=d.getObject('A_RASTER_'+str(threshold)).Shape;assert sh.isValid();b=sh.BoundBox;common=sh.common(old);assert common.isValid();a=old.cut(sh);c=sh.cut(old)
 for v in [a,c]:
  if not v.isNull():assert v.isValid()
 rows.append(dict(threshold=threshold,new_area_mm2=sh.Area,old_area_mm2=old.Area,intersection_area_mm2=common.Area,old_minus_new_area_mm2=0 if a.isNull() else a.Area,new_minus_old_area_mm2=0 if c.isNull() else c.Area,width_mm=b.YLength,height_mm=b.ZLength,width_minus_projection_mm=b.YLength-target['width_candidate_mm'],height_minus_projection_mm=b.ZLength-target['height_candidate_mm']))
App.closeDocument(d.Name);App.closeDocument(e.Name);assert hs=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
audit=dict(status='NEUE_A_RASTERREFERENZEN_GEGEN_ALTREFERENZ_UND_PROJEKTION_GEPRUEFT',inputs=hs,rows=rows,hinweise=['Neue Referenz ist äußere Rasterstrichkante, Projektion verwendet Strichmitten; keine Gleichheit verschiedener Messdefinitionen behaupten.','Historischer Maßstab dient nur zur Vergleichbarkeit.','Flächenüberlappung bestätigt keine Quellenregistrierung.','Alle ursprünglichen CAD- und Quelldateien unverändert.'],originalform_bestaetigt=False,produktion_freigegeben=False)
(B/'freecad_A_raster_v2_comparison.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(rows))
