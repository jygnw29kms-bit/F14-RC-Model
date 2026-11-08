"""Exportiert nur nach bestandener Mesh-Geometrieprüfung den v326-EDF-Übergang.
Entwicklungsstand, keine Druck-/Flugfreigabe."""
import FreeCAD as App
import pathlib, json, hashlib
R=pathlib.Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model")
src=R/"migration/freecad/F14_v326_PRINTABLE_TRANSITION_WALL_MESH.FCStd"
out=R/"manufacturing/development/v326_transition_wall"
out.mkdir(parents=True,exist_ok=True)
doc=App.openDocument(str(src))
report={"source":src.name,"classification":"engineering development - NOT RELEASED","parts":[]}
all_pass=True
for side in ("R","L"):
    obj=doc.getObject("V326_TRANSITION_WALL_"+side)
    if obj is None: raise RuntimeError("Missing v326 mesh "+side)
    mesh=obj.Mesh
    pairs=mesh.getSelfIntersections()
    ok=bool(mesh.isSolid() and not mesh.hasNonManifolds() and len(pairs)==0)
    entry={"side":side,"facets":mesh.CountFacets,"is_solid":bool(mesh.isSolid()),"has_nonmanifolds":bool(mesh.hasNonManifolds()),"self_intersections":len(pairs),"geometry_gate_pass":ok}
    if ok:
        dest=out/("F14_v326_EDF_transition_"+side+"_DEV_ONLY.stl")
        mesh.write(str(dest))
        entry["stl"]=dest.name
        entry["bytes"]=dest.stat().st_size
        entry["sha256"]=hashlib.sha256(dest.read_bytes()).hexdigest()
    else:
        all_pass=False
    report["parts"].append(entry)
report["geometry_gate_pass"]=all_pass
report["slicer_verified"]=False
report["print_release"]=False
report["flight_release"]=False
(out/"GEOMETRY_AUDIT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2),flush=True)
if not all_pass: raise RuntimeError("v326 geometry gate failed, STL export blocked")
