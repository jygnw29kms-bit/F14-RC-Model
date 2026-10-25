import bpy,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
fbx=r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\Sketchfab_Reference\F14D SuperTomcat\F14D_SUPERTOMCAT.fbx"
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=fbx)
objs={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'};scale=46.08423263874968;nose_y=-11.756381034851074

def makebvh(o):
 dg=bpy.context.evaluated_depsgraph_get();oe=o.evaluated_get(dg);return BVHTree.FromObject(oe,dg)
def ray(o,bvh,x,y,up=False):
 origin=Vector((x,y,-10 if up else 10));direction=Vector((0,0,1 if up else -1));inv=o.matrix_world.inverted();ol=inv@origin;dl=(inv.to_3x3()@direction).normalized();loc,_,_,_=bvh.ray_cast(ol,dl,30)
 if loc is None:return None
 w=o.matrix_world@loc;return float(w.z)
f=objs['vehicle#fuse_79'];w=objs['vehicle#wing_l_166'];bf=makebvh(f);bw=makebvh(w)
xs=[482.346,488.346,496.346,504.346,512.346,520.346,526.346];ys=[105.209,115.0,125.209,130.826,137.209,148.826]
rows=[]
for xm in xs:
 for ym in ys:
  xf=ym/scale; yf=nose_y+xm/scale; fb=ray(f,bf,xf,yf,True); wb=ray(w,bw,xf,yf,True)
  rows.append({'model_x_mm':xm,'model_abs_y_mm':ym,'fbx_x':xf,'fbx_y':yf,'fuse_bottom_z':fb,'wing_bottom_z':wb,'fuse_minus_wing_model_mm':None if fb is None or wb is None else (fb-wb)*scale})
out={'status':'SKETCHFAB_GLOVE_GRID_SECONDARY_REFERENCE','scale_mm_per_fbx_unit':scale,'rows':rows,'limits':['secondary visual/reference mesh only','span-normalized and nose-min longitudinal registration','not production OML']}
open(r"C:\Users\dezen\Desktop\JL1976\F14-Tomcat\F14-RC-Model\analysis\sketchfab_glove_grid_compare.json",'w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
