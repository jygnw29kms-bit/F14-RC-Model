from pathlib import Path
import re
path=Path(r'C:\Users\dezen\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\F14TomcatRC_v18\F14TomcatRC_v18.py')
s=path.read_text(encoding='utf-8')
insert=s.index('def build_project_revision():')
fn=r'''

def build_registered_clearance_keepout_review_v23():
    """Derive conservative fixed-body keepout envelopes from exact v22 BRep intersections."""
    build_registered_fuselage_collision_review_v22()
    design=adsk.fusion.Design.cast(_app.activeProduct)
    root=design.rootComponent
    _app.activeDocument.name='F14_v23_REGISTERED_SWEEP_KEEPOUT_REVIEW'
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
    fus=next(b for b in root.bRepBodies if b.name=='UPC_FUSELAGE_OML_WL_REGISTERED_v22')
    temporary=adsk.fusion.TemporaryBRepManager.get()
    records=[]; per_side={'R':[],'L':[]}
    for sweep in [20,30,40,50,60,68]:
        for sign,label in [(1,'R'),(-1,'L')]:
            angle=-sign*math.radians(sweep-20.0)
            rot=adsk.core.Matrix3D.create(); rot.setToRotation(angle,adsk.core.Vector3D.create(0,0,1),adsk.core.Point3D.create(mm(px),mm(sign*py),mm(pz)))
            wing=next(b for b in root.bRepBodies if b.name.startswith('SOURCE_GRUMMAN_BASIC_WING_'+label+'_'))
            lug=next(b for b in root.bRepBodies if b.name=='ENG_ROOT_LUG_'+label+'_v19')
            for body,kind in [(wing,'outer_wing'),(lug,'root_lug')]:
                moving=temporary.copy(body)
                if not temporary.transform(moving,rot): raise RuntimeError('v23 moving body transform failed')
                fixed=temporary.copy(fus)
                ok=temporary.booleanOperation(moving,fixed,adsk.fusion.BooleanTypes.IntersectionBooleanType)
                iv=moving.volume if ok and moving.isValid else 0.0
                rec=dict(sweep_deg=sweep,side=label,kind=kind,intersection_volume_cm3=iv,positive_overlap=iv>1e-4)
                if iv>1e-4:
                    bb=moving.boundingBox
                    bounds={a:[getattr(bb.minPoint,a)*10,getattr(bb.maxPoint,a)*10] for a in ['x','y','z']}
                    rec['intersection_bounds_mm']=bounds
                    per_side[label].append(bounds)
                records.append(rec)
    margin=2.0; keepouts={}
    for label in ['R','L']:
        bs=per_side[label]
        if not bs: continue
        agg={a:[min(v[a][0] for v in bs)-margin,max(v[a][1] for v in bs)+margin] for a in ['x','y','z']}
        keepouts[label]=agg
        body=extrude_poly(root,'ENG_SWEEP_KEEPOUT_'+label+'_v23_NOT_CUT_GEOMETRY',[(agg['x'][0],agg['y'][0]),(agg['x'][1],agg['y'][0]),(agg['x'][1],agg['y'][1]),(agg['x'][0],agg['y'][1])],agg['z'][0],agg['z'][1]-agg['z'][0])
        body.opacity=0.25
    audit=dict(status='REGISTERED_SWEEP_COLLISION_KEEPOUT_REVIEW',registration_inherited_from='v22',
      pivot_waterline_original_aircraft_verified=False,keepout_margin_mm=margin,intersection_records=records,
      conservative_keepout_bounds_mm=keepouts,exact_cut_geometry_created=False,
      note='Keepout boxes bound exact sampled BRep intersections plus 2 mm margin; they are packaging envelopes, not final glove cut geometry.',
      clearance_release=False,mechanical_detail_release=False,print_release=False,flight_release=False)
    with open(os.path.join(base,'F14TomcatRC_config.json'),encoding='utf-8') as stream: config=json.load(stream)
    outdir=os.path.join(config['export_dir'],'registered_keepout_v23'); os.makedirs(outdir,exist_ok=True)
    target=os.path.join(outdir,'F14_v23_REGISTERED_SWEEP_KEEPOUT_REVIEW.f3d')
    if not design.exportManager.execute(design.exportManager.createFusionArchiveExportOptions(target)): raise RuntimeError('v23 export failed')
    with open(os.path.join(outdir,'F14_v23_registered_keepout_audit.json'),'w',encoding='utf-8') as stream: json.dump(audit,stream,indent=2)
    _app.activeViewport.fit(); _app.activeViewport.saveAsImageFile(os.path.join(outdir,'F14_v23_registered_keepout_review.png'),1600,1000)
    return audit

'''
s=s[:insert]+fn+s[insert:]
s=s.replace('return build_registered_fuselage_collision_review_v22()','return build_registered_clearance_keepout_review_v23()',1)
path.write_text(s,encoding='utf-8')
print('patched',path)
