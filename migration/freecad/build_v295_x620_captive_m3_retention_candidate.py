import FreeCAD as App, Part, pathlib, json, hashlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v293_X620_INTERNAL_JOINER_CANDIDATE.FCStd'
out=R/'migration/freecad/F14_v295_X620_CAPTIVE_M3_RETENTION_CANDIDATE.FCStd'
audp=R/'migration/freecad/freecad_v295_x620_captive_m3_retention_candidate_audit.json'
d=App.openDocument(str(src)); doc=App.newDocument('F14_v295_X620_CAPTIVE_M3_RETENTION_CANDIDATE')
for ob in d.Objects:
    if hasattr(ob,'Shape') and not ob.Shape.isNull():
        q=doc.addObject('PartDesign::Feature',ob.Name); q.Shape=ob.Shape.copy(); q.Label=ob.Label
fus=doc.getObject('FUSELAGE_CURRENT').Shape
critical=[n for n in ['BATTERY_TRAY_v165','BATTERY_REFERENCE_PACK','V225_SERVO_SERVICE','V225_SYNC_YOKE_M4_20','V221_CASSETTE_R','V221_CASSETTE_L','V233_TORQ_TCM1022_R','V233_TORQ_TCM1022_L','V247_TAIL_SERVO_CRADLE_R','V247_TAIL_SERVO_CRADLE_L','V229_ESC_SERVICE_R','V229_ESC_SERVICE_L'] if doc.getObject(n)]
AF=5.7; nut_depth=2.8; Rhex=AF/math.sqrt(3.0)
def hex_prism(cx,y0,cz,depth):
    pts=[App.Vector(cx+Rhex*math.cos(math.radians(30+60*i)),y0,cz+Rhex*math.sin(math.radians(30+60*i))) for i in range(6)]
    pts.append(pts[0]); return Part.Face(Part.makePolygon(pts)).extrude(App.Vector(0,depth,0))
rows=[]; total=0.0
x=620; ay=25; z=0; od=8
for sgn in (-1,1):
    y=sgn*ay; side='R' if sgn>0 else 'L'; tag=f'X620_{side}'
    bore=od/2+0.15; sleeve_or=bore+1.2; ir=sleeve_or+0.10; orr=ir+1.15; w=7.0
    ring=Part.makeCylinder(orr,w,App.Vector(x+2,y,z),App.Vector(1,0,0)).cut(Part.makeCylinder(ir,w,App.Vector(x+2,y,z),App.Vector(1,0,0)))
    slit=Part.makeBox(w+2,1.0,orr-ir+3.0,App.Vector(x+1,y-0.5,z+ir-0.5)); ring=ring.cut(slit)
    # Keep the screw/nut lugs above the receiving sleeve OD in the nominal state.
    # The clamp ring may close elastically during tightening, but the CAD candidate must not start with a hard sleeve/tube interference.
    lugz=z+ir+0.10
    lug1=Part.makeBox(7.0,3.2,7.0,App.Vector(x+2,y-4.0,lugz)); lug2=Part.makeBox(7.0,3.4,7.0,App.Vector(x+2,y+0.6,lugz))
    sh=ring.fuse(lug1).fuse(lug2)
    cx=x+5.5; cz=lugz+3.5
    sh=sh.cut(Part.makeCylinder(1.6,9.0,App.Vector(cx,y-4.5,cz),App.Vector(0,1,0)))
    sh=sh.cut(hex_prism(cx,y+1.2,cz,nut_depth)).removeSplitter()
    o=doc.addObject('PartDesign::Feature','V295_C_CLAMP_'+tag); o.Shape=sh; o.Label=f'v295 X620 C-ring clamp captive M3 nut {side}'
    cont=sh.common(fus).Volume/sh.Volume if sh.Volume else 0.0
    mg=sh.Volume/1000*1.25; total+=mg
    mind=min((sh.distToShape(doc.getObject(n).Shape)[0] for n in critical),default=999)
    sleeve=doc.getObject(f'V293_X620_SLEEVE_{side}_AFT').Shape
    tube=doc.getObject(f'V293_X620_CF_TUBE_{side}').Shape
    rows.append({'side':side,'valid':sh.isValid(),'solid_count':len(sh.Solids),'containment':cont,'mass_PPA_CF_g':mg,'critical_hardware_min_distance_mm':mind,'aft_sleeve_clearance_mm':sh.distToShape(sleeve)[0],'aft_sleeve_intersection_mm3':sh.common(sleeve).Volume,'cf_tube_clearance_mm':sh.distToShape(tube)[0],'cf_tube_intersection_mm3':sh.common(tube).Volume,'M3_clearance_d_mm':3.2,'nut_pocket_AF_mm':AF,'nut_pocket_depth_mm':nut_depth,'clamp_inner_radius_mm':ir,'sleeve_outer_radius_mm':sleeve_or})
doc.recompute(); doc.saveAs(str(out))
aud={'status':'V295_X620_CAPTIVE_M3_RETENTION_CANDIDATE','source':src.name,'architecture':{'X620_retention_defined':True,'receiving_sleeve_C_clamp':True,'CF_tube_cross_drilled':False,'captive_M3_hex_nut':True,'nominal_radial_clamp_gap_mm':0.10,'actual_nut_measurement_required':True,'aft_nacelle_OML_still_open':True},'rows':rows,'mass':{'PPA_CF_clamps_screen_g':total},'gates':{'all_valid_single_solids':all(r['valid'] and r['solid_count']==1 for r in rows),'containment_ge_0p98':all(r['containment']>=0.98 for r in rows),'critical_hardware_clearance_ge_10mm':all(r['critical_hardware_min_distance_mm']>=10 for r in rows),'no_nominal_sleeve_or_tube_interference':all(r['aft_sleeve_intersection_mm3']<1e-6 and r['cf_tube_intersection_mm3']<1e-6 for r in rows),'mass_lt_2g':total<2.0,'actual_M3_nut_fit_measured':False,'bench_clamp_force_test_required':True,'proof_load':False,'aft_nacelle_OML_registered':False,'print_release':False,'flight_release':False}}
aud['sha256']=hashlib.sha256(out.read_bytes()).hexdigest(); audp.write_text(json.dumps(aud,indent=2),encoding='utf-8'); print(json.dumps(aud,indent=2))
