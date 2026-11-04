# NASA-QUICK-Referenzstudien: geprüfter Stand 22.10.2026

Das Gesamtflugzeug bleibt unvollständig. Die folgenden Ergebnisse prüfen getrennte Quellenstudien; sie ersetzen weder die Registrierung der Außenform noch die RC-Konstruktion.

## Ausgeführt und nachgerechnet

- Historische KRVDEF/CURVES aus dem über PDAS verteilten SHIFARC-Archiv: ein direkter F-14-ELLY-Fall mit 101 Proben, einschließlich erster und zweiter Ableitung. Der als EL LY bezeichnete Bodyline-Typ akzeptiert auch einen negativen quadratischen Koeffizienten. Die frühere reine Ellipsenannahme war dafür zu eng.
- Original-CSMCOE: Zentren und Halbachsen von zehn BUP/CAN-Studienbögen an fünf Stationen. Größte Abweichung gegenüber der unabhängigen Konikrechnung: 0,000123 Quelleneinheiten.
- Original-CSCALC, NDERV=0: 110 Radien dieser Bögen nach Verschiebung auf die rechnerische ZMAPAXIS. Größte Abweichung gegenüber den Studienpunkten: 0,000007754 Quelleneinheiten. Alle erwarteten Proben sind genau einmal vorhanden; keine negative Diskriminantenwarnung im geprüften Lauf.
- Fünf offene Nasen- und fünf offene Canopy-Halbsektionslinien liegen in getrennten FreeCAD-Dateien vor. Gültigkeit, Endpunkte und Dateiintegrität wurden geprüft. Das sind Referenzlinien, keine geschlossene Haut.

## Reproduktion und Grenzen

`analysis/original_front_sources/verify_SHIFARC_canopy_radial_run.py` prüft die gespeicherten Originalrohdaten gegen die Studienpunkte, einschließlich Eingabehashes und Probenabdeckung. Der Originalaufrufer liegt daneben als `run_SHIFARC_CSCALC_reference.f`.

Der historische CSCALC-Cache benötigt statische lokale Variablen. Der erfolgreiche Compilerlauf verwendete `-std=legacy -fno-automatic -ffixed-line-length-72`. Der erste Lauf ohne statische Speicherung war ungültig und wurde nicht als Prüfergebnis übernommen. Historische Dummy-Arraydeklarationen bei KRVDEF verursachen Compilerwarnungen; der Aufrufer stellt die tatsächlich adressierten drei Koeffizienten bereit.

Die Radienprüfung umfasst keine Längsableitungen und keinen vollständigen THELIM/CSMINT-Lauf zur Auswahl der äußeren Hülle. Die Identität der historischen Routineversion mit der F-14-WBPPW-Version ist nicht vollständig nachgewiesen. Diskrete Schnittprüfungen der Studienpolygone sind keine analytische Schnittfreiheit aller Kurvenzwischenpunkte.

## Vor einer produktiven Außenhaut offen

1. Physische Einheit und gemeinsame Längs-/Höhenregistrierung der NASA-, Navy- und UPC-Quellen belegen. ZMAPAXIS ist eine Rechenachse und keine automatisch übertragbare Flugzeug-Wasserlinie.
2. Quellenmodell und Originaltreue trennen: Der NASA-Rumpf stammt laut Bericht aus einem 1:40-Dreiriss und enthält Vereinfachungen. Erfolgreiche Routinevergleiche machen ihn nicht zu Hersteller-Fertigungskoordinaten.
3. Weitere Rumpfmodelle und ihre Übergänge numerisch binden; degenerierte Spitzen-/Canopy-Anfangselemente ausdrücklich behandeln.
4. Erst darauf die Außenhaut, RC-Innenstruktur, Mechanik, Antrieb, Berechnungen und Druckexporte als zusammenhängendes Modell prüfen.

Die FreeCAD-Referenzen benutzen ausdrücklich **1 Quelleneinheit = 1 Darstellungs-mm**. Das bestätigt keinen physischen Flugzeug- oder RC-Maßstab. Keine Gesamtmodell-, Druck- oder Flugfreigabe.
