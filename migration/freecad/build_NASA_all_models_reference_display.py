from pathlib import Path
import json,hashlib
import FreeCAD as App,Part
R=Path(__file__).resolve().parents[2];O=R/'analysis/original_front_sources';B=Path(__file__).parent
out=B/'NASA_ALL_MODELS_OPEN_REFERENCE_DISPLAY.FCStd';assert not out.exists()
inv=json.loads((O/'NASA_all_models_reference_study_inventory.json').read_text(encoding='utf-8'));doc=App.newDocument('NASA_ALL_MODELS_OPEN_REFERENCE_DISPLAY');rows=[];hashes={}
for entry in inv['rows']:
 f=O/entry['file'];h=hashlib.sha256(f.read_bytes()).hexdigest();assert h==entry['sha256'];hashes[f.name]=h;j=json.loads(f.read_text(encoding='utf-8'))
 for index,row in enumerate(j['rows']):
  model=row.get('model',entry['models'][0]);x=row['x_source'];points=[App.Vector(x-93,y,z-131.45) for y,z in row['points_YZ_source']]
  shape=Part.makePolygon(points);assert shape.isValid() and not shape.isClosed() and len(shape.Solids)==0 and len(shape.Faces)==0
  obj=doc.addObject('PartDesign::Feature','MODEL_'+str(model)+'_SECTION_'+str(len(rows)+1));obj.Shape=shape
  obj.addProperty('App::PropertyString','CoordinateMeaning');obj.CoordinateMeaning='1 source unit = 1 display mm; NOT physical aircraft scale; X-93, Z-131.45'
  obj.addProperty('App::PropertyBool','ProductionRelease');obj.ProductionRelease=False
  obj.addProperty('App::PropertyString','SourceBoundarySide');obj.SourceBoundarySide=str(row.get('source_boundary_side') or '')
  rows.append(dict(model=model,x_source=x,source_file=f.name,source_row=index,boundary_side=row.get('source_boundary_side'),edges=len(shape.Edges),valid=shape.isValid(),closed=shape.isClosed(),solids=len(shape.Solids),faces=len(shape.Faces),first_display_xyz=list(points[0]),last_display_xyz=list(points[-1])))
assert len(rows)==35;doc.recompute();doc.saveAs(str(out));App.closeDocument(doc.Name)
for name,h in hashes.items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==h
report=dict(status='35_OFFENE_QUELLENREFERENZEN_8_MODELLE_NATIV_ERZEUGT',inputs_sha256=hashes,rows=rows,output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),limits=['Darstellungskoordinaten, kein physischer RC-Massstab oder UPC-Datum.','Nur offene Halbsektionspolylinien; keine Spiegelung, Flaeche, Verbindung, Loft oder geschlossene Haut.','697links/rechts und Modellgrenzen bleiben getrennte Objekte; keine Glattung.','Teilvalidiertes vereinfachtes NASA-Quellenmodell, keine Herstellerhaut-/Produktionsfreigabe.'],production_release=False)
(B/'NASA_all_models_native_reference_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('35open reference wires, 0 faces, 0 solids')
