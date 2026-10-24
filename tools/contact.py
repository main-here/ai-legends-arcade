# Contact sheet of sprites on magenta to check background removal
import glob, os, sys
from PIL import Image
fs = sorted(glob.glob(os.path.join(sys.argv[1], '*_[is].webp')))
cols = 8; cw, ch = 260, 250
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * cw, rows * ch), (200, 0, 160))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGBA'); im.thumbnail((cw - 6, ch - 6))
    sheet.paste(im, ((i % cols) * cw, (i // cols) * ch), im)
sheet.save(sys.argv[2])
