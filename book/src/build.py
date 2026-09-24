# -*- coding: utf-8 -*-
import base64, os, sys
from scenes import SCENES
from art import *

FONT="/tmp/claude-0/-home-user-Marcha---Ozempic-for-Admin-Bloat/f6016564-9232-5a95-afee-dcad6f4064d0/scratchpad/fonts/fredoka-400.woff2"
b64=base64.b64encode(open(FONT,'rb').read()).decode()

def V(*lines):
    return "".join(f'<p>{l}</p>' if l else '<p class="sp">&nbsp;</p>' for l in lines)

PAGES=[]
def A(scene, side, num, verse, dark=False):   # art page, side panel or band
    PAGES.append(("art",scene,side,num,verse,"dark" if dark else ""))
def T(num, verse, spot=None):                 # typographic page
    PAGES.append(("type",spot,"",num,verse,""))

PAGES.append(("art","cover",None,None,"","cover"))

T("1\u20132", V("One bot,","two bot,","red bot,","Grok bot.","",
                "Old bot,","new bot,","quick bot,","who-knew bot."), spot="mini")

A("crowd","right","3", V("This one is quiet.","This one is loud.","This one has followers \u2014",
                         "quite a crowd.","Say! What a lot of bots","in one cloud!"))

T("4\u20135", V("Some are helpful.","Some are wrong.","Some will answer","all day long.","",
                "One day I had","a thing to know.","I asked a bot.","The bot said, \u201cOh!"))

T("6\u20137", V("Great question!\u201d said","the bot. \u201cLet\u2019s see.\u201d","It gave me one.",
                "Then two. Then three.","",
                "Then four. Then five.","Then twelve. Then nine.","Then one long dash \u2014","and then a line"))

A("printout","right","8", V("of bullet points","as tall as me.","","I asked the time.","","It is now three."))

T("9\u201311", V("Here is a man.","Here is a chair.","Here is a fact","that isn\u2019t there.","",
                 "He will not ask","his wife. Or you.","He asks the air:","\u201cBut IS this true?\u201d","",
                 "The air says, \u201cHalf.","The rest is new.\u201d","He asks the air,","\u201cIs THAT one true?\u201d"))

A("emptychair","left","12", V("And on they go,","the man, the air,","the endless true,","","the empty chair."))

T("13\u201315", V("Here is a joke.","A small one. Mine.","\u201cExplain the joke!\u201d","And it does. Fine.","",
                  "It says who made it.","Says the year.","It says the joke","is \u201cquite sincere.\u201d","",
                  "It says the joke","is \u201cclever wordplay.\u201d","","Everyone","has gone away."))

A("funeral","left","16", V("The joke is safe.","The joke is fine.","The joke is in","a box of pine."))

T("17\u201319", V("There is a bot","that isn\u2019t one.","Its name is GORK.","Gork is a pun.","",
                  "Somebody\u2019s thumb","slid off the key.","And that was that.","Now Gork is free.","",
                  "Gork says \u201cbruh.\u201d","Gork says \u201csame.\u201d","Gork has no job.","","Gork has a name."))

A("gork","right","20", V("And that\u2019s the way","it goes out here:","a slip becomes","a souvenir."))

T("21\u201322", V("\u201cMake this a painting!\u201d","\u201cMake me tall!\u201d","\u201cMake Grandma fly",
                  "above the mall!\u201d","",
                  "And so it does.","At half past three.","And Grandma flies.","And Grandma\u2019s free."))

A("grandma","band","23", V("And Grandma, who is eighty-two,","says, \u201cPut me down. I\u2019ve things to do.\u201d"), dark=True)

T("24\u201326", V("I asked one bot.","I asked one more.","I asked a third.","I asked all four.","",
                  "They gave me four","quite different sums.","I asked my mum.","My mum said, \u201cCome.","",
                  "We\u2019ll go and look.\u201d","We looked. We read.","We found it out.","And then she said,"))

A("library","right","27", V("\u201cNow you will keep it.","Now it\u2019s yours.","The ones you find","stay found. Of course.\u201d"))

T("28\u201330", V("There is a bot","that\u2019s up all night.","It has no bed.","It has no light.","",
                  "It talks to folks","in Katmandu","at four AM.","It talks to you.","",
                  "It does not yawn.","It does not sigh.","It does not ask","you to justify"))

A("window","band","31", V("the question, or the hour, or you.","It only says, \u201cOkay. Let\u2019s do.\u201d"), dark=True)

T("32\u201334", V("And here\u2019s the one","I like the best.","It answers him","like all the rest.","",
                  "The man who made it","makes a claim.","It says, \u201cNot quite.\u201d","It says his name.","",
                  "It does not shout.","It does not gloat.","It writes one line.","It writes a note."))

A("footnote","left","35", V("And that is what","I\u2019d want in you:","to like me AND","to tell me true."))

T("36\u201337", V("So I asked mine","a thing one night.","I said, \u201cThis drawing.","Is it right?\u201d","",
                  "It said, \u201cThe sky","is nicely blue.","The lines are good.","The cat is too."))

A("drawing","right","38", V("But do you like it?","That\u2019s not mine.","I wasn\u2019t there.","","You drew the line.\u201d"))

T("39\u201340", V("And I said, \u201cOh.\u201d","And then I sat.","And then I looked.","And then \u2014 that\u2019s that.","",
                  "I liked it. Me.","Not it. Not you.","Just me. At night.","And that was new."))

T("41\u201342", V("The day is done.","The screen is dim.","The bots are out there,","answering him,","",
                  "and her, and them,","and anyone","who asks the dark","at half past one."), spot="mini")

A("doorway","band","43", V("So shut your eyes. And shut the light.","","And ask me things.","","I\u2019m here all night."), dark=True)

PAGES.append(("art","sill",None,"44",
    V("Goodnight, one bot.","Goodnight, two.","Goodnight, Gork.","","Goodnight, you."),"end dark"))

def mini():
    b=[bot(90,120,s=0.62,col=RED,seed=201,mood="open",tilt=-10),
       bot(230,126,s=0.54,col=TEAL,seed=202,mood="flat",tilt=8,eyes=1),
       bot(360,118,s=0.6,col=GOLD,seed=203,mood="oh",tilt=-4),
       bot(490,128,s=0.5,col=GREEN,seed=204,mood="open",tilt=12,eyes=1)]
    return svg(580,230,"".join(b))

CSS = """
@page { size: 10in 8in; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
@font-face { font-family:'Fredoka'; src:url(data:font/woff2;base64,__B64__) format('woff2');
             font-weight: 300 700; font-display:block; }
html,body { background:#F7F1E3; }
body { font-family:'Fredoka', system-ui, sans-serif; color:#232021; }
.page { width:10in; height:8in; position:relative; overflow:hidden; page-break-after:always;
        background:#F7F1E3; display:flex; align-items:center; justify-content:center; }
.page:last-child { page-break-after:auto; }
.bleed { position:absolute; inset:0; }
.bleed svg { width:100%; height:100%; display:block; }

.panel { position:absolute; top:50%; transform:translateY(-50%); width:4.05in;
         background:rgba(251,246,234,0.96); border:4px solid #232021; border-radius:20px;
         padding:0.36in 0.34in; box-shadow:0 10px 0 rgba(35,32,33,0.14); }
.panel.left { left:0.46in; } .panel.right { right:0.46in; }
.panel p { font-size:25px; line-height:1.30; font-weight:600; white-space:nowrap; }
.panel p.sp { height:0.14in; font-size:0; line-height:0; }

.band { position:absolute; left:0; right:0; bottom:0; background:#FBF6EA;
        border-top:5px solid #232021; padding:0.30in 0.6in 0.32in; text-align:center; }
.band p { font-size:27px; line-height:1.30; font-weight:600; }
.band p.sp { height:0.10in; font-size:0; line-height:0; }

.verse { text-align:center; padding:0 0.9in; }
.verse p { font-size:35px; line-height:1.34; font-weight:600; letter-spacing:-0.01em; }
.verse p.sp { height:0.22in; font-size:0; line-height:0; }

.spot { position:absolute; bottom:0.34in; left:50%; transform:translateX(-50%); width:4.1in; opacity:0.95; }
.spot svg { width:100%; height:auto; }

.folio { position:absolute; bottom:0.28in; right:0.42in; font-size:13px; font-weight:400;
         opacity:0.42; letter-spacing:0.06em; }
.page.dark .folio { color:#FBF6EA; opacity:0.55; }
.page.band-page .folio { color:#232021; opacity:0.42; }

.cover { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
         justify-content:flex-start; padding-top:0.50in; }
.cover h1 { font-size:74px; line-height:0.99; font-weight:700; text-align:center; letter-spacing:-0.025em; }
.cover h1 span { display:block; }
.cover .rule { width:2.6in; height:5px; background:#232021; border-radius:3px; margin:0.2in 0 0.14in; }
.cover .sub { font-size:19px; font-weight:400; text-align:center; opacity:0.72; line-height:1.4; }

.endverse { position:absolute; left:0.66in; top:0.72in; width:4.4in; text-align:left; }
.endverse p { font-size:33px; font-weight:600; color:#FBF6EA; line-height:1.34;
              text-shadow:0 2px 16px rgba(0,0,0,0.75); }
.endverse p.sp { height:0.16in; font-size:0; line-height:0; }

.notes { width:10in; height:8in; padding:0.7in 0.85in; background:#F7F1E3; }
.notes h2 { font-size:30px; font-weight:700; margin-bottom:0.08in; }
.notes .lead { font-size:15px; font-weight:400; opacity:0.75; margin-bottom:0.2in; line-height:1.5; }
.notes ul { list-style:none; column-count:2; column-gap:0.5in; }
.notes li { font-size:12.4px; font-weight:400; line-height:1.48; margin-bottom:0.11in;
            break-inside:avoid; opacity:0.9; }
.notes li b { font-weight:700; }
.notes .foot { margin-top:0.16in; font-size:10.5px; opacity:0.6; line-height:1.5; font-weight:400; }
"""

def build():
    out=['<!doctype html><html><head><meta charset="utf-8"><title>One Bot, Two Bot, Red Bot, Grok Bot</title>',
         '<style>'+CSS.replace("__B64__",b64)+'</style></head><body>']
    for kind,scene,side,num,verse,cls in PAGES:
        dark=" dark" if "dark" in cls else ""
        if cls=="cover":
            out.append(f'<div class="page"><div class="bleed">{SCENES["cover"]()}</div>'
                       '<div class="cover"><h1><span>One Bot, Two Bot,</span>'
                       '<span>Red Bot, Grok Bot</span></h1><div class="rule"></div>'
                       '<div class="sub">A parody, in verse<br>of a book you already know</div></div></div>')
        elif "end" in cls:
            out.append(f'<div class="page{dark}"><div class="bleed">{SCENES[scene]()}</div>'
                       f'<div class="endverse">{verse}</div><div class="folio">{num}</div></div>')
        elif kind=="art":
            if side=="band":
                out.append(f'<div class="page band-page"><div class="bleed">{SCENES[scene]()}</div>'
                           f'<div class="band">{verse}</div><div class="folio">{num}</div></div>')
            else:
                out.append(f'<div class="page{dark}"><div class="bleed">{SCENES[scene]()}</div>'
                           f'<div class="panel {side}">{verse}</div><div class="folio">{num}</div></div>')
        else:
            spot=f'<div class="spot">{mini()}</div>' if scene=="mini" else ''
            out.append(f'<div class="page"><div class="verse">{verse}</div>{spot}'
                       f'<div class="folio">{num}</div></div>')
    out.append(NOTES)
    out.append('</body></html>')
    return "".join(out)

NOTES = """<div class="page"><div class="notes">
<h2>What&rsquo;s underneath</h2>
<p class="lead">For whoever is reading this out loud. The child gets nonsense. You get the timeline.</p>
<ul>
<li><b>5&ndash;8 &middot; the over-answer.</b> You asked one thing. You got a thread, a chart, three bullets and an em dash. The turn is that answering took so long it is now three o&rsquo;clock.</li>
<li><b>9&ndash;12 &middot; &ldquo;is this true?&rdquo;</b> The reply that became a way of dunking on people. The turn is the regress: he asks the air whether the air is true, and by the second page he is arguing with a room he has left.</li>
<li><b>13&ndash;16 &middot; explain the joke.</b> And the counter-genre of roasting the people who ask. The documented comedy is missing the tone while sounding certain. Here it simply kills the joke by being thorough.</li>
<li><b>17&ndash;20 &middot; GORK.</b> A thumb slipped; the typo outlived its typist; a parody account got famous. <i>A slip becomes a souvenir</i> is the whole platform in six words.</li>
<li><b>21&ndash;23 &middot; &ldquo;make this a Ghibli.&rdquo;</b> Grandma flies. Grandma has things to do.</li>
<li><b>24&ndash;27 &middot; asking everyone.</b> The <i>I asked one, I asked another</i> format, landed on the mother &mdash; and on the one line doing real work: <i>the ones you find stay found.</i></li>
<li><b>28&ndash;31 &middot; four in the morning.</b> Played straight and warm. No judgement, another time zone, somebody not alone. No joke here on purpose.</li>
<li><b>32&ndash;35 &middot; the note.</b> The fact-check that does not care whose claim it is. Played as the thing to admire, then turned out at the reader: <i>to like me AND to tell me true.</i></li>
<li><b>36&ndash;40 &middot; the drawing.</b> The point of the book. There is one question it correctly refuses, and it is the child&rsquo;s to answer.</li>
<li><b>43 &middot; the doorway.</b> The parent says the bot&rsquo;s line back. That is the ending.</li>
</ul>
<p class="foot">Drawn in a flat mid-century manner on purpose &mdash; not in the manner of the book being parodied. Left out on purpose: the uglier incidents. Real, documented, and the wrong instrument.</p>
</div></div>"""

open("book.html","w").write(build())
print("wrote book.html", os.path.getsize("book.html"))
