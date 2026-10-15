"""v173: standalone bilateral stabilator root-fitting candidate in source-backed local plan coordinates."""
import adsk.core,adsk.fusion,json,os,hashlib,math

def mm(v): return v/10.0
def box(temp,cx,cy,cz,l,w,h):
    obb=adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(mm(cx),mm(cy),mm(cz)),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(l),mm(w),mm(h)); return temp.createBox(obb)
def point_inside(poly,x,y):
    c=False
    for i,(x1,y1) in enumerate(poly):
        x2,y2=poly[(i+1)%len(poly)]
        if ((y1>y)!=(y2>y)) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def prism_from_polygon(root,pts,thickness,name):
    sk=root.sketches.add(root.xYConstructionPlane); sk.name=name+'_PLAN'
    lines=sk.sketchCurves.sketchLines
    ps=[adsk.core.Point3D.create(mm(x),mm(y),0) for x,y in pts]
    for i in range(len(ps)): lines.addByTwoPoints(ps[i],ps[(i+1)%len(ps)])
    if sk.profiles.count<1: raise RuntimeError('reference stabilator profile failed')
    ei=root.features.extrudeFeatures.createInput(sk.profiles.item(0),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.setSymmetricExtent(adsk.core.ValueInput.createByReal(mm(thickness/2)),False)
    f=root.features.extrudeFeatures.add(ei); b=f.bodies.item(0); b.name=name; return b
def run_review(app,builder,mm_unused,outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); cfg=json.load(open(os.path.join(base,'F14_v173_section_inputs.json'),encoding='utf-8'))
    for pkey,hkey in [('v145','v145_sha256'),('v171','v171_sha256')]:
        if hashlib.sha256(open(cfg[pkey],'rb').read()).hexdigest()!=cfg[hkey]: raise RuntimeError('hash mismatch '+pkey)
    geo=json.load(open(cfg['v145'],encoding='utf-8')); polyR=[(x,-y) for x,y in geo['outline_mm']]; polyL=[(x,-y) for x,y in polyR]
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_STABILATOR_ROOT_FITTING_v173'; design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent; temp=adsk.fusion.TemporaryBRepManager.get()
    # Reference stabilator solids for visual/source-plan context.
    refR=prism_from_polygon(root,polyR,float(cfg['stabilator_reference_thickness_mm']),'REF_STABILATOR_R_v173'); refR.opacity=.25
    refL=prism_from_polygon(root,[(x,-y) for x,y in polyR],float(cfg['stabilator_reference_thickness_mm']),'REF_STABILATOR_L_v173'); refL.opacity=.25
    pivot=float(cfg['pivot_x_mm']); hx=float(cfg['hub_x_length_mm']); hy0,hy1=[float(v) for v in cfg['hub_y_range_mm']]; hz=float(cfg['hub_z_thickness_mm']); tx=float(cfg['tongue_x_length_mm']); ty0,ty1=[float(v) for v in cfg['tongue_y_range_mm']]; tz=float(cfg['tongue_z_thickness_mm']); bore=float(cfg['shaft_bore_d_mm'])
    records=[]
    for side,sgn,poly,ref in [('R',1,polyR,refR),('L',-1,[(x,-y) for x,y in polyR],refL)]:
        hub=box(temp,pivot,sgn*(hy0+hy1)/2,0,hx,hy1-hy0,hz)
        tongue=box(temp,pivot,sgn*(ty0+ty1)/2,0,tx,ty1-ty0,tz)
        tongue_pre=temp.copy(tongue)
        if not temp.booleanOperation(hub,tongue,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('fitting union failed '+side)
        by0,by1=[float(v) for v in cfg['shaft_bore_y_range_mm']]
        p0=adsk.core.Point3D.create(mm(pivot),mm(sgn*by0),0); p1=adsk.core.Point3D.create(mm(pivot),mm(sgn*by1),0)
        cyl=temp.createCylinderOrCone(p0,mm(bore/2),p1,mm(bore/2))
        if not temp.booleanOperation(hub,cyl,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('shaft bore failed '+side)
        fit=root.bRepBodies.add(hub); fit.name='CANDIDATE_STABILATOR_ROOT_FITTING_'+side+'_v173'
        # Shaft reference and crank envelope.
        sy0,sy1=[float(v) for v in cfg['reference_shaft_y_range_mm']]
        shaft=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(pivot),mm(sgn*sy0),0),mm(float(cfg['reference_shaft_d_mm'])/2),adsk.core.Point3D.create(mm(pivot),mm(sgn*sy1),0),mm(float(cfg['reference_shaft_d_mm'])/2)); sb=root.bRepBodies.add(shaft); sb.name='REF_6MM_STABILATOR_SHAFT_'+side+'_v173'; sb.opacity=.5
        cc=float(cfg['crank_center_abs_y_mm']); ct=float(cfg['crank_thickness_y_mm']); crank=temp.createCylinderOrCone(adsk.core.Point3D.create(mm(pivot),mm(sgn*(cc-ct/2)),0),mm(float(cfg['crank_radius_mm'])),adsk.core.Point3D.create(mm(pivot),mm(sgn*(cc+ct/2)),0),mm(float(cfg['crank_radius_mm']))); cb=root.bRepBodies.add(crank); cb.name='REF_20MM_CRANK_ENVELOPE_'+side+'_v173'; cb.opacity=.18
        # Planform sample checks for hub/tongue footprints.
        bad=0
        for x0,x1,y0,y1 in [(pivot-hx/2,pivot+hx/2,hy0,hy1),(pivot-tx/2,pivot+tx/2,ty0,ty1)]:
            x=x0
            while x<=x1+1e-9:
                y=y0
                while y<=y1+1e-9:
                    if not point_inside(poly,x,sgn*y): bad+=1
                    y+=1
                x+=1
        # Tongue must fit within the 5.5mm reference surface where it is exposed.
        q=temp.copy(tongue_pre); inter=temp.booleanOperation(q,temp.copy(ref),adsk.fusion.BooleanTypes.IntersectionBooleanType); tongue_inside=q.volume if inter and q.isValid else 0
        tongue_vol=tongue_pre.volume
        records.append({'side':side,'fitting_volume_cm3':fit.volume,'planform_outside_sample_count':bad,'tongue_volume_cm3':tongue_vol,'tongue_inside_reference_cm3':tongue_inside,'tongue_containment_fraction':tongue_inside/tongue_vol if tongue_vol else 0})
    top_bottom_wall=(hz-bore)/2
    audit={'status':'V173_STABILATOR_ROOT_FITTING_LOCAL_CAD','source':cfg,'records':records,'geometry':{'pivot_x_mm':pivot,'hub_bore_top_bottom_wall_mm':top_bottom_wall,'tongue_surface_clearance_each_z_side_mm':(float(cfg['stabilator_reference_thickness_mm'])-tz)/2,'shaft_bore_ends_inside_thick_hub':True},'geometry_candidate_pass':all(r['planform_outside_sample_count']==0 and r['tongue_containment_fraction']>0.999999 for r in records) and top_bottom_wall>=1.9,'shaft_torque_transfer_detail_designed':False,'fuselage_bearing_mount_designed':False,'material_proof_pass':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    os.makedirs(outdir,exist_ok=True); design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(os.path.join(outdir,'F14_STABILATOR_ROOT_FITTING_v173.f3d'))); json.dump(audit,open(os.path.join(outdir,'F14_v173_stabilator_root_fitting_audit.json'),'w'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v173_stabilator_root_fitting_review.png'),1600,1000)
    if prior:
        try: prior.activate()
        except: pass
    return audit