import FreeCAD as App,Part,json,hashlib,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent;O=R/'analysis/original_front_sources';src=O/'C_aperture_white_envelopes_v2.json';frame=O/'front_shared_frame_candidate.json';old=O/'front_sections_pixel_candidates.json';paths=[src,frame,old];hs={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};j=json.loads(src.read_text(encoding='utf-8'));f=json.loads(frame.read_text())['profiles'][2];c=json.loads(old.read_text())['profiles'][2];ax=c['source_section_axis_pixel'];scale=f['isotropic_mm_per_section_pixel'];spec=importlib.util.spec_from_file_location('topo',str(O/'audit_pixel_topology.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def face(pts):
 xyz=[App.Vector(f['station_X_candidate_mm'],(x-ax[0])*scale,f['axis_Z_candidate_mm']+(ax[1]-y)*scale) for x,y in pts];return Part.Face(Part.makePolygon(xyz+[xyz[0]]))
outer=face(c['loops_pixel'][0]);assert outer.isValid();d=App.newDocument('F14_C_WHITE_APERTURE_V2_REFERENCES');rows=[]
for case in j['cases']:
 faces=[]
 for v in case['apertures']:
  pts=v['loop_pixel'];N=len(pts)
  for i in range(N):
   assert pts[i]!=pts[(i+1)%N]
   for k in range(i+1,N):
    if k==i+1 or (i==0 and k==N-1):continue
    assert not m.intersects(pts[i],pts[(i+1)%N],pts[k],pts[(k+1)%N])
  sh=face(pts);assert sh.isValid() and len(sh.Wires)==1;expected=v['area_pixel2']*scale**2;assert abs(sh.Area-expected)<1e-6;outside=sh.cut(outer)
  if not outside.isNull():assert outside.isValid()
  obj=d.addObject('PartDesign::Feature','C_WHITE_'+str(case['threshold'])+'_'+v['label']);obj.Shape=sh;faces.append(sh);gap=sh.Wires[0].distToShape(outer.Wires[0])[0]
  rows.append(dict(threshold=case['threshold'],label=v['label'],vertices=N,simple_polygon=True,native_valid=True,native_area_mm2=sh.Area,analytic_area_mm2=expected,outside_old_outer_area_mm2=0 if outside.isNull() else outside.Area,minimum_planar_boundary_gap_to_old_outer_mm=gap))
 overlap=faces[0].common(faces[1]);assert overlap.isNull() or overlap.Area<1e-8
 assert faces[0].distToShape(faces[1])[0]>0
out=B/'F14_C_WHITE_APERTURE_V2_REFERENCES.FCStd';d.recompute();d.saveAs(str(out));App.closeDocument(d.Name);assert hs=={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
a=dict(status='C_WEISSRAUM_REFERENZEN_TOPOLOGISCH_UND_NATIV_GEPRUEFT',inputs=hs,rows=rows,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),hinweise=['Außenkontur weiterhin alte grobe Nachzeichnung; Abstand dazu kein Originalwandnachweis.','Weißraumrand, nicht Strichmitte.','Achsenlücke607..611 bleibt ungemessen.','Metrischer Rahmen ungeprüft; keine Duct- oder Masteränderung.'],produktion_freigegeben=False)
(B/'freecad_C_white_aperture_v2_audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(rows))
