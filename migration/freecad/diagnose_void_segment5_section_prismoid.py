from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];p=R/'migration/freecad/WING_R_ADAPTIVE_VOID_SEGMENTS_ONLY.FCStd';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=H(p);out=R/'analysis/v192_void_segment5_section_prismoid_diagnostic.json';assert not out.exists();build=json.loads((R/'analysis/v192_adaptive_void_segments_build.json').read_text());assert h==build['output_sha256'];a=build['rows'][5]['y_start'];b=build['rows'][5]['y_end'];L=b-a;D=A.openDocument(str(p));s=D.getObject('VOID_TOOL_5').Shape.copy();A.closeDocument(D.Name);rows=[]
for t in [0,.25,.5,.75,1]:
 y=a+L*t
 if t in [0,1]:
  candidates=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-y)<1e-6 and f.BoundBox.YLength<1e-6];assert len(candidates)==1;f=candidates[0];method='saved_planar_cap'
 else:
  wires=s.slice(A.Vector(0,1,0),y);assert len(wires)==1;f=Part.Face(wires[0]);assert f.isValid();method='native_slice_planar_face'
 props=GProp_GProps();err=brepgprop.SurfaceProperties(Part.__toPythonOCC__(f),props,1e-11,False);rows.append({'fraction':t,'y_mm':y,'method':method,'area_mm2':props.Mass(),'estimated_relative_error':err});print(rows[-1],flush=True)
A0,Aq,Am,At,A1=[r['area_mm2'] for r in rows];single=L/6*(A0+4*Am+A1);composite=L/12*(A0+4*Aq+2*Am+4*At+A1)
def quadratic(t):return A0*2*(t-.5)*(t-1)+Am*(-4*t*(t-1))+A1*2*t*(t-.5)
residuals=[{'fraction':r['fraction'],'measured_minus_quadratic_area_mm2':r['area_mm2']-quadratic(r['fraction'])} for r in rows];assert H(p)==h
out.write_text(json.dumps({'status':'FIVE_SECTION_PRISMOID_DIAGNOSTIC_MEASURED_NOT_EXACT_VOLUME_CERTIFICATE','input_sha256_unchanged':h,'object':'VOID_TOOL_5','span_mm':[a,b],'rows':rows,'single_prismoid_volume_mm3':single,'composite_simpson_volume_mm3':composite,'composite_minus_single_mm3':composite-single,'default_native_volume_mm3':s.Volume,'section_quadratic_residuals':residuals,'limits':['Prismoid formula exact only if corresponding ruled profiles give quadratic section area; tested at five stations, not proven globally','Native slice and planar area routines introduce numerical approximations; estimates not rigorous bounds','Different cap and interior construction methods retained in report','No new CAD, geometry/tolerance modification or print/flight release'],'print_release':False,'flight_release':False},indent=2)+'\n');print('volumes',single,composite,'difference',composite-single,flush=True)
