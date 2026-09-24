# -*- coding: utf-8 -*-
"""Characters drawn with the ink engine. Lumpy, droopy, nothing true."""
from ink import *
import math, random

_uid=[0]
def uid(p="c"):
    _uid[0]+=1; return f"{p}{_uid[0]}"

def eye(cx,cy,r=14,look=(0,0),shut=False,seed=1,lashes=False):
    if shut:
        return stroke([(cx-r,cy),(cx-r*0.3,cy+r*0.55),(cx+r*0.3,cy+r*0.55),(cx+r,cy)],
                      2.8,seed,1.0,twice=False)
    g=shape(lump(cx,cy,r,r*1.06,seed=seed,n=18,amt=0.035),CREAM,seed=seed,w=2.3,amp=0.8)
    g+=f'<ellipse cx="{cx+look[0]:.1f}" cy="{cy+look[1]:.1f}" rx="{r*0.36:.1f}" ry="{r*0.40:.1f}" fill="{INK}"/>'
    # heavy Seussian lid
    g+=stroke([(cx-r*1.05,cy-r*0.42),(cx,cy-r*1.12),(cx+r*1.05,cy-r*0.42)],2.9,seed+7,1.2,twice=False)
    if lashes: g+=tuft(cx,cy-r*1.05,3,10,30,seed+3,2.0)
    return g

def hand(x,y,a=0,s=1.0,seed=1):
    """Three splayed fingers."""
    out=[]
    for i in range(3):
        aa=math.radians(a-34+i*34)
        out.append(stroke([(x,y),(x+math.cos(aa)*11*s, y+math.sin(aa)*11*s)],2.4,seed+i,0.8,twice=False))
    return "".join(out)

def bird_foot(x,y,d=1,s=1.0,seed=1):
    out=[stroke([(x,y-6*s),(x,y)],2.6,seed,0.7,twice=False)]
    for i in (-1,0,1):
        out.append(stroke([(x,y),(x+d*(9+i*4)*s, y+ (5 if i==0 else 3)*s)],2.4,seed+i+4,0.7,twice=False))
    return "".join(out)

def bot(cx, cy, s=1.0, col=RED, seed=5, eyes=2, mood="open", tilt=-14,
        arms=True, legs=True, look=(0,0), hatch=True, fur=True):
    """A Grok bot, drawn the way everything else in the book is drawn:
    lumpy pear body, drooping antenna, splayed hands, bird feet."""
    g=[]; bw,bh=50*s,60*s
    r=random.Random(seed)
    if legs:
        for d in (-1,1):
            hx=cx+d*15*s
            g.append(stroke([(hx,cy+bh*0.72),(hx+d*4*s,cy+bh*1.16),(hx+d*(10+r.randint(0,6))*s,cy+bh*1.52)],
                            2.8*s**0.4,seed+d+2,1.4))
            g.append(bird_foot(cx+d*(10+ (6 if d>0 else 4))*s, cy+bh*1.52, d, s*0.95, seed+d))
    body=lump(cx,cy,bw,bh,seed=seed,n=24,amt=0.055,squash=0.05)
    hid=uid("b")
    g.append(shape(body,col,seed=seed,w=2.9*s**0.3,amp=1.35,
                   hatch=hatching(cx-bw*1.2,cy-bh*1.2,cx+bw*1.2,cy+bh*1.2,
                                  step=6.0,ang=-34,w=1.05,op=0.155,seed=seed+3) if hatch else None,
                   hid=hid if hatch else None))
    if fur:
        g.append(tuft(cx-bw*0.60,cy-bh*0.70,4,14*s,24,seed+11,2.0*s**0.4))
        g.append(tuft(cx+bw*0.58,cy-bh*0.68,3,11*s,26,seed+13,1.9*s**0.4))
    if arms:
        for d in (-1,1):
            ex=cx+d*bw*1.72; ey=cy+(14 if d<0 else -16)*s
            g.append(stroke([(cx+d*bw*0.88,cy-4*s),(cx+d*bw*1.35,ey-8*s),(ex,ey)],2.9*s**0.35,seed+d+20,1.6))
            g.append(hand(ex,ey,0 if d>0 else 180,s*0.95,seed+d+30))
    # antenna: droops, then curls, then a knob
    ax,ay=cx+tilt*0.5*s, cy-bh*0.98
    tx,ty=ax+tilt*1.5*s, ay-34*s
    g.append(stroke([(cx,cy-bh*0.88),(ax,ay-18*s),(tx,ty)],2.8*s**0.4,seed+50,1.3))
    g.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{6.5*s:.1f}" fill="{CREAM}" stroke="{INK}" stroke-width="{2.6*s**0.4:.1f}"/>')
    ec=cy-10*s
    if mood=="sleep":
        for dx in ((-17*s,17*s) if eyes==2 else (0,)):
            g.append(eye(cx+dx,ec,13*s,shut=True,seed=seed+60))
    elif eyes==2:
        g.append(eye(cx-17*s,ec,12.5*s,look,seed=seed+60))
        g.append(eye(cx+17*s,ec,12.5*s,look,seed=seed+63))
    else:
        g.append(eye(cx,ec,20*s,look,seed=seed+60))
    my=cy+19*s
    if mood=="open":
        g.append(stroke([(cx-12*s,my-3*s),(cx,my+9*s),(cx+12*s,my-3*s)],2.7*s**0.4,seed+70,1.0,twice=False))
    elif mood=="flat":
        g.append(stroke([(cx-12*s,my),(cx+12*s,my-2*s)],2.7*s**0.4,seed+70,1.0,twice=False))
    elif mood=="oh":
        g.append(shape(lump(cx,my+2*s,7*s,9*s,seed=seed+80,n=9,amt=0.12),INK,seed=seed+80,w=1.6,amp=0.8))
    elif mood=="sleep":
        g.append(stroke([(cx-9*s,my),(cx,my+7*s),(cx+9*s,my)],2.5*s**0.4,seed+70,0.9,twice=False))
    return "".join(g)

def person(cx, cy, s=1.0, col=BLUE, seed=9, face="calm", hairstyle="tuft",
           hair=None, arms=True, nose=True, hatch=True):
    """Seussian human: long droopy limbs, prominent nose, a tuft."""
    g=[]; th,tw=64*s,36*s
    hair=hair or INK
    for d in (-1,1):
        hx=cx+d*11*s
        g.append(stroke([(hx,cy+th*0.86),(hx+d*7*s,cy+th*1.34),(hx+d*5*s,cy+th*1.78)],3.0*s**0.4,seed+d,1.5))
        g.append(shape(lump(cx+d*11*s,cy+th*1.86,15*s,8*s,seed=seed+d+5,n=11,amt=0.14),INK,seed=seed+d+5,w=2.2,amp=1.0))
    body=[(cx-tw,cy+th),(cx-tw*0.66,cy),(cx-tw*0.74,cy-th*0.56),(cx+tw*0.74,cy-th*0.56),
          (cx+tw*0.66,cy),(cx+tw,cy+th),(cx-tw,cy+th)]
    hid=uid("p")
    g.append(shape(body,col,seed=seed,w=2.9*s**0.3,amp=1.4,
                   hatch=hatching(cx-tw*1.4,cy-th,cx+tw*1.4,cy+th*1.2,step=6.0,ang=-30,w=1.05,op=0.14,seed=seed+9) if hatch else None,
                   hid=hid if hatch else None))
    if arms:
        for d in (-1,1):
            ex=cx+d*tw*1.85; ey=cy+th*0.46
            g.append(stroke([(cx+d*tw*0.72,cy-th*0.34),(cx+d*tw*1.5,cy-th*0.02),(ex,ey)],2.9*s**0.35,seed+d+20,1.6))
            g.append(hand(ex,ey,60 if d>0 else 120,s,seed+d+40))
    hy=cy-th*0.56-27*s
    g.append(shape(lump(cx,hy,26*s,28*s,seed=seed+50,n=20,amt=0.045),CREAM,seed=seed+50,w=2.9*s**0.3,amp=1.5))
    if hairstyle=="tuft":
        g.append(tuft(cx+3*s,hy-26*s,4,22*s,26,seed+55,2.6*s**0.4,hair))
    elif hairstyle=="bun":
        g.append(shape(lump(cx-2*s,hy-32*s,14*s,12*s,seed=seed+56,n=11,amt=0.12),hair,seed=seed+56,w=2.5,amp=1.2))
        g.append(stroke([(cx-25*s,hy-6*s),(cx-6*s,hy-26*s),(cx+22*s,hy-10*s)],2.6,seed+57,1.3,twice=False,col=hair))
    elif hairstyle=="frizz":
        g.append(tuft(cx,hy-27*s,7,17*s,17,seed+58,2.3*s**0.4,hair))
    g.append(f'<ellipse cx="{cx-9*s:.1f}" cy="{hy-3*s:.1f}" rx="{3.4*s:.1f}" ry="{3.9*s:.1f}" fill="{INK}"/>')
    g.append(f'<ellipse cx="{cx+10*s:.1f}" cy="{hy-3*s:.1f}" rx="{3.4*s:.1f}" ry="{3.9*s:.1f}" fill="{INK}"/>')
    if nose:
        g.append(stroke([(cx+2*s,hy-1*s),(cx+14*s,hy+7*s),(cx+2*s,hy+11*s)],2.5*s**0.4,seed+60,1.0,twice=False))
    if face=="calm":
        g.append(stroke([(cx-8*s,hy+16*s),(cx,hy+21*s),(cx+9*s,hy+15*s)],2.5*s**0.4,seed+61,0.9,twice=False))
    elif face=="oh":
        g.append(shape(lump(cx,hy+18*s,5.5*s,7*s,seed=seed+62,n=9,amt=0.14),INK,seed=seed+62,w=1.6,amp=0.7))
    elif face=="flat":
        g.append(stroke([(cx-8*s,hy+17*s),(cx+9*s,hy+16*s)],2.5*s**0.4,seed+61,0.9,twice=False))
    return "".join(g)

def ground(y,w=900,seed=1,col=None,amp=6):
    """A Seuss horizon: never level."""
    pts=[(-20,y+amp),(w*0.22,y-amp*1.6),(w*0.5,y+amp*0.6),(w*0.78,y-amp*1.2),(w+20,y+amp)]
    return stroke(pts,3.2,seed,2.2,col=col)

def hill(y,w=900,h=70,seed=1,col=YELLOW,hatch=True):
    pts=[(-20,y+16),(w*0.18,y-h*0.5),(w*0.46,y-h*0.1),(w*0.74,y-h*0.62),(w+20,y-h*0.1),
         (w+20,y+260),(-20,y+260),(-20,y+16)]
    hid=uid("g")
    return shape(pts,col,seed=seed,w=3.2,amp=2.4,
                 hatch=hatching(-20,y-h,w+20,y+120,step=10,ang=-28,w=1.5,op=0.16,seed=seed+2) if hatch else None,
                 hid=hid if hatch else None)
