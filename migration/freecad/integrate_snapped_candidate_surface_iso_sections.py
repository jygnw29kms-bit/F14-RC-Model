from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math,ast
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt,gp_Vec
R=Path(__file__).resolve().parents[2];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();qp=R/'analysis/gauss_legendre_16_32_64_nodes_weights.json';Q=json.loads(qp.read_text());helper=R/'migration/freecad/integrate_segment5_caps_3D_Green.py';node=next(n for n in ast.parse(helper.read_text(encoding='utf-8-sig')).body if isinstance(n,ast.FunctionDef) and n.name=='integrate');exec(compile(ast.Module(body=[node],type_ignores=[]),str(helper),'exec'))
p=R/'migration/freecad/VOID_SEGMENT5_SNAPPED_ENDPOINT_STUDY_ONLY.FCStd';h=H(p);out=R/'analysis/v192_snapped_candidate_surface_iso_Green_sections.json';assert not out.exists();D=A.openDocument(str(p));s=D.getObject('SNAPPED_ENDPOINT_CANDIDATE_ONLY').Shape.copy();A.closeDocument(D.Name);sides=[]
for i,f in enumerate(s.Faces,1):
 if type(f.Surface).__name__=='Plane':continue
 surf=f.Surface;u0,u1,v0,v1=f.ParameterRange;p00=surf.value(u0,v0);p10=surf.value(u1,v0);p01=surf.value(u0,v1);p11=surf.value(u1,v1)
 if abs(p10.y-p00.y)>9 and abs(p01.y-p00.y)<1e-7:axis='u';start=u0;end=u1;plo=v0;phi=v1;ylo=p00.y;yhi=p10.y
 elif abs(p01.y-p00.y)>9 and abs(p10.y-p00.y)<1e-7:axis='v';start=v0;end=v1;plo=u0;phi=u1;ylo=p00.y;yhi=p01.y
 else:raise AssertionError(('nonconstant_span_direction',i,[p00.y,p10.y,p01.y,p11.y]))
 assert abs(min(ylo,yhi)-230)<1e-6 and abs(max(ylo,yhi)-240)<1e-6;sides.append((i,surf,axis,start,end,plo,phi,ylo,yhi))
assert len(sides)==98;rows=[]
for t in [0,.25,.5,.75,1]:
 target=230+10*t;edges=[]
 for i,surf,axis,start,end,plo,phi,ylo,yhi in sides:
  param=start+(end-start)*(target-ylo)/(yhi-ylo);curve=surf.uIso(param) if axis=='u' else surf.vIso(param);edges.append(curve.toShape(plo,phi))
 groups=Part.sortEdges(edges);assert len(groups)==1;wire=Part.Wire(groups[0]);assert wire.isClosed();samples=[integrate(wire,n,x) for n in [32,64] for x in [0,700]];rows.append({'fraction':t,'target_y_mm':target,'edge_count':len(edges),'samples':samples});print(t,samples[-1],flush=True)
areas=[r['samples'][-1]['area_with_hypothetical_line_connectors_mm2'] for r in rows];single=10/6*(areas[0]+4*areas[2]+areas[4]);composite=10/12*(areas[0]+4*areas[1]+2*areas[2]+4*areas[3]+areas[4]);assert H(p)==h
out.write_text(json.dumps({'status':'RULED_SURFACE_ISOCURVE_GREEN_SECTION_DIAGNOSTIC_MEASURED','input_sha256_unchanged':h,'helper_sha256':H(helper),'quadrature_sha256':H(qp),'side_surface_count':len(sides),'rows':rows,'single_prismoid_volume_mm3':single,'composite_simpson_volume_mm3':composite,'default_native_volume_mm3':s.Volume,'limits':['Surface span-direction recognized numerically from parameter corners; no global analytical certificate','Hypothetical line closures retained as bookkeeping; inspect raw/closed areas and endpoint gaps','Quadrature finite and native curve/surface evaluation shared; no rigorous absolute error bounds','No geometry/tolerance edits or master/print/flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n');print('volumes',single,composite,s.Volume,flush=True)
