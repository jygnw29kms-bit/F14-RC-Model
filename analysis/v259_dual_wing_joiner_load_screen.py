import FreeCAD as App, Part, json, pathlib, math
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
d=App.openDocument(str(R/'migration/freecad/F14_v256_CONSOLIDATED_JOINER_STATE.FCStd'))
wd=json.load(open(R/'cad/fusion/F14TomcatRC/NASA_F14_basic_wing_v08.json',encoding='utf-8'))
sec=next(s for s in wd['sections'] if abs(s['wbl_in']-274.36816)<1e-5); rows=sec['ordinates_xc_upper_lower']; scale=1.1697428086486623; shift=187.59240693460868; fs0=93.0; chord=sec['trailing_edge_fs_in']-sec['leading_edge_fs_in']; seam_y=sec['wbl_in']*scale
def interp(x,idx):
 for a,b in zip(rows[:-1],rows[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]); return a[idx]+t*(b[idx]-a[idx])
 raise ValueError(x)
joiners=[]
for xc in [0.30,0.42]:
 yc=(interp(xc,1)+interp(xc,2))/2; x=(sec['leading_edge_fs_in']+xc*chord-fs0)*scale; z=(sec['reference_vertical_wl_in']+yc*chord)*scale-shift; jr={'xc':xc,'x_mm':x,'z_mm':z,'length_mm':40,'sides':[]}
 for lab,sgn in [('R',1),('L',-1)]:
  wing=d.getObject('WING_'+lab).Shape; st=App.Vector(x,sgn*(seam_y-20),z); ax=App.Vector(0,sgn,0); od=Part.makeCylinder(3,40,st,ax); cav=Part.makeCylinder(3.15,40,st,ax); jr['sides'].append({'side':lab,'tube_containment':od.common(wing).Volume/od.Volume,'cavity_containment':cav.common(wing).Volume/cav.Volume})
 joiners.append(jr)
sep=abs(joiners[1]['x_mm']-joiners[0]['x_mm']); rootM=19.221033999999996; pivot_y=125.20927023775282; tip_y=450.0; rem=tip_y-seam_y; full=tip_y-pivot_y; outerM=rootM*(rem/full)**2
I=math.pi/64*(6**4-4**4); stress=(outerM*1000/2)*3/I; allow=350.0; fos=allow/stress
out={'status':'V259_DUAL_WING_JOINER_LOAD_SCREEN','joiners':joiners,'center_spacing_mm':sep,'tube_OD_ID_mm':[6,4],'embed_each_side_mm':20,'load_screen':{'root_moment_8g_Nm':rootM,'pivot_to_tip_mm':full,'seam_to_tip_mm':rem,'uniform_spanload_scaled_seam_moment_Nm':outerM,'moment_share_per_tube_Nm':outerM/2,'tube_I_mm4':I,'outer_fiber_stress_MPa':stress,'candidate_allowable_MPa':allow,'candidate_FOS':fos,'material_values_verified':False},'gates':{'both_tubes_and_6p3_cavities_contained_ge_0p999':all(s['tube_containment']>=0.999 and s['cavity_containment']>=0.999 for j in joiners for s in j['sides']),'tube_centers_separated_gt_9mm':sep>9,'candidate_FOS_ge_3':fos>=3,'adhesive_bond_shear_verified':False,'torsion_split_verified':False,'tube_datasheet_verified':False,'proof_load':False,'print_release':False,'flight_release':False}}
(R/'analysis/v259_dual_wing_joiner_load_screen.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))