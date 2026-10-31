import FreeCAD as App, Part, Mesh, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model'); D=R/'manufacturing/fit_coupons'; D.mkdir(parents=True,exist_ok=True)
fc=D/'F14_v291_EDF_INTERCHANGEABLE_ADAPTER_RINGS.FCStd'; aud=D/'v291_edf_interchangeable_adapter_rings_audit.json'
doc=App.newDocument('F14_v291_EDF_INTERCHANGEABLE_ADAPTER_RINGS')
outer_d=55.2; width=10.0; rows=[]
for inner_d in [52.0,52.5,53.0,53.2]:
    ro=outer_d/2; ri=inner_d/2
    ring=Part.makeCylinder(ro,width).cut(Part.makeCylinder(ri,width))
    # split for clamp compliance; 0.8 mm slot
    slot=Part.makeBox(ro+1,0.8,width+2,App.Vector(0,-0.4,-1))
    sh=ring.cut(slot).removeSplitter()
    name=f'EDF_ADAPTER_OD55p2_ID{str(inner_d).replace(".","p")}'
    o=doc.addObject('PartDesign::Feature',name); o.Shape=sh; o.Label=f'v291 EDF adapter 55.2 OD / {inner_d:.1f} ID split ring'
    stl=D/(name+'.stl'); Mesh.export([o],str(stl))
    rows.append({'carrier_OD_mm':outer_d,'shroud_ID_mm':inner_d,'radial_wall_mm':(outer_d-inner_d)/2,'valid':sh.isValid(),'solid_count':len(sh.Solids),'stl':stl.name,'production_allowed_only_after_actual_shroud_measurement':True})
doc.recompute(); doc.saveAs(str(fc))
data={'status':'V291_EDF_INTERCHANGEABLE_ADAPTER_RINGS','carrier_OD_mm':outer_d,'axial_width_mm':width,'rows':rows,'decision':{'accepted_measured_shroud_OD_range_mm':[52.0,53.2],'OD_gt_53p2_requires_mount_redesign':True,'rings_are_hardware_fit_candidates_not_aft_nacelle_OML_release':True},'gates':{'all_valid':all(r['valid'] and r['solid_count']==1 for r in rows),'min_radial_wall_ge_1mm':min(r['radial_wall_mm'] for r in rows)>=1.0,'actual_X5_OD_measured':False,'clamp_force_bench_tested':False,'aft_nacelle_OML_registered':False,'print_release':False,'flight_release':False}}
data['sha256']=hashlib.sha256(fc.read_bytes()).hexdigest(); aud.write_text(json.dumps(data,indent=2),encoding='utf-8'); print(json.dumps(data,indent=2))
