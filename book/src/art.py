# -*- coding: utf-8 -*-
"""Illustration library for 'One Bot, Two Bot, Red Bot, Grok Bot'.
Flat mid-century cut-paper look: bold shapes, limited palette, wobbly ink.
Deliberately NOT Dr. Seuss's drawing style."""
import math, random

INK="#232021"; PAPER="#F7F1E3"; RED="#E14B28"; TEAL="#2B7C86"
GOLD="#E9A93A"; LILAC="#8B7AB8"; GREEN="#5E8C4A"; NIGHT="#1D2A3A"; CREAM="#FBF6EA"

def wobble(pts, amt=2.0, seed=1):
    r=random.Random(seed); out=[]
    for x,y in pts: out.append((x+r.uniform(-amt,amt), y+r.uniform(-amt,amt)))
    return out

def poly(pts, fill="none", stroke=INK, w=3, close=True, op=1.0):
    d="M "+" L ".join(f"{x:.1f},{y:.1f}" for x,y in pts)+(" Z" if close else "")
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>'

def blob(cx,cy,rx,ry,fill,seed=3,n=18,amt=0.06,stroke=INK,w=3):
    r=random.Random(seed); pts=[]
    for i in range(n):
        a=2*math.pi*i/n
        k=1+r.uniform(-amt,amt)
        pts.append((cx+math.cos(a)*rx*k, cy+math.sin(a)*ry*k))
    d="M "+" ".join(f"{x:.1f},{y:.1f}" for x,y in [pts[0]])
    # smooth with quadratic through midpoints
    d=f"M {(pts[0][0]+pts[-1][0])/2:.1f},{(pts[0][1]+pts[-1][1])/2:.1f} "
    for i in range(n):
        p=pts[i]; nxt=pts[(i+1)%n]
        mx,my=(p[0]+nxt[0])/2,(p[1]+nxt[1])/2
        d+=f"Q {p[0]:.1f},{p[1]:.1f} {mx:.1f},{my:.1f} "
    d+="Z"
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'

def eye(cx,cy,r=13,look=(0,0),lid=False):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>'
    s+=f'<circle cx="{cx+look[0]}" cy="{cy+look[1]}" r="{r*0.42:.1f}" fill="{INK}"/>'
    if lid:
        s+=f'<path d="M {cx-r-1},{cy-2} Q {cx},{cy-r*1.5} {cx+r+1},{cy-2}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    return s

def antenna(cx,cy,h=34,tilt=0,col=RED,knob=7):
    ex=cx+math.sin(math.radians(tilt))*h; ey=cy-math.cos(math.radians(tilt))*h
    return (f'<path d="M {cx},{cy} Q {cx+tilt*0.4},{cy-h*0.6} {ex:.1f},{ey:.1f}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{knob}" fill="{col}" stroke="{INK}" stroke-width="3"/>')

def limb(x1,y1,x2,y2,bend=14,w=3):
    mx,my=(x1+x2)/2,(y1+y2)/2
    return f'<path d="M {x1},{y1} Q {mx+bend},{my} {x2},{y2}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'

def foot(x,y,d=1):
    return f'<path d="M {x},{y} q {10*d},2 {13*d},9" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'

def bot(cx, cy, s=1.0, col=RED, seed=5, eyes=2, mood="open", tilt=-8, arms=True, legs=True, look=(0,0)):
    """Standard little bot. cy = centre of body."""
    g=[]
    bw,bh=52*s,58*s
    if legs:
        g.append(limb(cx-14*s,cy+bh*0.85,cx-20*s,cy+bh*1.5,bend=-6))
        g.append(limb(cx+14*s,cy+bh*0.85,cx+20*s,cy+bh*1.5,bend=6))
        g.append(foot(cx-20*s,cy+bh*1.5,-1)); g.append(foot(cx+20*s,cy+bh*1.5,1))
    g.append(blob(cx,cy,bw,bh,col,seed=seed,amt=0.05))
    if arms:
        g.append(limb(cx-bw*0.95,cy-6*s,cx-bw*1.7,cy+16*s,bend=-10))
        g.append(limb(cx+bw*0.95,cy-6*s,cx+bw*1.7,cy-14*s,bend=10))
    g.append(antenna(cx,cy-bh*0.95,h=30*s,tilt=tilt,col=CREAM if col!=CREAM else RED,knob=6*s))
    if mood=="sleep":
        for dx in ((-17*s,17*s) if eyes==2 else (0,)):
            g.append(f'<path d="M {cx+dx-12*s:.1f},{cy-10*s:.1f} q {12*s:.1f},{11*s:.1f} {24*s:.1f},0" '
                     f'fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
    elif eyes==2:
        g.append(eye(cx-17*s,cy-10*s,12*s,look))
        g.append(eye(cx+17*s,cy-10*s,12*s,look))
    elif eyes==1:
        g.append(eye(cx,cy-10*s,19*s,look))
    if mood=="sleep":
        g.append(f'<path d="M {cx-8*s},{cy+18*s} q {8*s},{6*s} {16*s},0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif mood=="open":
        g.append(f'<path d="M {cx-11*s},{cy+16*s} Q {cx},{cy+27*s} {cx+11*s},{cy+16*s}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif mood=="flat":
        g.append(f'<path d="M {cx-11*s},{cy+19*s} L {cx+11*s},{cy+19*s}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif mood=="oh":
        g.append(f'<ellipse cx="{cx}" cy="{cy+19*s}" rx="{7*s}" ry="{9*s}" fill="{INK}"/>')
    return "".join(g)

def person(cx, cy, s=1.0, col=TEAL, hair=INK, seed=9, face="calm", arms=True, hairstyle="bob"):
    """Simple human. cy = centre of torso."""
    g=[]
    th,tw=62*s,40*s
    g.append(limb(cx-10*s,cy+th*0.9,cx-14*s,cy+th*1.7,bend=-5,w=4))
    g.append(limb(cx+10*s,cy+th*0.9,cx+14*s,cy+th*1.7,bend=5,w=4))
    g.append(foot(cx-14*s,cy+th*1.7,-1)); g.append(foot(cx+14*s,cy+th*1.7,1))
    g.append(poly(wobble([(cx-tw,cy+th),(cx-tw*0.7,cy-th*0.55),(cx+tw*0.7,cy-th*0.55),(cx+tw,cy+th)],2,seed),fill=col))
    if arms:
        g.append(limb(cx-tw*0.8,cy-th*0.3,cx-tw*1.6,cy+th*0.4,bend=-8,w=4))
        g.append(limb(cx+tw*0.8,cy-th*0.3,cx+tw*1.6,cy+th*0.4,bend=8,w=4))
    hy=cy-th*0.55-26*s
    g.append(f'<circle cx="{cx}" cy="{hy:.1f}" r="{26*s:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    if hairstyle=="bob":
        g.append(f'<path d="M {cx-27*s},{hy} a {27*s},{27*s} 0 0 1 {54*s},0 q {-6*s},{-9*s} {-27*s},{-9*s} q {-21*s},0 {-27*s},{9*s}" fill="{hair}" stroke="{INK}" stroke-width="3"/>')
    elif hairstyle=="tuft":
        g.append(f'<path d="M {cx-8*s},{hy-24*s} q {8*s},{-14*s} {17*s},{-2*s}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    elif hairstyle=="bun":
        g.append(f'<circle cx="{cx}" cy="{hy-27*s:.1f}" r="{11*s:.1f}" fill="{hair}" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<path d="M {cx-26*s},{hy-4*s} a {26*s},{26*s} 0 0 1 {52*s},0 q {-10*s},{-12*s} {-26*s},{-12*s} q {-16*s},0 {-26*s},{12*s}" fill="{hair}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<circle cx="{cx-9*s:.1f}" cy="{hy-2*s:.1f}" r="{3.4*s:.1f}" fill="{INK}"/>')
    g.append(f'<circle cx="{cx+9*s:.1f}" cy="{hy-2*s:.1f}" r="{3.4*s:.1f}" fill="{INK}"/>')
    if face=="calm":
        g.append(f'<path d="M {cx-7*s},{hy+11*s} q {7*s},{6*s} {14*s},0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif face=="oh":
        g.append(f'<ellipse cx="{cx}" cy="{hy+12*s:.1f}" rx="{5*s:.1f}" ry="{6*s:.1f}" fill="{INK}"/>')
    elif face=="flat":
        g.append(f'<path d="M {cx-7*s},{hy+12*s} L {cx+7*s},{hy+12*s}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    return "".join(g)

def svg(w,h,body,bg=PAPER):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def cloud(cx,cy,rx,ry,fill=CREAM,stroke=INK,w=4,seed=1):
    """A real cloud: overlapping lobes, one clean outline (silhouette-then-fill trick)."""
    import random as _r
    r=_r.Random(seed)
    lobes=[(-0.80,0.16,0.38),(-0.44,-0.26,0.50),(0.00,-0.44,0.57),
           (0.44,-0.22,0.49),(0.82,0.16,0.37),(0.26,0.26,0.45),(-0.26,0.28,0.43)]
    ell=[]
    for ox,oy,rr in lobes:
        k=1+r.uniform(-0.05,0.05); R=rr*rx*k
        ell.append((cx+ox*rx, cy+oy*ry, R, R*0.94))
    sil="".join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{a_+w:.1f}" ry="{b+w:.1f}"/>' for x,y,a_,b in ell)
    inn="".join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{a_:.1f}" ry="{b:.1f}"/>' for x,y,a_,b in ell)
    return f'<g><g fill="{stroke}">{sil}</g><g fill="{fill}">{inn}</g></g>'
