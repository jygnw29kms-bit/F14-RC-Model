import Part
s=Part.makeBox(1,1,1)
print([(n,getattr(s,n).__doc__) for n in dir(s) if any(k in n.lower() for k in ['volume','mass','moment'])])
