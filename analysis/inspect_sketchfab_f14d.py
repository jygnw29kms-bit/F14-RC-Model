import bpy, json, math, os
fbx=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/Sketchfab_Reference/F14D SuperTomcat/F14D_SUPERTOMCAT.fbx'
out=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/sketchfab_f14d_inventory.json'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
rows=[]
mins=[1e30]*3;maxs=[-1e30]*3
for o in bpy.context.scene.objects:
    if o.type!='MESH': continue
    vs=[o.matrix_world @ v.co for v in o.data.vertices]
    if not vs: continue
    mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
    for i in range(3): mins[i]=min(mins[i],mn[i]);maxs[i]=max(maxs[i],mx[i])
    rows.append({'name':o.name,'verts':len(o.data.vertices),'bounds_min':mn,'bounds_max':mx,'dims':[mx[i]-mn[i] for i in range(3)]})
rows=sorted(rows,key=lambda r:r['verts'],reverse=True)
res={'mesh_count':len(rows),'bounds_min':mins,'bounds_max':maxs,'dims':[maxs[i]-mins[i] for i in range(3)],'objects':rows}
os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w',encoding='utf-8').write(json.dumps(res,indent=2))
print(json.dumps({'mesh_count':res['mesh_count'],'dims':res['dims'],'top_objects':rows[:20]},indent=2))
