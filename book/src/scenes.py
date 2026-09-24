# -*- coding: utf-8 -*-
"""The thirteen illustrations, drawn with the ink engine."""
from ink import *
from chars import *
import math, random

W,H=900,720

def sky_night():
    g=[f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    r=random.Random(12)
    for _ in range(100):
        x,y=r.randint(0,W),r.randint(0,H-200)
        rr=r.choice([1.2,1.8,2.4])
        if r.random()<0.16:
            g.append(tuft(x,y+4,4,7,90,r.randint(0,999),1.3,MOON))
        else:
            g.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{MOON}" opacity="{r.uniform(0.35,1):.2f}"/>')
    return g

def moon(cx,cy,r_,seed=3):
    g=shape(lump(cx,cy,r_,r_*0.97,seed=seed,n=22,amt=0.035),MOON,seed=seed,w=2.6,amp=1.0)
    g+=stroke([(cx-r_*0.4,cy-r_*0.2),(cx-r_*0.2,cy-r_*0.36)],2.0,seed+5,0.8,twice=False,op=0.35)
    g+=stroke([(cx+r_*0.22,cy+r_*0.3),(cx+r_*0.42,cy+r_*0.18)],2.0,seed+6,0.8,twice=False,op=0.35)
    return g

def bubble(cx,cy,rx,ry,txt="",seed=1,tail=(-0.4,1.0),fs=42):
    g=shape(lump(cx,cy,rx,ry,seed=seed,n=20,amt=0.07),CREAM,seed=seed,w=2.9,amp=1.4)
    tx,ty=cx+rx*tail[0], cy+ry*tail[1]
    g+=shape([(tx-14,ty-6),(tx-30,ty+34),(tx+16,ty+6),(tx-14,ty-6)],CREAM,seed=seed+2,w=2.7,amp=1.2)
    if txt:
        g+=(f'<text x="{cx}" y="{cy+fs*0.34:.0f}" font-family="Fredoka, sans-serif" font-size="{fs}" '
            f'font-weight="700" text-anchor="middle" fill="{INK}">{txt}</text>')
    return g

# ---------------------------------------------------------------- 1. cover
def s_cover():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(hill(H-86,W,86,seed=4,col=YELLOW))
    GY=H-86
    cast=[(150,RED,1.24,"open",-16,"drop"),(372,BLUE,1.04,"flat",9,"circle"),
          (596,YELLOW,1.32,"oh",-6,"tri"),(800,GREEN,0.98,"open",16,"hex")]
    for i,(x,c,sc,m,t,fm) in enumerate(cast):
        g.append(bot(x,GY-56*sc-12,s=sc,col=c,seed=10+i*3,mood=m,tilt=t,form=fm,
                     look=(2 if i%2 else -2,2)))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 2. crowd
def s_crowd():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    # one enormous lumpy cloud, hatched
    g.append(cloud(W*0.40,H*0.42,330,185,seed=21,w=3.4))
    spots=[(196,250,.42,RED),(310,200,.36,BLUE),(416,246,.42,YELLOW),(512,206,.34,PINK),
           (250,336,.40,BLUE),(366,326,.46,RED),(474,338,.36,GREEN),(556,284,.30,YELLOW),
           (150,320,.30,YELLOW),(586,356,.26,BLUE),(296,410,.30,PINK),(424,406,.26,RED),
           (516,398,.22,YELLOW),(206,404,.22,BLUE)]
    r=random.Random(7)
    for i,(x,y,sc,c) in enumerate(spots):
        g.append(bot(x,y,s=sc*2.0,col=c,seed=30+i*3,
                     mood=["open","flat","oh"][i%3],tilt=r.randint(-24,24),
                     form=["circle","egg","tri","square","hex","drop","arch"][i%7],
                     look=(r.randint(-3,3),2)))
    g.append(ground(H-110,W,seed=5))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 3. printout
def s_printout():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    x0=336
    edgeL=[(x0+10,H-30)]+[(x0+math.sin(i*0.7)*9, H-120-i*64) for i in range(11)]
    edgeR=[(x0+184+math.sin(i*0.6+2)*9, H-120-i*64) for i in range(10,-1,-1)]+[(x0+192,H-40)]
    g.append(shape(edgeL+edgeR+[edgeL[0]],CREAM,seed=31,w=3.4,amp=2.2))
    r=random.Random(3); y=18
    while y<H-70:
        wd=r.randint(46,142)
        g.append(stroke([(x0+28,y),(x0+28+wd,y+r.uniform(-2,2))],2.6,int(y),1.1,twice=False,op=0.72))
        if r.random()<0.34:
            g.append(f'<circle cx="{x0+16}" cy="{y}" r="3.6" fill="{RED}"/>')
        y+=r.randint(24,32)
    # the pooled curl at the foot
    g.append(shape([(x0+6,H-46),(x0-72,H-58),(x0-124,H-16),(x0-64,H+10),(x0+22,H-12),(x0+6,H-46)],
                   CREAM,seed=33,w=3.2,amp=2.0))
    g.append(person(158,H-200,s=1.02,col=BLUE,seed=40,face="oh",hairstyle="frizz"))
    # the clock
    cx,cy=752,158
    g.append(shape(lump(cx,cy,76,74,seed=35,n=22,amt=0.035),CREAM,seed=35,w=3.2,amp=1.3))
    for i in range(12):
        a=math.radians(i*30)
        g.append(f'<circle cx="{cx+math.sin(a)*58:.1f}" cy="{cy-math.cos(a)*58:.1f}" r="2.8" fill="{INK}"/>')
    g.append(stroke([(cx,cy),(cx+2,cy-50)],4.0,36,0.8,twice=False))
    g.append(stroke([(cx,cy),(cx+54,cy+3)],4.0,37,0.8,twice=False))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{INK}"/>')
    g.append(ground(H-44,W,seed=6))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 4. empty chair
def s_emptychair():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    cx,cy=600,H-124; sy=cy-130
    for dx,w_ in ((-74,7.0),(74,7.0),(-42,5.5),(42,5.5)):
        g.append(stroke([(cx+dx,sy),(cx+dx*1.16,cy)],w_,int(40+dx),1.6))
    g.append(shape([(cx-74,sy-160),(cx-58,sy+4),(cx-74,sy+4),(cx-74,sy-160)],RED,seed=42,w=2.9,amp=1.4))
    g.append(shape([(cx+58,sy-160),(cx+74,sy-160),(cx+74,sy+4),(cx+58,sy+4)],RED,seed=43,w=2.9,amp=1.4))
    for yy,hh in ((sy-172,24),(sy-106,18),(sy-58,18)):
        g.append(shape([(cx-80,yy),(cx+80,yy-4),(cx+80,yy+hh),(cx-80,yy+hh+4)],RED,seed=44+int(yy),w=2.9,amp=1.4))
    g.append(shape([(cx-82,sy),(cx+82,sy-4),(cx+98,sy+26),(cx-98,sy+30)],RED,seed=47,w=3.1,amp=1.6,
                   hatch=hatching(cx-100,sy-6,cx+100,sy+32,step=7,ang=-30,w=1.1,op=0.16,seed=8),hid="ch1"))
    for i,(x,y,rx,ry,t) in enumerate([(430,112,92,56,"?"),(658,92,72,48,"?"),
                                      (772,244,56,40,"?"),(600,306,42,32,"")]):
        g.append(bubble(x,y,rx,ry,t,seed=50+i*4,tail=(0.2,1.0),fs=44))
    g.append(ground(H-112,W,seed=9))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 5. funeral
def s_funeral():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(hill(H-118,W,58,seed=12,col=GREEN))
    bx,by=236,H-126
    g.append(shape([(bx-58,by),(bx-44,by-32),(bx+44,by-34),(bx+58,by-2),(bx-58,by)],YELLOW,
                   seed=60,w=3.0,amp=1.5,
                   hatch=hatching(bx-60,by-36,bx+60,by+4,step=6.5,ang=-32,w=1.1,op=0.18,seed=11),hid="cf1"))
    g.append(stroke([(bx-44,by-32),(bx+44,by-34)],2.6,61,1.2,twice=False))
    g.append(shape(lump(bx+6,by-44,9,8,seed=62,n=11,amt=0.12),RED,seed=62,w=2.2,amp=1.0))
    g.append(tuft(bx+6,by-52,3,11,30,63,2.0))
    # eulogist at a lectern
    g.append(bot(492,H-250,s=1.02,col=BLUE,seed=64,mood="oh",tilt=-12,form="arch",look=(4,1)))
    g.append(shape([(470,H-196),(438,H-118),(546,H-118),(514,H-196)],PINK,seed=65,w=3.0,amp=1.5))
    g.append(shape([(434,H-208),(548,H-212),(548,H-192),(434,H-188)],CREAM,seed=66,w=2.8,amp=1.3))
    for i,(x,sc,c) in enumerate([(646,0.96,RED),(748,0.80,YELLOW),(836,0.88,PINK)]):
        g.append(bot(x,H-206,s=sc,col=c,seed=70+i*5,mood="flat",tilt=6,look=(-4,3)))
    g.append(shape(lump(800,H-150,13,12,seed=75,n=13,amt=0.08),CREAM,seed=75,w=2.4,amp=1.0))
    g.append(stroke([(800,H-150),(800,H-158)],2.2,76,0.6,twice=False))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 6. gork
def s_gork():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    cx,cy=326,400
    for d in (-1,1):
        g.append(stroke([(cx+d*128,cy+84),(cx+d*198,cy+52),(cx+d*226,cy+14)],4.2,80+d,1.8))
        g.append(hand(cx+d*226,cy+14,0 if d>0 else 180,1.25,82+d))
    g.append(shape(lump(cx,cy+62,152,150,seed=81,n=26,amt=0.06),GREEN,seed=81,w=3.4,amp=1.6,
                   hatch=hatching(cx-160,cy-100,cx+160,cy+220,step=6.5,ang=-34,w=1.1,op=0.17,seed=13),hid="gk1"))
    g.append(shape(lump(cx,cy-96,120,98,seed=82,n=24,amt=0.055),GREEN,seed=82,w=3.4,amp=1.5,
                   hatch=hatching(cx-130,cy-200,cx+130,cy,step=6.5,ang=-34,w=1.1,op=0.17,seed=14),hid="gk2"))
    for d in (-1,1):
        g.append(shape([(cx+d*116,cy-118),(cx+d*172,cy-166),(cx+d*152,cy-78),(cx+d*116,cy-118)],
                       GREEN,seed=83+d,w=3.0,amp=1.5))
    g.append(tuft(cx-18,cy-190,5,26,20,85,2.6))
    g.append(stroke([(cx-54,cy-52),(cx,cy-24),(cx+54,cy-52)],3.0,86,1.2,twice=False))
    for d in (-1,1):
        g.append(shape([(cx+d*44,cy-38),(cx+d*52,cy-74),(cx+d*34,cy-84),(cx+d*44,cy-38)],CREAM,seed=87+d,w=2.6,amp=1.1))
    # reading glasses
    for d in (-1,1):
        g.append(shape(lump(cx+d*36,cy-118,31,29,seed=88+d,n=20,amt=0.04),CREAM,seed=88+d,w=3.0,amp=1.2))
        g.append(f'<ellipse cx="{cx+d*36}" cy="{cy-114}" rx="9" ry="10" fill="{INK}"/>')
        g.append(stroke([(cx+d*66,cy-122),(cx+d*106,cy-134)],3.0,90+d,1.1,twice=False))
    g.append(stroke([(cx-6,cy-118),(cx+6,cy-118)],3.0,92,0.6,twice=False))
    g.append(bubble(618,120,100,58,"bruh",seed=93,tail=(-0.5,1.0),fs=46))
    g.append(ground(H-96,W,seed=15))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 7. grandma
def s_grandma():
    g=[f'<rect width="{W}" height="{H}" fill="{BLUE}"/>']
    for i,(x,y,rx,ry) in enumerate([(148,126,120,52),(770,420,100,44),(318,486,128,50),(600,98,92,40)]):
        g.append(cloud(x,y,rx,ry,seed=100+i,w=0))
    # kite, upper right
    g.append(shape([(756,112),(818,182),(756,252),(694,182),(756,112)],RED,seed=104,w=3.2,amp=1.5,
                   hatch=hatching(690,106,822,256,step=7,ang=-30,w=1.1,op=0.17,seed=16),hid="kt1"))
    g.append(stroke([(694,182),(818,182)],2.4,105,1.0,twice=False,op=0.55))
    g.append(stroke([(756,112),(756,252)],2.4,106,1.0,twice=False,op=0.55))
    g.append(stroke([(756,252),(772,290),(748,308),(774,330),(760,364)],2.8,107,1.4))
    gx,gy=430,318
    g.append(stroke([(694,182),(600,232),(512,262)],2.6,108,1.6))        # string to her hand
    g.append('<g transform="rotate(-14 %d %d)">' % (gx,gy))
    # legs streaming out behind her
    for i,(oy,ll) in enumerate([(26,-214),(50,-200)]):
        g.append(stroke([(gx-70,gy+oy),(gx-140,gy+oy+16),(gx+ll,gy+oy+26)],4.4,120+i,1.8))
        g.append(shape(lump(gx+ll-16,gy+oy+28,22,11,seed=122+i,n=12,amt=0.14),INK,seed=122+i,w=2.2,amp=1.0))
    # shawl: a lump, not a slab, with a hatched fringe
    g.append(shape(lump(gx,gy,112,62,seed=110,n=24,amt=0.07),PINK,seed=110,w=3.2,amp=1.6,
                   hatch=hatching(gx-124,gy-74,gx+124,gy+74,step=7,ang=-30,w=1.1,op=0.16,seed=17),hid="gm1"))
    for i in range(9):
        g.append(stroke([(gx-98+i*24,gy+52),(gx-104+i*24,gy+80)],2.6,111+i,1.0,twice=False))
    # arm forward to the string
    g.append(stroke([(gx+84,gy-14),(gx+120,gy-34),(gx+148,gy-56)],4.0,124,1.4))
    g.append(hand(gx+148,gy-56,-30,1.1,125))
    # head, bun, specs, delight
    hx,hy=gx+104,gy-74
    g.append(shape(lump(hx,hy,38,37,seed=126,n=22,amt=0.045),CREAM,seed=126,w=3.2,amp=1.3))
    g.append(shape(lump(hx-20,hy-42,19,17,seed=127,n=15,amt=0.10),CREAM,seed=127,w=2.8,amp=1.2))
    g.append(stroke([(hx-36,hy-12),(hx-14,hy-36),(hx+24,hy-20)],2.8,128,1.3,twice=False))
    for d in (0,1):
        g.append(shape(lump(hx+2+d*30,hy-6,14,14,seed=129+d,n=16,amt=0.05),CREAM,seed=129+d,w=2.6,amp=1.0))
        g.append(f'<circle cx="{hx+2+d*30}" cy="{hy-6}" r="3.8" fill="{INK}"/>')
    g.append(stroke([(hx+16,hy-6),(hx+18,hy-6)],2.6,131,0.5,twice=False))
    g.append(stroke([(hx+12,hy+14),(hx+24,hy+22),(hx+36,hy+11)],2.6,132,1.0,twice=False))
    g.append('</g>')
    # the watch she is checking, held clear of the shawl
    g.append(shape(lump(gx+96,gy+40,22,21,seed=133,n=16,amt=0.05),CREAM,seed=133,w=2.9,amp=1.1))
    g.append(stroke([(gx+96,gy+40),(gx+96,gy+27)],2.4,134,0.6,twice=False))
    g.append(stroke([(gx+96,gy+40),(gx+108,gy+45)],2.4,135,0.6,twice=False))
    g.append(stroke([(gx+52,gy+30),(gx+80,gy+38)],4.0,136,1.2))
    # the mall, far below
    g.append(shape([(40,H-174),(268,H-180),(272,H-108),(36,H-104)],YELLOW,seed=137,w=3.0,amp=1.6))
    g.append(shape([(296,H-152),(432,H-158),(436,H-106),(292,H-102)],YELLOW,seed=138,w=3.0,amp=1.6))
    return svg(W,H,"".join(g),bg=BLUE)

# ---------------------------------------------------------------- 8. library
def s_library():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    for i,y in enumerate([78,192]):
        r=random.Random(140+i); x=64
        while x<828:
            bw=r.randint(17,32); bh=r.randint(56,88)
            c=[RED,BLUE,YELLOW,PINK,GREEN][r.randint(0,4)]
            g.append(shape([(x,y-bh),(x+bw,y-bh-r.randint(0,6)),(x+bw,y),(x,y)],c,seed=145+x,w=2.3,amp=1.1))
            x+=bw+r.randint(1,5)
        g.append(stroke([(58,y+2),(834,y+6)],4.4,150+i,1.6))
    g.append(person(234,H-224,s=1.14,col=RED,seed=160,face="calm",hairstyle="bun",hair=CREAM))
    g.append(person(396,H-242,s=0.94,col=BLUE,seed=164,face="calm",hairstyle="frizz"))
    for i,(x,y,sc) in enumerate([(320,H-108,1.3),(150,H-92,0.9),(474,H-96,1.0)]):
        pw,ph=64*sc,42*sc
        g.append(shape([(x,y-ph*0.52),(x-pw,y-ph*0.16),(x-pw*0.92,y+ph*0.40),(x,y),(x,y-ph*0.52)],
                       CREAM,seed=170+i,w=2.7,amp=1.2))
        g.append(shape([(x,y-ph*0.52),(x+pw,y-ph*0.16),(x+pw*0.92,y+ph*0.40),(x,y),(x,y-ph*0.52)],
                       CREAM,seed=174+i,w=2.7,amp=1.2))
        g.append(stroke([(x,y-ph*0.52),(x,y)],2.6,178+i,0.9,twice=False))
    r=random.Random(5)
    for _ in range(30):
        g.append(f'<circle cx="{r.randint(96,516)}" cy="{r.randint(258,470)}" r="{r.choice([2,2.6,3.2])}" fill="{YELLOW}" opacity="0.8"/>')
    g.append(ground(H-70,W,seed=18))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 9. lit window
def s_window():
    g=sky_night()
    g.append(moon(742,126,52,seed=180))
    r=random.Random(19); xs=0
    while xs<W:
        bw=r.randint(112,172); bh=r.randint(300,412)
        g.append(shape([(xs,H-bh),(xs+bw,H-bh-r.randint(0,14)),(xs+bw,H),(xs,H)],"#18242F",seed=185+xs,w=3.0,amp=1.8))
        for cxp in range(2):
            for cyp in range(4):
                wx=xs+24+cxp*(bw-76); wy=H-bh+32+cyp*70
                if wy<H-60:
                    g.append(shape([(wx,wy),(wx+44,wy-2),(wx+44,wy+42),(wx,wy+44)],"#0F1720",seed=190+wx+wy,w=2.2,amp=1.0))
        xs+=bw
    lx,ly=392,336
    g.append(shape([(lx,ly),(lx+122,ly-4),(lx+120,ly+104),(lx-2,ly+106)],YELLOW,seed=200,w=3.4,amp=1.6))
    g.append(stroke([(lx+60,ly-2),(lx+60,ly+105)],2.8,201,1.1,twice=False))
    g.append(stroke([(lx,ly+52),(lx+121,ly+50)],2.8,202,1.1,twice=False))
    g.append(shape(lump(lx+34,ly+48,17,18,seed=203,n=16,amt=0.06),INK,seed=203,w=2.0,amp=0.9))
    g.append(shape([(lx+14,ly+106),(lx+22,ly+64),(lx+50,ly+62),(lx+56,ly+106)],INK,seed=204,w=2.0,amp=1.0))
    g.append(shape(lump(lx+88,ly+64,21,23,seed=205,n=18,amt=0.08),INK,seed=205,w=2.0,amp=1.0))
    g.append(stroke([(lx+88,ly+40),(lx+94,ly+22)],2.6,206,0.9,twice=False,col=INK))
    g.append(f'<circle cx="{lx+95}" cy="{ly+19}" r="5" fill="{INK}"/>')
    g.append(f'<path d="M {lx},{ly+106} L {lx-56},{H} L {lx+186},{H} L {lx+122},{ly+106} Z" fill="{YELLOW}" opacity="0.14"/>')
    return svg(W,H,"".join(g),bg=NIGHT)

# ---------------------------------------------------------------- 10. the note
def s_footnote():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(person(648,H-262,s=1.78,col=YELLOW,seed=210,face="flat",hairstyle="frizz"))
    g.append(bot(258,H-172,s=1.06,col=BLUE,seed=214,mood="flat",tilt=-8,form="circle",look=(6,0)))
    nx,ny=418,H-236
    g.append(f'<g transform="rotate(-8 {nx} {ny})">')
    g.append(shape([(nx-48,ny-34),(nx+48,ny-30),(nx+46,ny+34),(nx-50,ny+30)],CREAM,seed=218,w=3.0,amp=1.4))
    for k,wd in enumerate((26,30,14)):
        g.append(stroke([(nx-32,ny-14+k*15),(nx+wd,ny-15+k*15)],2.6,220+k,0.9,twice=False,op=0.7))
    g.append(f'<text x="{nx-38}" y="{ny-20}" font-family="Fredoka, sans-serif" font-size="21" font-weight="700" fill="{RED}">1.</text>')
    g.append('</g>')
    g.append(ground(H-70,W,seed=20))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 11. the drawing
def s_drawing():
    g=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    dx,dy=330,310
    g.append(f'<g transform="rotate(-4 {dx} {dy})">')
    g.append(shape([(dx-176,dy-130),(dx+176,dy-126),(dx+172,dy+128),(dx-172,dy+124)],CREAM,seed=230,w=3.6,amp=1.6))
    g.append(shape([(dx-160,dy-114),(dx+160,dy-110),(dx+158,dy+18),(dx-158,dy+16)],BLUE,seed=231,w=0,amp=1.4))
    g.append(shape(lump(dx+98,dy-72,28,27,seed=232,n=18,amt=0.07),YELLOW,seed=232,w=2.6,amp=1.2))
    g.append(shape([(dx-158,dy+18),(dx+158,dy+16),(dx+158,dy+112),(dx-158,dy+110)],GREEN,seed=233,w=0,amp=1.4))
    ccx,ccy=dx-56,dy+46
    g.append(shape(lump(ccx,ccy,54,36,seed=234,n=20,amt=0.07),RED,seed=234,w=3.0,amp=1.4))
    g.append(shape(lump(ccx-46,ccy-28,27,26,seed=235,n=18,amt=0.06),RED,seed=235,w=3.0,amp=1.3))
    for ox,oy,tx,ty in ((-64,-46,-60,-74),(-32,-52,-20,-76)):
        g.append(shape([(ccx+ox,ccy+oy),(ccx+tx,ccy+ty),(ccx+ox+22,ccy+oy+4),(ccx+ox,ccy+oy)],RED,seed=236,w=2.6,amp=1.1))
    g.append(curl(ccx+66,ccy-16,1.3,4,20,seed=237,w=3.0))
    for d in (0,1):
        g.append(f'<circle cx="{ccx-54+d*17}" cy="{ccy-30}" r="3.6" fill="{INK}"/>')
    for k in range(3):
        g.append(stroke([(ccx-58,ccy-16+k*6),(ccx-88,ccy-22+k*9)],2.2,238+k,0.8,twice=False))
        g.append(stroke([(ccx-32,ccy-16+k*6),(ccx-4,ccy-22+k*9)],2.2,242+k,0.8,twice=False))
    g.append('</g>')
    g.append(person(692,H-226,s=0.94,col=RED,seed=250,face="calm",hairstyle="frizz"))
    g.append(bot(830,H-214,s=1.10,col=BLUE,seed=254,mood="flat",tilt=18,form="egg",look=(-6,0)))
    g.append(ground(H-96,W,seed=21))
    return svg(W,H,"".join(g))

# ---------------------------------------------------------------- 12. doorway
def s_doorway():
    FL=556
    g=[f'<rect width="{W}" height="{H}" fill="#2A3A4B"/>']
    g.append(shape([(92,64),(330,60),(328,268),(90,264)],NIGHT,seed=260,w=4.0,amp=1.8))
    g.append(stroke([(210,62),(210,266)],3.0,261,1.2,twice=False))
    g.append(stroke([(92,166),(329,163)],3.0,262,1.2,twice=False))
    g.append(moon(262,122,42,seed=263))
    r=random.Random(31)
    for _ in range(22):
        g.append(f'<circle cx="{r.randint(102,320)}" cy="{r.randint(74,256)}" r="{r.choice([1.5,2,2.6])}" fill="{MOON}" opacity="{r.uniform(0.45,1):.2f}"/>')
    dx,dw=596,256
    g.append(shape([(dx,120),(dx+dw,116),(dx+dw,FL+40),(dx,FL+40)],YELLOW,seed=265,w=4.0,amp=1.8))
    g.append(shape([(dx+20,140),(dx+dw-20,136),(dx+dw-20,FL+40),(dx+20,FL+40)],"#F6D98F",seed=266,w=0,amp=1.4))
    g.append(f'<path d="M {dx},{FL} L 256,{FL+40} L {dx+dw},{FL+40} Z" fill="{YELLOW}" opacity="0.12"/>')
    px=724
    g.append(shape([(px-72,FL),(px-48,FL-142),(px-24,FL-176),(px+24,FL-176),(px+48,FL-142),(px+72,FL)],
                   INK,seed=267,w=3.0,amp=1.6))
    for d in (-1,1):
        g.append(stroke([(px+d*60,FL-138),(px+d*80,FL-76),(px+d*72,FL-16)],14,268+d,1.6,twice=False))
    g.append(shape(lump(px,FL-212,39,40,seed=270,n=22,amt=0.05),INK,seed=270,w=2.6,amp=1.2))
    g.append(tuft(px+6,FL-250,4,20,24,271,3.0,INK))
    bx,bw2,bh2=64,392,118
    by=FL-bh2
    g.append(shape([(bx,by),(bx+bw2,by-6),(bx+bw2,FL),(bx,FL)],PINK,seed=272,w=3.4,amp=1.6))
    g.append(shape([(bx,by),(bx+bw2,by-6),(bx+bw2,by+42),(bx,by+46)],CREAM,seed=273,w=3.2,amp=1.5))
    g.append(shape([(bx+bw2-28,by-58),(bx+bw2,by-62),(bx+bw2,FL),(bx+bw2-28,FL)],PINK,seed=274,w=3.2,amp=1.5))
    kx,ky=bx+80,by-28
    g.append(shape(lump(kx,ky,32,31,seed=275,n=22,amt=0.045),CREAM,seed=275,w=3.2,amp=1.3))
    g.append(tuft(kx+4,ky-30,4,18,26,276,2.6))
    for d in (0,1):
        g.append(f'<circle cx="{kx-11+d*22}" cy="{ky+2}" r="3.6" fill="{INK}"/>')
    g.append(stroke([(kx-9,ky+16),(kx,ky+22),(kx+10,ky+15)],2.5,277,0.9,twice=False))
    g.append(shape([(bx+bw2+24,FL-88),(bx+bw2+110,FL-92),(bx+bw2+110,FL),(bx+bw2+24,FL)],"#36485C",seed=278,w=3.0,amp=1.5))
    g.append(bot(bx+bw2+67,FL-122,s=0.44,col=BLUE,seed=280,mood="sleep",tilt=8,legs=False,arms=False))
    return svg(W,H,"".join(g),bg=NIGHT)

# ---------------------------------------------------------------- 13. the sill
def s_sill():
    g=sky_night()
    g.append(moon(716,168,78,seed=290))
    SY=H-196
    cast=[(300,RED,0.80,"arch"),(430,BLUE,0.70,"circle"),(556,YELLOW,0.86,"square"),(676,GREEN,0.68,"drop")]
    for i,(x,c,sc,fm) in enumerate(cast):
        g.append(bot(x,SY-54*sc,s=sc,col=c,seed=292+i*6,mood="sleep",
                     tilt=[-10,6,-4,11][i],form=fm))
    g.append(shape([(-20,SY),(W+20,SY-6),(W+20,SY+36),(-20,SY+40)],PINK,seed=300,w=3.6,amp=1.8))
    g.append(f'<rect x="0" y="{SY+36}" width="{W}" height="{H-SY-36}" fill="#2A3A4B"/>')
    g.append(stroke([(-20,SY+62),(W+20,SY+58)],3.0,320,1.4,op=0.4))
    return svg(W,H,"".join(g),bg=NIGHT)

SCENES={"cover":s_cover,"crowd":s_crowd,"printout":s_printout,"emptychair":s_emptychair,
        "funeral":s_funeral,"gork":s_gork,"grandma":s_grandma,"library":s_library,
        "window":s_window,"footnote":s_footnote,"drawing":s_drawing,
        "doorway":s_doorway,"sill":s_sill}
