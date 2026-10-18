"""Fail-closed-Prüfung: Liegt die rekonstruierte Radom-Trennlinie im X-Bereich der vorhandenen Frontsektionen?"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEAM = ROOT / "analysis/independent_reviews/crank_localization_20261017/UPC_forward_radome_seam_traces.json"
FRAME = ROOT / "analysis/propulsion_source_silhouette_constraints_v134.json"
SECTIONS = ROOT / "analysis/original_front_sources/ABCDEF_shared_frame_candidate.json"
OUTPUT = ROOT / "analysis/radom_frontsektionen_screening_20261018.json"

seam = json.loads(SEAM.read_text(encoding="utf-8"))
frame = json.loads(FRAME.read_text(encoding="utf-8"))
sections = json.loads(SECTIONS.read_text(encoding="utf-8"))

scale = frame["common_scale_mm_per_pixel"]
e_px = frame["x_mapping"]["E_source_px"]
e_mm = frame["x_mapping"]["E_model_mm"]

def x_mm(px):
    return e_mm + (px - e_px) * scale

rows = []
all_x = []
for view in seam["views"]:
    xs = [x_mm(p["x_stroke_center_px"]) for p in view["points"]]
    all_x.extend(xs)
    rows.append({
        "ansicht": view["view"],
        "x_min_mm": min(xs),
        "x_max_mm": max(xs),
        "punkte": len(xs),
    })

section_x = [p["station_X_candidate_mm"] for p in sections["profiles"]]
first_section = min(section_x)
seam_max = max(all_x)
seam_min = min(all_x)
forward_gap = first_section - seam_max

overlap = not (seam_max < min(section_x) or seam_min > max(section_x))
status = "BLOCKIERT_KEINE_3D_PROJEKTION_AUF_ABCDEF_LOFT" if not overlap else "BEREICH_UEBERLAPPT"

report = {
    "status": status,
    "radom_trennlinie_x_mm": {"min": seam_min, "max": seam_max},
    "ansichten": rows,
    "frontsektionen_x_mm": {"min": min(section_x), "max": max(section_x)},
    "erste_frontsektion": sections["profiles"][section_x.index(first_section)]["section"],
    "abstand_radom_bis_erster_sektion_mm": forward_gap,
    "x_bereich_ueberlappt": overlap,
    "schlussfolgerung": (
        "Die aktuelle ABCDEF-Outer-Loft-Studie beginnt hinter der Radom-Trennlinie. "
        "Sie darf deshalb nicht als Zieloberfläche für eine 3D-Projektion der Radom-Trennlinie verwendet werden."
    ),
    "freigaben": {
        "3d_radom_trennlinie": False,
        "master_aendern": False,
        "produktionsgeometrie": False,
    },
    "naechster_schritt": (
        "Zuerst belastbare Nasen-/Radom-Querschnitte vor Sektion A erzeugen und deren gemeinsamen "
        "Koordinatenrahmen verifizieren; erst danach die 2D-Trennlinien auf eine 3D-Oberfläche projizieren."
    ),
}

OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))

if overlap:
    raise SystemExit(2)
