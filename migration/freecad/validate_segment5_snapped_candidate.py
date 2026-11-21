from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
from OCC.Core.BRepLib import BRepLib_CheckCurveOnSurface
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
R=Path(__file__).resolve().parents[2];names=['VOID_SEGMENT5_SNAPPED_ENDPOINT_STUDY_ONLY.FCStd','F14_CURRENT_FULL_VIEW_v192.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_segment5_snapped_candidate_validation.json';assert not out.exists();D=A.openDocument(str(ps[0]));s=D.getObject('SNAPPED_ENDPOINT_CANDIDATE_ONLY').Shape.copy();A.closeDocument(D.Name);native=Part.__toPythonOCC__(s);an=BRepCheck_Analyzer(native,True,False,True);valid=an.IsValid();pairs=[]
for i,f in enumerate(s.Faces,1):
 face=topods.Face(Part.__toPythonOCC__(f))
 for j,e in enumerate(f.Edges,1):
  edge=topods.Edge(Part.__toPythonOCC__(e));check=BRepLib_CheckCurveOnSurface(edge,face);check.Perform();row={'face_one_based':i,'edge_local_index_one_based':j,'done':check.IsDone(),'error_status':check.ErrorStatus(),'stored_edge_tolerance_mm':BRep_Tool.Tolerance(edge)}
  if check.IsDone():row['max_distance_mm']=check.MaxDistance()
  pairs.append(row)
finished=[r for r in pairs if r['done'] and r['error_status']==0];maxdist=max(r['max_distance_mm'] for r in finished);print('curve_pairs',len(pairs),'complete',len(finished),'max',maxdist,'native_exact_valid',valid,flush=True)
report={'status':'RUNNING_AFTER_CURVE_CHECK','native_exact_method_valid':valid,'edge_face_pair_count':len(pairs),'completed_pair_count':len(finished),'max_curve_surface_distance_mm':maxdist,'pairs_exceeding_stored_tolerance':[r for r in finished if r['max_distance_mm']>r['stored_edge_tolerance_mm']],'curve_pairs':pairs};out.write_text(json.dumps(report,indent=2)+'\n')
D=A.openDocument(str(ps[1]));wing=D.getObject('WING_R').Shape.copy();A.closeDocument(D.Name);outside=s.cut(wing).Volume;gap=s.distToShape(wing.Shells[0])[0];props=GProp_GProps();err=brepgprop.VolumePropertiesGK(native,props,1e-11,True,True,False,False,False);gk=props.Mass();areas=[]
for t in [0,.25,.5,.75,1]:
 y=230+10*t
 if t in [0,1]:f=next(f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-y)<1e-6 and f.BoundBox.YLength<1e-6)
 else:
  wires=s.slice(A.Vector(0,1,0),y);assert len(wires)==1;f=Part.Face(wires[0])
 p=GProp_GProps();ae=brepgprop.SurfaceProperties(Part.__toPythonOCC__(f),p,1e-11,False);areas.append({'fraction':t,'area_mm2':p.Mass(),'estimated_relative_error':ae})
a=[r['area_mm2'] for r in areas];single=10/6*(a[0]+4*a[2]+a[4]);composite=10/12*(a[0]+4*a[1]+2*a[2]+4*a[3]+a[4]);assert [H(p) for p in ps]==hs
report.update(status='SNAPPED_SEGMENT5_EXACT_CHECK_CONTAINMENT_AND_VOLUME_DIAGNOSTICS_MEASURED',input_sha256_unchanged=dict(zip(names,hs)),max_native_tolerance_mm=s.getTolerance(1),outside_current_master_wing_mm3=outside,min_distance_to_current_wing_boundary_mm=gap,default_volume_mm3=s.Volume,GK_volume_mm3=gk,GK_reported_relative_error=err,section_areas=areas,single_prismoid_volume_mm3=single,composite_simpson_volume_mm3=composite,limits=['Native exact-method check uses stored tolerances, not exact arithmetic','Min boundary distance/zero outside volume concern only current heuristic wing master, not verified original aircraft OML','Five-section quadrature and native integrators share geometry; no rigorous absolute error bound','Whole candidate deviation from original loft and global17 cavity/split remain unverified','No master promotion, material, structural, print or flight acceptance'],print_release=False,flight_release=False);out.write_text(json.dumps(report,indent=2)+'\n');print('outside',outside,'gap',gap,'volumes',s.Volume,gk,single,composite,flush=True)
