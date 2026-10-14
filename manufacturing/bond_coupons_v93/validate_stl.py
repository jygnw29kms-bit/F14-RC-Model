from pathlib import Path
base=Path(r"C:\Users\dezen\Desktop\F14-RC-Model\manufacturing\bond_coupons_v93")
for p in sorted(base.glob("*.stl")):
    txt=p.read_text()
    n=txt.count("facet normal")
    verts=[]
    for line in txt.splitlines():
        s=line.strip()
        if s.startswith("vertex "):
            _,x,y,z=s.split(); verts.append((float(x),float(y),float(z)))
    assert n==12 and len(verts)==36, (p,n,len(verts))
    xs=[x for x,_,_ in verts]; ys=[y for _,y,_ in verts]; zs=[z for _,_,z in verts]
    print(p.name,"facets",n,"bbox",min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))