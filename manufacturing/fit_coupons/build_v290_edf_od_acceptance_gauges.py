import FreeCAD as App, Part, Mesh, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
outdir=R/'manufacturing/fit_coupons'; outdir.mkdir(parents=True,exist_ok=True)
fc=outdir/'F14_v290_EDF_OD_ACCEPTANCE_GAUGES.FCStd'; aud=outdir/'v290_edf_od_acceptance_gauges_audit.json'
doc=App.newDocument('F14_v290_EDF_OD_ACCEPTANCE_GAUGES')
rows=[]
for d in [52.0,52.5,53.0,53.2,53.5,54.0]:
    ri=d/2.0; ro=ri+3.0; w=6.0
    ring=Part.makeCylinder(ro,w).cut(Part.makeCylinder(ri,w))
    # remove a wide radial sector so the gauge can clip around an assembled shroud
    cut=Part.makeBox(ro*2.4, ro*1.15, w+2, App.Vector(-ro*1.2,-0.2,-1))
    cg=ring.cut(cut).removeSplitter()
    name=f'EDF_OD_GAUGE_{str(d).replace(".","p")}'
    o=doc.addObject('PartDesign::Feature',name); o.Shape=cg; o.Label=f'v290 EDF shroud OD C-gauge {d:.1f} mm'
    stl=outdir/(name+'.stl'); Mesh.export([o],str(stl))
    rows.append({'nominal_OD_mm':d,'valid':cg.isValid(),'solid_count':len(cg.Solids),'stl':stl.name,'use':'largest gauge that fits without force bounds measured shroud OD; verify with caliper'})
# adapter acceptance ring at existing corridor maximum
ri=53.2/2; ro=ri+4; w=8
ring=Part.makeCylinder(ro,w).cut(Part.makeCylinder(ri,w))
o=doc.addObject('PartDesign::Feature','EDF_ADAPTER_MAX_OD_53p2'); o.Shape=ring; o.Label='v290 53.2 mm maximum-shroud acceptance reference'
Mesh.export([o],str(outdir/'EDF_ADAPTER_MAX_OD_53p2.stl'))
doc.recompute(); doc.saveAs(str(fc))
data={'status':'V290_EDF_OD_ACCEPTANCE_GAUGES','hardware':'XFly Galaxy X5 50mm 4S candidate','published_facts':{'internal_diameter_mm':50,'external_diameter_published':False,'current_A':40,'thrust_g':900},'gauges':rows,'existing_adapter_gate':{'max_shroud_OD_mm':53.2,'note':'engineering acceptance limit from prior carrier corridor, not a claimed XFly dimension'},'measurement_protocol':['measure bare cylindrical shroud body with caliper at >=3 axial positions and 2 orthogonal directions','use C-gauges only as print/process sanity check, not as substitute for caliper','record intake lip OD separately','freeze production adapter only after actual unit measurement'],'gates':{'all_gauges_valid':all(x['valid'] and x['solid_count']==1 for x in rows),'actual_X5_shroud_OD_measured':False,'actual_X5_lip_OD_measured':False,'adapter_OD_frozen':False,'print_release':False,'flight_release':False}}
data['sha256']=hashlib.sha256(fc.read_bytes()).hexdigest(); aud.write_text(json.dumps(data,indent=2),encoding='utf-8'); print(json.dumps(data,indent=2))
