# F-14: v334/v335 Bauraum der Carbon-Flügelverbinder

**09.11.2026 · FreeCAD-Konstruktionsstudie · nicht druck- oder flugfreigegeben**

Die v282-Schwenkflügel haben sechs 8×6-mm-Carbonrohrverbinder an der Flügelsegmentfuge. Der nominelle Aufnahmedurchmesser beträgt 8,3 mm. Für die spätere leichte, hohle Flügelbauweise wurden separate zylindrische Verstärkungshülsen gegen den bestehenden v282-Flügelvolumenkörper verglichen: 3 Positionen × 2 Flügel × 2 Segmenthälften = **12 Positionen**.

| Hülse außen | Nominale radiale Hülsenwand | Vollständig in bestehender Kontur bei |
|---|---:|---:|
| 8,6 mm | 0,15 mm | 12/12 |
| 9,0 mm | 0,35 mm | 10/12 |
| 9,5 mm | 0,60 mm | 8/12 |
| 10,0 mm | 0,85 mm | 0/12 |

Eine zusätzliche v334-Studie ergab bei 11/12 mm Durchmesser noch größere Konturüberschreitungen.

**Entscheidung:** Keine der geprüften Hülsen ist als tragende Verbindung freigegeben. Die einzige vollständig passende Variante mit 8,6 mm OD wäre nur 0,15 mm dick und praktisch keine belastbare Verstärkung. Bei größeren Durchmessern kollidiert die ringförmige Hülse lokal mit der aerodynamischen Flügelaußenkontur. Auch 9 mm ist wegen der zwei vorderen Randfälle keine durchgehende Lösung.

**Nächste echte Konstruktionsaufgabe:** Eine integrierte Aufnahme aus schalenintegrierten lokalen Stegen/Gurten und längerer Lastübertragung entwickeln, nicht bloß einen dünnen Ring um das Carbonrohr. Dafür muss zuerst eine hohle, FDM-gerechte Flügelstruktur mit definierten Wandstärken und Fasergurten konstruiert werden. Anschließend Fügeflächen, Klebstoff, Druckorientierung, Scher-/Biegelasten, Torsion und Passprobe verifizieren.

FreeCAD-Daten:
- `migration/freecad/F14_v334_JOINER_REINFORCEMENT_ENVELOPE.FCStd`
- `migration/freecad/F14_v335_JOINER_REINFORCEMENT_SIZING.FCStd`
- `migration/freecad/freecad_v334_joiner_reinforcement_envelope_audit.json`
- `migration/freecad/freecad_v335_joiner_reinforcement_sizing_audit.json`

Diese Studien ändern den freigegebenen Basiskandidaten v282 nicht. Sie zeigen quantitativ, warum mehr Material ohne geänderte Lastpfade keine tragfähige Lösung wäre.
