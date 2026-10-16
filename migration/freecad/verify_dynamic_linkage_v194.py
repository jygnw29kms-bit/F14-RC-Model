import FreeCAD as App, Part, json, os, math
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SRC=os.path.join(BASE,'migration','freecad','F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd')
KIN=os.path.join(BASE,'analysis','F14_sweep_linkage_kinematics_v40.json')
OUT=os.path.join(BASE,'migration','freecad','freecad_v194_dynamic_linkage_audit.json')
DOCOUT=os.path.join(BASE,'migration','freecad','F14_CURRENT_FULL_VIEW_v194_DYNAMIC_LINKAGE.FCStd')
SHIFT=187.59240693460868
PX=613.1323905812828; PY=125.20927023775282
Z=196.0-SHIFT

def box(x0,x1,y0,y1,z0,z1): return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))
def ivol(a,b):
    try:
        c=a.common(b); return c.Volume if not c.isNull() else 0.0
    except Exception: return 0.0

def cyl_between(a,b,r):
    va=App.Vector(*a); vb=App.Vector(*b); v=vb-va; L=v.Length
    if L<1e-9: return Part.Shape()
    return Part.makeCylinder(r,L,va,v)

def addfeat(doc,name,label,shape):
    o=doc.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=shape; return o

with open(KIN,encoding='utf-8') as f: kin=json.load(f)
c=kin['top_candidates'][1]
# Legacy fixed geometry transformed into local datum.
legacy={
 'CF_FRONT_LOWER': (594.1323905812828,600.1323905812828,-72,72,180.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'RISER_FRONT_R': (591.1323905812828,603.1323905812828,68,78,175.09240693460868-SHIFT,187.09240693460868-SHIFT),
 'RISER_FRONT_L': (591.1323905812828,603.1323905812828,-78,-68,175.09240693460868-SHIFT,187.09240693460868-SHIFT),
 'CF_REAR_LOWER': (626.1323905812828,632.1323905812828,-72,72,179.09240693460868-SHIFT,185.09240693460868-SHIFT),
 'RISER_REAR_R': (623.1323905812828,635.1323905812828,68,78,175.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'RISER_REAR_L': (623.1323905812828,635.1323905812828,-78,-68,175.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'CF_FRONT_UPPER': (594.1323905812828,600.1323905812828,-72,72,196.09240693460868-SHIFT,202.0924069346087-SHIFT),
 'CF_REAR_UPPER': (626.1323905812828,632.1323905812828,-72,72,196.09240693460868-SHIFT,202.0924069346087-SHIFT),
 'SERVO_SERVICE': (517.1323905812828,565.1323905812828,-13.5,13.5,0.0,44.0),
}
obs={k:box(*v) for k,v in legacy.items()}
doc=App.openDocument(SRC)
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
wings={'R':doc.getObject('WING_R').Shape,'L':doc.getObject('WING_L').Shape}
for nm in ['BATTERY_TRAY_v165','INLET_EDF_R','INLET_EDF_L']:
    o=doc.getObject(nm)
    if o and hasattr(o,'Shape') and not o.Shape.isNull(): obs[nm]=o.Shape
# Skip static v193 slider envelope objects as obstacles; they are the mechanism envelope itself.
rows=[]; global_max_hit=0.0; global_min_inside=1.0
for sample in c['samples']:
    sweep=float(sample['sweep_deg'])
    if sweep<20 or sweep>68: continue
    sx=float(sample['slider_x_mm'])
    cp=sample['crank_pin_mm']
    sides=[]
    for lab,sgn in [('R',1),('L',-1)]:
        py=sgn*PY; sy=sgn*float(c['slider_attach_y_mm'])
        # Mirror source R crank-pin y around centerline for L.
        cpx=float(cp[0]); cpy=sgn*abs(float(cp[1]))
        crank=cyl_between((PX,py,Z),(cpx,cpy,Z),4.0)
        rod=cyl_between((cpx,cpy,Z),(sx,sy,Z),2.0)
        slider=box(sx-4,sx+4,sy-3,sy+3,Z-2.5,Z+2.5)
        parts={'crank':crank,'rod':rod,'slider':slider}
        partrows={}; sidehit=0.0; mininside=1.0
        for pn,sh in parts.items():
            vol=sh.Volume if not sh.isNull() else 0.0
            wing=wings[lab].copy()
            ang=(-sgn)*math.radians(sweep-20.0)
            wing.rotate(App.Vector(PX,py,0),App.Vector(0,0,1),math.degrees(ang))
            inside=min(1.0,(ivol(sh,fuse)+ivol(sh,wing))/vol) if vol else 0.0
            hits={k:ivol(sh,v) for k,v in obs.items()}
            hit=sum(hits.values())
            partrows[pn]={'inside_fuselage_fraction':inside,'collision_mm3':hit,'hits_mm3':hits}
            sidehit+=hit; mininside=min(mininside,inside)
        sides.append({'side':lab,'total_collision_mm3':sidehit,'min_inside_fuselage_fraction':mininside,'parts':partrows})
        global_max_hit=max(global_max_hit,sidehit); global_min_inside=min(global_min_inside,mininside)
    rows.append({'sweep_deg':sweep,'slider_x_mm':sx,'sides':sides})
# Add representative 20/44/68 deg geometry in separate groups for review.
grp=doc.addObject('App::DocumentObjectGroup','DYNAMIC_LINKAGE_V194'); grp.Label='05 DYNAMIC LINKAGE v194 REVIEW / NOT RELEASED'
for sample in c['samples']:
    sw=int(round(float(sample['sweep_deg'])))
    if sw not in (20,44,68): continue
    sx=float(sample['slider_x_mm']); cp=sample['crank_pin_mm']
    for lab,sgn in [('R',1),('L',-1)]:
        py=sgn*PY; sy=sgn*float(c['slider_attach_y_mm']); cpx=float(cp[0]); cpy=sgn*abs(float(cp[1]))
        crank=cyl_between((PX,py,Z),(cpx,cpy,Z),4.0); rod=cyl_between((cpx,cpy,Z),(sx,sy,Z),2.0); slider=box(sx-4,sx+4,sy-3,sy+3,Z-2.5,Z+2.5)
        for pn,sh in [('CRANK',crank),('ROD',rod),('SLIDER',slider)]:
            o=addfeat(doc,f'V194_{pn}_{lab}_{sw}',f'v194 {pn.lower()} {lab} @ {sw}deg review',sh); grp.addObject(o)
doc.recompute(); doc.saveAs(DOCOUT)
audit={
 'status':'FREECAD_V194_DYNAMIC_LINKAGE_AUDIT',
 'source_candidate':'migration/freecad/F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd',
 'v40_candidate_index':1,
 'local_mechanism_z_mm':Z,
 'rod_radius_mm':2.0,
 'crank_radius_section_mm':4.0,
 'slider_block_mm':[8.0,6.0,5.0],
 'sample_count':len(rows),
 'maximum_fixed_collision_mm3_per_side_sample':global_max_hit,
 'minimum_fuselage_containment_fraction_any_part':global_min_inside,
 'fixed_structure_collision_pass':global_max_hit<1e-6,
 'full_fuselage_containment_pass':global_min_inside>=0.999,
 'v40_min_linkage_moment_arm_mm':c['min_linkage_moment_arm_mm'],
 'moment_arm_gate_15mm_pass':c['min_linkage_moment_arm_mm']>=15.0,
 'servo_hardware_geometry_verified':False,
 'joint_hardware_verified':False,
 'mechanical_detail_release':False,
 'print_release':False,
 'flight_release':False,
 'samples':rows
}
with open(OUT,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps({k:audit[k] for k in ['status','sample_count','maximum_fixed_collision_mm3_per_side_sample','minimum_fuselage_containment_fraction_any_part','fixed_structure_collision_pass','full_fuselage_containment_pass','v40_min_linkage_moment_arm_mm','moment_arm_gate_15mm_pass']},indent=2))

