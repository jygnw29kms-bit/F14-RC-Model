# Radom-3D-Prüfung – 18.10.2026

## Ergebnis

Die aktuell rekonstruierte Radom-Trennlinie liegt deutlich **vor** der ersten vorhandenen ABCDEF-Frontsektion. Eine direkte 3D-Projektion auf die bestehende Outer-Loft-Studie ist deshalb technisch nicht zulässig.

## Verifizierte Lage

Die Radom-Trennlinie liegt im verwendeten Kandidatenrahmen ungefähr bei **X = 52,5 bis 54,6 mm**. Die erste vorhandene Frontsektion **A** beginnt erst bei **X = 110,775 mm**.

Damit fehlt zwischen dem hintersten Punkt der Radom-Trennlinie und Sektion A ein Bereich von rund **56,1 mm** ohne belastbare Nasen-/Radom-Querschnittsgeometrie.

## Konsequenz

Die Datei `F14_ORIGINAL_OUTER_RULED_LOFT_STUDY.FCStd` darf nicht als Zieloberfläche für die 3D-Radom-Trennlinie verwendet werden. Sie beginnt zu weit hinten und ist außerdem weiterhin nur eine nicht freigegebene Studiengeometrie.

Bis belastbare Nasen-/Radom-Querschnitte vor Sektion A vorhanden und im gemeinsamen Koordinatenrahmen verifiziert sind, gelten folgende Sperren:

- keine Freigabe einer 3D-Radom-Trennlinie
- keine Änderung des aktuellen Masters auf dieser Grundlage
- keine Produktions- oder Druckfreigabe der Nasengeometrie

## Neue automatische Schutzprüfung

`analysis/pruefe_radom_gegen_frontsektionen.py` prüft den X-Bereich der rekonstruierten Radom-Trennlinie gegen die vorhandenen ABCDEF-Sektionen. Die Prüfung arbeitet fail-closed und dokumentiert das Ergebnis in `analysis/radom_frontsektionen_screening_20261018.json`, sobald sie in einer passenden Arbeitsumgebung ausgeführt wird.

## Nächster konstruktiver Schritt

1. belastbare Nasen-/Radom-Querschnitte zwischen der Trennlinie und Sektion A aus den Originalreferenzen ableiten,
2. Maßstab, X-Ursprung und Symmetrieachse unabhängig verifizieren,
3. daraus eine geschlossene Nasen-/Radom-Oberfläche als **Studie** erzeugen,
4. die Drauf- und Seitenansicht der Trennlinie auf diese Oberfläche projizieren,
5. erst bei übereinstimmender Projektion den 3D-Radomverlauf als Kandidat in den sichtbaren FreeCAD-Stand übernehmen.

Der aktuelle Master bleibt unverändert.
