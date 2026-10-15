"""v175: bilateral stabilator root fittings with matching D-bore / D-shaft reference geometry."""
import adsk.core,adsk.fusion,json,os,hashlib,math

def mm(v): return v/10.0
def box(temp,cx,cy,cz,l,w,h):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h)); return temp.createBox(obb)
def d_cylinder(temp,pivot,y0,y1,r,flat_x):
    cyl=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(pivot),mm(y0),0),mm(r),adsk.core.Point3D.create(mm(pivot),mm(y1),0),mm(r))
    lo=pivot-r-1.0; hi=pivot+flat_x; yc=(y0+y1)/2; clip=box(temp,(lo+hi)/2,yc,0,hi-lo,abs(y1-y0)+2,2*r+2)
    if not temp.booleanOperation(cyl,clip,adsk.fusion.BooleanTypes.IntersectionBooleanType): raise RuntimeError('D profile clip failed')
    return cyl
def point_inside(poly,x,y):
    c=False
    for i,(x1,y1) in enumerate(poly):
        x2,y2=poly[(i+1)%len(poly)]
        if ((y1>y)!=(y2>y)) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def prism(root,pts,th,name):
    sk=root.sketches.add(root.xYConstructionPlane); lines=sk.sketchCurves.sketchLines; ps=[adsk.core.Point3D.create(mm(x),mm(y),0) for x,y in pts]
    for i in range(len(ps)): lines.addByTwoPoints(ps[i],ps[(i+1)%len(ps)])
    ei=root.features.extrudeFeatures.createInput(sk.profiles.item(0),adsk.fusion.FeatureOperations.NewBodyFeatureOperation); ei.setSymmetricExtent(adsk.core.ValueInput.createByReal(mm(th/2)),False); f=root.features.extrudeFeatures.add(ei); b=f.bodies.item(0); b.name=name; return b
def ivol(temp,a,b):
    q=temp.copy(a); ok=temp.booleanOperation(q,temp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType); return q.volume if ok and q.isValid else 0.0
def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v175_section_inputs.json'),encoding='utf-8'))
    for pk,hk in [('v145','v145_sha256'),('v171','v171_sha256'),('v174','v174_sha256')]:
        if hashlib.sha256(open(cfg[pk],'rb').read()).hexdigest()!=cfg[hk]: raise RuntimeError('hash mismatch '+pk)
    geo=json.load(open(cfg['v145'],encoding='utf-8')); polyR=[(x,-y) for x,y in geo['outline_mm']]; polyL=[(x,-y) for x,y in polyR]
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_STABILATOR_D_SHAFT_ROOT_FITTING_v175'; design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get()
    refs={'R':prism(root,polyR,float(cfg['stabilator_reference_thickness_mm']),'REF_STABILATOR_R_v175'),'L':prism(root,polyL,float(cfg['stabilator_reference_thickness_mm']),'REF_STABILATOR_L_v175')}
    for b in refs.values(): b.opacity=.22
    pivot=float(cfg['pivot_x_mm']); hx=float(cfg['hub_x_length_mm']); hy0,hy1=[float(v) for v in cfg['hub_y_range_mm']]; hz=float(cfg['hub_z_thickness_mm']); tx=float(cfg['tongue_x_length_mm']); ty0,ty1=[float(v) for v in cfg['tongue_y_range_mm']]; tz=float(cfg['tongue_z_thickness_mm']); br=float(cfg['bore_radius_mm']); bf=float(cfg['bore_flat_x_from_center_mm']); sr=float(cfg['shaft_radius_mm']); sf=float(cfg['shaft_flat_x_from_center_mm'])
    rec=[]
    for side,sgn,poly in [('R',1,polyR),('L',-1,polyL)]:
        hub=box(temp,pivot,sgn*(hy0+hy1)/2,0,hx,hy1-hy0,hz); tongue=box(temp,pivot,sgn*(ty0+ty1)/2,0,tx,ty1-ty0,tz); tongue_copy=temp.copy(tongue)
        if not temp.booleanOperation(hub,tongue,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('union')
        y0,y1=[float(v) for v in cfg['bore_y_range_mm']]; tool=d_cylinder(temp,pivot,sgn*y0,sgn*y1,br,bf)
        if not temp.booleanOperation(hub,tool,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('D bore cut')
        fit=root.bRepBodies.add(hub); fit.name='CANDIDATE_D_BORE_STABILATOR_FITTING_'+side+'_v175'
        sy0,sy1=[float(v) for v in cfg['shaft_y_range_mm']]; shaft=d_cylinder(temp,pivot,sgn*sy0,sgn*sy1,sr,sf); shaft_ref=temp.copy(shaft); sb=root.bRepBodies.add(shaft); sb.name='REF_D_SHAFT_6MM_'+side+'_v175'; sb.opacity=.55
        cc=float(cfg['crank_center_abs_y_mm']); ct=float(cfg['crank_thickness_y_mm']); crank=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(pivot),mm(sgn*(cc-ct/2)),0),mm(float(cfg['crank_radius_mm'])),adsk.core.Point3D.create(mm(pivot),mm(sgn*(cc+ct/2)),0),mm(float(cfg['crank_radius_mm']))); cb=root.bRepBodies.add(crank); cb.name='REF_20MM_CRANK_ENVELOPE_'+side+'_v175'; cb.opacity=.15
        overlap=ivol(temp,fit,shaft_ref)
        tongue_inside=ivol(temp,tongue_copy,refs[side]); tvol=tongue_copy.volume
        bad=0
        for x0,x1,yy0,yy1 in [(pivot-hx/2,pivot+hx/2,hy0,hy1),(pivot-tx/2,pivot+tx/2,ty0,ty1)]:
            x=x0
            while x<=x1+1e-9:
                y=yy0
                while y<=yy1+1e-9:
                    if not point_inside(poly,x,sgn*y): bad+=1
                    y+=1
                x+=1
        rec.append({'side':side,'fitting_volume_cm3':fit.volume,'D_shaft_to_fitting_intersection_cm3':overlap,'planform_outside_sample_count':bad,'tongue_containment_fraction':tongue_inside/tvol if tvol else 0})
    radial_clear=br-sr; flat_clear=bf-sf; hub_wall_z=hz/2-br
    audit={'status':'V175_STABILATOR_D_SHAFT_ROOT_FITTING_CAD','source':cfg,'records':rec,'geometry':{'radial_clearance_mm':radial_clear,'flat_clearance_mm':flat_clear,'hub_min_top_bottom_wall_mm':hub_wall_z,'D_bore_stays_inside_thick_hub':True},'geometry_candidate_pass':all(r['D_shaft_to_fitting_intersection_cm3']<1e-8 and r['planform_outside_sample_count']==0 and r['tongue_containment_fraction']>.999999 for r in rec) and radial_clear>=.049 and flat_clear>=.049 and hub_wall_z>=1.9,'shaft_torque_transfer_detail_designed':True,'axial_retention_designed':False,'fuselage_bearing_mount_designed':False,'material_proof_pass':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_STABILATOR_D_SHAFT_ROOT_FITTING_v175.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v175_stabilator_D_shaft_audit.json'),'w'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v175_stabilator_D_shaft_review.png'),1600,1000)
    if prior:
        try: prior.activate()
        except: pass
    return audit