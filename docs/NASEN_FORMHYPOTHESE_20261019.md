# Nasen-Formhypothese – keine Originalaußenform

Eine getrennte native FreeCAD-Studie verwendet die normierte A-Polygonform an neun Stationen. Ihre Breite und Höhe werden auf die vorhandenen Projektionsproben skaliert. Diese Formannahme ist nicht durch originale Querschnitte vor A belegt. Auch das Endprofil ist skaliert und entspricht deshalb nicht der unveränderten Originalsektion A.

Die native Erstellung ist ausgeführt: neun gültige Profilflächen, ein gültiger geschlossener Studienkörper, Volumen131031.284558mm³. Dateihash und Archivintegrität wurden geprüft. Das bestätigt nur technische Erzeugbarkeit, keine Quellenpassung.

Datei: `migration/freecad/F14_NOSE_A_SHAPE_SENSITIVITY.FCStd`. Der separate Audit und Generator dokumentieren Eingaben und Annahmen. Der aktuelle Master, Originalquerschnitte und Radom-Projektionssperren bleiben unverändert. Keine Druck-, Produktions- oder Flugfreigabe.

Als Nächstes sind native Zwischenkonturen und der Übergang zur unveränderten A-Sektion zu vergleichen. Die Studie darf die fehlenden Originalquerschnitte nicht als Nachweis ersetzen.

## Zwischenkonturen geprüft

Acht native Zwischenkonturen wurden mit zusätzlichen Originalproben verglichen. Der erste Vergleich meldete2.108466mm maximale Breitenabweichung bei Bildspalte537. Die visuelle Quellenprüfung zeigt dort zusammenlaufende Radomfugen- und Umrissstriche; deren Dunkellaufmittelpunkt ist kein belastbarer Umrissmittelpunkt. Der Breitenwert537 wurde deshalb in Version2 ausdrücklich ausgelassen, nicht passend korrigiert. Der historische Erstvergleich bleibt erhalten, ist für diesen Maximalwert jedoch überholt. Version2 ergibt maximal0.790675mm Restabweichung an der unteren Seitenprojektion bei634. Diese Probe und der Übergang zur unveränderten SektionA bleiben zu prüfen. Keine Toleranz- oder Originalformfreigabe.


### Quellenprüfung der unteren Probe634

Die untere Strichgruppe bei634 berührt das Ende des gewählten Bildausschnitts und geht in ein Anbauteil über. Ihr Mittelpunkt ist kein belastbarer Rumpfumriss. Version3 lässt deshalb auch diesen Einzelwert aus. Von24 möglichen Vergleichswerten bleiben22 auswertbar; ihr größter Betrag beträgt0.295185mm. Die Geometrie wurde dabei nicht verändert. Dieser kleinere Wert gilt nur für die verbliebenen Projektionsproben und bestätigt weder verdeckte Konturen noch Querschnittsform, Registrierung oder den Anschluss an OriginalsektionA. Die historischen Maximalwerte2.108466mm und0.790675mm sind durch die Quellenprüfung für diese beiden mehrdeutigen Proben überholt.


## Anschluss an unveränderte OriginalsektionA

Der native Vergleich ist ausgeführt. Das skalierte Hypothesen-Endprofil ist3.529307mm niedriger und0.131779mm breiter als die unveränderte A-Kontur. Originalfläche:2817.850020mm²; Hypothesenfläche:2655.879905mm². Die native Flächendifferenz beträgt166.041282mm² nur im Original und4.071166mm² nur in der Hypothese. Abgetastete Randabstände erreichen1.896603mm bzw.1.621552mm in den beiden Richtungen. Das ist kein exakter Hausdorff-Abstand.

Die kleinen verbleibenden Zwischenprojektionsfehler erlauben deshalb keine nahtlose Übernahme des Nasenkörpers an OriginalsektionA. Endprofil und Originalkontur wurden nicht angepasst. Vor einer weiteren Loft-Variante müssen Quellenregistrierung und unterschiedliche Projektions-/Schnittdefinition geklärt werden.

