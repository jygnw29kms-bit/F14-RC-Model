import json, statistics, hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = root / 'migration/freecad/freecad_C_axis_closure_hypotheses_audit.json'
out = Path(__file__).with_name('C_axis_closure_neutral_candidate.json')

data = json.loads(src.read_text(encoding='utf-8'))
rows = data['rows']
areas = [r['native_area_mm2'] for r in rows]
center = next(r for r in rows if r['threshold'] == 128 and r['offset_pixel'] == 0)

result = {
  'status': 'NEUTRALER_C_SCHLIESSUNGSKANDIDAT_NUR_STUDIE',
  'source': str(src.relative_to(root)).replace('\\','/'),
  'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
  'variants_checked': len(rows),
  'all_simple_polygon': all(r['simple_polygon'] for r in rows),
  'all_native_valid': all(r['native_valid'] for r in rows),
  'all_apertures_inside': all(a['outside_area_mm2'] == 0.0 for r in rows for a in r['apertures']),
  'area_min_mm2': min(areas),
  'area_max_mm2': max(areas),
  'area_span_mm2': max(areas) - min(areas),
  'area_span_percent_of_mean': 100.0 * (max(areas)-min(areas)) / statistics.mean(areas),
  'neutral_candidate': center,
  'selection_reason': [
    'threshold 128 ist der mittlere der drei untersuchten Schwellwerte 96/128/160.',
    'offset 0 ist der mittlere der drei untersuchten Achsenversätze -1/0/+1 Pixel.',
    'Der Kandidat ist nativ gueltig, schnittfrei und beide Oeffnungen liegen vollstaendig innerhalb.',
    'Die Auswahl ist neutral fuer weitere Studien und keine Quellenbestaetigung.'
  ],
  'limits': [
    'Die vier Achsenbruecken bleiben konstruktive Annahmen.',
    'Planarer Abstand zu Oeffnungen ist kein 3D-Wandabstand.',
    'Keine Originalhaut, keine Master-Aenderung und keine Produktionsfreigabe.'
  ],
  'master_change_allowed': False,
  'production_release': False
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
