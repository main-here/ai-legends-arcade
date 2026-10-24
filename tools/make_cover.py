# Builds the itch.io cover (630x500) from the pixel sheets: red Lovelace vs blue Turing
import os
from PIL import Image, ImageDraw, ImageFont
from build_assets import ROOT, SRC, poses

W, H = 630, 500
OUT = os.path.join(ROOT, 'dist', 'cover_630x500.png')
FONT = os.path.join(ROOT, 'assets', 'PixelifySans.ttf')

def fighter(key, h, flip=False):
    s = poses(Image.open(os.path.join(SRC, 'personajes', 'pixel', key + '.png')).convert('RGB'))[1]
    s = s.resize((round(s.width * h / s.height), h), Image.LANCZOS)
    return s.transpose(Image.FLIP_LEFT_RIGHT) if flip else s

def text(d, xy, t, size, fill, shadow, anchor='mm'):
    f = ImageFont.truetype(FONT, size)
    x, y = xy
    for o in (8, 4):
        d.text((x + o, y + o), t, font=f, fill=shadow if o == 4 else '#000', anchor=anchor)
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def main():
    im = Image.new('RGB', (W, H), '#0b0716')
    d = ImageDraw.Draw(im)
    # red vs blue diagonal split
    d.polygon([(0, 0), (370, 0), (260, H), (0, H)], fill='#a3122a')
    d.polygon([(370, 0), (W, 0), (W, H), (260, H)], fill='#123c9c')
    d.line([(370, 0), (260, H)], fill='#ffd23e', width=6)
    for y in range(0, H, 3):  # scanlines
        d.line([(0, y), (W, y)], fill=(0, 0, 0), width=1)
    im = Image.blend(im, Image.new('RGB', (W, H), '#0b0716'), .25)
    a, b = fighter('lovelace', 330), fighter('turing', 330, flip=True)
    im.paste(a, (10, H - a.height - 6), a)
    im.paste(b, (W - b.width - 10, H - b.height - 6), b)
    d = ImageDraw.Draw(im)
    text(d, (W // 2, 70), 'AI LEGENDS', 78, '#fff6e0', '#2e1050')
    text(d, (W // 2, 140), 'ARCADE', 56, '#ffd23e', '#8a5a00')
    text(d, (W // 2, 300), 'VS', 72, '#ffd23e', '#a3122a')
    d.rectangle([0, H - 52, W, H], fill='#0b0716')
    text(d, (W // 2, H - 28), 'PICK YOUR LEGEND · FIGHT ABOUT AI', 22, '#fff6e0', '#000')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    im.save(OUT, optimize=True)
    print(OUT)

if __name__ == '__main__':
    main()
