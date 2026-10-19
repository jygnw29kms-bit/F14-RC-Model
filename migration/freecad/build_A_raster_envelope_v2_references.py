import FreeCAD as App,Part,json,hashlib,importlib.util,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=Path(__file__).parent;O=R/'analysis/original_front_sources';src=O/'A_raster_envelope_v2_candidates.json';frame=O/'front_shared_frame_candidate.json';axis=O/'front_sections_pixel_candidates.json';paths=[src,frame,axis];hs={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
j=json.loads(src.read_text(encoding='utf-8'));f=json.loads(frame.read_text())['profiles'][0];ax=json.loads(axis.read_text())['profiles'][0]['source_section_axis_pixel'];scale=f['isotropic_mm_per_section_pixel'];spec=importlib.util.spec_from_file_location('topo',str(O/'audit_pixel_topology.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);d=App.newDocument('F14_A_RASTER_ENVELOPE_V2_REFERENCES');rows=[]
for c in j['cases']:
 pts=c['loop_pixel'];N=len(pts);hits=[]
 for i in range(N):
  assert pts[i]!=pts[(i+1)%N]
  for k in range(i+1,N):
   if k==i+1 or (i==0 and k==N-1):continue
   if m.intersects(pts[i],pts[(i+1)%N],pts[k],pts[(k+1)%N]):hits.append([i,k])
 assert not hits
 xyz=[App.Vector(f['station_X_candidate_mm'],(x-ax[0])*scale,f['axis_Z_candidate_mm']+(ax[1]-y)*scale) for x,y in pts];w=Part.makePolygon(xyz+[xyz[0]]);face=Part.Face(w);assert face.isValid() and len(face.Faces)==1;expected=c['area_pixel2']*scale**2;assert abs(face.Area-expected)<1e-6
 o=d.addObject('PartDesign::Feature','A_RASTER_'+str(c['threshold']));o.Label='A Raster-Aussenkante Schwelle'+str(c['threshold'])+' / Rahmen ungeprueft';o.Shape=face
 rows.append(dict(threshold=c['threshold'],polygon_simple=True,vertices=N,native_face_valid=True,native_area_mm2=face.Area,analytic_area_mm2=expected,face_count=len(face.Faces),boundary_count=len(face.Wires)))
d.recompute();out=B/'F14_A_RASTER_ENVELOPE_V2_REFERENCES.FCStd';d.saveAs(str(out));App.closeDocument(d.Name);assert hs=={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
a=dict(status='NEUE_A_RASTERREFERENZEN_NATIV_UND_TOPOLOGISCH_GEPRUEFT',inputs=hs,rows=rows,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),hinweise=['Historischer Kandidatenrahmen nur zur Vergleichbarkeit übernommen; metrisch nicht freigegeben.','Raster-Außenstrichkante, nicht Strichmitte.','Achsenlücke275..277 bleibt ungemessen und linear überbrückt.','Keine bestehende A-Kontur, Hypothese oder Masterdatei ersetzt.'],produktion_freigegeben=False)
(B/'freecad_A_raster_envelope_v2_audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print(json.dumps(rows))
