import Mesh
facets=[[(0,0,0),(1,0,0),(0,1,0)],[(0,0,0),(0,1,0),(0,0,1)]]
try:
 m=Mesh.Mesh(facets)
 print('BULK_MESH_OK',m.CountFacets,m.CountPoints,flush=True)
except Exception as e:
 print('BULK_MESH_ERROR',repr(e),flush=True)
