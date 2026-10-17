from pathlib import Path
import json

FILES = [
    Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC\F14TomcatRC.py'),
    Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py'),
]

FUNC = r'''
def build_sweep_envelope_review_v20():
    """Rotate the real source-wing + v19 root-lug BReps through the full sweep range and audit packaging envelopes."""
    build_root_lug_review_v19()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v20_SWEEP_MOVING_ASSEMBLY_ENVELOPE_REVIEW'
    base=os.path.dirname(__file__)
    with open(os.path.join(base,'NASA_F14_basic_wing_v08.json'),encoding='utf-8') as stream: data=json.load(stream)
    with open(os.path.join(base,'F14_pivot_datum_v16.json'),encoding='utf-8') as stream: pivot=json.load(stream)
    factor=900.0/(2.0*data['sections'][-1]['wbl_in'])
    px=pivot['derived_full_scale_pivot_fs_in']*factor
    py=pivot['derived_full_scale_pivot_bl_in']*factor
    s0,s1=data['sections'][0],data['sections'][1]
    dz=(s1['reference_vertical_wl_in']-s0['reference_vertical_wl_in'])/(s1['wbl_in']-s0['wbl_in'])
    pivot_wl_in=s0['reference_vertical_wl_in']+(pivot['derived_full_scale_pivot_bl_in']-s0['wbl_in'])*dz
    pz=pivot_wl_in*factor
    temporary=adsk.fusion.TemporaryBRepManager.get()
    sweeps=[]
    for sweep in [20,30,40,50,60,68]:
        side_results=[]
        for sign,label in [(1,'R'),(-1,'L')]:
            wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
            lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
            angle=-sign*math.radians(sweep-20.0)
            transform=adsk.core.Matrix3D.create()
            transform.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            bounds=[]
            for body in [wing,lug]:
                copy=temporary.copy(body)
                if not temporary.transform(copy,transform):
                    raise RuntimeError('Temporary BRep transform failed at sweep %s side %s'%(sweep,label))
                bb=copy.boundingBox
                bounds.append(dict(x=[bb.minPoint.x*10,bb.maxPoint.x*10],y=[bb.minPoint.y*10,bb.maxPoint.y*10],z=[bb.minPoint.z*10,bb.maxPoint.z*10]))
            combined=dict(x=[min(v['x'][0] for v in bounds),max(v['x'][1] for v in bounds)],
                          y=[min(v['y'][0] for v in bounds),max(v['y'][1] for v in bounds)],
                          z=[min(v['z'][0] for v in bounds),max(v['z'][1] for v in bounds)])
            side_results.append(dict(side=label,bounds_mm=combined))
        span=max(s['bounds_mm']['y'][1] for s in side_results)-min(s['bounds_mm']['y'][0] for s in side_results)
        sweeps.append(dict(sweep_deg=sweep,span_mm=span,sides=side_results))
    audit=dict(status='NATIVE_BREP_SWEEP_MOVING_ASSEMBLY_ENVELOPE',
               source_pivot_fs_bl_verified=True,pivot_waterline_original_aircraft_verified=False,
               root_lug_overlap_depth_mm=8.0,pivot_model_mm=dict(x=px,y=py,z=pz),
               sweep_results=sweeps,body_glove_collision_checked=False,
               note='Native wing + root-lug BReps rotated about engineering pivot. Fixed fuselage/body-glove collision awaits source-registered body geometry.',
               mechanical_detail_release=False,print_release=False,flight_release=False)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'sweep_v20'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v20_SWEEP_MOVING_ASSEMBLY_ENVELOPE_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v20 export failed')
    with open(os.path.join(outdir,'F14_v20_sweep_envelope_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v20_sweep_envelope_review.png'),1600,1000)
    return audit

'''

for p in FILES:
    s=p.read_text(encoding='utf-8')
    if 'def build_sweep_envelope_review_v20()' not in s:
        marker='def build_project_revision():'
        s=s.replace(marker,FUNC+marker,1)
    s=s.replace('return build_root_lug_review_v19()','return build_sweep_envelope_review_v20()')
    p.write_text(s,encoding='utf-8')
    print('patched',p)

manifest=Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.manifest')
data=json.loads(manifest.read_text(encoding='utf-8-sig'))
data['version']='0.2.1'
manifest.write_text(json.dumps(data,indent=2),encoding='utf-8')
print('manifest',data['version'])
