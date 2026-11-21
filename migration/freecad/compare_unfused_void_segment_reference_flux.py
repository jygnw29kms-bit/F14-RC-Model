from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepGProp import BRepGProp_Face,BRepGProp_Domain,BRepGProp_Vinert
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';q=R/'analysis/v192_adaptive_void_segments_build.json';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);build=json.loads(q.read_text());assert build['output_sha256']==h;out=R/'analysis/v192_void_segments_reference_flux_comparison.json';assert not out.exists();D=A.openDocument(str(p));rows=[]
for i in range(17):
 s=D.getObject('VOID_TOOL_'+str(i)).Shape;samples=[]
 for point in [(700,280,0),(700,300,0)]:
  values=[]
  for face in s.Faces:
   f=topods.Face(Part.__toPythonOCC__(face));v=BRepGProp_Vinert(BRepGProp_Face(f,True),BRepGProp_Domain(f),gp_Pnt(*point),1e-11);values.append(v.Mass())
  samples.append({'reference_point_mm':point,'signed_face_flux_sum_mm3':math.fsum(values)})
 rows.append({'segment_index':i,'span_interval_mm':[build['rows'][i]['y_start'],build['rows'][i]['y_end']],'face_count':len(s.Faces),'samples':samples,'P300_minus_P280_flux_mm3':samples[1]['signed_face_flux_sum_mm3']-samples[0]['signed_face_flux_sum_mm3']});print(i,rows[-1]['P300_minus_P280_flux_mm3'],flush=True);out.write_text(json.dumps({'status':'RUNNING','rows':rows},indent=2)+'\n')
A.closeDocument(D.Name);assert H(p)==h
priorp=R/'analysis/v192_cavity_shell_saved_void_comparison.json';prior=json.loads(priorp.read_text());sums=[math.fsum(r['samples'][j]['signed_face_flux_sum_mm3'] for r in rows) for j in range(2)]
out.write_text(json.dumps({'status':'ALL17_UNFUSED_VOID_SEGMENT_REFERENCE_FLUX_MEASURED','input_sha256_unchanged':h,'build_report_sha256':H(q),'fused_void_comparison_sha256':H(priorp),'rows':rows,'sum_unfused_segment_flux_mm3':sums,'unfused_sum_P300_minus_P280_mm3':sums[1]-sums[0],'unfused_sum_minus_saved_fused_at_same_point_mm3':[sums[j]-prior['rows'][j]['saved_void_signed_face_flux_sum_mm3'] for j in range(2)],'limits':['Numerical signed flux, not exact volume or rigorous bounds','Adjacent segment sum is not proof of nonoverlap or identical fusion boundary','No new fusion, geometry, tolerance change or release'],'print_release':False,'flight_release':False},indent=2)+'\n')
