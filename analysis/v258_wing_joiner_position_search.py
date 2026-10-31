import FreeCAD as App, Part, json, pathlib, bisect
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v256_CONSOLIDATED_JOINER_STATE.FCStd'))
wd=json.load(open(R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
scale=1.1697428086486623; shift=187.59240693460868; fs0=93.0; sec=next(s for s in wd['sections'] if abs(s['wbl_in']-274.36816)<1e-5); chord=sec['trailing_edge_fs_in']-sec['leading_edge_fs_in']; rows=sec['ordinates_xc_upper_lower']
def interp(x,idx):
 for a,b in zip(rows[:-1],rows[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]) if b[0]!=a[0] else 0; return a[idx]+t*(b[idx]-a[idx])
 raise ValueError(x)
seam_y=sec['wbl_in']*scale; outrows=[]
for xc in [0.30,0.34,0.38,0.40,0.42]:
 yc=(interp(xc,1)+interp(xc,2))/2; x=(sec['leading_edge_fs_in']+xc*chord-fs0)*scale; z=(sec['reference_vertical_wl_in']+yc*chord)*scale-shift
 for L in [40,50,60]:
  rec={'xc':xc,'length_mm':L,'x_mm':x,'z_mm':z,'sides':[]}
  for lab,sgn in [('R',1),('L',-1)]:
   wing=d.getObject('WING_'+lab).Shape; start=App.Vector(x,sgn*(seam_y-L/2),z); axis=App.Vector(0,sgn,0)
   od=Part.makeCylinder(3.0,L,start,axis); cav=Part.makeCylinder(3.15,L,start,axis); rec['sides'].append({'side':lab,'tube_containment':od.common(wing).Volume/od.Volume,'cavity_containment':cav.common(wing).Volume/cav.Volume})
  rec['min_tube']=min(s['tube_containment'] for s in rec['sides']); rec['min_cavity']=min(s['cavity_containment'] for s in rec['sides']); outrows.append(rec)
valid=[r for r in outrows if r['min_tube']>=0.999 and r['min_cavity']>=0.999]
best=sorted(valid,key=lambda r:(-r['length_mm'],abs(r['xc']-0.38)))[0] if valid else None
out={'status':'V258_WING_JOINER_POSITION_SEARCH','source_station_WBL_in':274.36816,'tested':outrows,'best':best,'gates':{'valid_candidate_found':best is not None,'best_length_ge_50mm':bool(best and best['length_mm']>=50),'best_cavity_containment_ge_0p999':bool(best and best['min_cavity']>=0.999)}}
(R/'analysis/v258_wing_joiner_position_search.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps({'status':out['status'],'best':best,'valid_count':len(valid),'gates':out['gates']},indent=2))