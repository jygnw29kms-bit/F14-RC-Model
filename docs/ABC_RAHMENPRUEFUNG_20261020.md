# A/B/C-Rahmenprüfung – 20.10.2026

## Ergebnis
Die verifizierten bzw. neu rekonstruierten Frontreferenzen A, B und C wurden gegen den bisherigen gemeinsamen Kandidatenrahmen geprüft.

A → B verhält sich im Kandidatenrahmen geometrisch stetig: Breite und Höhe nehmen zu. Der Übergang B → C ist dagegen nicht als belastbare Loft-Grundlage freigabefähig. Zwischen B und C wächst die Breite um rund 160,507 mm, während die Höhe um rund 24,683 mm abnimmt.

Sektion C trägt im historischen gemeinsamen Rahmen zusätzlich einen Seitenhöhen-Residualwert von -17,021 Pixel. Die Quelldaten markieren selbst `aircraft_X_registration_verified=false`, `section_metric_scale_verified=false`, `common_waterline_verified=false` und `production_loft_allowed=false`.

## Prüfung des neuen neutralen C-Rasterkandidaten
Der neutrale C-Schließungskandidat (Schwellwert 128, Achsenversatz 0 Pixel) wurde in denselben historischen Rahmen übertragen und mit der alten C-Polygonkontur verglichen.

Die Unterschiede sind klein:
- Breite: -0,687 mm
- Höhe: -0,100 mm
- Mittelpunkt Y: +0,115 mm
- Mittelpunkt Z: -0,179 mm

Damit stammt der große C-Widerspruch nicht wesentlich aus der alten groben Konturzeichnung. Der Engpass liegt im metrischen bzw. vertikalen gemeinsamen Rahmen selbst.

## Unabhängige Seitenprojektionsprüfung
Die gültigen Seitenprojektionsproben bei X≈391,464 mm und X≈417,820 mm wurden auf die C-Station X≈403,325 mm interpoliert. Daraus ergibt sich eine Seitenhülle von Z oben ≈ +41,870 mm bis Z unten ≈ -33,323 mm. Der neutrale C-Kandidat liegt im alten Rahmen bei +36,891/-35,476 mm.

Der Hauptunterschied ist eine vertikale Mittellagenverschiebung von rund +3,566 mm. Nach einer reinen Z-Translation ohne Formskalierung bleiben oben und unten symmetrische Restabweichungen von etwa ±1,413 mm. Das ist eine Diagnose, keine Freigabe zur Skalierung oder Verformung der C-Kontur.

## Konsequenz
Es wird derzeit **kein A-B-C-Loft** aufgebaut und der Master bleibt unverändert. Vor einer 3D-Frontstudie muss geklärt werden, welche oberen und unteren C-Kanten semantisch zur Seitenhülle gehören und ob die gemeinsame Wasserlinie unabhängig bestätigt werden kann.

Keine Produktions-, Druck- oder Flugfreigabe.
