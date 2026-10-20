# Offene C-Konturreferenzen

Die 26 getrennten Rastersegmente sind je Schwelle zu vier offenen Ketten konsolidiert. Ueberlappungen wurden deterministisch an naechsten Rasterpunkten zugeschnitten; neue Anschlussstrecken zwischen Rasterproben sind hoechstens sqrt(2) Pixel lang. Vier durch Zeichnungsachsen verdeckte Bereiche bleiben offen.

Ausgefuehrt und geprueft: drei Schwellen (96/128/160), insgesamt zwoelf gueltige offene native Linien, keine Solids. Bei Schwelle128 bestehen die vier Linien aus362/241/238/356Kanten. Die native Offenheit, Kantenanzahl, transformierten Endpunkte, Eingabehashes, Archivhash und ZIP-Integritaet wurden geprueft. Unabhaengige ganzzahlige Rasterpruefung ergab keine nichtbenachbarten Streckenschnitte.

Datei: `migration/freecad/F14_C_OPEN_RASTER_CHAINS.FCStd`. Die Einzelreferenzen bleiben erhalten. Die Reihenfolge und Zuschnitte stehen in den zugehoerigen JSON-Dateien unter `analysis/original_front_sources`.

Die Referenz beschreibt die dunkle Strichaussenkante, keine gesicherte Strichmitte oder originale Flugzeughaut. Der historische metrische Rahmen ist ungeprueft. Keine geschlossene Sektion, kein produktiver Rumpf, keine Druck- oder Flugfreigabe. Eine kuenftige Verbindung ueber die Achsen muss als Rekonstruktionshypothese separat behandelt werden.
