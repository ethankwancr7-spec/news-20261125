"""Build the original editorial artwork with Pillow and Windows system fonts."""
from pathlib import Path
from math import cos, pi, sin
from random import Random
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
S = 2
PAPER, INK = "#f4efe2", "#192e2c"
NIGHT, TEAL, GOLD = "#102e36", "#9fe3cd", "#ffdb88"
im = Image.new("RGB", (2048, 2048), PAPER)
d = ImageDraw.Draw(im)
fonts = Path("C:/Windows/Fonts")

def xy(vals):
    return tuple(round(a*S) for a in vals)

def box(x,y,w,h,c):
    d.rectangle(xy((x,y,x+w-.5,y+h-.5)),fill=c)

def dot(x,y,r,c):
    d.ellipse(xy((x-r,y-r,x+r,y+r)),fill=c)

def poly(pts,c):
    d.polygon([xy(p) for p in pts],fill=c)

def line(pts,c,w=1):
    d.line([xy(p) for p in pts],fill=c,width=w*S)

def text(x,y,s,size,c=INK,f="arialbd",a="lt",right=995):
    font=ImageFont.truetype(str(fonts/(f+".ttf")),size*S)
    l,t,r,b=d.textbbox(xy((x,y)),s,font=font,anchor=a)
    assert 0<=l<=r<=right*S and 0<=t<=b<=2048,(s,(l,t,r,b),right)
    d.text(xy((x,y)),s,font=font,fill=c,anchor=a)

def lines(x,y,ss,size,step,c=INK,f="arialbd",right=995):
    for i,s in enumerate(ss):
        text(x,y+i*step,s,size,c,f,right=right)

box(28,24,968,4,INK)
text(30,41,"25 November 2026",52,f="georgiab")
text(994,44,"WORLD / IN VIEW",23,a="rt")
text(994,74,"WEDNESDAY EDITION",18,a="rt")

box(28,111,968,360,NIGHT)
# Draw the orbit illustration on its own clipped plate.
page=d
plate=Image.new("RGB",(500*S,360*S),NIGHT)
d=ImageDraw.Draw(plate)
rng=Random(25)
for _ in range(124):
    x,y=rng.randrange(8,494),rng.randrange(4,272)
    dot(x,y,rng.choice((.65,1,1.25)),rng.choice(("#42616a","#598083","#819e9c")))
for radius in range(315,274,-2):
    k=(315-radius)/40
    dot(363,543,radius,(int(33+12*k),int(74+48*k),int(85+44*k)))
# Stylized illuminated land and cloud bands, not a geographic locator.
poly([(160,352),(188,324),(225,319),(241,303),(271,301),(294,288),
      (329,277),(364,277),(378,290),(347,304),(307,310),(281,334),
      (241,338),(224,366)],"#76a994")
poly([(376,325),(407,302),(447,302),(462,290),(481,303),(505,315),
      (500,352),(461,340),(421,352),(398,345)],"#77a393")
for start,end in [(20,160),(97,229),(207,375),(304,466)]:
    line([(start,347-(start%4)*4),(end,312-(start%5)*3)],"#98c5b5",2)
# Two schematic vehicles with tonal faces, panel grids and a docking gap.
def panel(x,y):
    p=[(x,y),(x+74,y-13),(x+91,y+17),(x+17,y+31)]
    poly(p,"#4b86a3")
    for j in range(1,6):
        u=j/6
        line([(x+74*u,y-13*u),(x+17+74*u,y+31-14*u)],"#a1cad2")
    line([(x+8,y+15),(x+82,y+2)],"#a1cad2")
    line(p+[p[0]],"#c0e4e6",2)

for x,y in [(273,89),(388,69),(310,192),(395,171)]:
    line([(x+43,y+10),(x+47,y+(-34 if y>150 else 53))],TEAL,5)
    panel(x,y)
poly([(256,140),(453,104),(473,120),(477,145),(279,183),(257,169)],"#e6e5ca")
poly([(257,156),(470,118),(477,145),(279,183),(257,169)],"#83a6a0")
poly([(342,114),(369,110),(392,178),(365,184)],"#f8e8b3")
poly([(353,117),(370,111),(392,178),(376,181)],"#b9afa2")
dot(358,140,8,NIGHT)
dot(357,138,4,TEAL)
box(237,153,24,12,"#a8c6b9")
poly([(45,184),(89,171),(108,181),(106,207),(58,217),(43,207)],"#64938e")
poly([(95,175),(122,169),(151,163),(171,172),(175,190),(156,204),(121,210),(105,205)],"#ececd7")
poly([(108,190),(174,175),(175,190),(156,204),(121,210),(105,205)],"#a7b9a7")
poly([(150,166),(178,166),(186,179),(175,190)],GOLD)
for x in range(191,237,9):
    dot(x,177-(x-191)*.39,2.25,GOLD)
box(0,267,500,93,NIGHT)
box(16,239,468,28,NIGHT)
line([(33,254),(441,254)],"#6caba6",2)
for x in (33,441):
    dot(x,254,5,GOLD)
text(32,268,"08:18",31,GOLD)
text(441,268,"11:56",31,GOLD,a="rt")
text(32,305,"JIUQUAN LAUNCH",19,"#fff6de")
text(441,305,"TIANGONG DOCKING",19,"#fff6de",a="rt")
text(237,331,"25 NOV  /  BEIJING TIME  /  CMSA",15,TEAL,a="mt")
d=page
im.paste(plate,xy((496,111)))
text(48,134,"01   SPACE  /  CHINA + PAKISTAN",19,TEAL)
lines(46,177,["Shenzhou-24","docks with","Tiangong"],55,57,"#fff6de","georgiab",right=487)
lines(49,373,["Pakistan’s Muhammad Zeeshan Ali","is the first foreign astronaut","aboard China’s space station."],23,27,"#fff6de","arial",right=486)
text(719,132,"DOCKING SCHEMATIC",16,TEAL,a="mt")

# The two largest secondary illustrations make the news mechanisms visible.
def support(x,fill,k,head,caption):
    box(x,487,475,216,fill)
    box(x,487,475,4,INK)
    text(x+15,504,k,17)
    lines(x+14,536,head,33,37,INK,"georgiab",right=x+339)
    lines(x+15,644,caption,19,23,INK,"arial",right=x+350)

support(28,"#ebd8b6","02   UNITED STATES  /  TRADE",
        ["U.S. proposes","new import tariffs"],
        ["Targets include China, the EU","and Brazil; duties not yet in force."])
support(521,"#d7e6d8","03   DR CONGO  /  HEALTH",
        ["Fighting disrupts","Ebola response"],
        ["Teams leave affected areas","and contact tracing is disrupted."])
# Stacked cargo with a customs document, not a trade-volume chart.
for x,y,c in [(346,600,"#527c77"),(367,564,"#b36543"),(399,601,"#d29453")]:
    box(x,y,83,38,c)
    for j in range(1,7):
        box(x+10*j,y+5,2,27,"#efd7a3")
    box(x,y+34,83,4,INK)
poly([(392,513),(449,523),(440,582),(383,572)],"#fff5db")
line([(400,531),(439,537)],INK,3)
line([(398,540),(437,546)],INK,3)
dot(416,556,10,"#b36543")
# Interrupted contact chain, schematic rather than patient data.
line([(865,606),(973,606)],"#638579",3)
for x in (858,965):
    dot(x,606,23,NIGHT)
box(845,601,26,10,TEAL)
box(853,593,10,26,TEAL)
dot(965,599,6,TEAL)
d.rounded_rectangle(xy((954,608,976,617)),radius=4*S,fill=TEAL)
box(901,589,32,35,"#d7e6d8")
line([(904,595),(915,616)],"#a74231",4)
line([(916,595),(927,616)],"#a74231",4)

def brief(x,y,w,k,head,caption,fill):
    box(x,y,w,119,fill)
    box(x,y,w,2,INK)
    text(x+11,y+10,k,15,right=x+w-5)
    lines(x+11,y+34,head,27 if w>400 else 24,25,INK,"georgiab",right=x+w-5)
    text(x+11,y+(80 if w>400 else 92),caption,18 if w>400 else 17,
         f="arial",right=x+w-5)

brief(28,717,312,"04   SOUTH PACIFIC",["Solomons sign","Australia treaty"],"Canberra pact bars foreign bases.","#e6e4d9")
brief(356,717,312,"05   SPAIN  /  ATLANTIC",["Canaries record","1,990 migrant arrivals"],"Spain’s rescue service • Nov 24","#ecd9b9")
brief(684,717,312,"06   COLOMBIA",["Cartagena supermarket","hostages freed"],"President says all were rescued.","#e6e4d9")
brief(28,847,475,"07   GLOBAL MARKETS",["Brent crude settles at $94.61"],"Per barrel, up 3.5% at the Nov 25 settlement.","#e6e4d9")
brief(521,847,475,"08   VATICAN  /  CLIMATE",["Pope faults lack of climate deal"],"COP31 ended Nov 22 without an overall deal.","#e6e4d9")
line([(28,981),(996,981)],INK)
text(29,991,"ORIGINAL GRAPHICS  /  SOURCES: AP, REUTERS, CMSA, USTR, AUSTRALIAN PM’S OFFICE",14)
im.resize((1024,1024),Image.Resampling.LANCZOS).convert(
    "P",palette=Image.Palette.ADAPTIVE,colors=208
).save(ROOT/"artwork.png",optimize=True)
