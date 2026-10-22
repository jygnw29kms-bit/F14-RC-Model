import FreeCAD as App, Part, json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).parent
SRC=ROOT/'analysis'/'original_front_sources'
FRAME=SRC/'ABCDEF_shared_frame_candidate.json'
XREG=SRC/'ABCDEF_FS_from_Navy_UPC_side_registration.json'
frame=json.loads(FRAME.read_text(encoding='utf-8'))
xreg=json.loads(XREG.read_text(encoding='utf-8'))
xmap={r['section']:r for r in xreg['sections']}
profiles={p['section']:p for p in frame['profiles']}

doc=App.newDocument('F14_ABCDEF_X_REGISTERED_LOCAL_Z_STUDY')
rows=[]
for sec in 'ABCDEF':
    p=profiles[sec]; xr=xmap[sec]
    x=float(xr['nose_relative_X_nominal_mm'])
    z0=float(p.get('axis_Z_candidate_mm',0.0))
    loop_shapes=[]; all_y=[]; all_z=[]
    for li,loop in enumerate(p['loops_xyz_candidate_mm']):
        pts=[App.Vector(x,float(q[1]),float(q[2])-z0) for q in loop]
        if len(pts)>=2:
            loop_shapes.append(Part.makePolygon(pts+[pts[0]]))
            all_y += [v.y for v in pts]; all_z += [v.z for v in pts]
    comp=Part.makeCompound(loop_shapes)
    o=doc.addObject('PartDesign::Feature',f'Section_{sec}_LocalZ')
    o.Label=f'Sektion {sec} – X registriert, Z lokal – STUDIE'
    o.Shape=comp
    # Unsicherheitsbereich in X als zwei vertikale Referenzlinien durch den lokalen Schnittbereich.
    xmin,xmax=[float(v) for v in xr['nose_relative_X_sensitivity_range_mm']]
    ymin,ymax=min(all_y),max(all_y); zmin,zmax=min(all_z),max(all_z)
    for tag,xx in [('Xmin',xmin),('Xmax',xmax)]:
        g=doc.addObject('PartDesign::Feature',f'Section_{sec}_{tag}')
        g.Label=f'{sec} {tag} Sensitivitätsgrenze – keine Kontur'
        g.Shape=Part.makeLine(App.Vector(xx,0,zmin),App.Vector(xx,0,zmax))
    rows.append({'section':sec,'X_nominal_mm':x,'X_range_mm':[xmin,xmax],
                 'FS_nominal_in':float(xr['FS_nominal_in']),'FS_range_in':[float(v) for v in xr['FS_sensitivity_range_in']],
                 'source_axis_Z_removed_mm':z0,'local_Y_range_mm':[ymin,ymax],'local_Z_range_mm':[zmin,zmax],
                 'loop_count':len(loop_shapes)})

# FS93-Nasenbezug und X-Achse als reine Referenzen.
all_x=[r['X_nominal_mm'] for r in rows]
axis=doc.addObject('PartDesign::Feature','LocalZ_Reference_Axis')
axis.Label='Lokale Z=0 Referenz – KEINE gemeinsame Aircraft-Waterline'
axis.Shape=Part.makeLine(App.Vector(min(all_x)-20,0,0),App.Vector(max(all_x)+20,0,0))
nose=doc.addObject('PartDesign::Feature','FS93_NoseReference')
nose.Label='FS93 / X=0 Nasenbezug – Engineering-Referenz'
nose.Shape=Part.makeLine(App.Vector(0,0,-50),App.Vector(0,0,50))

doc.recompute()
out=BASE/'F14_ABCDEF_X_REGISTERED_LOCAL_Z_STUDY.FCStd'
doc.saveAs(str(out)); App.closeDocument(doc.Name)
audit={
 'status':'ABCDEF_X_REGISTERED_LOCAL_Z_NATIVE_STUDY_NO_LOFT',
 'inputs':{str(FRAME.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(FRAME.read_bytes()).hexdigest(),
           str(XREG.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(XREG.read_bytes()).hexdigest()},
 'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'sections':rows,
 'gates':{'side_X_engineering_candidate_used':True,'common_aircraft_Z_registered':False,'loft_created':False,'master_changed':False,'production_release':False},
 'limits':['A-F verwenden die neue Navy/UPC-Seiten-X-Registrierung nur longitudinal.','Jede Sektion wurde um ihre bisherige candidate axis_Z auf lokales Z=0 rezentriert.','Das gemeinsame lokale Z=0 ist nur eine Darstellungsachse und ausdrücklich keine Aircraft-Waterline.','Keine Flaechenverbindung, kein Loft, keine Master-, Druck- oder Flugfreigabe.']}
(BASE/'freecad_ABCDEF_X_registered_local_Z_study_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(audit,indent=2,ensure_ascii=False))
