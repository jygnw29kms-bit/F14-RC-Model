# F-14 v331/v332 – Integrations- und Verbinderprüfung (09.11.2026)

## Prüfgrundlage
- `migration/freecad/F14_v330_INTEGRATED_ASSEMBLY_REVIEW.FCStd`
- Nachweisdateien: `freecad_v331_assembly_interface_audit.json` und `freecad_v332_joiner_clearances_audit.json`
- FreeCAD 1.1.4; numerische Geometrieprüfungen, **keine** physische Abnahme

## Ergebnisse
- 18 ausgewählte BRep-Baugruppenpaare wurden mit `Shape.common()` geprüft.
- Zwischen Flügel-Innen-/Außensegmenten und sechs 8×6-Verbindern gab es in dieser nominalen Anordnung **keine positive Volumenüberschneidung**.
- Bei allen sechs Verbindern beträgt der gemeldete minimale Solid-zu-Solid-Abstand sowohl zum Innen- als auch zum Außensegment **0,0 mm**. Das weist auf berührende Flächen hin, **nicht** auf einen nachgewiesenen realen Montage-/Druckspalt.
- Linkes/rechtes Stabilator-Teil schneiden die zusätzliche v312-Rumpf-OML-Referenz mit etwa **6.162 / 6.328 mm³**. Die Einbaubedingung und etwaige Ausschnitte sind noch nicht validiert.
- Linker/rechter Einlaufadapter schneiden den `FUSELAGE_CURRENT`-Vollkörper um etwa **7.017 / 7.013 mm³**. Da dieser Rumpfkörper eine Referenz und keine ausgehöhlte Produktionsschale ist, folgt daraus noch keine unzulässige Kollision.

## Konsequenz für die Konstruktion
1. Die Wing-Joiner dürfen **nicht** als fertig montierbare Press-/Schiebepassung freigegeben werden, bevor eine definierte Toleranzgeometrie und ein realer P2S-Passcoupon vorliegen.
2. Die Einlaufadapter und Stabilatoren brauchen explizite Ausschnitte/Strukturanschlüsse in einer produktionsfähigen Rumpfgeometrie; die Überschneidung mit einer Vollreferenz darf weder ignoriert noch ungeprüft weggeschnitten werden.
3. Dynamische Schwenkflügel- und Leitwerksfreigängigkeit, Massenbudget, echte Hardwareabmessungen sowie Material- und Drucktests sind noch offen.
4. Die v326-EDF-Übergangswände bleiben die geprüfte Entwicklungsbasis. v329 bleibt wegen realer Mesh-Selbstüberschneidungen **nicht freigegeben**.

**Status:** Integrationsdiagnose abgeschlossen; weder gesamtes CAD-Modell noch Druck oder Flug freigegeben.
