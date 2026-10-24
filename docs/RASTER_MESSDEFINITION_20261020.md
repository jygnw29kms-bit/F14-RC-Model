# Messdefinition fuer die A/B/C-Rasterreferenzen

Die vorhandenen Referenzen messen unterschiedliche Dinge. Vor einem gemeinsamen Front-Loft muessen diese Definitionen je Quelle erhalten und explizit miteinander verglichen werden. Ein Wechsel der Messdefinition darf keine stillschweigende Konturkorrektur sein.

| Referenz | Tatsaechliche Messgroesse | Verbleibende Einschraenkung |
|---|---|---|
| A/B-Rasterhuellen v2 | Aeusserste dunkle Pixel je Zeile | Strichaussenkante, Achsenbruecken angenommen |
| C-offene Rasterketten | Stueckweise aeussere Dunkelpixel | Vier Achsenluecken offen; Kontursemantik ungeprueft |
| C-Schliessungshypothesen | Rasterketten plus angenommene Bruecken | Keine gemessene geschlossene Originalsektion |
| C-Weissoeffnungen v2 | Grenze zusammenhaengender weisser Rasterbereiche | Keine Strichmitte oder physisch nachgewiesene freie Einlaufflaeche |
| A/B-horizontale Laufmittel | Mitte des aeussersten zusammenhaengenden Dunkellaufs | Schraffurvereinigung, Neigung und Rastertreppen beeinflussen die Mitte |
| Lokale Normalprofile | Dunkellauf entlang geschaetzter lokaler Normalen | Abhaengig von Tangentenfenster, Interpolation, Schwelle und Strichidentitaet |
| Seitenprojektionsproben | Silhouetten-/Strichproben in einer anderen Ansicht | Physische Identitaet mit Stationshaut und gemeinsame Wasserlinie offen |

## Ausgefuehrte lokale Pruefungen

Die drei Schwellen96/128/160 aendern bei festen Extraktionsfenstern die A/B/C-Boundingbreiten und -hoehen nicht. Das beweist keine Messgenauigkeit. Die Flaechen aendern sich trotzdem; Strichdicke, Stationszuordnung und Kalibrierung liegen ausserhalb dieses Tests.

Die dichten horizontalen Laufmittel zeigen lokale Zacken. Vier vergoesserte Beispiele zeigen sowohl Schraffuranschluesse als auch echte Einbuchtungen oder Halsuebergaenge. Ein numerischer Richtungswechsel darf deshalb weder automatisch geloescht noch geglaettet werden.

Drei der zuerst untersuchten vier Normalprofilorte liegen an Schraffurvereinigungen. Ihre Zahlen bleiben nachvollziehbare Rechenergebnisse, sind jedoch keine isolierten Strichmittenmessungen. A bei Zeile300 und der vorab visuell gepruefte B-Ort bei Zeile550 sind vorlaeufig isolierte lokale Kandidaten. Sie erlauben keine globale Korrektur und begrenzen keine gesamte Konturunsicherheit. Eine Abtastung in0.1Pixel-Schritten erzeugt keine zusaetzliche Originalaufloesung.

## Verbindliche naechste Konstruktionsschritte

1. Fuer jede verwendete Kontur den semantischen Strich und die Messdefinition angeben. Unklare Schraffuranschluesse und Achsenueberdeckungen separat markieren.
2. Stationslage, Ansichtsmassstab und Wasserlinie an unabhaengig identifizierten gemeinsamen Merkmalen pruefen. Der interpolierte C-Seitenwert ist keine direkte Stationsmessung; er ueberquert einen lokalen Projektionsabschluss.
3. Erst danach eine separate native Frontstudie aus gleichartig definierten Referenzen erstellen. Hypothetische Bruecken und Registrierungsvarianten bleiben sichtbar gekennzeichnet; vorhandene Quellen und der Master werden nicht automatisch ersetzt.

Die geprueften lokalen Rasterstudien liefern noch keine originale Aussenhaut, druckfertige Baugruppe, Festigkeitsbewertung oder Flugfreigabe.
