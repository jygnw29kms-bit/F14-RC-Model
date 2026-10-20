# Sektion C – Vertikaldatum-Prüfung – 20.10.2026

## Ergebnis
Für Sektion C ist derzeit **kein quellenverfolgbares absolutes Z-/Waterline-Datum verifiziert**. Deshalb bleibt C in lokalen Sektionskoordinaten und darf nicht in einen A-B-C-Loft oder den Master übernommen werden.

## Geprüfte mögliche Datumsquellen

### 1. Horizontale Achsen der UPC-Querschnitte
Die UPC-Querschnitte besitzen gezeichnete Symmetrieachsen. B und C liegen im Raster zufällig auf derselben y-Lage von 610,098 px, A dagegen auf 275,173 px. Die Quelldaten markieren `common_waterline_verified=false`.

Bewertung: **lokale Zeichnungs-/Symmetrieachse, keine bestätigte Flugzeug-Waterline.**

### 2. UPC-Stationsmarken A/B/C
Die Stationsmarken liefern nur die X-Lage. Ihre y-Position ist laut eigener Quelleninterpretation lediglich die Beschriftungs-/Ticklage und ausdrücklich keine Waterline.

Bewertung: **nicht als Z-Datum verwendbar.**

### 3. Seitenprojektion um C
Die linke Probe vor C ist als `upper body/canopy contour` dokumentiert. Die rechte Probe hinter C ist nur eine `overall side projection`, bei der Wing-/Glove-Strukturen den Rumpf verdecken können. Die Planbreiten in diesem Bereich sind zudem Fixed-glove-Gesamthüllen und keine Rumpfkernbreiten.

Bewertung: **semantisch gemischte Projektion, kein Stationsanker.** Die diagnostisch ermittelte Verschiebung von +3,566 mm ist ausdrücklich **keine Geometriekorrektur**.

### 4. Grumman/NASA-Wing-Referenz-WL
Der Datensatz `NASA_F14_basic_wing_v08.json` stammt aus NASA CR-3992 Appendix 2 und beschreibt die Grumman-Basisflügelprofile. Die Zuordnung lautet `WL = reference_WL + yc * chord`. Die Referenz-WL ändert sich mit WBL und liegt über die vorhandenen Flügelstationen zwischen 159,93018 und 152,03552 in.

Der ältere Pivot-WL von rund 160,84 in wurde aus diesen **Flügelprofil-Referenzlinien** extrapoliert. Das frühere Audit kennzeichnet ihn selbst als nicht als Originalflugzeug-Pivot-WL verifiziert.

Bewertung: **Wing-Section-Referenzlinie, keine nachgewiesene Fuselage-C-Waterline.** Eine Übertragung auf Sektion C ist gesperrt.

### 5. Historischer gemeinsamer A/B/C-Rahmen
Der alte Rahmen ist weiterhin als Kandidat markiert. Metrische Registrierung, kontinuierliche OML und Produktions-Loft sind nicht verifiziert. Zusätzlich ist dokumentiert, dass die C-Unterkante mit einem Einlauflippen-Schritt zusammenfällt und die Originalstationsdarstellung ungeklärt ist.

Bewertung: **nur Studienrahmen.**

## Sperren
Bis ein quellenverfolgbares fuselage-/aircraft-bezogenes Vertikaldatum gefunden und C eindeutig daran registriert ist, bleiben gesperrt:
- absolute C-Z-Position,
- Übernahme der +3,566-mm-Diagnoseverschiebung,
- Übertragung der Grumman-Wing-WL auf C,
- A-B-C-Loft,
- Master-Änderung,
- Druck-, Produktions- und Flugfreigabe.

## Nächster Schritt
Navy-/NADC-/Grumman-Originalunterlagen werden gezielt nach einem fuselage-bezogenen WL/BL/FS-Datum oder einer anderen stationsbezogenen vertikalen Referenz durchsucht. Falls kein belastbarer Bezug auffindbar ist, bleibt C bewusst lokal und der absolute 3D-Loft wird verschoben.
