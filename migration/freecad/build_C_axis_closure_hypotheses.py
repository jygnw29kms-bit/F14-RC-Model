import FreeCAD as App,Part,json,hashlib,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent;O=R/'analysis/original_front_sources';paths=[O/n for n in ['C_axis_closure_sensitivity.json','C_aperture_white_envelopes_v2.json','front_shared_frame_candidate.json','front_sections_pixel_candidates.json']];hs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};j,w,f,c=[json.loads(p.read_text(encoding='utf-8')) for p in paths];f=f['profiles'][2];ax=c['profiles'][2]['source_section_axis_pixel'];scale=f['isotropic_mm_per_section_pixel'];spec=importlib.util.spec_from_file_location('topo',str(O/'audit_pixel_topology.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def face(pts):
 xyz=[App.Vector(f['station_X_candidate_mm'],(x-ax[0])*scale,f['axis_Z_candidate_mm']+(ax[1]-y)*scale) for x,y in pts];return Part.Face(Part.makePolygon(xyz+[xyz[0]]))
d=App.newDocument('F14_C_AXIS_CLOSURE_HYPOTHESES');rows=[]
for case in j['cases']:
 pts=case['points_pixel'];N=len(pts);bounds=[(min(a[0],b[0]),max(a[0],b[0]),min(a[1],b[1]),max(a[1],b[1])) for a,b in zip(pts,pts[1:]+pts[:1])];tested=0
 for i in range(N):
  assert pts[i]!=pts[(i+1)%N]
  for k in range(i+1,N):
   if k==i+1 or (i==0 and k==N-1):continue
   a,b=bounds[i],bounds[k]
   if a[1]<b[0] or b[1]<a[0] or a[3]<b[2] or b[3]<a[2]:continue
   tested+=1;assert not m.intersects(pts[i],pts[(i+1)%N],pts[k],pts[(k+1)%N])
 sh=face(pts);assert sh.isValid() and len(sh.Wires)==1;expected=case['area_pixel2']*scale**2;assert abs(sh.Area-expected)<1e-6;ap=[]
 for v in next(x for x in w['cases'] if x['threshold']==case['threshold'])['apertures']:
  hole=face(v['loop_pixel']);outside=hole.cut(sh);outsidearea=0 if outside.isNull() else outside.Area;assert outsidearea<1e-7
  ap.append(dict(label=v['label'],outside_area_mm2=outsidearea,minimum_planar_boundary_gap_mm=hole.Wires[0].distToShape(sh.Wires[0])[0]))
 obj=d.addObject('PartDesign::Feature','C_HYP_'+str(case['threshold'])+'_'+str(case['offset_pixel']).replace('-','minus'));obj.Shape=sh
 rows.append(dict(threshold=case['threshold'],offset_pixel=case['offset_pixel'],vertices=N,simple_polygon=True,native_valid=True,native_area_mm2=sh.Area,analytic_area_mm2=expected,apertures=ap))
out=B/'F14_C_AXIS_CLOSURE_HYPOTHESES.FCStd';d.recompute();d.saveAs(str(out));App.closeDocument(d.Name);assert hs=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(B/'freecad_C_axis_closure_hypotheses_audit.json').write_text(json.dumps(dict(status='NEUN_HYPOTHESEN_NATIV_GEPRUEFT',inputs=hs,rows=rows,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),limits=['VierAchsenbruecken jeVariante sind Annahmen.','Abstand zu Weissoeffnungen ist kein Originalwand- oder3DNormalabstand.','Historischer Rahmen ungeprueft; keine Originalhaut oder Produktionsfreigabe.'],production_release=False),ensure_ascii=False,indent=2),encoding='utf-8');print('9nativeHypothesenflaechen geprueft; keine Produktionsfreigabe.')
