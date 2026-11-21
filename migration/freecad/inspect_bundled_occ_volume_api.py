import Part
from OCC.Core.BRepGProp import brepgprop
print([n for n in dir(Part) if 'occ' in n.lower()]);print(brepgprop.VolumeProperties.__doc__)
