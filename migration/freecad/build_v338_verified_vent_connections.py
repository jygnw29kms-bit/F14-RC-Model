"""F-14 v338: fail-closed underwing vents for the existing v336 wing cavities.

Development CAD generator. No production or flight release.
Run under FreeCADCmd with the v336 FCStd and audit in the same checkout.
"""
from pathlib import Path
import hashlib
import json

import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]
CAD = ROOT / "migration" / "freecad"
SOURCE = CAD / "F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd"
SOURCE_AUDIT = CAD / "freecad_v336_internal_wing_channels_audit.json"
TARGET = CAD / "F14_v338_VENTED_WING_CHANNELS_REVIEW.FCStd"
REPORT = CAD / "freecad_v338_vented_wing_channels_audit.json"

VENT_RADIUS = 0.7
CONNECT_MIN_VOLUME_MM3 = 0.5
JOINER_X_MM = (542.0, 552.0, 562.0)
JOINER_Z_MM = -1.0
JOINER_Y_SEAM = 234.8834084849764
JOINER_RAD_MM = 4.15
KEEP_OUT_MM = 3.0
JOINER_LENGTH_MM = 40.0


def fail(reason):
    raise RuntimeError("v338 rejected: " + reason)


def shape_valid(sh):
    return bool(not sh.isNull() and sh.isValid() and len(sh.Solids) == 1)


def joiner_keepout(side, x):
    sign = 1 if side == "R" else -1
    return Part.makeCylinder(
        JOINER_RAD_MM + KEEP_OUT_MM,
        JOINER_LENGTH_MM,
        App.Vector(x, sign * (JOINER_Y_SEAM - 20.0), JOINER_Z_MM),
        App.Vector(0, sign, 0),
    )


def geometry_bounds_equal(a, b, tol=1e-3):
    attrs = ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax")
    return all(abs(getattr(a.BoundBox, k) - getattr(b.BoundBox, k)) < tol for k in attrs)


def inner_channel_volume(ch, side):
    # Exact axis direction and origin match the v336 construction.
    sign = 1 if side == "R" else -1
    return Part.makeCylinder(
        float(ch["radius_mm"]),
        float(ch["length_mm"]),
        App.Vector(float(ch["x_mm"]), float(ch["y_mm"]), float(ch["z_mm"])),
        App.Vector(0, sign, 0),
    )


def build():
    audit = json.loads(SOURCE_AUDIT.read_text(encoding="utf-8"))
    if audit.get("classification") != "EXPERIMENTAL_INTERNAL_CHANNELS":
        fail("unexpected v336 source audit")
    records = {(r["side"], r["segment"]): r for r in audit["rows"]}
    src = App.openDocument(str(SOURCE))
    target = App.newDocument("F14_v338_VENTED_WING_CHANNELS_REVIEW")
    rows = []
    accepted_total = 0
    for side in ("R", "L"):
        sign = 1 if side == "R" else -1
        for segment in ("INNER", "OUTER"):
            key = (side, segment)
            old = src.getObject("V336_WING_" + side + "_" + segment)
            if old is None or not shape_valid(old.Shape):
                fail("invalid source wing " + str(key))
            wing = old.Shape.copy()
            work = wing.copy()
            channels = records[key]["accepted"]
            tests = []
            for ch in channels:
                cavity = inner_channel_volume(ch, side)
                cx, cy, cz = (float(ch["x_mm"]), float(ch["y_mm"]), float(ch["z_mm"]))
                # An accessible vent enters at the global underside and reaches
                # the centre of the existing spanwise channel.
                mid_y = cy + sign * float(ch["length_mm"]) / 2.0
                z_start = wing.BoundBox.ZMin - 1.0
                height = cz - z_start + 0.5
                if height <= 0.0:
                    fail("invalid vent height " + str(key))
                vent = Part.makeCylinder(
                    VENT_RADIUS, height,
                    App.Vector(cx, mid_y, z_start),
                    App.Vector(0, 0, 1),
                )
                # The prior solid wing contains the already-carved void, so
                # intersect the proposed vent with the *recorded void cylinder*.
                connected_volume = vent.common(cavity).Volume
                keepout_overlap = sum(
                    vent.common(joiner_keepout(side, pos)).Volume
                    for pos in JOINER_X_MM
                )
                cut_volume = work.common(vent).Volume
                next_shape = work.cut(vent)
                good = (
                    connected_volume >= CONNECT_MIN_VOLUME_MM3
                    and keepout_overlap < 1e-4
                    and 0.05 < cut_volume < 100.0
                    and shape_valid(next_shape)
                    and geometry_bounds_equal(wing, next_shape)
                )
                test = {
                    "channel_x_mm": cx, "channel_mid_y_mm": round(mid_y, 4),
                    "channel_z_mm": cz, "vent_d_mm": VENT_RADIUS * 2.0,
                    "connected_void_overlap_mm3": round(connected_volume, 4),
                    "joiner_keepout_overlap_mm3": round(keepout_overlap, 6),
                    "cut_solid_volume_mm3": round(cut_volume, 4),
                    "accepted": bool(good),
                }
                tests.append(test)
                if not good:
                    fail("failed vent gate " + json.dumps({"key": key, "test": test}))
                work = next_shape
                accepted_total += 1
            if not shape_valid(work):
                fail("invalid final wing " + str(key))
            obj = target.addObject("PartDesign::Feature", "V338_WING_" + side + "_" + segment)
            obj.Label = "v338 vented experimental wing " + side + " " + segment
            obj.Shape = work
            rows.append({
                "side": side, "segment": segment, "vents": tests,
                "valid_one_solid": True, "bbox_unchanged": geometry_bounds_equal(wing, work),
                "removed_volume_mm3": round(wing.Volume - work.Volume, 4),
            })
            print("v338:", side, segment, len(tests), "vents", flush=True)
    if accepted_total != 4:
        fail("expected four inner-wing vents, found " + str(accepted_total))
    target.recompute()
    target.saveAs(str(TARGET))
    result = {
        "classification": "V338_GEOMETRY_REVIEW_ONLY",
        "source": SOURCE.name,
        "checked_joiner_keepout_mm": KEEP_OUT_MM,
        "accepted_vents": accepted_total,
        "rows": rows,
        "channel_connected_by_positive_boolean_overlap": True,
        "outer_skin_local_thickness_verified": False,
        "cavity_surface_opening_topology_verified": False,
        "slicer_verified": False,
        "static_strength_verified": False,
        "fatigue_verified": False,
        "print_release": False,
        "flight_release": False,
        "cad_sha256": hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    }
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"created": TARGET.name, "accepted_vents": accepted_total}), flush=True)


if __name__ == "__main__":
    build()
