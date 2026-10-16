"""Sensitivity of raster envelope comparison to station-column selection."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).parent;r=p.parents[1]
source=r/'references/UPC_Figure3_15_source_exact.png'
a=np.array(Image.open(source).convert('L'))
profiles=json.loads((p/'front_sections_pixel_candidates.json').read_text())['profiles']
results=[]
for label,x,bands in [('A',642,[(1230,1255),(1340,1360),(2753,2769),(2860,2872)]),('B',905,[(1223,1237),(1355,1370),(2668,2688),(2855,2868)])]:
    low,high=next(v for v in profiles if v['section']==label)['loop_summary'][0]['bounds_pixels']
    ratio=(high[1]-low[1])/(high[0]-low[0]);rows=[]
    for xx in range(x-5,x+6):
        edges=[]
        for n,(lo,hi) in enumerate(bands):
            ys=np.where(a[lo:hi,xx]<128)[0]+lo
            runs=np.split(ys,np.where(np.diff(ys)>1)[0]+1)
            if not len(ys):raise ValueError('missing contour')
            run=runs[0] if n in (0,2) else runs[-1]
            edges.append(float((run[0]+run[-1])/2))
        width=edges[1]-edges[0];height=edges[3]-edges[2]
        rows.append(dict(x_pixel=xx,selected_edge_centers=edges,plan_width_pixels=width,side_height_pixels=height,height_residual_pixels=width*ratio-height))
    residuals=[v['height_residual_pixels'] for v in rows]
    results.append(dict(section=label,edge_bands=bands,column_offset_pixels=5,samples=rows,residual_range_pixels=[min(residuals),max(residuals)]))
report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),method='Within each manually selected contour band split dark pixels into contiguous runs. Select first run for upper edge, last run for lower edge. Scan station column plus/minus five native pixels. Never average disconnected contour and internal-line runs.',results=results,interpretation='Sensitivity experiment only, not a statistical confidence interval or verified tracing uncertainty. Band selection remains manual; overlapping appendages and source depiction differences remain unresolved.',production_loft_allowed=False)
(p/'front_AB_station_sensitivity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print([(v['section'],v['residual_range_pixels']) for v in results])
