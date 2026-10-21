import FreeCAD as App, Part, json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).parent
SRC=ROOT/'analysis'/'original_front_sources'
files=[SRC/'C_axis_closure_sensitivity.json',SRC/'front_shared_frame_candidate.json',SRC/'front_sections_pixel_candidates.json',SRC/'C_side_projection_registration_screen.json']
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
sens,frame,pix,reg=[json.loads(p.read_text(encoding='utf-8')) for p in files]
case=next(c for c in sens['cases'] if c['threshold']==128 and c['offset_pixel']==0)
f=frame['profiles'][2]; p=pix['profiles'][2]
X=float(f['station_X_candidate_mm']); scale=float(f['isotropic_mm_per_section_pixel']); ax=p['source_section_axis_pixel']
vec=[App.Vector(X,(x-ax[0])*scale,float(f['axis_Z_candidate_mm'])+(ax[1]-y)*scale) for x,y in case['points_pixel']]
wire=Part.makePolygon(vec+[vec[0]]); face=Part.Face(wire)
assert face.isValid() and len(face.Wires)==1
ys=[v.y for v in vec]; zs=[v.z for v in vec]; ymin,ymax=min(ys),max(ys); zmin,zmax=min(zs),max(zs)
target=reg['interpolated_side_envelope_at_C']; target_center=float(target['center_Z_mm'])
neutral_center=(zmin+zmax)/2; dz=target_center-neutral_center
moved=face.copy(); moved.translate(App.Vector(0,0,dz)); assert moved.isValid()
mtop=max(v.z+dz for v in vec); mbottom=min(v.z+dz for v in vec)
doc=App.newDocument('F14_C_NEUTRAL_REGISTRATION_STUDY')
o=doc.addObject('PartDesign::Feature','C_Neutral_LegacyPlacement');o.Label='C neutral 128/0 – historischer Rahmen – STUDIE';o.Shape=face
t=doc.addObject('PartDesign::Feature','C_Neutral_CenterAligned');t.Label='C neutral – nur Z-Translation auf Seitenhüllenmitte – STUDIE';t.Shape=moved
for name,z,label in [('SideGuideTop',float(target['top_Z_mm']),'Interpolierte Seitenhülle oben'),('SideGuideBottom',float(target['bottom_Z_mm']),'Interpolierte Seitenhülle unten'),('SideGuideCenter',target_center,'Interpolierte Seitenhüllenmitte')]:
    g=doc.addObject('PartDesign::Feature',name);g.Label=label+' – keine Originalsektion';g.Shape=Part.makeLine(App.Vector(X,ymin,z),App.Vector(X,ymax,z))
doc.recompute()
out=BASE/'F14_C_NEUTRAL_REGISTRATION_STUDY.FCStd';doc.saveAs(str(out));App.closeDocument(doc.Name)
audit={
 'status':'C_NEUTRAL_REGISTRATION_NATIVE_STUDY_TRANSLATION_ONLY',
 'inputs':hashes,
 'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'station_X_mm':X,
 'legacy':{'area_mm2':face.Area,'top_Z_mm':zmax,'bottom_Z_mm':zmin,'center_Z_mm':neutral_center},
 'interpolated_side_envelope':target,
 'translation_only':{'delta_Z_mm':dz,'top_Z_mm':mtop,'bottom_Z_mm':mbottom,'top_residual_mm':mtop-float(target['top_Z_mm']),'bottom_residual_mm':mbottom-float(target['bottom_Z_mm']),'height_preserved_mm':mtop-mbottom},
 'limits':['Keine anisotrope oder isotrope Formskalierung angewendet.','Z-Translation richtet nur die Mittellage aus und ist keine Quellenfreigabe.','Seitenhüllen-Guides sind interpolierte Projektionsreferenzen, keine C-Stationskontur.','Master unveraendert; keine Produktions-, Druck- oder Flugfreigabe.'],
 'master_change_allowed':False,'production_release':False}
(BASE/'freecad_C_neutral_registration_study_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
