from pathlib import Path
import FreeCAD as A,Part,json,hashlib
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepLib import BRepLib_CheckCurveOnSurface
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods
R=Path(__file__).resolve().parents[2];names=['WING_R_NORMALIZED_SHARED_PROFILE_SEGMENTS_STUDY_ONLY.FCStd','F14_CURRENT_FULL_VIEW_v192.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_normalized_segments_containment_interfaces.json';assert not out.exists();D=A.openDocument(str(ps[0]));parts=[(i,D.getObject('NORMALIZED_VOID_SEG_'+str(i)).Shape.copy(),float(D.getObject('NORMALIZED_VOID_SEG_'+str(i)).SpanStart),float(D.getObject('NORMALIZED_VOID_SEG_'+str(i)).SpanEnd)) for i in range(17)];A.closeDocument(D.Name);D=A.openDocument(str(ps[1]));wing=D.getObject('WING_R').Shape.copy();A.closeDocument(D.Name);rows=[];interfaces=[]
def checkpoint(stage):out.write_text(json.dumps({'status':'RUNNING','stage':stage,'rows':rows,'interfaces':interfaces},indent=2)+'\n')
for i,s,a,b in parts:
 exact=BRepCheck_Analyzer(Part.__toPythonOCC__(s),True,False,True).IsValid();pair_count=0;failed=[];maxdist=0;exceed=[]
 for fi,f in enumerate(s.Faces,1):
  face=topods.Face(Part.__toPythonOCC__(f))
  for ei,e in enumerate(f.Edges,1):
   pair_count+=1;edge=topods.Edge(Part.__toPythonOCC__(e));c=BRepLib_CheckCurveOnSurface(edge,face);c.Perform()
   if not c.IsDone() or c.ErrorStatus()!=0:failed.append([fi,ei,c.ErrorStatus()]);continue
   dist=c.MaxDistance();maxdist=max(maxdist,dist);tol=BRep_Tool.Tolerance(edge)
   if dist>tol:exceed.append({'face':fi,'local_edge':ei,'distance_mm':dist,'stored_tolerance_mm':tol})
 outside=s.cut(wing).Volume;gap=s.distToShape(wing.Shells[0])[0];rows.append({'index':i,'span_mm':[a,b],'native_exact_method_valid':exact,'edge_face_pair_count':pair_count,'failed_curve_surface_pairs':failed,'max_curve_surface_distance_mm':maxdist,'curve_pairs_exceeding_stored_tolerance':exceed,'max_native_tolerance_mm':s.getTolerance(1),'outside_current_wing_volume_mm3':outside,'min_distance_to_current_wing_boundary_mm':gap});print('SEGMENT',i,'outside',outside,'gap',gap,'maxCurveGap',maxdist,flush=True);checkpoint('segment_checks')
for (i,s,a,b),(j,t,c,d) in zip(parts,parts[1:]):
 assert b==c
 sf=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-b)<1e-6 and f.BoundBox.YLength<1e-6];tf=[f for f in t.Faces if type(f.Surface).__name__=='Plane' and abs(f.CenterOfMass.y-b)<1e-6 and f.BoundBox.YLength<1e-6];assert len(sf)==len(tf)==1
 area=sf[0].common(tf[0]).Area;overlap=s.common(t).Volume;interfaces.append({'left_index':i,'right_index':j,'y_mm':b,'left_cap_area_mm2':sf[0].Area,'right_cap_area_mm2':tf[0].Area,'common_face_area_mm2':area,'left_area_minus_common_mm2':sf[0].Area-area,'right_area_minus_common_mm2':tf[0].Area-area,'solid_overlap_mm3':overlap});print('INTERFACE',i,j,overlap,flush=True);checkpoint('interface_checks')
assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'NORMALIZED_17_SEGMENTS_CONTAINMENT_CURVES_AND16_INTERFACES_MEASURED','input_sha256_unchanged':dict(zip(names,hs)),'rows':rows,'interfaces':interfaces,'limits':['Containment and distance only against current heuristic wing, not verified original aircraft OML','Native exact-method check remains tolerance-based; curve gaps measured separately','Face common and volume intersection numerical, not exact topology proof','No whole candidate deviation, new fusion, wing subtraction, split, manufacturing or flight acceptance'],'print_release':False,'flight_release':False},indent=2)+'\n')
