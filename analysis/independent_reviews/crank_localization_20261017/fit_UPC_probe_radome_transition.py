"""Fit a pixel-width changepoint for source registration screening, not aircraft geometry."""
from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];src=R/'references/UPC_Figure3_15_source_exact.png';im=np.array(Image.open(src).convert('L'));rows=[]
for lab,(lo,hi) in {'plan':(1270,1320),'side':(2790,2870)}.items():
 runs=[]
 for threshold in (96,128,160):
  for start,end in ((435,470),(432,468),(437,472)):
   x=np.arange(start,end+1);width=np.array([np.ptp(np.where(im[lo:hi,int(q)]<threshold)[0]) for q in x]);candidates=[]
   for k in np.arange(438,453,.25):
    A=np.column_stack((np.ones(len(x)),np.maximum(0,x-k)));c=np.linalg.lstsq(A,width,rcond=None)[0];mse=float(np.mean((A@c-width)**2));candidates.append((mse,float(k),float(c[0]),float(c[1])))
   mse,k,base,slope=min(candidates);runs.append(dict(threshold=threshold,x_window=[start,end],hinge_px=k,width_baseline_px=base,width_slope=slope,mse_px2=mse))
  
 rows.append(dict(view=lab,roi_y=[lo,hi],runs=runs,hinge_sensitivity_interval_px=[min(t['hinge_px'] for t in runs),max(t['hinge_px'] for t in runs)]))
assert len(rows)==2 and all(len(r['runs'])==9 for r in rows)
j=dict(status='ORIGINAL_PIXEL_PROBE_RADOME_TRANSITION_SCREEN_NOT_EXACT_FS93_REGISTRATION',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),method='Least-squares width=a+b*max(0,x-k),kgrid0.25px,9threshold/window combinations per view. Grid precision is computational, not source accuracy.',views=rows,qualitative_landmark_basis='Labeled Navy14315Fig2-3 FS93 at end of narrow probe / widening radome.',finding='Plan and side yield different changepoints. Preserve separate view origins; previous common raster-X assumption is not verified at nose.',limits=['Simplified width hinge estimates a drawing transition; it does not prove an exact physical surface point.','Line thickness and probe angle affect fitted hinge.','Sensitivity range is not a statistical confidence interval.','No new source contour or CAD profile is generated.'],next='Compare independent shared panel/radome joint landmarks in plan and side; estimate view-specific affine mapping rather than force shared pixel origin.',metric_registration_verified=False,geometry_changed=False,production_release=False)
Path(__file__).with_name('UPC_probe_radome_transition_screen.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps([{'view':r['view'],'range':r['hinge_sensitivity_interval_px']} for r in rows]))
