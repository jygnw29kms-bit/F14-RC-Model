from pathlib import Path
import FreeCAD as App,json,hashlib
R=Path(__file__).resolve().parents[2];f=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';before=hashlib.sha256(f.read_bytes()).hexdigest();d=App.openDocument(str(f));names=['FUSELAGE_CURRENT','WING_R','WING_L','STABILATOR_L','STABILATOR_R','VTAIL_L','VTAIL_R','VENTRAL_L','VENTRAL_R','INLET_EDF_R','INLET_EDF_L'];rows=[]
for name in names:
 o=d.getObject(name);assert o is not None;sh=o.Shape
 rows.append(dict(name=name,label=o.Label,valid=sh.isValid(),solid_count=len(sh.Solids),face_count=len(sh.Faces),surface_area_mm2=sh.Area,geometric_solid_volume_mm3=sh.Volume))
App.closeDocument(d.Name);assert before==hashlib.sha256(f.read_bytes()).hexdigest()
r=dict(status='V192_REFERENZGEOMETRIE_FLAECHEN_VOLUMEN_NATIVE_READ_ONLY',source_sha256=before,rows=rows,total_surface_area_mm2=sum(v['surface_area_mm2'] for v in rows),limits=['Geometrische Flaeche umfasst vorhandene End-/Anschlussflaechen, keine exklusiv bestimmte Druckhaut.','Vollvolumen ist keine Schalen-/Slicermasse; keine Dichtezuordnung oder AUW-Summe.','Geometrie/Originalhautregistrierung unverifiziert; source-datei nicht gespeichert oder geaendert.','Keine Produktionsfreigabe.'],production_release=False)
(R/'analysis/v192_surface_volume_mass_basis_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print([(v['name'],v['surface_area_mm2'],v['geometric_solid_volume_mm3']) for v in rows])
