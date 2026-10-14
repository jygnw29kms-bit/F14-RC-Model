"""Constrain candidate internal carbon caps to the existing polygonal wing loft.

No new exterior geometry is introduced. The inherited wing OML itself is provisional.
"""
import ast
import json
import math
from pathlib import Path

PROJECT=Path(__file__).resolve().parents[1]


def coefficients():
    source=PROJECT/'cad/fusion/F14TomcatRC/F14TomcatRC.py'
    tree=ast.parse(source.read_text(encoding='utf-8-sig'))
    func=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_f14_wings_20deg')
    result={}
    for n in func.body:
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('uw209','lw209','uw208','lw208'):
            result[n.targets[0].id]=ast.literal_eval(n.value)
    assert len(result)==4
    return result


def cst(weights,x):
    n=len(weights)-1
    return math.sqrt(x)*(1-x)*sum(math.comb(n,i)*a*x**i*(1-x)**(n-i) for i,a in enumerate(weights))


def profile_samples(r,coef):
    """Corresponding points of the two existing 28-point wing profiles, in mm."""
    chord=150.15+(55.03-150.15)*r
    le=456.5-20.4+math.tan(math.radians(20))*319*r
    data=[]
    for i in range(28):
        x=0.5*(1-math.cos(math.pi*i/27))
        vals=[]
        for tag,tc,base,c in [('209',0.0965,0.09,150.15),('208',0.0891,0.08,55.03)]:
            u=cst(coef['uw'+tag],x); l=cst(coef['lw'+tag],x)
            cam=(u+l)/2; half=(u-l)/2*tc/base
            vals.append((24+c*(cam+half),24+c*(cam-half)))
        upper=(1-r)*vals[0][0]+r*vals[1][0]
        lower=(1-r)*vals[0][1]+r*vals[1][1]
        data.append((le+x*chord,upper,lower))
    return data,chord,le


def bounded_height(samples,x0,x1,skin):
    upper=[]; lower=[]
    for a,b in zip(samples,samples[1:]):
        lo=max(x0,a[0]); hi=min(x1,b[0])
        if lo>hi: continue
        dx=b[0]-a[0]
        su=(b[1]-a[1])/dx; sl=(b[2]-a[2])/dx
        for x in [lo,hi]:
            upper.append(a[1]+su*(x-a[0])-skin*math.sqrt(1+su*su))
            lower.append(a[2]+sl*(x-a[0])+skin*math.sqrt(1+sl*sl))
    assert upper and lower
    return min(upper),max(lower)


def build_stations(skin=0.8,width=16,tip_width=8,cap=1,web=0.8,clearance=0.2):
    coef=coefficients(); stations=[]
    for i in range(33):
        r=i/32
        samples,chord,le=profile_samples(r,coef)
        xc=le+0.30*chord
        local_width=width+(tip_width-width)*r
        x0,x1=xc-local_width/2,xc+local_width/2
        top,bottom=bounded_height(samples,x0,x1,skin+clearance)
        separation=top-bottom-cap
        web_height=top-bottom-2*cap
        if web_height<=0:
            raise ValueError(f'No web height at station {i}: {web_height:.3f} mm')
        stations.append(dict(index=i,y_mm=131+319*r,x_mm=xc,x0_mm=x0,x1_mm=x1,cap_width_mm=local_width,
            upper_z0_mm=top-cap,upper_z1_mm=top,
            lower_z0_mm=bottom,lower_z1_mm=bottom+cap,
            web_z0_mm=bottom+cap,web_z1_mm=top-cap,
            cap_centroid_separation_mm=separation,
            I_caps_mm4=2*(local_width*cap**3/12+local_width*cap*(separation/2)**2),
            extreme_fiber_mm=(separation+cap)/2))
    return dict(status='CANDIDATE_NOT_FLIGHT_OR_PRINT_RELEASED',
        external_shape='existing v04 28-point polygonal wing profiles; source fidelity unresolved',
        skin_mm=skin,clearance_mm=clearance,cap_width_root_mm=width,cap_width_tip_mm=tip_width,cap_thickness_mm=cap,
        web_thickness_mm=web,station_count=len(stations),stations=stations)


if __name__=='__main__':
    result=build_stations()
    target=PROJECT/'analysis/wing_spar_stations_v05.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Wrote',target.name,'stations',result['station_count'])
    print('Cap separation root/tip:',result['stations'][0]['cap_centroid_separation_mm'],result['stations'][-1]['cap_centroid_separation_mm'])
