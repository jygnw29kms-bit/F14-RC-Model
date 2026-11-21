from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['WING_R_ADAPTIVE_PARTIAL_SPAN_TRIAL_ONLY.FCStd','WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_partition_bspline_surface_area_groups.json';assert not out.exists();groups={}
def signature(s):
 return hashlib.sha256(json.dumps([s.UDegree,s.VDegree,s.getUKnots(),s.getVKnots(),s.getUMultiplicities(),s.getVMultiplicities(),s.getWeights(),[[[v.x,v.y,v.z] for v in row] for row in s.getPoles()]],separators=(',',':')).encode()).hexdigest()
for label,p in zip(['SOURCE','PARTS'],ps):
 D=A.openDocument(str(p))
 for o in D.Objects:
  for i,f in enumerate(o.Shape.Faces,1):
   s=f.Surface
   if type(s).__name__!='BSplineSurface':continue
   key=signature(s);g=groups.setdefault(key,{'SOURCE':[],'PARTS':[]});g[label].append({'object':o.Name,'face':i,'area_mm2':f.Area})
 A.closeDocument(D.Name)
rows=[]
for key,g in groups.items():
 delta=sum(r['area_mm2'] for r in g['PARTS'])-sum(r['area_mm2'] for r in g['SOURCE']);rows.append({'surface_data_sha256':key,'source_count':len(g['SOURCE']),'part_count':len(g['PARTS']),'part_minus_source_area_mm2':delta,'faces':g})
rows.sort(key=lambda r:abs(r['part_minus_source_area_mm2']),reverse=True);assert [H(p) for p in ps]==hs
out.write_text(json.dumps({'status':'BSPLINE_RAW_SURFACE_DATA_GROUP_AREA_DIAGNOSTIC','input_sha256_unchanged':dict(zip(names,hs)),'group_count':len(rows),'matched_group_count':sum(r['source_count']>0 and r['part_count']>0 for r in rows),'unmatched_group_count':sum(not(r['source_count']>0 and r['part_count']>0) for r in rows),'sum_part_minus_source_area_mm2':sum(r['part_minus_source_area_mm2'] for r in rows),'largest_30_groups':rows[:30],'limits':['Raw degrees/knots/multiplicities/weights/poles matching only; trim domains may change','Native area integration numerical; area residual is not volume error bound or exact geometry defect','No geometry modification, tolerance relaxation or release'],'print_release':False,'flight_release':False},indent=2)+'\n');print('groups',len(rows),'unmatched',sum(not(r['source_count']>0 and r['part_count']>0) for r in rows));print(rows[:2])
