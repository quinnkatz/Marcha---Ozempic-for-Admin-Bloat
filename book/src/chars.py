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

# --- Grok bots, drawn to the reference: flat solid forms, no outline,
# --- two small dark eyes, no mouth, no limbs. Crisp against the inked world.
GROK={ "pink":"#E5447E", "purple":"#7B4FD8", "orange":"#E8712B", "charcoal":"#3E4654",
       "teal":"#35C4A5", "blue":"#2E7DE8", "yellow":"#F2C43F", "white":"#FFFFFF" }
GROK_EYE="#1A1D2E"
_MAP={ RED:"orange", BLUE:"blue", YELLOW:"yellow", GREEN:"teal", PINK:"pink",
       CREAM:"white", INK:"charcoal" }
_FORMS=["circle","egg","tri","square","hex","drop","arch"]

def _rr(pts, r, close=True):
    """Polygon with rounded corners -> path d."""
    n=len(pts); d=""
    for i in range(n):
        p0=pts[(i-1)%n]; p1=pts[i]; p2=pts[(i+1)%n]
        v1=(p1[0]-p0[0], p1[1]-p0[1]); v2=(p2[0]-p1[0], p2[1]-p1[1])
        l1=math.hypot(*v1) or 1; l2=math.hypot(*v2) or 1
        rr=min(r, l1/2, l2/2)
        a=(p1[0]-v1[0]/l1*rr, p1[1]-v1[1]/l1*rr)
        c=(p1[0]+v2[0]/l2*rr, p1[1]+v2[1]/l2*rr)
        d += (f"M {a[0]:.1f},{a[1]:.1f} " if i==0 else f"L {a[0]:.1f},{a[1]:.1f} ")
        d += f"Q {p1[0]:.1f},{p1[1]:.1f} {c[0]:.1f},{c[1]:.1f} "
    return d+("Z" if close else "")

def grok_form(cx,cy,w,h,form,fill):
    if form=="circle":
        return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{w*0.5:.1f}" ry="{h*0.5:.1f}" fill="{fill}"/>'
    if form=="egg":
        return (f'<path d="M {cx:.1f},{cy-h*0.5:.1f} C {cx+w*0.46:.1f},{cy-h*0.38:.1f} '
                f'{cx+w*0.52:.1f},{cy+h*0.22:.1f} {cx:.1f},{cy+h*0.5:.1f} '
                f'C {cx-w*0.52:.1f},{cy+h*0.22:.1f} {cx-w*0.46:.1f},{cy-h*0.38:.1f} '
                f'{cx:.1f},{cy-h*0.5:.1f} Z" fill="{fill}"/>')
    if form=="tri":
        p=[(cx,cy-h*0.52),(cx+w*0.52,cy+h*0.42),(cx-w*0.52,cy+h*0.42)]
        return f'<path d="{_rr(p,w*0.22)}" fill="{fill}"/>'
    if form=="square":
        p=[(cx-w*0.44,cy-h*0.48),(cx+w*0.44,cy-h*0.48),(cx+w*0.44,cy+h*0.48),(cx-w*0.44,cy+h*0.48)]
        return f'<path d="{_rr(p,w*0.30)}" fill="{fill}"/>'
    if form=="hex":
        p=[(cx,cy-h*0.52),(cx+w*0.47,cy-h*0.24),(cx+w*0.47,cy+h*0.26),
           (cx,cy+h*0.52),(cx-w*0.47,cy+h*0.26),(cx-w*0.47,cy-h*0.24)]
        return f'<path d="{_rr(p,w*0.20)}" fill="{fill}"/>'
    if form=="drop":
        return (f'<path d="M {cx-w*0.36:.1f},{cy-h*0.40:.1f} '
                f'C {cx+w*0.18:.1f},{cy-h*0.58:.1f} {cx+w*0.50:.1f},{cy-h*0.06:.1f} '
                f'{cx+w*0.36:.1f},{cy+h*0.22:.1f} '
                f'C {cx+w*0.20:.1f},{cy+h*0.54:.1f} {cx-w*0.34:.1f},{cy+h*0.52:.1f} '
                f'{cx-w*0.44:.1f},{cy+h*0.16:.1f} '
                f'C {cx-w*0.50:.1f},{cy-h*0.10:.1f} {cx-w*0.46:.1f},{cy-h*0.30:.1f} '
                f'{cx-w*0.36:.1f},{cy-h*0.40:.1f} Z" fill="{fill}"/>')
    # arch: round top, flat bottom
    return (f'<path d="M {cx-w*0.42:.1f},{cy+h*0.48:.1f} L {cx-w*0.42:.1f},{cy-h*0.06:.1f} '
            f'A {w*0.42:.1f},{h*0.44:.1f} 0 0 1 {cx+w*0.42:.1f},{cy-h*0.06:.1f} '
            f'L {cx+w*0.42:.1f},{cy+h*0.48:.1f} Z" fill="{fill}"/>')

def bot(cx, cy, s=1.0, col=RED, seed=5, eyes=2, mood="open", tilt=-14,
        arms=True, legs=True, look=(0,0), hatch=True, fur=True, form=None):
    """A Grok bot: one flat form, two eyes, nothing else."""
    key=_MAP.get(col,"blue"); fill=GROK.get(key,GROK["blue"])
    form=form or _FORMS[random.Random(seed*97+13).randrange(len(_FORMS))]
    w=h=104*s
    if form in ("egg","arch"): h=112*s; w=96*s
    if form=="square": w=h=98*s
    rot=tilt*0.42
    g=[f'<g transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})">']
    g.append(grok_form(cx,cy,w,h,form,fill))
    ey=cy-h*0.06 if form!="tri" else cy+h*0.06
    ex=w*0.145; er=w*0.052; eh=er*1.5
    if mood=="sleep":
        for d in (-1,1):
            g.append(f'<path d="M {cx+d*ex-er*1.3:.1f},{ey:.1f} Q {cx+d*ex:.1f},{ey+er*1.7:.1f} '
                     f'{cx+d*ex+er*1.3:.1f},{ey:.1f}" fill="none" stroke="{GROK_EYE}" '
                     f'stroke-width="{er*0.8:.1f}" stroke-linecap="round"/>')
    else:
        k=1.22 if mood=="oh" else (0.82 if mood=="flat" else 1.0)
        for d in (-1,1):
            g.append(f'<ellipse cx="{cx+d*ex+look[0]*0.5:.1f}" cy="{ey+look[1]*0.4:.1f}" '
                     f'rx="{er*k:.1f}" ry="{eh*k:.1f}" fill="{GROK_EYE}"/>')
    g.append('</g>')
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
