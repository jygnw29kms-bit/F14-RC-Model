import bpy, json, math, statistics, os
fbx=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/Sketchfab_Reference/F14D SuperTomcat/F14D_SUPERTOMCAT.fbx'
out=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/sketchfab_f14d_sweep_limit_geometry.json'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=fbx)
names=[n for n in bpy.data.objects.keys() if 'sweep_lim' in n]
rows=[]
for n in sorted(names):
 o=bpy.data.objects[n]
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 if not vs:continue
 mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
 cen=[sum(v[i] for v in vs)/len(vs) for i in range(3)]
 rows.append({'name':n,'verts':len(vs),'origin':list(o.matrix_world.translation),'centroid':cen,'bounds_min':mn,'bounds_max':mx,'dims':[mx[i]-mn[i] for i in range(3)]})
# summarize L/R centroids by family
res={'objects':rows}
open(out,'w',encoding='utf-8').write(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
