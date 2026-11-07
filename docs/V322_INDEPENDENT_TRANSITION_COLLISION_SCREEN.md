# v322 unabhängiger Stichproben-Check der v321-Übergangswand

- Der Prüfer lädt das gespeicherte FreeCAD-v321-Mesh unabhängig vom Generator und prüft gegen die ursprünglichen v310-Keepout-BReps sowie die v312-Heckhülle.
- Keepout: jede 12. Mesh-Facette, Mittelpunkt; bei jeder 96. Facette zusätzlich die drei Eckpunkte.
- OML: Teilstichprobe jeder 48. Facette, ebenfalls Mittelpunkt und ggf. Eckpunkte.
- **Befund:** 8 Keepout-Treffer rechts, 2 links. In der kleineren OML-Stichprobe 0 Treffer. Keine dieser Stichproben stellt einen vollständigen Kollisionsnachweis dar.
- Beide Meshes werden nach dem Laden von FreeCAD als `isSolid=True` und `hasNonManifolds=False` eingestuft. Selbstüberschneidungsfreiheit wurde **nicht** nachgewiesen.
- Die vorherige zu grobe Stichprobe (jede 48. Facette) lieferte 0 Treffer. Das ist ausdrücklich ein demonstrierter False Negative und darf nicht als Freigabe verwendet werden.
- **Nächster Gate:** freie Querschnitte und die Zwischenflächen volumetrisch gegen die kompletten v310-Keepouts und v312-OML prüfen; lokales Rerouting/zusätzliche Stationen mit Clearance-Margin. Danach Null-Selbstschnitt-Volltest und Slicer-Test.
- Druck-/Flugfreigabe bleiben gesperrt.
