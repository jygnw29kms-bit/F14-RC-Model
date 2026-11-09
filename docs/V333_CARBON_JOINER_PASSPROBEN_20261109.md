# v333 – Carbonrohr-Passproben für F-14-Schwenkflügel

**Stand 09.11.2026. Entwicklungsproben, keine Bau- oder Flugfreigabe.**

Die bestehende v282-Flügelkonstruktion verwendet Carbonrohre mit 8 mm Außendurchmesser und 6 mm Innendurchmesser; die Flügelaufnahmen wurden mit 8,3 mm Nenndurchmesser angelegt. Der v332-BRep-Minimalabstand von 0 mm beruht auf berührenden geometrischen Grenzen an den Verbindern und ist keine unmittelbare Aussage über die radiale Bohrungsluft.

Zum Test der tatsächlichen PETG-Passung auf dem Bambu Lab P2S liegen jetzt drei einzelne STL-Prüfkörper vor: 8,2 mm, 8,3 mm und 8,4 mm Innendurchmesser. Im parametrisch erzeugten FreeCAD-Dokument sind alle drei feste Körper gültig; die exportierten Meshes sind geschlossen, ohne nichtmannigfaltige Flächen.

| Bohrung | Nominelle Durchmesserluft bei Carbonrohr-OD 8,0 mm | Nominelle radiale Luft |
| --- | ---: | ---: |
| 8,2 mm | 0,2 mm | 0,10 mm |
| 8,3 mm | 0,3 mm | 0,15 mm |
| 8,4 mm | 0,4 mm | 0,20 mm |

**Dateien:** [Prüfproben und Prüfdaten](../manufacturing/fit_coupons/v333_8mm_joiner/), [FreeCAD-Quelldatei](../migration/freecad/F14_v333_JOINER_FIT_COUPONS.FCStd), [Generator](../migration/freecad/build_v333_joiner_fit_coupons.py).

**Nächste Fertigungsmessung:** Alle drei Prüfkörper mit identischen P2S-/PETG-Einstellungen drucken, realen Rohr-OD mit Messschieber kontrollieren, Bohrungsmaß und Einschubverhalten prüfen. Vor einer Festlegung zudem Klebstoffsystem, Fügefläche, Schub-/Biegebeanspruchung und Haltbarkeit des CF-Rohrs gegen die tatsächlich gewählte Aufnahmestruktur verifizieren. Eine reine Einschubprobe ersetzt keinen Belastungsnachweis.

**Freigabestand:** STL nur für Passproben. Tragende Schwenkflügelverbindungen, gesamtes Flugzeug und Flug **nicht freigegeben**.
