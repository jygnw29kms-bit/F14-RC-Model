# F-14 v338: Kanalanschluss und Carbonverbinder-Schutz

**11.11.2026 | GitHub-Arbeitsstand | FreeCAD-Ausführung noch offen**

Der Generator `migration/freecad/build_v338_verified_vent_connections.py` baut auf den vorhandenen Flügelkörpern v336 auf. Er bearbeitet ausschließlich die vier im v336-Prüfprotokoll erfassten Hohlkanäle der inneren Flügelsegmente. Die äußeren Segmente werden unverändert in das neue Arbeitsdokument übernommen.

## Neue technische Prüfgatter

1. **Echter Kanalanschluss:** Die geplante Unterseitenbohrung (Ø 1,4 mm) muss den ursprünglichen 4-mm-Hohlkanal über eine positive Boolean-Schnittmenge von wenigstens 0,5 mm³ erreichen. Ein bloßer Volumenverlust im Flügel reicht nicht.
2. **Carbonverbinder-Keepout:** Für alle sechs 8×6-mm-Rohranschlüsse gilt bei der Kanalöffnung ein radialer Prüf-Sicherheitsabstand von 3,0 mm zusätzlich zum 8,3-mm-Aufnahmebohrungsradius. Jede Volumenüberschneidung mit dem Keepout sperrt den Kandidaten.
3. **BRep-Gültigkeit:** Nach jedem Schnitt muss genau ein gültiger Volumenkörper übrig bleiben. Schnittvolumen zwischen 0,05 und 100 mm³ und unveränderte Bounding-Box werden vorausgesetzt.
4. **Fail closed:** Wenn auch nur eine vorgesehene Kanalöffnung scheitert oder nicht exakt vier Öffnungen akzeptiert werden, bricht der Generator ab. Es wird keine druckfertige Datei ausgegeben.

Der Generator schreibt bei Erfolg `migration/freecad/F14_v338_VENTED_WING_CHANNELS_REVIEW.FCStd` und `migration/freecad/freecad_v338_vented_wing_channels_audit.json`.

## Noch nicht nachgewiesen

Das Programm ist bislang **nur im GitHub-Branch gespeichert** und wurde noch **nicht in FreeCAD ausgeführt**, da Desktop Commander das Monatskontingent gemeldet hat. Auch nach erfolgreicher Ausführung sind die tatsächliche Mündung an der Außenhaut, lokale Resthautdicken, schäl-/biegebelastbare Carbonrohr-Anschlüsse, Flügel-Torsionssteifigkeit, P2S-Slicer-Schnittbild und reale Belastungsversuche ausdrücklich offen.

Das ist eine kontrollierte Weiterentwicklung der Entlüftung, **noch nicht die geforderte tragfähige hohle Flügelstruktur**. Eine vollständige Druck- oder Flugfreigabe wäre falsch.

## Ausführung nach Freigabe der lokalen CAD-Umgebung

Vom Repository-Verzeichnis aus:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe' 'migration\freecad\build_v338_verified_vent_connections.py'
```

Bei fehlender Ausgabe oder Geometriefehler: zuerst `F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd` und den v336-Auditstand prüfen, keine automatische Freigabe.
