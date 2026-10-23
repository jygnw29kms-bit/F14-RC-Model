# 135er F-14 Tomcat RC

Neuaufbau des RC-/FDM-F-14-Projekts von Grund auf.

**Pilot / Projektkontext:** 135erHeli RC Pilot

## Aktueller sichtbarer FreeCAD-Entwicklungsstand

![Aktueller F-14-FreeCAD-Entwicklungsstand ohne UPC-ReferenzhÃ¼lle](docs/images/f14_freecad_current_20261016.png)

*FreeCAD-v194-Entwicklungsansicht vom 16. Oktober 2026. UPC-/Quellrumpf-ReferenzhÃ¼lle und ReferenzhÃ¼llen sind ausgeblendet, damit die aktuell modellierten ZellenoberflÃ¤chen, Einlauf-/EDF-Geometrie und Mechanik-Kandidaten sichtbar bleiben. Dies ist ein Entwicklungsstand, keine Druck- oder Flugfreigabe.*

Sobald ein neuer **sichtbarer und sinnvoll prÃ¼fbarer Entwicklungsstand** verfÃ¼gbar ist, wird er im Repository dokumentiert und mit einem aktuellen Bild bzw. einer geeigneten Vorschau verknÃ¼pft. ZwischenstÃ¤nde werden klar als Entwicklung, Prototyp oder freigegebener Stand gekennzeichnet.

### Referenz-/Registrierungsstudie Sektion C â€“ 20.10.2026

![Sektion C Registrierungsstudie](docs/images/f14_C_registration_study_20261020.svg)

*Entwicklungsstand / Referenzstudie: Der neutrale C-Rasterkandidat ist einmal im historischen Kandidatenrahmen und einmal ausschlieÃŸlich in Z auf die Mitte einer unabhÃ¤ngig interpolierten SeitenprojektionshÃ¼lle verschoben dargestellt. Die SeitenhÃ¼llen-Guides sind keine bestÃ¤tigte C-Stationskontur. Die dort gezeigte Z-Verschiebung ist inzwischen ausdrÃ¼cklich nur noch als Diagnose eingestuft und keine Geometriekorrektur. Keine Master-, Druck-, Produktions- oder Flugfreigabe.*

### Navy/UPC-Seiten-X-Registrierung â€“ 21.10.2026

![Navy/UPC Seiten-X-Registrierung](docs/images/f14_side_x_registration_summary_20261021.svg)

*Entwicklungsstand / Referenzstudie: Drei homologe Seitenansichtslandmarken â€“ FS93/Radomaufweitung, mittlerer Canopy-Bow und hinterster Nozzle-Endpunkt â€“ stÃ¼tzen eine affine UPC-Seitenansichtsregistrierung auf Aircraft-Fuselage-Station. Nominaler Fit-RMS 0,185 Pixel; A-F kÃ¶nnen damit als Engineering-X-/FS-Kandidaten gefÃ¼hrt werden. Die Z-/Waterline-Registrierung bleibt offen; keine Master-, Druck-, Produktions- oder Flugfreigabe.*

### Aâ€“F X-registrierte FreeCAD-Studie mit lokalem Z â€“ 22.10.2026

![Aâ€“F X registriert, Z lokal](docs/images/f14_ABCDEF_X_registered_local_Z_20261022.svg)

*Entwicklungsstand / native FreeCAD-Studie: Die sechs Frontsektionen Aâ€“F stehen erstmals gemeinsam an den neuen Navy/UPC-basierten longitudinalen Engineering-X-Positionen. Jede Sektion wurde nur um ihre bisherige Kandidaten-Achse auf lokales Z=0 rezentriert; dieses lokale Z=0 ist ausdrÃ¼cklich keine gemeinsame Aircraft-Waterline. Es wurde kein Loft erzeugt und der Master blieb unverÃ¤ndert. Keine Druck-, Produktions- oder Flugfreigabe.*


### CR-172559 Quick-Geometry-Referenzrails – 23.10.2026

![CR-172559 Quick-Geometry-Referenzrails](docs/images/f14_CR172559_quick_geometry_rails_20261023.svg)

*Entwicklungsstand / Referenzstudie: Native 3D-Referenzrails aus NASA CR-172559 fuer FS352–780. Sektion C liegt longitudinal bei FS428,03 im Segment Inlet → Nacelle Aft Fairing. Die CR-172559-Fuselage ist ein 1:40-Quick-Geometry-Modell und keine Produktions-OML; C-Z bleibt bewusst unregistriert.*

## Aktueller technischer Stand

Das Flugzeug ist weiterhin **unvollstÃ¤ndig, nicht druckfertig und nicht fÃ¼r den Flug freigegeben**.

Noch offen sind unter anderem die belastbare durchgehende Rumpf-/Wing-Glove-Geometrie, die gemeinsame Baugruppenregistrierung, vermessene RC-Hardware, vollstÃ¤ndige Strukturvalidierung und physische Nachweise. Eine Kollisions- oder HÃ¼llprÃ¼fung gegen einen interpolierten Quellkandidaten ist kein Nachweis der originalen AuÃŸenkontur des Flugzeugs.

Zu den zuletzt ausgefÃ¼hrten Entwicklungsarbeiten gehÃ¶ren native verbundene Einlauf-/AdapterwÃ¤nde, interne Auslasskandidaten, ein internes Twin-EDF-Layout und lokale P2S-Slicing-Versuche. Die Auslassgeometrie besitzt zusÃ¤tzlich eine Ã¤ltere native parametrische Fusion-Historie mit sechs benannten Parametern; Reimport, Parameterregeneration und Kandidaten-Loft-HÃ¼llprÃ¼fung wurden geprÃ¼ft. STL-/3MF-Dateien bleiben ausdrÃ¼cklich nicht freigegebene Entwicklungsartefakte.

Aktuell wird die Referenzgeometrie der F-14-Nase weiter abgesichert. Dazu gehÃ¶ren Navy-StationsbezÃ¼ge, UPC-/MaÃŸstabsprÃ¼fungen sowie rekonstruierte Radom-Trennlinien aus Drauf- und Seitenansicht. Diese dienen derzeit als Referenzen und sind noch keine freigegebene 3D-Trennfuge oder Produktionsgeometrie.

- [Aktueller Stand Antrieb und offene PrÃ¼fschritte](docs/PROPULSION_CANDIDATE_STATUS_20261016.md)
- [Workflow zur PrÃ¼fung der QuellflÃ¼gel](cad/fusion/source_review/README.md)
- [Verbindliches Massenbudget](docs/04_MASS_BUDGET.md)
- [Verifikationsplan](docs/05_DESIGN_VERIFICATION.md)
- [C-AchsschlieÃŸung â€“ neutraler Studienkandidat](docs/C_ACHSSCHLIESSUNG_STUDIENKANDIDAT_20261020.md)
- [A/B/C-RahmenprÃ¼fung und aktueller C-Registrierungsblocker](docs/ABC_RAHMENPRUEFUNG_20261020.md)
- [Navy/UPC-Seiten-X-Registrierung und A-F-FS-Kandidaten](docs/SEITEN_X_REGISTRIERUNG_20261021.md)
- [Sektion C: Vertikaldatum bleibt gesperrt](docs/C_VERTIKALDATUM_PRUEFUNG_20261020.md)

## Konstruktionsziel

- optisch maÃŸstabsgetreue AuÃŸenkontur der Grumman F-14 Tomcat
- 900 mm Spannweite bei 20Â° FlÃ¼gelschwenkung
- MaÃŸstab etwa 1:21,7
- zwei 50-mm-EDF
- 4S-LiPo
- funktionsfÃ¤hige SchwenkflÃ¼gel von 20Â° bis 68Â°
- vollbewegliche HÃ¶henleitwerke
- FDM-orientierte Struktur fÃ¼r Bambu Lab P2S
- FreeCAD 1.1.4 als primÃ¤res Headless-Master-CAD
- Fusion nur fÃ¼r unvermeidbare AltbestandsprÃ¼fung oder Export, niemals fÃ¼r neue Konstruktion

## Nicht verhandelbare Regel

Die ausgemusterten Geometrien F14_RC_FDM R2/R3/R4 sowie deren OpenSCAD-, STL-/3MF-Dateien und Hardwareannahmen sind **keine Konstruktionsgrundlage** fÃ¼r dieses Projekt.

## Entwicklungsablauf

1. belastbare Originalreferenzgeometrie festlegen
2. MaÃŸstab und AuÃŸenkontur festschreiben
3. Aerodynamik- und Schwerpunktbereich definieren
4. zentralen FlÃ¼gelkasten und Schwenkmechanismus konstruieren
5. EDF, ESC, Akku und Elektronik integrieren
6. leichte FDM-Struktur und CarbonverstÃ¤rkungen entwickeln
7. Masseneigenschaften prÃ¼fen
8. druckbare Module exportieren
9. PrÃ¼fstandtests durchfÃ¼hren
10. kontrollierte Flugerprobung schrittweise erweitern

## Dokumentation

- [Projektanforderungen](docs/00_PROJECT_REQUIREMENTS.md)
- [Referenzbasis](docs/01_REFERENCE_BASELINE.md)
- [RC-Vergleichsreferenzen](docs/02_RC_BENCHMARKS.md)
- [Systemarchitektur](docs/03_SYSTEM_ARCHITECTURE.md)
- [Massenbudget](docs/04_MASS_BUDGET.md)
- [Verifikationsplan](docs/05_DESIGN_VERIFICATION.md)

## CAD

FreeCAD 1.1.4 ist der aktive Headless-orientierte CAD-Workflow unter `migration/freecad`. Das Ã¤ltere Fusion-Add-in unter `cad/fusion/F14TomcatRC` bleibt ausschlieÃŸlich aus GrÃ¼nden der Nachvollziehbarkeit und fÃ¼r unvermeidbare AltbestandsprÃ¼fung bzw. Export erhalten. Es darf nicht fÃ¼r neue F-14-Konstruktionsarbeit verwendet werden und wird nach solchen Altaufgaben wieder geschlossen.

## Sprache und sichtbare ProjektstÃ¤nde

Das Repository wird ab jetzt **auf Deutsch gefÃ¼hrt**. Neue README-Dateien, Statusberichte, PrÃ¼fdokumente und Beschreibungen werden deutsch erstellt. Technische Dateinamen, API-Bezeichner, Quellcode-Symbole und historisch notwendige Begriffe dÃ¼rfen englisch bleiben, wenn eine Umbenennung die Nachvollziehbarkeit oder Funktion beeintrÃ¤chtigen wÃ¼rde.

Sichtbare EntwicklungsstÃ¤nde werden mÃ¶glichst frÃ¼h im Repository abgelegt, sobald sie technisch sinnvoll beurteilt werden kÃ¶nnen. Dabei wird klar zwischen Referenz, Entwicklungsstand, Prototyp und Freigabestand unterschieden.

