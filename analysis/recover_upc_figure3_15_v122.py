"""Recover and verify the exact UPC Figure 3.15 raster used by the D/E/F source registrations.

This script intentionally performs provenance recovery only. It does not infer an aircraft
waterline or release CAD geometry.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

EXPECTED_PDF_SHA256 = "49393a9ef94e1952eb361fc53e202b5fc4431445f280ba3d6f1c1c0e768996d6"
EXPECTED_IMAGE_SHA256 = "63413c7958648165ca381ebda27ef31a4d6aabed725b84d3e2f804da5bafb5b4"
PDF_PAGE_ONE_BASED = 31
EXPECTED_XREF = 92
EXPECTED_SIZE = (2113, 2953)

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "references" / "UPC_F14_Structure_Report.pdf"
OUTPUT_PATH = ROOT / "references" / "UPC_Figure3_15_source_exact.png"
AUDIT_PATH = ROOT / "analysis" / "upc_figure3_15_recovery_v122.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run() -> dict:
    import pymupdf

    if not PDF_PATH.exists():
        raise FileNotFoundError(PDF_PATH)
    pdf_sha = sha256_file(PDF_PATH)
    if pdf_sha != EXPECTED_PDF_SHA256:
        raise RuntimeError(f"UPC PDF hash mismatch: {pdf_sha}")

    doc = pymupdf.open(PDF_PATH)
    page_index = PDF_PAGE_ONE_BASED - 1
    if page_index < 0 or page_index >= len(doc):
        raise RuntimeError("UPC PDF page index out of range")

    page = doc[page_index]
    images = page.get_images(full=True)
    candidates = []
    recovered = None
    for image in images:
        xref = int(image[0])
        extracted = doc.extract_image(xref)
        raw = extracted["image"]
        record = {
            "xref": xref,
            "width": int(extracted["width"]),
            "height": int(extracted["height"]),
            "ext": extracted["ext"],
            "sha256": sha256_bytes(raw),
            "bytes": len(raw),
        }
        candidates.append(record)
        if record["sha256"] == EXPECTED_IMAGE_SHA256:
            recovered = (record, raw)

    if recovered is None:
        raise RuntimeError("Exact Figure 3.15 raster not found on UPC PDF page 31")

    record, raw = recovered
    if record["xref"] != EXPECTED_XREF:
        raise RuntimeError(f"Unexpected image xref: {record['xref']}")
    if (record["width"], record["height"]) != EXPECTED_SIZE:
        raise RuntimeError("Exact raster dimensions changed")

    OUTPUT_PATH.write_bytes(raw)
    output_sha = sha256_file(OUTPUT_PATH)
    if output_sha != EXPECTED_IMAGE_SHA256:
        raise RuntimeError("Recovered output hash mismatch")

    audit = {
        "status": "V122_EXACT_UPC_FIGURE3_15_RECOVERY_REPRODUCIBLE",
        "pdf": str(PDF_PATH.relative_to(ROOT)).replace("\\", "/"),
        "pdf_sha256": pdf_sha,
        "pdf_page_one_based": PDF_PAGE_ONE_BASED,
        "page_image_candidates": candidates,
        "selected_xref": record["xref"],
        "selected_size_px": [record["width"], record["height"]],
        "output": str(OUTPUT_PATH.relative_to(ROOT)).replace("\\", "/"),
        "output_sha256": output_sha,
        "matches_historical_DE_F_registration_source": True,
        "absolute_aircraft_Z_verified": False,
        "CAD_installation_allowed": False,
        "print_release": False,
        "flight_release": False,
    }
    AUDIT_PATH.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    return audit


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
