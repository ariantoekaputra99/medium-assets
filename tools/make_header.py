"""Generate an original abstract header image (code window + AI network), 1400x788 JPEG.
Usage: python3 tools/make_header.py --seed 3 --out 2026-11/2026-11-09-my-slug.jpg
Different seeds give different network shapes, code lines and colour palettes. No text, no logos."""
import random, math, argparse
from PIL import Image, ImageDraw, ImageFilter
ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int,default=7); ap.add_argument("--out",required=True)
args=ap.parse_args()
W,H=1400,788; S=2
random.seed(args.seed)
PALETTES=[
 ((8,18,48),(10,60,92),(80,220,210),(255,150,50)),
 ((20,10,45),(60,25,95),(190,120,255),(255,120,170)),
 ((6,30,36),(10,80,70),(100,240,170),(255,200,80)),
 ((12,16,40),(25,50,110),(110,180,255),(255,140,60)),
 ((28,14,20),(80,30,50),(255,140,120),(120,220,255)),
]
TOP,BOT,NET,WARM=PALETTES[args.seed%len(PALETTES)]
w,h=W*S,H*S
# vertical gradient background
bg=Image.new("RGB",(w,h))
px=bg.load()
top=TOP; bot=BOT
for y in range(h):
    t=y/h
    c=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))
    for x in range(w): px[x,y]=c
img=bg.convert("RGBA")

# glow layer
glow=Image.new("RGBA",(w,h),(0,0,0,0))
gd=ImageDraw.Draw(glow)
# network nodes on the right
nodes=[]
for i in range(26):
    x=random.uniform(0.52,0.96)*w; y=random.uniform(0.12,0.88)*h
    nodes.append((x,y))
hub=(0.50*w,0.50*h)
nodes.append(hub)
lines=Image.new("RGBA",(w,h),(0,0,0,0)); ld=ImageDraw.Draw(lines)
for i,a in enumerate(nodes):
    d=sorted(nodes,key=lambda b:(a[0]-b[0])**2+(a[1]-b[1])**2)[1:4]
    for b in d:
        ld.line([a,b],fill=NET+(110,),width=3*S//2+1)
for a in nodes:
    r=random.choice([8,10,12,16])*S//1
    gd.ellipse([a[0]-r*2.2,a[1]-r*2.2,a[0]+r*2.2,a[1]+r*2.2],fill=NET+(60,))
# hub glow (warm orange)
for k,(rad,al) in enumerate([(120,40),(80,70),(48,120)]):
    gd.ellipse([hub[0]-rad*S,hub[1]-rad*S,hub[0]+rad*S,hub[1]+rad*S],fill=WARM+(al,))
glow=glow.filter(ImageFilter.GaussianBlur(18*S))
img=Image.alpha_composite(img,glow)
img=Image.alpha_composite(img,lines)
d=ImageDraw.Draw(img)
for a in nodes:
    r=random.choice([5,6,7,9])*S
    d.ellipse([a[0]-r,a[1]-r,a[0]+r,a[1]+r],fill=tuple(min(255,c+70) for c in NET)+(255,))
r=18*S
d.ellipse([hub[0]-r,hub[1]-r,hub[0]+r,hub[1]+r],fill=tuple(min(255,c+40) for c in WARM)+(255,))
r=9*S
d.ellipse([hub[0]-r,hub[1]-r,hub[0]+r,hub[1]+r],fill=(255,240,210,255))

# code window on the left
x0,y0,x1,y1=0.06*w,0.17*h,0.46*w,0.83*h
panel=Image.new("RGBA",(w,h),(0,0,0,0)); pd=ImageDraw.Draw(panel)
pd.rounded_rectangle([x0,y0,x1,y1],radius=26*S,fill=(10,22,52,215),outline=(90,150,220,120),width=2*S)
pd.rounded_rectangle([x0,y0,x1,y0+52*S],radius=26*S,fill=(18,36,78,235))
for i,c in enumerate([(255,95,90),(255,190,60),(60,200,110)]):
    cx=x0+(34+i*30)*S; cy=y0+26*S
    pd.ellipse([cx-8*S,cy-8*S,cx+8*S,cy+8*S],fill=c+(255,))
cols=[(110,200,255),(255,170,90),(140,230,170),(190,160,255),(200,210,230)]
y=y0+86*S; row=0
while y<y1-40*S:
    indent=random.choice([0,0,1,1,2,3])
    x=x0+(30+indent*34)*S
    segs=random.randint(1,4)
    for s in range(segs):
        ln=random.randint(40,190)*S
        if x+ln>x1-30*S: break
        pd.rounded_rectangle([x,y,x+ln,y+14*S],radius=7*S,fill=random.choice(cols)+(235,))
        x+=ln+14*S
    y+=34*S; row+=1
img=Image.alpha_composite(img,panel)
# beams from code panel to hub
beam=Image.new("RGBA",(w,h),(0,0,0,0)); bd=ImageDraw.Draw(beam)
for i in range(5):
    sy=y0+(0.2+0.15*i)*(y1-y0)
    bd.line([(x1,sy),hub],fill=WARM+(70,),width=3*S)
beam=beam.filter(ImageFilter.GaussianBlur(1.5*S))
img=Image.alpha_composite(img,beam)
out=img.convert("RGB").resize((W,H),Image.LANCZOS)
out.save(args.out,quality=82,optimize=True,progressive=True)
