# -*- coding: utf-8 -*-
from art import *
import math, random

W,H=900,720

def s_cover():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(f'<path d="M 0,{H-70} Q {W*0.3},{H-100} {W*0.62},{H-72} T {W},{H-84} L {W},{H} L 0,{H} Z" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>')
    cols=[RED,TEAL,GOLD,GREEN]
    xs=[148,368,592,796]; sc=[1.18,1.02,1.28,0.96]
    moods=["open","flat","oh","open"]; tilts=[-14,6,-4,16]
    ground=H-86
    for i,(x,c) in enumerate(zip(xs,cols)):
        cy=ground-58*sc[i]*1.5          # feet land on the band
        g.append(bot(x,cy,s=sc[i],col=c,seed=10+i,eyes=2 if i!=2 else 1,
                     mood=moods[i],tilt=tilts[i],look=(2 if i%2 else -2,2)))
    return svg(W,H,"".join(g))

def s_crowd():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    # the cloud
    g.append(cloud(W*0.42,H*0.44,330,180,seed=21,w=5))
    r=random.Random(7)
    spots=[(210,252,.44),(318,206,.38),(420,248,.42),(516,212,.34),(258,334,.40),
           (372,326,.46),(480,336,.36),(560,286,.30),(158,322,.30),(588,352,.26),
           (300,404,.30),(430,402,.26),(520,398,.22),(212,400,.22)]
    cols=[RED,TEAL,GOLD,LILAC,GREEN]
    for i,(x,y,sc) in enumerate(spots):
        g.append(bot(x+r.randint(-8,8),y,s=sc,col=cols[i%5],seed=30+i,
                     eyes=2 if i%3 else 1,mood=["open","flat","oh"][i%3],
                     tilt=r.randint(-20,20),legs=False,arms=False,look=(r.randint(-3,3),2)))
    g.append(f'<path d="M 120,520 Q 300,495 470,515 T 830,505" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity="0.5"/>')
    return svg(W,H,"".join(g))

def s_printout():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    # giant printout going up out of frame
    x0=330
    g.append(f'<path d="M {x0},{H} L {x0},-20 Q {x0+90},-40 {x0+180},-15 L {x0+180},{H-40} Q {x0+90},{H-10} {x0},{H} Z" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    r=random.Random(3)
    y=20
    while y<H-60:
        wd=r.randint(50,150)
        g.append(f'<line x1="{x0+22}" y1="{y}" x2="{x0+22+wd}" y2="{y}" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.72"/>')
        if r.random()<0.34:
            g.append(f'<circle cx="{x0+13}" cy="{y}" r="4" fill="{RED}"/>')
        y+=r.randint(22,30)
    # curl pooling at the floor
    g.append(f'<path d="M {x0},{H-30} q -70,-10 -110,30 q -40,40 30,42 q 60,2 80,-42" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    # kid
    g.append(person(160,H-160,s=1.0,col=TEAL,face="oh",hairstyle="tuft",hair=INK))
    # clock
    g.append(f'<circle cx="760" cy="150" r="72" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<circle cx="760" cy="150" r="6" fill="{INK}"/>')
    g.append(f'<line x1="760" y1="150" x2="760" y2="100" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    g.append(f'<line x1="760" y1="150" x2="812" y2="150" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    for i in range(12):
        a=math.radians(i*30); 
        g.append(f'<circle cx="{760+math.sin(a)*58:.1f}" cy="{150-math.cos(a)*58:.1f}" r="2.6" fill="{INK}"/>')
    g.append(f'<path d="M 120,{H-40} L 820,{H-40}" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
    return svg(W,H,"".join(g))

def s_emptychair():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(f'<path d="M 380,{H-110} L 860,{H-110}" stroke="{INK}" stroke-width="3" opacity="0.45"/>')
    # chair, empty: three-quarter view so it reads as a chair
    cx,cy=596,H-120
    seatY=cy-128
    g.append(f'<line x1="{cx-72}" y1="{seatY}" x2="{cx-84}" y2="{cy}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    g.append(f'<line x1="{cx+72}" y1="{seatY}" x2="{cx+84}" y2="{cy}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    g.append(f'<line x1="{cx-40}" y1="{seatY-6}" x2="{cx-46}" y2="{cy-30}" stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity="0.75"/>')
    g.append(f'<line x1="{cx+40}" y1="{seatY-6}" x2="{cx+46}" y2="{cy-30}" stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity="0.75"/>')
    # back posts + slats
    g.append(f'<rect x="{cx-72}" y="{seatY-158}" width="16" height="164" rx="6" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{cx+56}" y="{seatY-158}" width="16" height="164" rx="6" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{cx-78}" y="{seatY-170}" width="156" height="22" rx="9" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{cx-58}" y="{seatY-104}" width="116" height="16" rx="7" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{cx-58}" y="{seatY-58}" width="116" height="16" rx="7" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    # seat, slightly in perspective
    g.append(poly([(cx-80,seatY),(cx+80,seatY),(cx+96,seatY+26),(cx-96,seatY+26)],fill=RED,w=4))
    g.append(f'<path d="M {cx-80},{seatY} L {cx+80},{seatY}" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
    # speech bubbles still going, nobody in them
    bubs=[(470,118,92,54,"?"),(672,96,72,46,"?"),(760,236,58,38,"?"),(628,300,44,30,"")]
    for i,(x,y,rx,ry,t) in enumerate(bubs):
        g.append(blob(x,y,rx,ry,CREAM,seed=40+i,n=16,amt=0.07,w=4))
        g.append(f'<path d="M {x-rx*0.4},{y+ry*0.8} l -16,26 l 30,-16 Z" fill="{CREAM}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        if t: g.append(f'<text x="{x}" y="{y+13}" font-family="Fredoka, sans-serif" font-size="40" font-weight="700" text-anchor="middle" fill="{INK}">{t}</text>')
    return svg(W,H,"".join(g))

def s_funeral():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(f'<path d="M 0,{H-120} Q {W*0.5},{H-150} {W},{H-118} L {W},{H} L 0,{H} Z" fill="{GREEN}" stroke="{INK}" stroke-width="3" opacity="0.85"/>')
    # tiny pine box
    bx,by=232,H-118
    g.append(poly([(bx-56,by),(bx-44,by-30),(bx+44,by-30),(bx+56,by)],fill=GOLD,w=4))
    g.append(f'<path d="M {bx-44},{by-30} L {bx+44},{by-30}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<path d="M {bx},{by-30} L {bx},{by}" stroke="{INK}" stroke-width="2.5" opacity="0.6"/>')
    # a very small flower
    g.append(f'<circle cx="{bx+4}" cy="{by-38}" r="7" fill="{RED}" stroke="{INK}" stroke-width="2.5"/>')
    # mourner bots, one delivering eulogy at a lectern
    g.append(bot(492,H-268,s=0.85,col=TEAL,seed=55,mood="oh",tilt=-10,look=(4,1)))
    g.append(poly([(474,H-188),(442,H-118),(542,H-118),(510,H-188)],fill=LILAC,w=4))
    g.append(f'<rect x="438" y="{H-195}" width="108" height="12" rx="5" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>')
    for i,(x,sc,c,m) in enumerate([(648,0.72,RED,"flat"),(742,0.6,GOLD,"flat"),(826,0.66,LILAC,"flat")]):
        g.append(bot(x,H-238,s=sc,col=c,seed=60+i,mood=m,tilt=6,look=(-4,3)))
    # one checking a watch
    g.append(f'<circle cx="794" cy="{H-208}" r="11" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<line x1="794" y1="{H-208}" x2="794" y2="{H-216}" stroke="{INK}" stroke-width="2.5"/>')
    return svg(W,H,"".join(g))

def s_gork():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    cx,cy=330,398
    # bulk
    g.append(limb(cx-120,cy+90,cx-215,cy+35,bend=-24,w=5))
    g.append(limb(cx+120,cy+90,cx+220,cy+45,bend=24,w=5))
    g.append(blob(cx,cy+60,150,150,GREEN,seed=71,n=20,amt=0.05,w=5))
    # head
    g.append(blob(cx,cy-95,118,96,GREEN,seed=73,n=18,amt=0.05,w=5))
    # ears
    g.append(poly(wobble([(cx-116,cy-115),(cx-165,cy-160),(cx-150,cy-80)],3,4),fill=GREEN,w=5))
    g.append(poly(wobble([(cx+116,cy-115),(cx+165,cy-160),(cx+150,cy-80)],3,5),fill=GREEN,w=5))
    # tusks
    g.append(f'<path d="M {cx-42},{cy-38} q -6,-34 10,-46" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<path d="M {cx+42},{cy-38} q 6,-34 -10,-46" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    # mouth
    g.append(f'<path d="M {cx-52},{cy-52} q 52,34 104,0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    # tiny reading glasses
    g.append(f'<circle cx="{cx-36}" cy="{cy-118}" r="30" fill="{CREAM}" stroke="{INK}" stroke-width="4" opacity="0.92"/>')
    g.append(f'<circle cx="{cx+36}" cy="{cy-118}" r="30" fill="{CREAM}" stroke="{INK}" stroke-width="4" opacity="0.92"/>')
    g.append(f'<line x1="{cx-6}" y1="{cy-118}" x2="{cx+6}" y2="{cy-118}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<line x1="{cx-66}" y1="{cy-122}" x2="{cx-104}" y2="{cy-132}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    g.append(f'<line x1="{cx+66}" y1="{cy-122}" x2="{cx+104}" y2="{cy-132}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    g.append(f'<circle cx="{cx-36}" cy="{cy-114}" r="9" fill="{INK}"/>')
    g.append(f'<circle cx="{cx+36}" cy="{cy-114}" r="9" fill="{INK}"/>')
    # speech
    g.append(blob(612,120,98,56,CREAM,seed=80,n=16,amt=0.07,w=4))
    g.append(f'<path d="M 556,158 l -30,34 l 44,-14 Z" fill="{CREAM}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    g.append(f'<text x="612" y="136" font-family="Fredoka, sans-serif" font-size="46" font-weight="700" text-anchor="middle" fill="{INK}">bruh</text>')
    g.append(f'<path d="M 80,{H-96} L 820,{H-96}" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
    return svg(W,H,"".join(g))

def s_grandma():
    g=[f'<rect width="{W}" height="{H}" fill="{TEAL}"/>']
    # clouds
    for i,(x,y,rx,ry) in enumerate([(150,120,120,52),(760,404,104,44),(320,470,132,50),(596,92,96,40)]):
        g.append(cloud(x,y,rx,ry,seed=90+i,w=0,stroke=CREAM))
    # kite
    g.append(poly([(752,120),(812,186),(752,254),(694,186)],fill=RED,w=4))
    g.append(f'<path d="M 752,254 q 16,30 -8,48 q 26,10 12,44" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    g.append(f'<path d="M 694,186 L 812,186 M 752,120 L 752,254" stroke="{INK}" stroke-width="3" opacity="0.55"/>')
    # string to grandma's hand
    g.append(f'<path d="M 694,186 Q 640,236 592,250" fill="none" stroke="{INK}" stroke-width="3"/>')
    # grandma, flying, horizontal-ish
    gx,gy=470,300
    g.append(f'<g transform="rotate(-12 {gx} {gy}) scale(1.34) translate({-gx*0.254:.1f} {-gy*0.254:.1f})">')
    g.append(poly(wobble([(gx-92,gy+40),(gx-74,gy-44),(gx+78,gy-46),(gx+96,gy+42)],2,11),fill=LILAC,w=4))
    # shawl fringe
    for i in range(7):
        g.append(f'<line x1="{gx-88+i*30}" y1="{gy+40}" x2="{gx-92+i*30}" y2="{gy+62}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # legs streaming back
    g.append(limb(gx-70,gy+30,gx-160,gy+58,bend=-14,w=5))
    g.append(limb(gx-62,gy+42,gx-150,gy+86,bend=-10,w=5))
    g.append(f'<ellipse cx="{gx-166}" cy="{gy+58}" rx="17" ry="10" fill="{INK}" transform="rotate(-14 {gx-166} {gy+58})"/>')
    g.append(f'<ellipse cx="{gx-156}" cy="{gy+88}" rx="17" ry="10" fill="{INK}" transform="rotate(-10 {gx-156} {gy+88})"/>')
    # arm up to kite string
    g.append(limb(gx+72,gy-20,gx+82,gy-34,bend=6,w=5))
    # head + bun
    hx,hy=gx+96,gy-62
    g.append(f'<circle cx="{hx}" cy="{hy}" r="34" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<circle cx="{hx-14}" cy="{hy-36}" r="16" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<path d="M {hx-34},{hy-6} a 34,34 0 0 1 56,-16 q -14,-14 -34,-12 q -18,2 -22,28" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    # specs + delighted-but-busy face
    g.append(f'<circle cx="{hx+6}" cy="{hy-4}" r="12" fill="none" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<circle cx="{hx+32}" cy="{hy-6}" r="12" fill="none" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<line x1="{hx+18}" y1="{hy-5}" x2="{hx+20}" y2="{hy-5}" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<path d="M {hx+8},{hy+18} q 12,8 22,-2" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    g.append('</g>')
    # the watch she is checking
    g.append(f'<circle cx="{gx+112}" cy="{gy+8}" r="20" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<line x1="{gx+112}" y1="{gy+8}" x2="{gx+112}" y2="{gy-4}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<line x1="{gx+112}" y1="{gy+8}" x2="{gx+122}" y2="{gy+12}" stroke="{INK}" stroke-width="3"/>')
    g.append(limb(gx+70,gy+8,gx+102,gy+8,bend=4,w=5))
    # the mall, far below
    g.append(f'<rect x="40" y="{H-172}" width="230" height="64" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<rect x="290" y="{H-152}" width="140" height="44" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>')
    return svg(W,H,"".join(g),bg=TEAL)

def s_library():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    # shelves behind
    for i,y in enumerate([70,175]):
        g.append(f'<rect x="60" y="{y}" width="780" height="14" fill="{INK}" opacity="0.8"/>')
        r=random.Random(100+i); x=72
        while x<820:
            bw=r.randint(16,30); bh=r.randint(54,84)
            c=[RED,TEAL,GOLD,LILAC,GREEN][r.randint(0,4)]
            g.append(f'<rect x="{x}" y="{y-bh}" width="{bw}" height="{bh}" fill="{c}" stroke="{INK}" stroke-width="2.5" rx="2"/>')
            x+=bw+r.randint(1,5)
    # floor
    g.append(f'<path d="M 0,{H-70} L {W},{H-70}" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
    # mother and kid sitting, open books
    g.append(person(232,H-208,s=1.12,col=RED,face="calm",hairstyle="bun",hair=CREAM,arms=True))
    g.append(person(392,H-224,s=0.92,col=TEAL,face="calm",hairstyle="tuft",arms=True))
    for i,(x,y,sc) in enumerate([(318,H-104,1.25),(150,H-88,0.85),(470,H-92,0.95)]):
        pw,ph=62*sc,40*sc                     # open book: two leaves meeting at a spine
        g.append(poly([(x,y-ph*0.50),(x-pw,y-ph*0.14),(x-pw*0.92,y+ph*0.40),(x,y)],fill=CREAM,w=3))
        g.append(poly([(x,y-ph*0.50),(x+pw,y-ph*0.14),(x+pw*0.92,y+ph*0.40),(x,y)],fill=CREAM,w=3))
        g.append(f'<line x1="{x}" y1="{y-ph*0.50:.1f}" x2="{x}" y2="{y:.1f}" stroke="{INK}" stroke-width="3"/>')
        for k in range(3):
            t=0.30+k*0.19
            g.append(f'<line x1="{x-pw*0.78:.1f}" y1="{y-ph*0.16+ph*t*0.5:.1f}" x2="{x-pw*0.18:.1f}" y2="{y-ph*0.34+ph*t*0.5:.1f}" stroke="{INK}" stroke-width="2" opacity="0.4"/>')
            g.append(f'<line x1="{x+pw*0.18:.1f}" y1="{y-ph*0.34+ph*t*0.5:.1f}" x2="{x+pw*0.78:.1f}" y2="{y-ph*0.16+ph*t*0.5:.1f}" stroke="{INK}" stroke-width="2" opacity="0.4"/>')
    # dust motes
    r=random.Random(5)
    for _ in range(30):
        g.append(f'<circle cx="{r.randint(90,520)}" cy="{r.randint(250,470)}" r="{r.choice([2,2.5,3])}" fill="{GOLD}" opacity="0.75"/>')
    return svg(W,H,"".join(g))

def s_window():
    g=[f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    r=random.Random(12)
    for _ in range(88):
        x,y=r.randint(0,W),r.randint(0,H-260)
        g.append(f'<circle cx="{x}" cy="{y}" r="{r.choice([1,1.4,2])}" fill="{CREAM}" opacity="{r.uniform(0.3,0.95):.2f}"/>')
    g.append(f'<circle cx="770" cy="105" r="46" fill="{CREAM}" opacity="0.95"/>')
    # terrace of dark houses
    xs=0; i=0
    while xs<W:
        bw=r.randint(110,170); bh=r.randint(300,410)
        g.append(f'<rect x="{xs}" y="{H-bh}" width="{bw}" height="{bh}" fill="#141E2B" stroke="{INK}" stroke-width="3"/>')
        # dark windows
        for cxp in range(2):
            for cyp in range(3):
                wx=xs+22+cxp*(bw-74); wy=H-bh+28+cyp*64
                if wy<H-40:
                    g.append(f'<rect x="{wx}" y="{wy}" width="44" height="42" fill="#0E1620" stroke="{INK}" stroke-width="2.5" rx="3"/>')
        xs+=bw; i+=1
    # THE lit window
    lx,ly=392,330
    g.append(f'<rect x="{lx}" y="{ly}" width="118" height="104" fill="{GOLD}" stroke="{INK}" stroke-width="4" rx="4"/>')
    g.append(f'<line x1="{lx+59}" y1="{ly}" x2="{lx+59}" y2="{ly+104}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<line x1="{lx}" y1="{ly+52}" x2="{lx+118}" y2="{ly+52}" stroke="{INK}" stroke-width="3"/>')
    # silhouettes in it: a person and a small bot
    g.append(f'<g opacity="0.92">')
    g.append(f'<circle cx="{lx+34}" cy="{ly+46}" r="15" fill="{INK}"/>')
    g.append(f'<path d="M {lx+14},{ly+104} q 20,-44 40,0 Z" fill="{INK}"/>')
    g.append(blob(lx+86,ly+62,20,22,INK,seed=3,w=0,stroke="none"))
    g.append(f'<line x1="{lx+86}" y1="{ly+38}" x2="{lx+90}" y2="{ly+24}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<circle cx="{lx+90}" cy="{ly+21}" r="4.5" fill="{INK}"/>')
    g.append('</g>')
    # spill of light
    g.append(f'<path d="M {lx},{ly+104} L {lx-46},{H} L {lx+170},{H} L {lx+118},{ly+104} Z" fill="{GOLD}" opacity="0.16"/>')
    return svg(W,H,"".join(g),bg=NIGHT)

def s_footnote():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(f'<path d="M 70,{H-70} L 830,{H-70}" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
    # large man
    mx=640
    g.append(person(mx,H-240,s=1.72,col=GOLD,face="flat",hairstyle="bob",hair=INK))
    # small bot offering a note
    g.append(bot(250,H-160,s=0.62,col=TEAL,seed=77,mood="flat",tilt=-6,look=(6,0)))
    # the note passing between them
    nx,ny=410,H-215
    g.append(f'<g transform="rotate(-8 {nx} {ny})">')
    g.append(f'<rect x="{nx-46}" y="{ny-32}" width="92" height="64" rx="4" fill="{CREAM}" stroke="{INK}" stroke-width="3.5"/>')
    for k in range(3):
        g.append(f'<line x1="{nx-32}" y1="{ny-14+k*15}" x2="{nx+{0:26,1:30,2:14}[k]}" y2="{ny-14+k*15}" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity="0.7"/>')
    g.append(f'<text x="{nx-36}" y="{ny-20}" font-family="Fredoka, sans-serif" font-size="20" font-weight="700" fill="{RED}">1.</text>')
    g.append('</g>')
    g.append(limb(304,H-190,376,H-212,bend=-8,w=3))
    return svg(W,H,"".join(g))

def s_drawing():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(f'<path d="M 0,{H-96} L {W},{H-96}" stroke="{INK}" stroke-width="3" opacity="0.35"/>')
    # the kid's drawing, held up, big
    dx,dy=330,300
    g.append(f'<g transform="rotate(-4 {dx} {dy})">')
    g.append(f'<rect x="{dx-170}" y="{dy-125}" width="340" height="250" rx="5" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{dx-158}" y="{dy-113}" width="316" height="130" fill="{TEAL}" opacity="0.85"/>')
    g.append(f'<circle cx="{dx+96}" cy="{dy-72}" r="26" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<rect x="{dx-158}" y="{dy+17}" width="316" height="96" fill="{GREEN}" opacity="0.8"/>')
    # a cat, drawn by a child
    ccx,ccy=dx-58,dy+44
    g.append(f'<ellipse cx="{ccx}" cy="{ccy}" rx="52" ry="34" fill="{RED}" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<circle cx="{ccx-44}" cy="{ccy-26}" r="26" fill="{RED}" stroke="{INK}" stroke-width="3.5"/>')
    g.append(poly([(ccx-62,ccy-44),(ccx-58,ccy-70),(ccx-40,ccy-50)],fill=RED,w=3.5))
    g.append(poly([(ccx-32,ccy-50),(ccx-22,ccy-72),(ccx-14,ccy-46)],fill=RED,w=3.5))
    g.append(f'<path d="M {ccx+50},{ccy-8} q 34,-10 22,-40" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    g.append(f'<circle cx="{ccx-52}" cy="{ccy-28}" r="3.4" fill="{INK}"/>')
    g.append(f'<circle cx="{ccx-36}" cy="{ccy-28}" r="3.4" fill="{INK}"/>')
    for k in range(3):
        g.append(f'<line x1="{ccx-56}" y1="{ccy-16+k*6}" x2="{ccx-84}" y2="{ccy-22+k*9}" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
        g.append(f'<line x1="{ccx-30}" y1="{ccy-16+k*6}" x2="{ccx-4}" y2="{ccy-22+k*9}" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    g.append('</g>')
    # kid beside it, looking at it
    g.append(person(690,H-210,s=0.92,col=RED,face="calm",hairstyle="tuft"))
    # bot, deliberately leaning out of frame, hands off
    g.append(f'<g opacity="0.95">')
    g.append(bot(836,H-215,s=0.9,col=TEAL,seed=91,mood="flat",tilt=18,look=(-6,0),arms=True))
    g.append('</g>')
    return svg(W,H,"".join(g))

def s_doorway():
    """Caption band covers the bottom ~22%. Everything lives above FL."""
    FL=556                                  # visual floor, well clear of the band
    g=[f'<rect width="{W}" height="{H}" fill="#223349"/>']
    # window + moon, upper left
    g.append(f'<rect x="92" y="64" width="236" height="206" rx="6" fill="{NIGHT}" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<line x1="210" y1="64" x2="210" y2="270" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<line x1="92" y1="167" x2="328" y2="167" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<circle cx="262" cy="122" r="42" fill="{CREAM}"/>')
    r=random.Random(31)
    for _ in range(20):
        g.append(f'<circle cx="{r.randint(102,320)}" cy="{r.randint(74,258)}" r="{r.choice([1.4,2,2.6])}" fill="{CREAM}" opacity="{r.uniform(0.45,1):.2f}"/>')
    # doorway, right, spilling warm light
    dx,dw=596,256
    g.append(f'<rect x="{dx}" y="120" width="{dw}" height="{FL-120+40}" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<rect x="{dx+18}" y="138" width="{dw-36}" height="{FL-138+40}" fill="#F7D28A"/>')
    g.append(f'<path d="M {dx},{FL} L 250,{FL+40} L {dx+dw},{FL+40} Z" fill="{GOLD}" opacity="0.14"/>')
    # parent in the doorway: feet on FL, head high
    px=724; top=FL-178
    g.append(f'<path d="M {px-70},{FL} q 2,-104 24,-138 q 13,-19 46,-19 q 33,0 46,19 q 22,34 24,138 Z" fill="{INK}"/>')
    g.append(f'<path d="M {px-64},{FL-136} q -18,42 -14,86" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>')
    g.append(f'<path d="M {px+64},{FL-136} q 18,42 14,86" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>')
    g.append(f'<circle cx="{px}" cy="{top+16}" r="38" fill="{INK}"/>')
    g.append(f'<path d="M {px-40},{top+10} a 40,40 0 0 1 80,-6 q -20,-24 -46,-20 q -26,6 -34,26" fill="{INK}"/>')
    # bed, left, kid tucked in
    bx,bw2,bh2=64,392,116
    by=FL-bh2
    g.append(f'<rect x="{bx}" y="{by}" width="{bw2}" height="{bh2}" rx="12" fill="{LILAC}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{bx}" y="{by}" width="{bw2}" height="44" rx="12" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<rect x="{bx+bw2-26}" y="{by-56}" width="26" height="{bh2+56}" rx="6" fill="{LILAC}" stroke="{INK}" stroke-width="4"/>')
    kx,ky=bx+78,by-26
    g.append(f'<circle cx="{kx}" cy="{ky}" r="31" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<path d="M {kx-31},{ky-6} a 31,31 0 0 1 60,-10 q -15,-15 -35,-13 q -20,4 -25,23" fill="{INK}"/>')
    g.append(f'<circle cx="{kx-10}" cy="{ky+2}" r="3.4" fill="{INK}"/>')
    g.append(f'<circle cx="{kx+11}" cy="{ky+2}" r="3.4" fill="{INK}"/>')
    g.append(f'<path d="M {kx-8},{ky+15} q 9,7 18,0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # one small bot asleep on the bedside table
    g.append(f'<rect x="{bx+bw2+22}" y="{FL-86}" width="86" height="86" fill="#2E4258" stroke="{INK}" stroke-width="4" rx="4"/>')
    g.append(bot(bx+bw2+65,FL-118,s=0.42,col=TEAL,seed=310,mood="sleep",tilt=8,legs=False,arms=False))
    return svg(W,H,"".join(g),bg=NIGHT)

def s_sill():
    """Four bots on a sill, backs half-turned, watching the moon. Verse sits upper-left."""
    g=[f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    r=random.Random(44)
    for _ in range(110):
        g.append(f'<circle cx="{r.randint(0,W)}" cy="{r.randint(0,H-230)}" r="{r.choice([1,1.5,2,2.6])}" fill="{CREAM}" opacity="{r.uniform(0.25,1):.2f}"/>')
    g.append(f'<circle cx="716" cy="168" r="74" fill="{CREAM}"/>')
    g.append(f'<circle cx="688" cy="144" r="13" fill="{NIGHT}" opacity="0.10"/>')
    g.append(f'<circle cx="734" cy="192" r="9" fill="{NIGHT}" opacity="0.10"/>')
    g.append(f'<circle cx="742" cy="146" r="6" fill="{NIGHT}" opacity="0.08"/>')
    SY=H-196                                  # top surface of the sill
    cast=[(300,RED,0.80),(438,TEAL,0.70),(566,GOLD,0.84),(690,GREEN,0.66)]
    for i,(x,c,sc) in enumerate(cast):
        g.append(bot(x,SY-58*sc,s=sc,col=c,seed=120+i,mood="sleep",
                     tilt=[-10,6,-4,11][i],legs=False,arms=False))
    g.append(f'<rect x="0" y="{SY}" width="{W}" height="34" fill="{LILAC}" stroke="{INK}" stroke-width="4"/>')
    for i,(x,c,sc) in enumerate(cast):        # legs hang in front of the ledge
        for d in (-1,1):
            g.append(f'<path d="M {x+d*15*sc:.1f},{SY-2:.1f} q {d*3},{30*sc:.1f} {d*2},{46*sc:.1f}" '
                     f'fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
            g.append(foot(x+d*17*sc, SY+46*sc, d))
    g.append(f'<rect x="0" y="{SY+34}" width="{W}" height="{H-SY-34}" fill="#26364C"/>')
    g.append(f'<path d="M 0,{SY+58} L {W},{SY+58}" stroke="{INK}" stroke-width="3" opacity="0.35"/>')
    return svg(W,H,"".join(g),bg=NIGHT)

SCENES={"cover":s_cover,"crowd":s_crowd,"printout":s_printout,"emptychair":s_emptychair,
        "funeral":s_funeral,"gork":s_gork,"grandma":s_grandma,"library":s_library,
        "window":s_window,"footnote":s_footnote,"drawing":s_drawing,
        "doorway":s_doorway,"sill":s_sill}
