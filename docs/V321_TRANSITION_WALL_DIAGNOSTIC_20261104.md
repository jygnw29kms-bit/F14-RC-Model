# v321 Übergangswand: Diagnose vom 04.11.2026

**Status:** WIP, keine Druck- oder Flugfreigabe. Geprüfter Basispunkt bleibt `main` bei v320 (`96d7129`).

## Verifizierte Befunde

- v321-Archiv enthält zwei geschlossene Meshes. Der nachträgliche FreeCAD-Lesetest meldet je Mesh `isSolid=True` und `hasNonManifolds=False`. Das ersetzt **keinen** Selbstschnitt-Test.
- Vorhandener v321-Audit: nominelle Wandstärke 0,8 mm; kleinster Innenquerschnitt etwa 0,929 FSA; X/Z-Routing bleibt im Grenzwert. Der ursprüngliche Selbstschnittzähler `-1` ist **nur ein Platzhalter** und keine bestandene Prüfung.
- Reproduzierbare explorative Facettenstichprobe (jede 12. Facette; berücksichtigt auch Innenwand) findet 9 Keepout-Treffer rechts bei ungefähr X=758–784 mm und 2 links bei X=758–760 mm.
- Frühere Vollprüfung des 48-Punkt-Kandidaten fand 140 Selbstüberschneidungen vor der letzten axialen Verdichtung. Für die aktuelle 29-Stationen-Datei ist der Volltest noch offen.
- Separater Keepout-Volumentest an X=758,5 / 766,5 / 778,5 / 790,5 / 806,5 mm: je Seite zwei getrennte Keepout-Solids, planare Face-Wire-Anzahlen jeweils 1. Keine Hinweise auf irrtümlich gefüllte Innenlöcher.

## Ursache und nächster Gate

Der Generator schneidet an einzelnen X-Stationen einen zulässigen 2D-Freiraum aus dem v310-Keepout. Zwischen den Stationen interpolierte Wanddreiecke werden dadurch **nicht** automatisch kollisionsfrei. Der nächste Generator muss Außen- und Innenwand **zwischen** allen Stationen mit dem echten 3D-Keepout prüfen und bei Kollision lokal zurückziehen, adaptiv zusätzliche Stationen hinzufügen oder die Sektion neu führen. Nur die 2D-Sektionsfreigabe zu prüfen ist unzureichend.

**Freigabe bleibt gesperrt**, bis ein vollständiger Selbstschnitt-Test, volumetrischer Keepout/OML-Test und Slicer-Probe erfolgreich sind.

Diagnosedaten: `migration/freecad/freecad_v321_keepout_location_diagnostic.json`. Scanner: `migration/freecad/diagnose_v321_keepout.py` (Stichprobe, kein Freigabetest).
