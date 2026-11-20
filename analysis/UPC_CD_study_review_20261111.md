# UPC C–D fairing study review

The source in analysis/original_front_sources/CD_projection_samples_v2.json corrects two lower boundary picks. At raster X 1225 and 1250 the old picks fell on the separate section E drawing. The corrected points lie on the plan outline. Nine later stations lack a usable width pick because the wing obscures the outline.

| Source X (px) | Width residual of the original study loft (mm) |
| --- | ---: |
| 1225 | -12.91 |
| 1250 | -26.18 |
| 1275 | -38.66 |
| 1300 | -50.62 |

The four local fairing patches use four intermediate profiles, two assumed edge heights per side, and attachment points at 80% of each section's lateral extent. The ruled Bézier patches showed normal changes up to 1.81° across their internal segment joints at 48 sampled points. The smooth loft variants gave these measurements over X 417.820–457.354 mm in the study frame.

- 228 intermediate sections gave a maximum sampled attachment gap of 0.003886 mm and a maximum lateral deviation from the plan polyline of 0.082669 mm.
- 24 midpoint normal comparisons against the study fuselage gave 0.024°–2.205°.
- Twelve attachment curves were cut directly from the study fuselage and reopened in FreeCAD. Their comparison against the smooth patch boundaries is pending.

The smooth loft is the candidate for the next attachment test. Check positional and tangent continuity against the extracted curves before joining the surfaces. Registration to v192 and the physical edge heights remain open. The measurements apply to the isolated study.

Study loft SHA-256: A1CB207D14AC861484BCD90B3148915F8F826066CC203EE6B51205004F47FDD9

## Sewn cubic study · 13 November 2026

FreeCAD produced one valid open shell from 56 patches. The reopened shell gave one intersection at each of six previously double-hit positions. The 165 internal seam samples gave position differences below 0.000001 mm and a maximum normal angle of about 0.0000012°. At the 56 patch midpoints, the largest measured offsets were 0.000056 mm to the inner attachment curve and 0.000235 mm to the outer study guide.

The measurements cover a local positive-Y portion in study coordinates. The guide height remains a design assumption. Registration to v192 and the connection to the fuselage are pending.

Local study file SHA-256: 662c5d1a292164e01a2b6256fea430e667f3d762923d2ebdbc3a5eebbd37558c

## Body intersection screen · 14 November 2026

The local C–D study fuselage was cropped to X 417.981–443.992 mm in study coordinates and reopened as one valid solid. Of 280 sampled shell points, 115 classified inside the cropped fuselage. A separate FreeCAD section and inside/outside classification found one crossing at 43 of 56 section midpoints and three crossings at the other 13. These 13 sampled positions lie between X 421.759 and 429.429 mm. The trim path remains unresolved.

Crossing report SHA-256: ab9afef2bfc282984b6a0d6dbbaac617dd7c6283c6840a066ccc323b82c7c098

## Follow-up trim checks · 15 November 2026

Of 168 sampled sections, 131 showed one crossing and 37 showed three in the tested interior parameter range. The longest intersection wire spans 26.012 mm in X. After excluding hits near the patch boundaries, seven of its 39 sampled X planes still contain three hits. In the second region the 17 recorded edges form a connected sequence with reversals in X. Selecting intersections by transverse order alone leaves the trim unresolved.

FreeCAD identified one valid closed intersection wire with three edges and a total length of 0.133 mm. Its X bounds are 427.164 to 427.229 mm in study coordinates. The physical significance of this local feature remains unresolved.

Closed-wire report SHA-256: 81b30af39f0b89cc6557508be03a3edc6488b6a088425ebd5631b042a4532b2e

## Boolean trim trial

FreeCAD reported valid inside and outside results against the local body slab. The outside result includes one shell of 736.756 mm2 and eight smaller shells. The original area minus the sum of both output areas is approximately -0.000036 mm2. FreeCAD logged topology hasher mismatch warnings during the run. The largest outside component was saved separately and reopened as one valid shell with 69 faces and an unchanged area of 736.756 mm2. The topology warnings and disposition of the eight smaller components remain open. Local study file SHA-256: 70425d230512dcdf840e0beba2c00ccb5c8b29f118a66ee64c3ae0d0ac19ad1c

Boolean report SHA-256: e392fc4886799b6a74cef8da0272ecdde089f11fc8ad66903f685dd49254cae8

A repeat cut reproduced the warnings and nine valid outside shell components. The eight detached shells total 0.227406 mm2, or 0.03086% of the outside area. The component report records area, face count and bounds in study coordinates. Area alone is insufficient to decide whether these components affect the attachment.

Component report SHA-256: b6f08d9961ef433969d2689f546b90d5d85c4b05e37f5351ff077f1a4ad34b62

FreeCAD minimum distances from the eight detached shells to the largest outside shell range from 5.515 to 6.977 mm. The study coordinates and nearest-point pairs are recorded in the distance report. The trim remains a local candidate.

Distance report SHA-256: ab360f27b2cf008e6d313139334db4be8c3cf0b837835a8ebe4501c2caea1b15

A FreeCAD 1.1.4 control run serialized both input shapes to BREP strings and reimported them into fresh Part shapes before cutting. It returned a valid result with 91 faces and nine shells, matching all component areas within 0.000000001 mm2. The control run emitted no topology hasher mismatch warnings. The attachment remains under study.

Control report SHA-256: 081f00e52f73faa6e76ebbfc6e8442ade0f6ea31d925fb0601f5c61b70773a67

The reopened 69-face outside shell has a single valid closed boundary wire formed by 148 edges incident to one face each. Its measured length is 131.697 mm. This check covers the local shell perimeter. Fit against the main fuselage remains pending.

Boundary report SHA-256: 86fefa3da3889bd24205aabb31b936bfd923a5310f1014e4a9fe0e8f44beb13b

## Diagnostic comparison with v192

Without applying a registration transform, the common operation with FUSELAGE_CURRENT in v192 returned all 69 faces and the entire 736.756 mm2 area of the retained study shell. This indicates containment or coincidence in the tested coordinates. Registration and surface attachment require further checks. The study body used for the earlier trim came from C_TO_D in F14_ORIGINAL_OUTER_RULED_LOFT_STUDY.FCStd.

Comparison report SHA-256: 89581ab5ea62569873335b6e213bbec05c9f4453c30c5dd758fb7191f2c850f3

A follow-up FreeCAD check classified all 148 shell vertices strictly inside FUSELAGE_CURRENT, with distances to its faces between 7.921 and 25.247 mm. These are measurements in the untransformed coordinates. They establish that the current study placement requires registration work before attachment. Face centers of mass provided no on-surface samples in the earlier attempted screen.

Vertex report SHA-256: 454999abf5cd3473d46a970b48608910f24a2dc0589bb18b13b68f0210a3f0cd

## Koordinatenbezug der Studie

Die Quelldatei analysis/original_front_sources/front_shared_frame_candidate.json beschreibt die Skalierung aus der Draufsichtbreite und eine gleich gewichtete Anpassung an Ober- und Unterkante der Seitenansicht. Die Datei front_vertical_registration_candidates.json kennzeichnet die gemeinsame Wasserlinie als ungeprüft. Auch ABCDEF_shared_frame_candidate.json führt metric_registration_verified=false.

Das Aufbauskript migration/freecad/normalize_datums_v191.py erzeugt FUSELAGE_CURRENT aus parametrisierten Stationsprofilen neu. Die dortige Z-Verschiebung um -187.59240693460868 mm gilt für die ausdrücklich aufgeführten Flügel- und Einbauobjekte. Daraus lässt sich keine bestätigte Transformation der C-D-Studie ableiten. Als nächster Schritt sind homologe Quellenbezüge für die Studienprofile und den aktuellen Rumpf zu vergleichen.

Die weitere Quellenprüfung präzisiert den Rumpfbezug. Das Skript workspace/RC-F14-Tomcat/Scripts/extract_upc_30stations_scaled.py setzt den Höhenursprung aus den ersten zehn Spalten der Nasenkontur. Der Frontprofilrahmen setzt Z=0 an der gezeichneten E-Achse. Der Bericht analysis/original_front_sources/v191_z_origin_extrapolation_provenance.json rekonstruiert die Verschiebung der Flügelobjekte als Extrapolation aus Flügelprofildaten und kennzeichnet die Schwenkpunkt-Wasserlinie als ungeprüft.

Ein rechnerischer Vergleich der Kandidatenbreiten mit linear interpolierten Daten aus analysis/upc_fuselage_30stations_scaled.json ergibt bei C 230,61 gegenüber 248,08 mm, bei D 211,75 gegenüber 239,60 mm, bei E 204,94 gegenüber 218,42 mm und bei F 209,28 gegenüber 225,47 mm. Dies ist ein Datenvergleich an den Kandidaten-X-Positionen. Native Querschnitte des Hauptmodells sind dafür noch zu prüfen. Für die Integration sind die Quellenbezüge sowie Form und Skalierung abzugleichen.

Die native FreeCAD-Prüfung an denselben Kandidaten-X-Positionen ergab jeweils einen gültigen Rumpfquerschnitt. Seine Breiten betragen C 247,563 mm, D 250,906 mm, E 220,444 mm und F 225,052 mm. Die Kandidatenprofile messen dort 230,613 mm, 211,755 mm, 204,941 mm und 209,282 mm. Der native Vergleich bestätigt Formunterschiede und zeigt zugleich Abweichungen zur einfachen Interpolation der Stationsbreiten. Eine bloße Höhenverschiebung kann diese Breitenunterschiede nicht beseitigen.

Querschnittsbericht SHA-256: 2b5c444d9be959fd8178ddbed1007c7e2b1eff37e2d5c1bdc95cacab27a52991

## Neuerer Längsregistrierungsnachweis auf main

Das Dokument docs/SEITEN_X_REGISTRIERUNG_20261021.md ist auf main vorhanden (Git-Blob cd250c2bfa3945f1f2bbc7194fac4a1b7f72d1ef). Es unterstützt einen Engineering-X-/FS-Kandidaten aus drei homologen Navy-/UPC-Seitenansichtsmerkmalen mit nominal 0,185 Pixel RMS. Die nasenrelativen X-Kandidaten im 900-mm-Modell betragen C 391,900 mm und D 580,514 mm. Die bisher untersuchten Profile verwenden C 403,325 mm und D 595,848 mm. Die Querschnittsvergleiche oben beziehen sich auf diese historischen Kandidatenpositionen.

Damit ist die ältere NADC-/UPC-Prüfung mit offenem Zweipunkt-Längsabgleich für diesen neueren Seiten-X-Kandidaten überholt. Die absolute Z-/Waterline-Registrierung bleibt laut neuerem Dokument offen. Die Zuordnung der Studienprofile muss längs und vertikal gemeinsam nachvollzogen werden.

An den neueren nominalen X-Kandidaten wurden native FreeCAD-Querschnitte des Hauptrumpfs geprüft. Die Breiten betragen C 238,232 mm, D 264,394 mm, E 218,494 mm und F 225,888 mm. Zum diagnostischen Vergleich wurden die vorhandenen Kandidatenprofilbreiten beibehalten. Die Breitenabweichungen bleiben bestehen. Die Ergebnisse setzen versuchsweise die nasenrelativen X-Werte der neuen Registrierung mit der aktuellen CAD-X-Achse gleich. Eine bestätigte Registrierung des Hauptrumpfs und eine Freigabe der Außenform folgen daraus nicht.

Bericht für neue X-Kandidaten SHA-256: 8802ae2b669fd738ea7e2da09eb9504ce31f4e4ca8b72da664be4d38ac63c515

## Prüfung weiterer Höhenreferenzen

Die Berichte auf main EMI_UPC_vertical_landmark_gate.json und NADC_EMI_WL145_source_convergence.json unterstützen weiterhin keine Zuordnung der UPC-C-Achse zur globalen Wasserlinie. Die Antennenmerkmale an FS411 und FS511 wurden dort als nicht eindeutig homolog verworfen.

NASA CR3992, PDF-Seite 88 (gedruckte Seite 81), Abbildungen 48 und 49, wurde am 20. November 2026 visuell geprüft. Die Darstellung zeigt räumlich versetzte Rumpfquerschnitte sowie die für A488 veränderten Konturen. In der geprüften Abbildung sind keine Stationsnummern, Wasserlinienmaße oder Maßstäbe erkennbar. Sie liefert allein keine metrische Höhenzuordnung der UPC-Profile. Bild-SHA-256 98b19e77814f6f155a6d47b9975e94578b44b083eeceb4ebfaef66840c865722.

Der neuere Bericht analysis/v246_cr3992_wing_wl_transform_gate.json auf main bestätigt die konstante Z-Transformation der Flügelgeometrie aus NASA CR3992 nach lokalem CAD. Er rekonstruiert 187,59240693460868 mm über eine direkte Profilreferenz und einen Vergleich der CAD-Höhenbereiche. Damit ergänzt er die oben beschriebene historische Extrapolationsherkunft. Die absolute Rumpf-Wasserlinie, die Schwenkpunkt-Wasserlinie und der gemeinsame absolute Rumpf-/Flügel-Höhenbezug bleiben im Bericht offen. CURRENT.json auf main führt weiterhin v192 als Hauptstand. Die höheren Versionsnummern der Prüfberichte stellen allein keinen Wechsel des Hauptmodells dar.

## Herkunft der D-Breitenskalierung

Die SHA-256-Prüfsummen der D-Kontur v49 und der Registrierung v50 stimmen mit den zusätzlichen Eingaben von ABCDEF_shared_frame_candidate.json überein. Das historische source_D_registration.py berechnet den isotropen Multiplikator aus der korrigierten Konturbreite und der plan_body_width_pixels-Angabe der älteren D/E-Registrierung v12. Dort stehen für D eine Draufsichtbreite von 401,722657665 Pixeln und eine X-Kandidatenposition von 1562,739579560 Pixeln. Der neuere Seitenriss-Tick liegt bei 1561,5 Pixeln. Diese Nähe belegt keine gemeinsame Registrierung von Drauf- und Seitenansicht. Die Breitenquelle ist daher im weiteren Vergleich mit ihrer historischen Ansichtszuordnung zu behandeln.

Die historische D/E-Datei enthält obere und untere Draufsichtspunkte, kennzeichnet source_station_pairing_verified=false und warnt vor der mehrdeutigen oberen D-Projektion im Bereich der Flügelwurzel. Das originale UPC-Bild wurde visuell gesichtet. Es zeigt unterschiedliche Flügelstellungen in den Draufsichten und separat gezeichnete Profile. Die korrigierte D-Konturdigitalisierung beseitigt somit die offene Zuordnung ihrer geerbten Breitenreferenz noch nicht.

Der Bericht UPC_NASA_lower_20deg_wing_screen.json auf main verwendet für die untere ausgefahrene Flügelhälfte einen Quermaßstab von 0,45285456150676867 Fullscale-inch pro Pixel. Er beruht auf einer halben Bildspannweite von 849,5 Pixeln und NASA-WBL 384,69995 inch. Mit dem RC-Maßstab 1,1697428086486623 mm/in ergibt die historische D-Breite von 401,722657665 Pixeln diagnostisch 212,802 mm. Dies liegt nahe an der Kandidatenbreite 211,755 mm. Die Zuordnung der gemessenen Draufsichtlinien zur D-Station bleibt dabei als Annahme bestehen. Der Unterschied zum nativen Hauptmodellquerschnitt wird durch diesen alternativen Quermaßstab allein nicht erklärt.

## Getrennte Rasterherkunft der Hauptmodell-Stationen

Das historische Skript workspace/RC-F14-Tomcat/Scripts/extract_upc_30stations_scaled.py verwendet UPC_page_041.png und eine blaue Farbmaske. Es waehlt die zwei groessten zusammenhaengenden Farbkomponenten als Drauf- und Seitenkontur. Beide Ansichten werden getrennt auf die Laenge 900*(1591.67/1629.17) mm skaliert. Die 30 Stationen liegen gleichmaessig zwischen 1 und 99 Prozent dieser Laenge. Die Halbbreite ist jeweils der groessere Abstand der Maskenextrema zur Mitte der Draufsicht-Begrenzungsbox, mit einem Abtastfenster von fuenf Pixelspalten. Der Hoehenursprung stammt aus den ersten zehn Spalten der Seitenkontur.

Dies ist ein anderer Rekonstruktionsweg als die separat digitalisierten A-F-Querschnittsprofile. Gleiche Stationsnamen oder eine Hoehenverschiebung allein stellen keine gemeinsame Quellenregistrierung her. Der naechste Vergleich muss die Rasterkonturen und die Zuordnung ihrer Laengskoordinaten gemeinsam pruefen, bevor eine Formkorrektur am Hauptmodell erfolgt. Das historische Skript wurde nur gelesen; seine fest eingetragenen alten Dateipfade wurden nicht ausgefuehrt oder neu angelegt. Bild-SHA-256: fc2a4dc77e43c64c21df205123ad36de0323e0bbe3c3bcdb693ccd19c356d026. Keine neue CAD-Geometrie oder Freigabe aus dieser Quellenpruefung.

## Stationsauswahl erklaert den nativen D-Querschnitt

normalize_datums_v191.py verwendet nur 16 der 30 extrahierten Stationen. Am neueren nominalen D-X=580,513580747 mm liegen die ausgewaehlten Nachbarstationen bei X=573,354 und 632,781 mm. Lineare Interpolation ihrer vollen Breiten ergibt 264,394431474 mm. Das stimmt mit dem zuvor nativ gemessenen, auf sechs Nachkommastellen angegebenen Wert 264,394431 mm innerhalb von 0,000001 mm ueberein. Der Vergleich mit allen 30 Stationen bildet diese ausgewaehlte Loft-Eingabe dagegen nicht nach. Dies erklaert hier den Unterschied zwischen einfacher Dateninterpolation und CAD-Schnitt. Es bestaetigt weder die Originaltreue dieser Kontur noch eine gemeinsame Registrierung mit dem D-Profil. Ausgefuehrt wurde eine Rechnung mit vorhandenen Stationsdaten, kein neuer CAD-Lauf.

## Sichtpruefung der Leitkonturquelle, 20. November 2026

UPC_page_041.png (gedruckte Seite 29) zeigt in Abbildung 5.3 blaue Leitkonturen ueber Drauf- und Seitenansicht und in Abbildung 5.4 die in SolidWorks angelegten Ebenen. Der Begleittext beschreibt 30 Ebenen, deren Positionen unter anderem an erkennbaren Querschnitten der Zeichnungen und zusaetzlich an zu grossen Zwischenraeumen orientiert wurden. Das historische Extraktionsskript erzeugt dagegen 30 gleichmaessige Laengsanteile zwischen 0,01 und 0,99. Die Zahl 30 allein belegt deshalb keine Uebernahme der urspruenglichen Ebenenpositionen aus der Arbeit. Die hier rekonstruierte Stationsliste ist als eigene Rasterabtastung der Leitkontur zu behandeln. Die Seite liefert in dieser Darstellung keine numerische Liste homologer Ebenenkoordinaten. Fuer den naechsten Registrierungsversuch sind eindeutig wiedererkennbare Merkmale derselben Ansichten erforderlich; die Gleichsetzung ueber die Stationsanzahl scheidet als Nachweis aus.
