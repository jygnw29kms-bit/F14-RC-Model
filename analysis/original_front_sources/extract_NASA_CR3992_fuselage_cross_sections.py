from pathlib import Path
import json, hashlib
import fitz

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / 'references' / 'NASA_CR3992_F14_VSTFE.pdf'
OUTDIR = ROOT / 'analysis' / 'original_front_sources' / 'NASA_CR3992_fuselage'
OUTDIR.mkdir(parents=True, exist_ok=True)

doc = fitz.open(PDF)
# Web text labels Figure 48 on PDF page index 87 and Figure 49 on the next page.
page_indexes = [86, 87, 88, 93, 94, 95]
records = []
for idx in page_indexes:
    page = doc[idx]
    text = page.get_text('text')
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
    path = OUTDIR / f'NASA_CR3992_page_{idx+1:03d}.png'
    pix.save(path)
    records.append({
        'pdf_page_index_0_based': idx,
        'pdf_page_number_1_based': idx + 1,
        'text': text,
        'render_path': str(path.relative_to(ROOT)).replace('\\','/'),
        'render_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'render_size_px': [pix.width, pix.height],
    })
report = {
    'status': 'NASA_CR3992_FUSELAGE_CROSS_SECTION_PAGES_RENDERED_FOR_SOURCE_REVIEW',
    'source_pdf': str(PDF.relative_to(ROOT)).replace('\\','/'),
    'source_sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
    'page_count': doc.page_count,
    'records': records,
    'limits': [
        'Rendered pages are source-review artifacts only.',
        'No cross-section station or waterline is accepted until labels are visually verified.',
        'NASA text states the source geometry was a 1/10-scale wind-tunnel definition with minor deviations from the production airplane.',
        'No master geometry is changed.'
    ],
    'production_release': False,
}
(OUTDIR / 'NASA_CR3992_fuselage_cross_section_page_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'page_count':doc.page_count,'renders':[(r['pdf_page_number_1_based'],r['render_size_px']) for r in records]}, indent=2))
