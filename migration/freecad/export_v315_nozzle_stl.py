import FreeCAD as App, Mesh, pathlib, json, hashlib
R=pathlib.Path(r'C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model')
src=R/'migration/freecad/F14_v315_PRINTABLE_VARIABLE_NOZZLE_WALL.FCStd'
outdir=R/'manufacturing/candidates/nozzle_slice_trial_20261103'; outdir.mkdir(parents=True,exist_ok=True)
d=App.openDocument(str(src)); rows=[]
for side in ('R','L'):
    ob=d.getObject('V315_NOZZLE_WALL_'+side); p=outdir/f'F14_V315_NOZZLE_WALL_{side}_NOT_RELEASED.stl'; Mesh.export([ob],str(p)); rows.append({'side':side,'file':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(outdir/'stl_export_audit.json').write_text(json.dumps({'status':'V315_STL_EXPORT_CANDIDATE','source':src.name,'files':rows,'print_release':False},indent=2),encoding='utf-8'); print(json.dumps(rows,indent=2))