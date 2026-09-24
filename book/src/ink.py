# -*- coding: utf-8 -*-
"""Hand-drawn ink engine: wobbly double-stroked lines, cross-hatching,
lumpy organic shapes. Everything curves; nothing is geometrically true."""
import math, random

# One Fish-era palette: warm cream, soft black, and three flats
PAPER="#FAF4E4"; INK="#1E1B1A"
RED="#D6392B"; BLUE="#2E6DA8"; YELLOW="#F0BE3C"; PINK="#E4907F"; CREAM="#FDFAF0"
GREEN="#6E9A52"; NIGHT="#22303F"; MOON="#F6EFD8"

def _noise(seed):
    r=random.Random(seed)
    return lambda: r.uniform(-1,1)

def wob(pts, amp=1.6, seed=1, dense=3):
    """Resample a polyline and push every point off true."""
    r=random.Random(seed); out=[]
    for i in range(len(pts)-1):
        x1,y1=pts[i]; x2,y2=pts[i+1]
        seg=max(1,int(math.hypot(x2-x1,y2-y1)/16)*dense)
        for k in range(seg):
            t=k/seg
            out.append((x1+(x2-x1)*t + r.uniform(-amp,amp),
                        y1+(y2-y1)*t + r.uniform(-amp,amp)))
    out.append((pts[-1][0]+r.uniform(-amp,amp), pts[-1][1]+r.uniform(-amp,amp)))
    return out

def smooth(pts, close=False):
    """Catmull-Rom-ish path through points, as one smooth d string."""
    if len(pts)<2: return ""
    d=f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    n=len(pts)
    for i in range(n-1):
        p0=pts[i-1] if i>0 else pts[0]
        p1=pts[i]; p2=pts[i+1]
        p3=pts[i+2] if i+2<n else pts[-1]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f" C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    if close: d+=" Z"
    return d

def stroke(pts, w=3.0, seed=1, amp=1.4, close=False, col=None, op=1.0, twice=True):
    """An inked line: drawn once, then again slightly off, the way a nib doubles back."""
    col=col or INK
    a=smooth(wob(pts,amp,seed),close)
    s=(f'<path d="{a}" fill="none" stroke="{col}" stroke-width="{w}" '
       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')
    if twice:
        b=smooth(wob(pts,amp*0.8,seed+977),close)
        s+=(f'<path d="{b}" fill="none" stroke="{col}" stroke-width="{w*0.62:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op*0.55:.2f}"/>')
    return s

def lump(cx,cy,rx,ry,seed=3,n=15,amt=0.12,squash=0.0):
    """An organic blob outline as a point list — never a true ellipse."""
    r=random.Random(seed); pts=[]
    for i in range(n):
        a=2*math.pi*i/n + r.uniform(-0.05,0.05)
        k=1+r.uniform(-amt,amt)
        y=math.sin(a)*ry*k
        if squash and y>0: y*= (1-squash)
        pts.append((cx+math.cos(a)*rx*k, cy+y))
    pts.append(pts[0])
    return pts

def shape(pts, fill, seed=1, w=3.0, amp=1.8, hatch=None, hid=None):
    """Filled organic shape with an inked outline, optional hatching."""
    d=smooth(wob(pts,amp,seed),True)
    s=f'<path d="{d}" fill="{fill}" stroke="none"/>'
    if hatch and hid:
        s+=(f'<clipPath id="{hid}"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#{hid})">{hatch}</g>')
    s+=stroke(pts,w,seed+41,amp,close=True)
    return s

def hatching(x0,y0,x1,y1,step=9,ang=-32,col=None,w=1.5,op=0.5,seed=7,cross=False):
    """Diagonal pen hatching to sit inside a clip."""
    col=col or INK; r=random.Random(seed); out=[]
    a=math.radians(ang); dx,dy=math.cos(a),math.sin(a)
    L=math.hypot(x1-x0,y1-y0)*1.6
    n=int(L/step)+4
    px,py=-dy,dx
    cx,cy=(x0+x1)/2,(y0+y1)/2
    angs=[ang, ang+74] if cross else [ang]
    for A in angs:
        a=math.radians(A); dx,dy=math.cos(a),math.sin(a); px,py=-dy,dx
        for i in range(-n,n):
            ox,oy=cx+px*i*step, cy+py*i*step
            j=r.uniform(-1.4,1.4)
            out.append(f'<line x1="{ox-dx*L/2+j:.1f}" y1="{oy-dy*L/2+j:.1f}" '
                       f'x2="{ox+dx*L/2+j:.1f}" y2="{oy+dy*L/2+j:.1f}" '
                       f'stroke="{col}" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>')
    return "".join(out)

def tuft(x,y,n=3,l=18,spread=26,seed=1,w=2.6,col=None):
    """The curling hair/fur flick that makes a shape feel drawn."""
    col=col or INK; r=random.Random(seed); out=[]
    for i in range(n):
        a=math.radians(-90 + (i-(n-1)/2)*spread + r.uniform(-8,8))
        ll=l*r.uniform(0.75,1.25)
        ex,ey=x+math.cos(a)*ll, y+math.sin(a)*ll
        cx,cy=x+math.cos(a)*ll*0.5 - math.sin(a)*ll*0.45, y+math.sin(a)*ll*0.5 + math.cos(a)*ll*0.45
        out.append(f'<path d="M {x:.1f},{y:.1f} Q {cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" '
                   f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    return "".join(out)

def curl(x,y,turns=1.6,r0=3,r1=17,seed=1,w=2.4,col=None,flip=1):
    """A Seussian spiral tail."""
    col=col or INK; pts=[]
    steps=int(26*turns)
    for i in range(steps+1):
        t=i/steps; a=t*turns*2*math.pi*flip
        rr=r0+(r1-r0)*t
        pts.append((x+math.cos(a)*rr, y+math.sin(a)*rr*0.9))
    return stroke(pts,w,seed,1.0,twice=False,col=col)

def svg(w,h,body,bg=PAPER):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def cloud(cx,cy,rx,ry,fill=None,seed=1,w=3.2,lobes=None):
    """A lobed cloud with one continuous inked outline (silhouette-then-fill)."""
    import random as _r
    fill=fill or CREAM; r=_r.Random(seed)
    lobes=lobes or [(-0.80,0.16,0.38),(-0.44,-0.26,0.50),(0.00,-0.46,0.58),
                    (0.44,-0.22,0.49),(0.82,0.16,0.37),(0.26,0.28,0.45),(-0.26,0.30,0.43)]
    outs=[]; ins=[]
    for k,(ox,oy,rr) in enumerate(lobes):
        R=rr*rx*(1+r.uniform(-0.05,0.05))
        x,y=cx+ox*rx, cy+oy*ry
        outs.append(smooth(wob(lump(x,y,R+w*0.9,R*0.94+w*0.9,seed=seed+k,n=20,amt=0.05),1.2,seed+k),True))
        ins.append(smooth(wob(lump(x,y,R,R*0.94,seed=seed+k,n=20,amt=0.05),1.2,seed+k),True))
    g='<g fill="'+INK+'">'+"".join(f'<path d="{d}"/>' for d in outs)+'</g>'
    g+='<g fill="'+fill+'">'+"".join(f'<path d="{d}"/>' for d in ins)+'</g>'
    return g
