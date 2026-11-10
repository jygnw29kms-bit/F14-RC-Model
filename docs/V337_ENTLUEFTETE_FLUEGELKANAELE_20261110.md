# F-14 v337 – belüftete Flügelkanäle, Generatorstand

**Stand 10.11.2026 · Entwicklungsbranch · nicht ausgeführt / keine CAD-Abnahme**

Die v336-Flügel enthalten in den inneren Segmenten je zwei geschlossene Kanäle. Der neue Generator `migration/freecad/build_v337_vented_wing_channels.py` versucht, diese Kanäle mit kleinen vertikalen Öffnungen von der Flügelunterseite aus zugänglich zu machen.

Die Eingaben stammen ausschließlich aus `F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd` und dem zugehörigen v336-Prüfbericht. Alle vier v336-Flügelkörper werden übernommen; unpassende Schnitte bleiben verworfen. Die Kandidaten werden durch Boolean-Operationen erzeugt, mit Einzelkörper-/Validitätsprüfungen versehen und in einer eigenständigen v337-FreeCAD-Datei gespeichert.

**Wichtig:** Der Generator ist ins GitHub-Repository geschrieben, wurde wegen des erschöpften Desktop-Commander-Monatskontingents aber **noch nicht auf Jens-PC mit FreeCAD ausgeführt**. Damit gibt es noch keine bestätigte `F14_v337_VENTED_WING_CHANNEL_CANDIDATE.FCStd` und keinen v337-Prüfbericht.

Nach Wiederherstellung der Remote-Ausführung sind zwingend zu prüfen:

1. Freies Durchgehen der Öffnung vom Unterboden bis in den bestehenden Kanal.
2. Tatsächliche Ober- und Unterhautstärken sowie Abstände zu Carbonrohraufnahmen.
3. Boolean-Solid-Prüfung, Mesh-Manifold-/Selbstüberschneidungsprüfung und Slicer-Schnittbild.
4. Verstärkungsstege und echte Lastübertragung zwischen den 8×6-mm-Carbonrohrverbindern.
5. Masse, Schwerpunkt, Biegung, Torsion und Probekörper.

**Keine Freigabe:** Dieses Skript ist noch kein druckfertiger Flügel. v336 bleibt der letzte mit FreeCAD erzeugte Flügel-Entwicklungskandidat; v337 ist ein nachfolgender reproduzierbarer Konstruktionsversuch.

Zum Ausführen in der Projektwurzel mit installiertem FreeCAD 1.1.4:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe' 'migration\freecad\build_v337_vented_wing_channels.py'
```
