# F-14 v336 – interne Flügelkanäle (09.11.2026)

## Neuer CAD-Kandidat
Die `F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd` wurde mit FreeCAD 1.1.4 aus den vier v282-Flügelsegmenten generiert. Es wurden nur geschlossene, vollständig im bestehenden Volumen liegende zylindrische Entlastungskanäle akzeptiert, wenn ein 1,5-mm-Prüfmantel ebenfalls im verbleibenden Körper lag und das Ergebnis genau einen gültigen Solid enthielt.

| Segment | Akzeptierte 4-mm-Kanäle | Rechnerisch entferntes Volumen |
|---|---:|---:|
| Rechts innen | 2 | 376,991 mm³ |
| Links innen | 2 | 376,991 mm³ |
| Rechts außen | 0 | 0 mm³ |
| Links außen | 0 | 0 mm³ |

Die äußeren Begrenzungsmaße blieben bei allen vier Flügelteilen unverändert. Die geprüften Körper sind als BRep gültig. Die kleine Volumenersparnis belegt **noch keine** effektive oder FDM-druckbare Hohlflügelbauweise; insbesondere können geschlossene Innenkanäle beim Slicen ungünstige Überhänge oder eingeschlossene Bereiche erzeugen.

## Weiterer Konstruktionsbedarf
Es fehlen offene, slicergerechte Hohlräume mit definierter Druckorientierung, schalenintegrierte Stege/Gurte, strukturelle Anschlusszonen für die 8×6-mm-Carbonverbinder sowie Festigkeits-, Schwerpunkt- und Verformungsnachweise. Die Außenflügelsegmente bleiben in diesem Versuch unverändert. Ein Belastungstest und die Passproben v333 sind weiterhin erforderlich.

**Keine Druck- oder Flugfreigabe.**

- [FreeCAD v336](../migration/freecad/F14_v336_INTERNAL_WING_CHANNEL_CANDIDATE.FCStd)
- [Python-Generator](../migration/freecad/build_v336_internal_wing_channels.py)
- [Geometrieprüfung](../migration/freecad/freecad_v336_internal_wing_channels_audit.json)
