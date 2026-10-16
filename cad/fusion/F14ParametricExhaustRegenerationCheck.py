import adsk.core,adsk.fusion,json,os,hashlib,math

def run_review(app,builder,mm,outdir):
    prior=app.activeDocument;cfg=json.load(open(os.path.join(os.path.dirname(__file__),'F14_parametric_regen_inputs.json')))
    if hashlib.sha256(open(cfg['path'],'rb').read()).hexdigest()!=cfg['sha256']:raise RuntimeError('Source changed')
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(cfg['path']));design=adsk.fusion.Design.cast(app.activeProduct)
    if design.designType!=adsk.fusion.DesignTypes.ParametricDesignType:raise RuntimeError('History missing')
    parameter=design.userParameters.itemByName('exit_FSA_ratio');original=parameter.expression;records=[]
    for ratio in [.9,.85,.95,.9]:
        parameter.expression=str(ratio)
        if not design.computeAll():raise RuntimeError('Recompute failed')
        bodies=[b for b in design.rootComponent.bRepBodies if b.name.startswith('PARAMETRIC_EXHAUST_')]
        if len(bodies)!=2:raise RuntimeError('Parametric bodies lost')
        vals=[]
        for body in bodies:
            if not body.isValid or not body.isSolid:raise RuntimeError('Invalid regenerated wall')
            faces=[f for f in body.faces if adsk.core.Cone.cast(f.geometry)]
            if len(faces)!=2:raise RuntimeError('Regenerated cone missing')
            gap=app.measureManager.measureMinimumDistance(faces[0],faces[1]).value*10
            diameter=math.sqrt(ratio*(50**2-28**2));expected=.83/math.sqrt(1+((50-diameter)/(2*(754.962281164333-731.5)))**2)
            if abs(gap-expected)>1e-7:raise RuntimeError('Analytic regenerated normal gap mismatch')
            vals.append(dict(body=body.name,volume_cm3=body.volume,normal_gap_mm=gap,analytic_normal_gap_mm=expected))
        records.append(dict(exit_ratio=ratio,bodies=vals))
    parameter.expression=original;design.computeAll()
    if abs(records[0]['bodies'][0]['volume_cm3']-records[-1]['bodies'][0]['volume_cm3'])>1e-8:raise RuntimeError('Baseline restoration failed')
    if records[1]['bodies'][0]['volume_cm3']==records[2]['bodies'][0]['volume_cm3']:raise RuntimeError('Parameter failed to change geometry')
    audit=dict(status='NATIVE_PARAMETER_REGENERATION_AND_RESTORE_VERIFIED',input=cfg,tests=records,baseline_restored=True,source_containment_for_changed_cases_verified=False,hardware_verified=False,print_release=False)
    os.makedirs(outdir,exist_ok=True);json.dump(audit,open(os.path.join(outdir,'F14_parametric_exhaust_regeneration_audit.json'),'w'),indent=2);doc.close(False)
    if prior:prior.activate()
    return audit
