"""v96: printable padded sandwich-clamp torsion fixture for the v94 representative joint coupon."""
import adsk.core, adsk.fusion, json, os, hashlib, re

def mm(v): return v/10.0

def _box(temp,sx,sy,sz,cx=0,cy=0,z0=0):
    c=adsk.core.Point3D.create(mm(cx),mm(cy),mm(z0+sz/2.0))
    return temp.createBox(adsk.core.OrientedBoundingBox3D.create(c,adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),mm(sx),mm(sy),mm(sz)))

def _cyl(temp,x,y,z0,z1,d):
    return temp.createCylinderOrCone(adsk.core.Point3D.create(mm(x),mm(y),mm(z0)),mm(d/2.0),adsk.core.Point3D.create(mm(x),mm(y),mm(z1)),mm(d/2.0))

def _cut_holes(temp,body,holes,d,z0,z1):
    for x,y in holes:
        tool=_cyl(temp,x,y,z0,z1,d)
        if not temp.booleanOperation(body,tool,adsk.fusion.BooleanTypes.DifferenceBooleanType): raise RuntimeError('Hole cut failed')
    return body

def _part(temp,spec,moving_top=False):
    sx=float(spec['x_mm']); sy=float(spec['y_mm']); sz=float(spec['z_mm']); d=float(spec['hole_d_mm'])
    body=_box(temp,sx,sy,sz); holes=[(float(x),float(y)) for x in spec['bolt_x_mm'] for y in spec['bolt_y_mm']]
    _cut_holes(temp,body,holes,d,-1,sz+1)
    if moving_top:
        lug=spec['lug']; xs=float(lug['x_start_mm'])-1.0; xl=float(lug['x_length_mm'])+1.0; ly=float(lug['y_mm']); lz=float(lug['z_mm'])
        lb=_box(temp,xl,ly,lz,cx=xs+xl/2.0)
        if not temp.booleanOperation(body,lb,adsk.fusion.BooleanTypes.UnionBooleanType): raise RuntimeError('Lug union failed')
        m5=[(float(x),float(lug['m5_y_mm'])) for x in lug['m5_x_mm']]
        _cut_holes(temp,body,m5,float(lug['m5_hole_d_mm']),-1,lz+1)
    return body

def run_review(app, build_source_wings, mm_unused, outdir):
    prior=app.activeDocument; base=os.path.dirname(__file__); src=json.load(open(os.path.join(base,'F14_v96_section_inputs.json'),encoding='utf-8'))
    if hashlib.sha256(open(src['plan_path'],'rb').read()).hexdigest()!=src['plan_sha256']: raise RuntimeError('Plan hash mismatch')
    plan=json.load(open(src['plan_path'],encoding='utf-8')); temp=adsk.fusion.TemporaryBRepManager.get()
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType); doc.name='F14_TORSION_FIXTURE_v96'
    design=adsk.fusion.Design.cast(app.activeProduct); design.designType=adsk.fusion.DesignTypes.DirectDesignType; root=design.rootComponent
    specs=[('FIXED_TOP_v96',plan['fixture']['fixed'],False),('FIXED_BOTTOM_v96',plan['fixture']['fixed'],False),('MOVING_BOTTOM_v96',plan['fixture']['moving'],False),('MOVING_TOP_LEVER_LUG_v96',plan['fixture']['moving'],True)]
    bodies=[]; records=[]
    for name,spec,mt in specs:
        tb=_part(temp,spec,mt); b=root.bRepBodies.add(tb); b.name=name; bodies.append(b)
        bb=b.boundingBox; props=b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy)
        records.append({'body':name,'volume_cm3':props.volume,'bbox_mm':{'x':[bb.minPoint.x*10,bb.maxPoint.x*10],'y':[bb.minPoint.y*10,bb.maxPoint.y*10],'z':[bb.minPoint.z*10,bb.maxPoint.z*10]}})
    os.makedirs(outdir,exist_ok=True); stldir=os.path.join(outdir,'torsion_fixture_v96_stl'); os.makedirs(stldir,exist_ok=True)
    stls=[]
    for b in bodies:
        fn=os.path.join(stldir,b.name+'.stl'); opt=design.exportManager.createSTLExportOptions(b,fn); opt.sendToPrintUtility=False
        if not design.exportManager.execute(opt): raise RuntimeError('STL export failed '+b.name)
        stls.append(fn)
    f3d=os.path.join(outdir,'F14_TORSION_FIXTURE_v96.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(f3d)): raise RuntimeError('F3D export failed')
    audit={'status':'V96_PRINTABLE_TORSION_FIXTURE','source':src,'plan':plan,'parts':records,'stl_files':stls,'fixture_geometry_created':True,'fixture_printed':False,'coupon_tested':False,'structural_capacity_verified':False,'print_release':False,'flight_release':False,'study_source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()}
    json.dump(audit,open(os.path.join(outdir,'F14_v96_torsion_fixture_audit.json'),'w',encoding='utf-8'),indent=2); app.activeViewport.fit(); app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v96_torsion_fixture_review.png'),1600,1000)
    try: doc.close(False)
    except: pass
    if prior:
        try: prior.activate()
        except: pass
    return audit