from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,hashlib
O=Path(__file__).parent;R=O.parent;f=R/'migration/freecad/F14_CURRENT_FULL_VIEW_v192.FCStd';z=zipfile.ZipFile(f);assert z.testzip() is None
root=E.fromstring(z.read('Document.xml'));rows=[]
for obj in root.findall('./ObjectData/Object'):
 name=obj.attrib['name'];shape=obj.find("./Properties/Property[@name='Shape']")
 if shape is None:continue
 label=obj.find("./Properties/Property[@name='Label']/String");label=label.attrib['value'] if label is not None else name
 material=obj.find("./Properties/Property[@name='ShapeMaterial']/PropertyMaterial")
 role='Alternative Schwenklage derselben Fluegel, nicht zusaetzliches Flugzeugbauteil' if '_SWEEP_' in name else 'Referenz-/Huellenobjekt, Masse nicht aus Vollvolumen ableiten' if any(s in name for s in ['_REF','_ENV','HOLE_REFS']) else 'Baugruppen-/Geometriekandidat, physische Massendefinition offen'
 rows.append(dict(name=name,label=label,material_uuid=material.attrib.get('uuid') if material is not None else None,mass_role_screen=role,measured_mass_g=None,current_mass_assignment_verified=False))
uuids=sorted(set(r['material_uuid'] for r in rows if r['material_uuid']));alternatives=[r['name'] for r in rows if '_SWEEP_' in r['name']]
assert len(alternatives)==6
r=dict(status='V192_OBJEKTROLLEN_FUER_MASSENAUFROLLUNG_STATISCH_GEPRUEFT',native_archive_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),shape_object_count=len(rows),material_uuid_count=len(uuids),material_uuids=uuids,alternative_wing_pose_objects=alternatives,rows=rows,limits=['Document.xml statisch gelesen, keine neue native Geometrieauswertung.','Material-UUID allein belegt keine bauteilspezifische Dichte, Druckstruktur oder gewogene Masse; referenzierte Bibliothek hier nicht validiert.','Sechs alternative Fluegelposen duerfen nicht als sechs zusaetzliche reale Fluegel in ein AUW eingehen.','Auch verbleibende Objekte enthalten Referenzen/Huellen; keine pauschale Volumen-Dichte-Summe.','Keine CAD-/Masteraenderung oder Produktionsfreigabe.'],production_release=False)
(O/'v192_mass_object_roles_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(len(rows),len(uuids),len(alternatives))
