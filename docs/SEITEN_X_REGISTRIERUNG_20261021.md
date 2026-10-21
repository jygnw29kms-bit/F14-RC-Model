# F-14 Seitenansicht – longitudinale X-/FS-Registrierung – 21.10.2026

## Status
**Entwicklungsstand / Referenzstudie.** Die longitudinale Registrierung der UPC-Seitenansicht auf Aircraft-Fuselage-Station (FS) ist als Engineering-Kandidat quellenbasiert unterstützt. Sie ist **keine Produktions-, OML-, Druck- oder Flugfreigabe**. Die absolute Z-/Waterline-Registrierung bleibt separat offen.

![Navy/UPC Seiten-X-Registrierung](images/f14_side_x_registration_summary_20261021.svg)

*Referenzstudie: oben US-Navy Figure 4-7, unten UPC Figure 3.15. Rote Linien markieren drei homologe Seitenansichtslandmarken. Sie definieren ausschließlich einen longitudinalen Registrierungs-Kandidaten.*

## Quellen
- US Navy NAVEDTRA 14014, Figure 4-7: F-14 Fuselage Station Diagram mit FS-Lineal.
- US Navy NAVEDTRA 14315, Figure 2-3: FS93 am Übergang vom schmalen Probe-/Nasenbereich zum sich verbreiternden Radom.
- UPC Figure 3.15: sekundäre Blueprint-Darstellung mit Seitenansicht und A-F-Sektionsmarken. Die zugrunde liegende Abbildung ist keine Grumman-/Navy-Herstellerstationszeichnung.

## Navy-FS-Lineal
Das horizontale Lineal in Figure 4-7 wurde im Originalraster kalibriert.

- FS0-Raster-x: **71,0965 px**
- Rastermaßstab: **0,605655 px pro FS-inch** bzw. **1,651104 in/px**
- RMS der 18 Hauptmarken FS0…FS850: **0,677 px**
- größtes Tick-Residual: **1,793 px**
- daraus FS93 bei **x = 127,422 px**

Die resultierende FS93-Lage fällt in der Navy-Grafik auf die sichtbare Radomaufweitung und stimmt damit mit der unabhängig beschrifteten FS93-Nasendarstellung aus NAVEDTRA 14315 überein.

## Drei homologe Seitenansichtslandmarken
Für die Abbildung `UPC-x = a * FS + b` wurden drei voneinander getrennte, in beiden Seitenansichten sichtbare Merkmale verwendet:

1. FS93 / Radomaufweitung: UPC **x = 440,75…441,25 px**.
2. mittlerer Canopy-Bow: Navy **x = 252…254 px**, UPC **x = 909…910 px**.
3. hinterster Nozzle-Endpunkt: Navy **x = 569 px**, UPC **x = 2087 px**.

Nominaler Dreipunkt-Fit:
- `a = 2,257457087 px/in`
- UPC-Maßstab longitudinal: **0,442976305 in/px**
- UPC-FS0: **x = 231,2380 px**
- RMS: **0,185 px**
- größtes Residual: **0,254 px**

Paarweise Holdout-Prüfungen sagen den jeweils dritten Landmarkenpunkt mit maximal **1,421 px** Abweichung voraus.

Unter Variation der sichtbaren Linienbreiten bleibt der Maßstab im Bereich **0,442617…0,443342 in/px**. Das ist ein Robustheits-/Sensitivitätsscreen, kein statistisches Konfidenzintervall.

## A-F-Sektionsstationen im Seitenriss
Die originalen Seitenansichts-Ticks wurden direkt im UPC-Raster lokalisiert:

| Sektion | Tick x [px] | FS nominal [in] | Sensitivitätsbereich FS [in] | FS93-nasenrelativ im 900-mm-Modell [mm] |
|---|---:|---:|---:|---:|
| A | 642,5 | 182,179 | 181,112…183,243 | 104,317 |
| B | 905,5 | 298,682 | 297,711…299,651 | 240,595 |
| C | 1197,5 | 428,031 | 427,167…428,895 | 391,900 |
| D | 1561,5 | 589,275 | 588,544…590,007 | 580,514 |
| E | 1663,5 | 634,458 | 633,764…635,154 | 633,367 |
| F | 1862,5 | 722,610 | 721,986…723,239 | 736,482 |

Die Bereiche enthalten die Landmarken-Linienbreiten-Sensitivität und einen zusätzlichen ±0,5-px-Screen der Stationsmarke. Sie sind keine Fertigungstoleranzen.

## Verworfener Weg: Planansicht auf Seitenansicht übertragen
Während der Prüfung wurde ein scheinbar sehr guter NASA/Grumman-Flügel-Mehrpunktfit aufgebaut. Dabei wurden zwei Probleme erkannt:

1. Eine ältere symmetrische Spannweitenmessung verwendete in der oberen Bildhälfte keine saubere Flügelspitze. Die UPC-Darstellung zeigt unterschiedliche Schwenkstellungen und darf dort nicht als symmetrische 20°-Planform behandelt werden.
2. Noch wichtiger: Plan- und Seitenansicht besitzen nicht nachgewiesen denselben Raster-X-Ursprung oder Maßstab. Die Nasen-Changepoints liegen getrennt bei Plan **444,25…445,25 px** und Seite **440,75…441,25 px**.

Daher sind die zuvor versuchsweise aus dem Plan-Flügelfit abgeleiteten A-F-FS-Werte ausdrücklich gesperrt. Die korrigierte untere, ausgefahrene Flügelhälfte bleibt als lokale Planform-/Formprüfung erhalten, darf aber keine Seitenansichts-Ticks registrieren.

## Was damit jetzt erlaubt ist
- A-F in der UPC-Seitenansicht als **Engineering-X-/FS-Kandidaten** führen.
- Historische X-Kandidaten gegen diesen neuen Rahmen vergleichen.
- Weitere Primärquellenpunkte auf derselben Seitenansicht prüfen.

## Was weiterhin gesperrt bleibt
- Produktionsfreigabe des X-Rahmens,
- automatische Übernahme in den Master,
- absolute Z-/Waterline-Position von Sektion C,
- A-B-C- oder A-F-Loft auf Basis eines ungeprüften Z-Datums,
- Druck- und Flugfreigabe.

## Nächster Schritt
Ein sichtbares, homologes F-14-Merkmal mit quellenverfolgbaren **FS- und WL-Koordinaten** muss direkt in der UPC-Seitenansicht identifiziert werden. Erst damit kann der jetzt belastbare longitudinale Seiten-X-Rahmen um eine vertikale Aircraft-Waterline-Registrierung ergänzt werden.
