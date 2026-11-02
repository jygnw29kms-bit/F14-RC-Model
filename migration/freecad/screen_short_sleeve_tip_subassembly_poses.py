from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[2];names=['WING_R_Y300_PARTITION_REVIEW_BLOCKED_ONLY.FCStd','FULLSPAN_SPAR_REFERENCE_UNFROZEN_ONLY.FCStd','Y300_SHORT_SLEEVE_ASSEMBLY_TRADE_STUDY_ONLY.FCStd'];ps=[R/'migration/freecad'/n for n in names];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hs=[H(p) for p in ps];out=R/'analysis/v192_short_sleeve_tip_subassembly_poses.json';assert not out.exists();D=A.openDocument(str(ps[0]));tip=next(o.Shape.copy() for o in D.Objects if min(v.Point.y for v in o.Shape.Vertexes)>299.999);A.closeDocument(D.Name);D=A.openDocument(str(ps[1]));fixed=[(o.Name,o.Shape.copy()) for o in D.Objects];A.closeDocument(D.Name);moving=[('TIP_SKIN',tip)];D=A.openDocument(str(ps[2]))
for o in D.Objects:
 (moving if o.Name in ('TIP_CARRIER','TIP_CARRIER_GEOMETRIC_SKIN_BOND','GEOMETRIC_BOND_1') else fixed).append((o.Name,o.Shape.copy()))
A.closeDocument(D.Name);rows=[]
for dy in (5,2.5,0):
 collisions=[];count=0
 for name,s in moving:
  t=s.copy();t.translate(A.Vector(0,dy,0))
  for fn,f in fixed:
   volume=t.common(f).Volume;count+=1
   if volume>1e-7:collisions.append({'moving':name,'fixed':fn,'overlap_mm3':volume})
 rows.append({'tip_subassembly_y_translation_mm':dy,'pair_checks':count,'positive_volume_collisions':collisions});print(rows[-1],flush=True);out.write_text(json.dumps({'status':'RUNNING','rows':rows},indent=2)+'\n')
assert [H(p) for p in ps]==hs;out.write_text(json.dumps({'status':'THREE_DISCRETE_SHORT_SLEEVE_TIP_SUBASSEMBLY_POSES_SCREENED','input_sha256_unchanged':dict(zip(names,hs)),'moving_objects':[n for n,s in moving],'fixed_objects':[n for n,s in fixed],'rows':rows,'limits':['Three discrete poses not continuous sweep proof','Adhesive placeholders rigid; no scraping, cure, insertion forces or tolerance analysis','No external tool access or actual assembly validation','Short sleeve reduced bond area remains unqualified; source partition volume gate blocked'],'print_release':False,'flight_release':False},indent=2)+'\n')
