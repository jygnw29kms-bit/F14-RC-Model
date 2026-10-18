# Quellenregistrierung: geprüfter Stand am 18. Oktober 2026

Das Gesamtmodell ist nicht registriert und nicht für Druck oder Flug freigegeben. Die folgenden Ergebnisse trennen Quellenbefunde von Konstruktionsannahmen.

| Bezug | Ausgeführt und geprüft | Weiter offen |
|---|---|---|
| Navy FS93 | Beschriftete Abbildung 2-3 aus NAVEDTRA14315 visuell geprüft: FS93 liegt am Übergang von kurzer Nasensonde zum sich verbreiternden Radom. | Exakte Zuordnung zu den Strichen der UPC-Zeichnung. |
| NASA-Nase | NASA CR172559, PDF-Seite24, Tabelle1 Blatt5: erste Nasenregion beginnt bei93.0. | Diese Rechenmodellbeschreibung gibt keine Produktionsfreigabe der Außenform. |
| Flügel und Drehpunkt | Aktueller FreeCAD-Aufbau verwendet für beide absolute FS-Koordinaten. DrehpunktX=613.132390581mm. | Gemeinsame Registrierung zum UPC-Rumpf; NADC-Modellursprung und Drehpunkt-Wasserlinie. |
| Verschiebungshypothese | Bei bestätigtem FS93-Nasenursprung wäre die gemeinsame X-Verschiebung -108.786081204mm. | Nicht nur den Drehpunkt verschieben: Flügel und zugehörige Mechanik müssen konsistent behandelt werden. |
| UPC-Nasenübergang | 18 Schwellenwert-/Fensterprüfungen: Draufsicht [444.25, 445.25], Seitenansicht [440.75, 441.25] Originalpixel. | Das einfache Breitenmodell liefert keine exakte physische Station; Ansichten besitzen nicht nachgewiesen denselben Ursprung. |
| UPC-Maßstab | 900mm /1701Pixel Flügelspannweite ergibt 0.529100529mm/Pixel. Historischer Kandidat: 0.527116552. | Die gedruckte Meterleiste liefert eine abweichende Spanne; keinen Maßstab stillschweigend übernehmen. |
| Radomfuge | 87 Originalstrichproben und native FreeCAD-Projektionskurven mit50/35 gültigen Kanten erstellt. | Keine räumliche Fuge, keine konstante FS-Ebene, keine geprüfte Flächenführung. |

Neun ausdrücklich hypothetische Kombinationen von Maßstab und Nasenursprung wurden berechnet. Die daraus vorhergesagte Drehpunktposition streut um 21.991 Originalpixel. Das ist eine Sensitivität der Annahmen und keine gemessene Passung.

## Nächste Arbeit

1. Der NADC-Originaldreiriss ist inzwischen abgerufen und visuell geprüft: Nasenstation7.7in im1:12-Modell entspricht92.4in; gegenüber NavyFS93 verbleiben0.6in bzw. rund0.702mm im RC-Maßstab. Gerundete Stationsangaben und separate UPC-Ursprünge gemeinsam berücksichtigen.
2. Einen homologen Längsbezug in den Originalansichten bestimmen. Die gekrümmte bzw. schräge Radomfuge darf nicht über beliebige Mittelpunkte gleichgesetzt werden.
3. Danach einen getrennten Baugruppenkandidaten mit konsistenten Flügel-, Drehpunkt- und Mechaniktransformationen erzeugen und gegen Originalkonturen prüfen.
4. Erst nach Quellenregistrierung die noch fehlende Wing-Glove-Außenform und RC-Innenstruktur konsolidieren. Aktuelle Masterzeiger unverändert lassen.

## Nachweise

Die Einzelbefunde, Originalausschnitte und reproduzierbaren Prüfungen liegen in `analysis/independent_reviews/crank_localization_20261017/`. Native Referenzen liegen in `migration/freecad/F14_ORIGINAL_RADOME_SEAM_GUIDES.FCStd`; der zugehörige Audit enthält Eingabe- und Ausgabedatei-Hashes. Kein physischer Test und keine Simulation wurden aus diesen Referenzen abgeleitet.

## Ausgeführte Bereichsprüfung der Radomfuge

Die externe vorbereitete Prüfung `analysis/pruefe_radom_gegen_frontsektionen.py` wurde ausgeführt. Ihr Ergebnis bestätigt die Bereichssperre: Die Radomfuge endet im historischen Kandidatenrahmen beiX=54.636964mm; SektionA beginnt beiX=110.774877mm. Dazwischen fehlen56.137913mm axialer Querschnittsabdeckung. Die ABCDEF-Loft-Studie ist deshalb keine geeignete Zieloberfläche für diese Fuge. Das ist eine numerische Bereichsprüfung, keine native Flächenprojektion. Die bestehende Schutzprüfung und der Master wurden nicht verändert.
