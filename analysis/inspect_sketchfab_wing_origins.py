import bpy, json, math
fbx=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/Sketchfab_Reference/F14D SuperTomcat/F14D_SUPERTOMCAT.fbx'
out=r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/sketchfab_f14d_wing_origins.json'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=fbx)
names=['vehicle#wing_l_166','vehicle#wing_r_180']
rows=[]
for n in names:
 o=bpy.data.objects[n]
 origin=o.matrix_world.translation.copy()
 vs=[o.matrix_world @ v.co for v in o.data.vertices]
 mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
 # nearest world vertex to object origin
 near=min(vs,key=lambda v:(v-origin).length)
 rows.append({'name':n,'origin_world':list(origin),'location':list(o.location),'rotation_euler':list(o.rotation_euler),'scale':list(o.scale),'bounds_min':mn,'bounds_max':mx,'nearest_vertex_to_origin':list(near),'nearest_distance':(near-origin).length,'parent':o.parent.name if o.parent else None})
# model bounds and normalization
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
allvs=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
mn=[min(v[i] for v in allvs) for i in range(3)];mx=[max(v[i] for v in allvs) for i in range(3)]
span=mx[0]-mn[0];scale900=900/span
res={'model_bounds_min':mn,'model_bounds_max':mx,'model_dims':[mx[i]-mn[i] for i in range(3)],'scale_mm_per_fbx_unit_for_900_span':scale900,'wings':rows}
open(out,'w',encoding='utf-8').write(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
