import bpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
fbx=r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\Sketchfab_Reference\F14D SuperTomcat\F14D_SUPERTOMCAT.fbx"
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=fbx)
objs={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'}
scale=46.08423263874968; px=2.7169655013951837; py=-0.8123708930204749

def ray_world(o, origin_w, dir_w, maxdist=30):
 dg=bpy.context.evaluated_depsgraph_get(); oe=o.evaluated_get(dg); bvh=BVHTree.FromObject(oe,dg)
 inv=o.matrix_world.inverted(); ol=inv @ origin_w; dl=(inv.to_3x3() @ dir_w).normalized()
 loc,norm,idx,dist=bvh.ray_cast(ol,dl,maxdist)
 if loc is None:return None
 w=o.matrix_world @ loc; return [float(w.x),float(w.y),float(w.z)]
res={}
for name in ['vehicle#fuse_79','vehicle#wing_l_166']:
 o=objs[name]; hits=[]
 for origin,dir in [(Vector((px,py,10)),Vector((0,0,-1))),(Vector((px,py,-10)),Vector((0,0,1)))]:
  h=ray_world(o,origin,dir)
  if h:hits.append(h)
 res[name]=hits
f=objs['vehicle#fuse_79']; grid=[]
for dx in [-0.2,-0.1,0,0.1,0.2]:
 for dy in [-0.2,-0.1,0,0.1,0.2]:
  qx,qy=px+dx,py+dy; t=ray_world(f,Vector((qx,qy,10)),Vector((0,0,-1))); b=ray_world(f,Vector((qx,qy,-10)),Vector((0,0,1)))
  grid.append({'x':qx,'y':qy,'top_z':None if not t else t[2],'bottom_z':None if not b else b[2]})
out={'status':'SKETCHFAB_PIVOT_VERTICAL_SECTION','pivot_fbx_xy':[px,py],'scale_mm_per_unit':scale,'hits':res,'grid':grid}
fh=res['vehicle#fuse_79']; wh=res['vehicle#wing_l_166']
if fh and wh:
 fzs=sorted([p[2] for p in fh]); wzs=sorted([p[2] for p in wh]);out['relative']={'fuse_bottom_z':fzs[0],'wing_bottom_z':wzs[0],'fuse_minus_wing_bottom_units':fzs[0]-wzs[0],'fuse_minus_wing_bottom_model_mm':(fzs[0]-wzs[0])*scale}
print(json.dumps(out,indent=2));open(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\analysis\sketchfab_pivot_vertical_section.json",'w').write(json.dumps(out,indent=2))
