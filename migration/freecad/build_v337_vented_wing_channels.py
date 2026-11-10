"""F-14 v337 – Öffnung der vorhandenen v336-Innenkanäle zur Unterseite.

Entwicklungsstand. Lässt alle tragenden Anschlussbereiche unangetastet.
Keine STL-/Druck-/Flugfreigabe ohne erfolgreiche FreeCAD- und Slicer-Prüfung.
Aufruf: FreeCADCmd.exe migration/freecad/build_v337_vented_wing_channels.py
"""
import FreeCAD as App
import Part
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CAD = ROOT / "migration" / "freecad"
source = CAD / "F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd"
audit_source = CAD / "freecad_v336_internal_wing_channels_audit.json"
target = CAD / "F14_v337_VENTED_WING_CHANNEL_CANDIDATE.FCStd"
report_path = CAD / "freecad_v337_vented_wing_channels_audit.json"

source_audit = json.loads(audit_source.read_text(encoding="utf-8"))
existing = {(x["side"], x["segment"]): x for x in source_audit["rows"]}
doc_source = App.openDocument(str(source))
doc = App.newDocument("F14_v337_VENTED_WING_CHANNEL_CANDIDATE")
rows = []
for side in ("R", "L"):
    for segment in ("INNER", "OUTER"):
        name = "V336_WING_" + side + "_" + segment
        obj = doc_source.getObject(name)
        if obj is None or obj.Shape.isNull():
            raise RuntimeError("Missing v336 input: " + name)
        original = obj.Shape.copy()
        work = original.copy()
        channels = existing[(side, segment)]["accepted"]
        candidates = []
        for ch in channels:
            # 1.4-mm nominal vertical vent, joining a closed channel from below.
            # Bore ends within the pre-existing 4-mm channel (at its center).
            x = float(ch["x_mm"])
            y = float(ch["y_mm"]) + (7.5 if side == "R" else -7.5)
            z = float(ch["z_mm"])
            bottom = work.BoundBox.ZMin - 1.0
            cutter = Part.makeCylinder(
                0.7, max(0.01, z - bottom + 0.5),
                App.Vector(x, y, bottom), App.Vector(0, 0, 1)
            )
            cavity = work.common(cutter)
            proposed = work.cut(cutter)
            good = (
                cavity.Volume > 0.05
                and proposed.isValid()
                and len(proposed.Solids) == 1
                and 0.05 < work.Volume - proposed.Volume < 100.0
            )
            candidates.append({
                "x_mm": x, "y_mm": y, "channel_z_mm": z,
                "cut_volume_mm3": round(cavity.Volume, 4),
                "accepted": bool(good)
            })
            if good:
                work = proposed
        valid = work.isValid() and len(work.Solids) == 1
        if not valid:
            raise RuntimeError("Invalid wing after vent cut: " + name)
        out_obj = doc.addObject("PartDesign::Feature", "V337_WING_" + side + "_" + segment)
        out_obj.Shape = work
        out_obj.Label = "v337 experimental vented wing " + side + " " + segment
        bb0, bb1 = original.BoundBox, work.BoundBox
        same_bbox = all(
            abs(getattr(bb0, key) - getattr(bb1, key)) < 1e-3
            for key in ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax")
        )
        rows.append({
            "side": side, "segment": segment, "original_volume_mm3": round(original.Volume, 4),
            "remaining_volume_mm3": round(work.Volume, 4),
            "additional_removed_mm3": round(original.Volume - work.Volume, 4),
            "valid_single_solid": bool(valid),
            "bounds_unchanged": bool(same_bbox),
            "vent_candidates": candidates
        })
doc.recompute()
doc.saveAs(str(target))
report = {
    "classification": "V337_UNVALIDATED_VENTED_CHANNEL_DEVELOPMENT",
    "source": source.name,
    "note": "Vent acceptance tests only volume change and solid validity. They do not certify communication to inner channel, skin thickness, strength or printability.",
    "rows": rows,
    "geometry_sweep_verified": False,
    "slicer_verified": False,
    "structural_verified": False,
    "print_release": False,
    "flight_release": False,
    "sha256": hashlib.sha256(target.read_bytes()).hexdigest()
}
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"file": target.name, "rows": rows}, indent=2), flush=True)
