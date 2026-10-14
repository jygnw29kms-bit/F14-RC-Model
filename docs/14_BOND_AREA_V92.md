# Wing insert bond-area verification — v92

v91 used each BRep face's minimum distance to the inner skin and credited the complete face area when that minimum was <= 0.25 mm. An independent review correctly identified that this can over-credit area and that `pointOnFace.y` does not geometrically clip a face at the axial boundary.

v92 therefore replaces v91's usable-area claim with a conservative pointwise surface quadrature.

## Result

- v91 candidate area: 680.1299 mm² (superseded as verified usable area)
- v92 dominant v91 subset sampled: 544.9105 mm² = 80.12% of the old candidate area
- ignored v91 candidate area: 135.2194 mm² (credited as zero in v92)
- conservative pointwise usable bond area: 66.3576 mm²
- SF3 equivalent torsion-transfer force: 110.8445 N
- required average bond shear on v92 lower bound: 1.6704 MPa

The method samples bounded BRep-face UV space at two resolutions, clips each sample point at the actual axial Y limit, checks point-to-skin distance, and credits the smaller usable fraction from both resolutions. The unexamined 19.88% of v91 area receives no credit.

## Release state

Geometry now has a conservative bond-area lower bound, but adhesive allowables, peel/stress concentration, printed-material surface preparation, environmental conditioning and physical coupons remain unverified. No print or flight release is granted by v92.