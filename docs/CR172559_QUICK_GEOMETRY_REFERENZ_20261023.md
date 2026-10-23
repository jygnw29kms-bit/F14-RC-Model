# CR-172559 Quick-Geometry-Referenz – 23.10.2026

## Ergebnis

NASA CR-172559 enthält in Tabelle 1 eine numerische F-14A-Fuselage-Quick-Geometry-Definition. Für den Bereich ab FS 352 wurden die gepaarten Y-/Z-Linien `MHB`, `CREASE`, `FUP`, `SCPUP`, `SCPCAN`, `SCPLO`, `FLO`, `INLTUP` und `INLTLO` als native 3D-Referenzrails in FreeCAD aufgebaut.

Sektion C liegt nach der Navy/UPC-Seiten-X-Registrierung bei FS 428,031 in. Damit fällt C in CR-172559 in das Segment `INLET TO NACELLE AFT FAIRING`, FS 425–433.

## Quellenbegrenzung

CR-172559 beschreibt dieses Fuselage-Nacelle-Modell ausdrücklich als Quick-Geometry-Modell auf Basis eines 1:40-F-14A-Dreirisses. Es sollte die aerodynamische Interferenzsimulation unterstützen und ist keine produktionsverifizierte OML. Der Bericht weist zudem darauf hin, dass insbesondere der hintere Nacelle-Bereich nicht exakt nachgebildet wurde.

Deshalb werden die Rails ausschließlich als unabhängiger Engineering- und Semantik-Check verwendet.

## C-Abgleich

Die lokale UPC-C-Höhe beträgt 72,367 mm im RC-Modell. Der Abgleich gegen plausible CR-172559-Z-Featurepaare bei FS 428,031 zeigt als beste Differenzen rund 3,2–3,8 mm. Das reicht nicht für eine absolute Z-Freigabe.

Folge:

- C-X/FS bleibt als Engineering-Kandidat nutzbar.
- WL≈145 bleibt als globaler Engineering-Datumkandidat erhalten.
- Die lokale UPC-C-Achse wird weiterhin nicht auf WL145 verschoben.
- Kein A–F-Loft, keine Masteränderung, keine Druck- oder Flugfreigabe.

## Sichtbarer CAD-Stand

`migration/freecad/F14_CR172559_QUICK_GEOMETRY_REFERENCE.FCStd`

Die UPC-C-Kontur wird im Modell bewusst in einer separaten Y-Vergleichsspur mit lokalem Z dargestellt. Dadurch entsteht keine scheinbare oder versteckte Z-Registrierung.
