import FreeCAD as App, Part, json, os, math
BASE=r'C:/Users/dezen/Desktop/F14-RC-Model'
SRC=os.path.join(BASE,'migration','freecad','F14_CURRENT_FULL_VIEW_v192.FCStd')
KIN=os.path.join(BASE,'analysis','F14_sweep_linkage_kinematics_v40.json')
OUT=os.path.join(BASE,'migration','freecad','freecad_v193_linkage_search_audit.json')
DOCOUT=os.path.join(BASE,'migration','freecad','F14_CURRENT_FULL_VIEW_v193_LINKAGE_CANDIDATE.FCStd')
SHIFT=187.59240693460868

def box(x0,x1,y0,y1,z0,z1):
    return Part.makeBox(x1-x0,y1-y0,z1-z0,App.Vector(x0,y0,z0))

def ivol(a,b):
    try:
        s=a.common(b)
        return s.Volume if (not s.isNull()) else 0.0
    except Exception:
        return 0.0

def addfeat(doc,name,label,shape):
    o=doc.addObject('PartDesign::Feature',name); o.Label=label; o.Shape=shape; return o

with open(KIN,encoding='utf-8') as f: kin=json.load(f)
c=kin['top_candidates'][1]
sy=float(c['slider_attach_y_mm']); xmin=float(c['slider_x_min_mm'])-4.0; xmax=float(c['slider_x_max_mm'])+4.0
legacy_zs=[188.0,192.0,196.0,200.0,204.0]
# v43 fixed envelopes translated into the v191/v192 common local datum.
legacy={
 'CF_FRONT_LOWER': (594.1323905812828,600.1323905812828,-72,72,180.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'RISER_FRONT_R': (591.1323905812828,603.1323905812828,68,78,175.09240693460868-SHIFT,187.09240693460868-SHIFT),
 'RISER_FRONT_L': (591.1323905812828,603.1323905812828,-78,-68,175.09240693460868-SHIFT,187.09240693460868-SHIFT),
 'CF_REAR_LOWER': (626.1323905812828,632.1323905812828,-72,72,179.09240693460868-SHIFT,185.09240693460868-SHIFT),
 'RISER_REAR_R': (623.1323905812828,635.1323905812828,68,78,175.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'RISER_REAR_L': (623.1323905812828,635.1323905812828,-78,-68,175.09240693460868-SHIFT,186.09240693460868-SHIFT),
 'CF_FRONT_UPPER': (594.1323905812828,600.1323905812828,-72,72,196.09240693460868-SHIFT,202.0924069346087-SHIFT),
 'CF_REAR_UPPER': (626.1323905812828,632.1323905812828,-72,72,196.09240693460868-SHIFT,202.0924069346087-SHIFT),
 'SERVO_SERVICE': (517.1323905812828,565.1323905812828,-13.5,13.5,187.59240693460868-SHIFT,231.59240693460868-SHIFT),
}
obs={k:box(*v) for k,v in legacy.items()}
doc=App.openDocument(SRC)
fuse=doc.getObject('FUSELAGE_CURRENT').Shape
current_obs={}
for nm in ['BATTERY_TRAY_v165','INLET_EDF_R','INLET_EDF_L','WINGBOX_REF']:
    o=doc.getObject(nm)
    if o and hasattr(o,'Shape') and not o.Shape.isNull(): current_obs[nm]=o.Shape
rows=[]
for width in [6.0,8.0,10.0,12.0]:
  for absz in legacy_zs:
    z=absz-SHIFT; t=5.0
    sides=[]; total_hit=0.0; min_inside=1.0
    for lab,sgn in [('R',1),('L',-1)]:
      yc=sgn*sy
      sh=box(xmin,xmax,yc-width/2,yc+width/2,z-t/2,z+t/2)
      vol=sh.Volume
      inside=ivol(sh,fuse)/vol if vol else 0.0
      hits={k:ivol(sh,s) for k,s in obs.items()}
      hits.update({k:ivol(sh,s) for k,s in current_obs.items()})
      hit=sum(hits.values())
      sides.append({'side':lab,'inside_fuselage_fraction':inside,'collision_mm3':hit,'hits_mm3':hits})
      total_hit+=hit; min_inside=min(min_inside,inside)
    rows.append({'strip_width_mm':width,'z_abs_legacy_mm':absz,'z_local_mm':z,'min_inside_fuselage_fraction':min_inside,'total_collision_mm3':total_hit,'sides':sides})
# Rank for zero collision first, then containment, then narrower/central plane.
rows.sort(key=lambda r:(0 if r['total_collision_mm3']<1e-6 else 1,-r['min_inside_fuselage_fraction'],r['strip_width_mm'],abs(r['z_abs_legacy_mm']-196.0)))
best=rows[0]
# Build candidate geometry into a new copy of current v192 document.
grp=doc.addObject('App::DocumentObjectGroup','SWEEP_LINKAGE_V193'); grp.Label='04 SWEEP LINKAGE v193 CANDIDATE / NOT RELEASED'
for lab,sgn in [('R',1),('L',-1)]:
    yc=sgn*sy; w=best['strip_width_mm']; z=best['z_local_mm']; t=5.0
    sh=box(xmin,xmax,yc-w/2,yc+w/2,z-t/2,z+t/2)
    o=addfeat(doc,'SWEEP_SLIDER_'+lab,'v193 split sweep slider '+lab,sh); grp.addObject(o)
# Add legacy servo envelope for visual reference only.
servo=addfeat(doc,'SWEEP_SERVO_SERVICE_REF','v35 sweep servo service envelope reference',obs['SERVO_SERVICE']); grp.addObject(servo)
doc.recompute(); doc.saveAs(DOCOUT)
audit={
 'status':'FREECAD_V193_SPLIT_SLIDER_SEARCH',
 'source_master':'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd',
 'v40_candidate_index':1,
 'slider_x_range_mm':[xmin,xmax],
 'slider_attach_abs_y_mm':sy,
 'legacy_full_plate_collision_cause':'v43 full plate spanned both side sliders and crossed central servo service envelope',
 'tested_strip_widths_mm':[6,8,10,12],
 'tested_legacy_absolute_planes_mm':legacy_zs,
 'datum_shift_mm':-SHIFT,
 'best':best,
 'zero_collision_candidate_count':sum(1 for r in rows if r['total_collision_mm3']<1e-6),
 'v40_min_linkage_moment_arm_mm':c['min_linkage_moment_arm_mm'],
 'v40_slider_travel_mm':c['slider_travel_mm'],
 'kinematics_changed':False,
 'servo_geometry_frozen':False,
 'dynamic_linkage_collision_verified':False,
 'print_release':False,
 'flight_release':False,
 'all_candidates':rows
}
with open(OUT,'w',encoding='utf-8') as f: json.dump(audit,f,indent=2)
print(json.dumps({k:audit[k] for k in ['status','zero_collision_candidate_count','v40_min_linkage_moment_arm_mm','v40_slider_travel_mm','best']},indent=2))
